# Arad Smart Meters under Wine — Working Setup (Ubuntu 24.04)

**Version:** v1.2 — verified working · **Supersedes:** v1.0, v1.1
**Result:** Arad Smart Meters v1.0.35 runs under Wine and talks to the Arad USB NFC reader. No Windows, no VM, no dual boot.

---

## ⚠️ The one step that matters most

If you only remember one thing from this document, remember this:

```
wine reg add "HKLM\System\CurrentControlSet\Services\winebus" /v "Enable SDL" /t REG_DWORD /d 0 /f
```

Wine's `winebus` driver has two backends for HID devices: **SDL** and **udev/hidraw**. By default it uses SDL, which only surfaces game controllers. A vendor HID device like this reader is completely invisible to Windows applications until SDL is disabled and the udev backend takes over.

Without this, everything else in this guide fails with a misleading, generic error and no clue as to the cause. Note the **space** in the value name `Enable SDL`.

---

## Known-good version stack

Record these. If something breaks after an update, this is what worked.

| Component | Version |
|---|---|
| OS | Ubuntu 24.04 LTS (`ubuntu-24.04.4-desktop-amd64.iso`) |
| Wine | `wine-9.0 (Ubuntu 9.0~repack-4build3)` — distro package, **not** WineHQ |
| Wine prefix | `~/.wine-arad`, `WINEARCH=win32` |
| .NET | Framework 4.6.2 (real, via winetricks — not wine-mono) |
| Fonts | winetricks `corefonts` + `tahoma` |
| Application | Arad Smart Meters 1.0.35, entry point `C:\Arad\Arad Smart Meters\Octave.UI.exe` |
| Reader | Arad USB NFC, P/N 70000093 = USB `0483:D0D0` |
| Reader chipset | STM32 bridge + STMicroelectronics CR95HF NFC transceiver |

---

## Hardware facts worth not rediscovering

An earlier plan described the reader as "PC/SC smartcard-class". **That was wrong**, and it sent the whole first attempt down a dead end. What it actually is:

- USB `0483:D0D0` — VID is STMicroelectronics
- Product string reads `STM32 Mass Storage` — **a leftover from ST's demo firmware.** There is no mass storage. Ignore it.
- **One interface, class 3 (HID)**, subclass 0, protocol 0, 2 endpoints
- Report descriptor: usage page `0x8C` (Bar Code Scanner), usage `0x01` (Bar Code Badge Reader)
  - Report ID 1 → Output (host → device), 63 bytes
  - Report ID 2 → Output (host → device), 63 bytes
  - Report ID 7 → Input (device → host), 63 bytes
  - i.e. 64-byte packets; no Feature reports
- `CR95HF.dll` in the install directory imports `HID.DLL` (`HidD_GetHidGuid`, `HidD_GetAttributes`, `HidD_GetPreparsedData`, `HidD_GetSerialNumberString`, `HidP_GetCaps`) and `SETUPAPI.dll` (`SetupDiGetClassDevsA`, `SetupDiEnumDeviceInterfaces`, `SetupDiGetDeviceInterfaceDetailA`) — standard Windows HID enumeration, which is exactly what Wine implements.

`pcscd`, `pcsc-tools` and `libccid` are **irrelevant to this reader**. The only device `pcsc_scan` ever found was the machine's own built-in contact smartcard slot. Harmless if left installed, but they do nothing for this project.

---

## Phase 1 — Ubuntu 24.04 LTS

1. Boot the installer from a Ubuntu 24.04 USB (disable Secure Boot in firmware if it won't boot; it's signed, so you can re-enable it afterwards).
2. Install: **Erase disk and install Ubuntu** → user account → ~15 min.
3. `sudo apt update && sudo apt full-upgrade -y`, connect WiFi.
   - If WiFi firmware is missing: `sudo apt install linux-firmware`, reboot.

## Phase 2 — Reader permissions (udev)

