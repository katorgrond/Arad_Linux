# Arad Smart Meters on Linux (Wine)

Run **Arad Smart Meters** — the Windows-only NFC configuration tool for Arad Octave ultrasonic water meters — on Linux under Wine. No Windows install, no dual boot, no VM.

## Environment
- Ubuntu 24.04 LTS · Wine (win32 prefix) · .NET Framework 4.6.2
- Arad Smart Meters v1.0.35
- Arad USB NFC reader — ST CR95HF, USB ID `0483:D0D0` (vendor **HID** class)

## The one thing that makes it work
The reader is a **vendor HID device, not a PC/SC (CCID) smartcard reader** — so the usual `pcscd` + Wine `winscard` bridge does nothing. The app only sees the reader once winebus stops using its SDL backend:

```
HKLM\System\CurrentControlSet\Services\winebus → "Enable SDL" = 0   (DWORD)
```

Mind the space in the value name. Without it, winebus exposes only game controllers and the reader is invisible to the application.

## Gotchas
- **Fonts are mandatory.** Install `corefonts` + `tahoma` in the prefix. A missing font triggers an uncatchable WPF `FailFast` the moment a text box is measured.
- The MSI won't install under Wine unmodified — use a launch-condition-stripped build.
- The app's *Reader Serial Number* field expects the reader's USB `iSerialNumber`.
- `pcscd` / PC-SC is irrelevant to this device — don't chase it.

## Contents
| File | Purpose |
|------|---------|
| `SETUP-GUIDE.md` | Verified working end-to-end setup (Ubuntu → udev perms → Wine prefix → .NET 4.6.2 + fonts → app install → winebus SDL fix → reader config), with troubleshooting and documented dead-ends. |
| `Arad-Smart-Meter-Software.zip` | Arad Smart Meters v1.0.35 installer (offline .NET bundled). |
| `arad-octave-reference.md` | Arad Octave meter technical reference. |
| `workstation-setup.py` | Optional Ubuntu office/paperwork toolchain installer (office / print / PDF). Unrelated to the meter software. |