hidraw device nodes are root-only by default. Wine must be able to open the node, **and it must be openable at the moment winebus starts**.

```
sudo tee /etc/udev/rules.d/70-arad-nfc.rules >/dev/null <<'EOF'
# Arad USB NFC reader (STM32 + CR95HF, vendor HID)
KERNEL=="hidraw*", SUBSYSTEM=="hidraw", ATTRS{idVendor}=="0483", ATTRS{idProduct}=="d0d0", MODE="0660", TAG+="uaccess"
SUBSYSTEM=="usb", ATTRS{idVendor}=="0483", ATTRS{idProduct}=="d0d0", MODE="0660", TAG+="uaccess"
EOF

sudo udevadm control --reload-rules
sudo udevadm trigger --subsystem-match=hidraw --subsystem-match=usb
```

Verify — and note that `ls -l` will **not** show this, because `uaccess` grants access by ACL:

```
getfacl /dev/hidraw1          # expect: user:<your-user>:rw-
```

Find the right node if it has moved (the number is not stable across replugs):

```
grep -H . /sys/class/hidraw/*/device/uevent | grep -i 0000D0D0
```

The rule matches on VID/PID, so the node number doesn't matter to Wine.

## Phase 3 — Wine prefix

```
sudo dpkg --add-architecture i386
sudo apt update
sudo apt install -y wine winetricks
```

Add these aliases — **every** wine/winetricks command for this app needs the prefix and arch set, or it will silently operate on `~/.wine`:

```
cat >> ~/.bashrc <<'EOF'
alias aradwine='WINEPREFIX=$HOME/.wine-arad WINEARCH=win32 wine'
alias aradcfg='WINEPREFIX=$HOME/.wine-arad WINEARCH=win32 winecfg'
alias aradtricks='WINEPREFIX=$HOME/.wine-arad WINEARCH=win32 winetricks'
EOF
source ~/.bashrc

aradcfg      # creates the prefix
```

The `err:ole:StdMarshalImpl_MarshalInterface` and `RpcSs` errors on a fresh prefix are normal noise.

## Phase 4 — .NET 4.6.2 and fonts

**.NET is mandatory.** wine-mono is not installed by Ubuntu's wine package at all, and this is a WPF application — Mono would not have been sufficient anyway. Use the offline installer that ships in the Arad zip rather than letting winetricks download:

```
mkdir -p ~/.cache/winetricks/dotnet462
cp "$HOME/arad/Arad Smart Meter Software/1.0.35/DotNetFX462/NDP462-KB3151800-x86-x64-AllOS-ENU.exe" \
   ~/.cache/winetricks/dotnet462/
aradtricks -q dotnet462
```

Verify:

```
ls "$HOME/.wine-arad/drive_c/windows/Microsoft.NET/Framework/v4.0.30319/" | head
```

**Fonts are also mandatory, not cosmetic.** Without them WPF calls `Environment.FailFast` — an uncatchable process kill — the instant a `TextBox`/`PasswordBox` is measured. Since the app's first screen is a password prompt, the app is unusable without this:

```
aradtricks -q corefonts tahoma
aradtricks -q fontsmooth=rgb
```

## Phase 5 — Install the application

The MSI refuses to install under Wine: action `VSDCA_VsdLaunchConditions` returns **1603**. This is the Visual Studio setup-project prerequisite check, implemented as a custom action (the `LaunchCondition` table is empty). It appears in **both** `InstallUISequence` and `InstallExecuteSequence`, so `/qn` does not bypass it. The Property table shows `VSDFrameworkVersion=v4.6.2` with `VSDAllowLaterFrameworkVersions=False` — it demands 4.6.2 exactly and rejects anything newer.

Strip the check from a copy of the MSI:

```
sudo apt install -y msitools
cd ~/arad
unzip Arad-Smart-Meter-Software.zip -d ~/arad
cp "Arad Smart Meter Software/1.0.35/AradMetersSetupF.msi" Arad-nolc.msi
msiinfo export Arad-nolc.msi InstallExecuteSequence > IES.idt
msiinfo export Arad-nolc.msi InstallUISequence      > IUS.idt
sed -i '/^VSDCA_VsdLaunchConditions\t/d' IES.idt IUS.idt
msibuild Arad-nolc.msi -i IES.idt -i IUS.idt
aradwine msiexec /i Arad-nolc.msi
```

Only `menubuilder:convert_to_native_icon` errors should appear — those are cosmetic (Wine failing on one frame of a multi-resolution icon while creating shortcuts).

This removes a **prerequisite check**, not functionality. .NET 4.6.2 is genuinely installed by Phase 4; the check simply can't detect it correctly under Wine.

Installs to `C:\Arad\Arad Smart Meters\` (not Program Files). The VC++ 2015+ runtime (`mfc140`, `msvcp140`, `vcruntime140`, `ucrtbase`, `concrt140`) is delivered by a merge module into `windows/system32` — no `vcrun` verb needed.

## Phase 6 — Enable Wine's hidraw backend ← THE CRITICAL STEP

```
aradwine reg add "HKLM\\System\\CurrentControlSet\\Services\\winebus" /v "Enable SDL" /t REG_DWORD /d 0 /f
aradwine reg add "HKLM\\System\\CurrentControlSet\\Services\\winebus" /v DisableHidraw /t REG_DWORD /d 0 /f
wineserver -k
sleep 2
```

Beware: most advice online sets `DisableHidraw=1` and `Enable SDL=1`. That is for **game controllers** and is the exact opposite of what this needs.

`wineserver -k` matters. winebus enumerates devices when it starts, and wineserver persists after the app exits — so a running wineserver will keep a stale, empty device list.

## Phase 7 — Application configuration

```
aradwine "$HOME/.wine-arad/drive_c/Arad/Arad Smart Meters/Octave.UI.exe"
```

On the login screen click **Settings → Connection**:

- **NFC** — ticked
- **Reader Serial Number** — the reader's USB `iSerialNumber`

This is a free-text field; there is no scan or dropdown. It's the USB `iSerialNumber`, which the app reads on Windows via `HidD_GetSerialNumberString`. Get it from Linux with:

```
sudo lsusb -v -d 0483:d0d0 2>/dev/null | grep -i iSerial
```

⚠️ `lsusb` prints e.g. `iSerial   3  <SERIAL>`. The leading **`3` is the string-descriptor index — not part of the serial.** Enter only the hex value.

Changes take effect on the next connection, so restart the app afterwards.

Other useful settings there: **NFC Debug Registers** (reads the CR95HF's registers — a good end-to-end test of the HID path) and **Demonstration mode** (the `SimulationMode` setting, for walking the UI without hardware).

Also create the folders the app writes to:

```
mkdir -p "$HOME/.wine-arad/drive_c/Octave/Logs" "$HOME/.wine-arad/drive_c/Octave/Recordings"
```

## Phase 8 — Back up the working prefix

**Do this now.** The prefix is the whole result of this work, and it is a single directory.

```
tar czf ~/wine-arad-WORKING-$(date +%F).tar.gz -C "$HOME" .wine-arad
```

Copy it off the machine to external storage. Restore:

```
wineserver -k
rm -rf ~/.wine-arad
tar xzf ~/wine-arad-WORKING-<date>.tar.gz -C "$HOME"
```

Keep alongside this guide: `Arad-nolc.msi` (the launch-condition-stripped installer) and `70-arad-nfc.rules`.

## Phase 9 — Capture for the Octave reference

With a real Octave connected, screenshot:

- [ ] Reader-detected / connection status
- [ ] Units configuration
- [ ] Outputs configuration
- [ ] Alarm log
- [ ] Firmware / version info

`Demonstration mode` can cover screens that don't strictly need hardware.

---

## Appendix A — Troubleshooting by symptom

| Symptom | Cause | Fix |
|---|---|---|
| `err:mscoree:CLRRuntimeInfo_GetRuntimeHost Wine Mono is not installed` | No .NET runtime in the prefix | Phase 4 |
| MSI aborts, `VSDCA_VsdLaunchConditions returned 1603` | VS prerequisite custom action | Phase 5 |
| `FailFast` at `FontFamily.get_FirstFontFamily` via `TextBox.GetLineHeight` | No usable fonts in the prefix | Phase 4 fonts |
| `X Error: GLXBadWindow` on `X_GLXDestroyWindow` | **Symptom, not cause** — `FailFast` killed the process and X saw a GLX window vanish | Fix the fonts |
| `Error — Action: Connection / Error: Illegal Input Value` | Generic comms-layer error. Identical with the reader plugged in or unplugged. | Phase 6 (and check the serial) |
| App enumerates only `HID\VID_845E&PID_0001` / `&PID_0002` | Those are **Wine's own synthetic mouse and keyboard**. No real HID device is reaching Windows. | Phase 6 |
| `USB\VID_0483&PID_D0D0` appears but `No driver registered for device` | `wineusb` (libusb) sees it as a bare USB device — wrong bus for a HID app | Phase 6 |

### The diagnostic that actually found it

```
wineserver -k && sleep 2
WINEDEBUG=+hid,+plugplay aradwine "$HOME/.wine-arad/drive_c/Arad/Arad Smart Meters/Octave.UI.exe" 2>&1 | head -60
```

Look for:

- `bus_main_thread L"UDEV"` and `udev_bus_init` — the udev backend running. **If you only see `L"SDL"` / `sdl_bus_init`, Phase 6 has not taken effect.**
- `bus_create_hid_device desc {vid 0483, pid d0d0, ...}` — the reader handed to Windows. If the only `bus_create_hid_device` lines are `vid 845e`, the reader is not being exposed.

Note: these traces come from Wine's **services** process, whose stderr does not go through a shell pipe. Read the terminal directly rather than relying on `tee`.

## Appendix B — Dead ends, so nobody repeats them

1. **PC/SC / `pcscd` / the winscard bridge.** The entire original plan. The reader is not a CCID device and `pcscd` will never see it.
2. **`dotnet48` as a substitute for `dotnet462`.** Blocked by `VSDAllowLaterFrameworkVersions=False`.
3. **Silent install (`/qn`) to skip the launch condition.** The custom action is in the execute sequence too.
4. **`DisableHWAcceleration` for WPF.** Reasonable-looking but irrelevant; the GLX error was a font crash in disguise.
5. **`log4net`.** It ships with the app but is not configured — there is no application log anywhere in the prefix. Don't go looking.
6. **Switching to WineHQ packages.** Unnecessary. Ubuntu's `wine-9.0` links `libudev.so.1` in `winebus.so`; the backend was present all along, just not selected.
7. **The Reader Serial Number field, before Phase 6.** Filling it in changes nothing while Wine isn't exposing the device — the error message is identical either way and will mislead you.

## Appendix C — If this ever stops working

The protocol underneath is documented, which makes a native Linux fallback realistic rather than hypothetical: the reader is an ST **CR95HF** behind an STM32 USB-HID bridge, and ST publishes the CR95HF command set for its own demo boards. Combined with the report layout in "Hardware facts" above, the handful of operations you actually need (read a meter, set units, dump the alarm log) could be reimplemented with `hidapi` in Python — no Windows involved.

Worth asking Arad for, in rough order of value: documentation of the reader's USB HID command set; an SDK or API reference for `CR95HF.dll` / `AradComm.dll` / `OctaveComm.dll`; a newer release than 1.0.35 (these binaries date from 2020); and whether an Android/iOS NFC app exists.
