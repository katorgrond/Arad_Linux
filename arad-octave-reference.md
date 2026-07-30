# Arad Octave Ultrasonic Water Meter — Technical Reference

A working reference for the Arad Octave transit-time ultrasonic water meter: measurement principle, outputs, configuration, and field requirements. Items that could not be confirmed against official Arad documentation are flagged in-line and in the "Unverified items" section.

---

## Executive Summary

The Arad Octave is a transit-time, dual-beam ultrasonic bulk water meter manufactured by Arad Ltd. (Israel), marketed under the Arad Group umbrella. It covers DN40–DN300 across three body materials (cast iron, polymer, stainless steel) and is certified to MID 2014/32/EU (ISO 4064:2014), AWWA, WRAS, NSF, and ACS. Key strengths are the absence of moving parts, IP68 submersibility, up to 15-year battery life, and a flexible output ecosystem (pulse, 4-20mA, Encoder/Sensus, M-Bus, Modbus, LoRaWAN). Configuration is performed via NFC using the proprietary Windows software **Arad Smart Meters**; the NFC reader clips to the meter display. Error codes visible on the display are limited to symbolic alarms (system error triangle, low battery banner, sleep mode); detailed alarm logging and configuration are handled exclusively in the Arad Smart Meters software. A critical field requirement is downstream back pressure of 0.5–0.7 bar and a completely water-filled pipe at all times — dry sensors will display zero and trigger sleep mode. Batteries are **not user-replaceable**; end-of-life means meter return to factory or authorised service.

---

## 1. Product Overview

### 1.1 What the Octave Is

The Octave is Arad's flagship bulk/commercial ultrasonic water meter, designed for:
- **Grid metering** — key meters in water supply grids and DMA (District Metered Areas)
- **District metering** — apartment buildings, housing estates, small neighbourhoods
- **Industrial metering** — challenging environments (production plants, mining)
- **Agricultural metering** — main meters for irrigation systems

It replaces mechanical (Woltmann/turbine) meters in these roles. There are **no moving parts**, which eliminates wear-related drift and reduces maintenance frequency significantly compared to mechanical alternatives.

### 1.2 Measurement Principle — Transit-Time Ultrasonic

The Octave uses a **transit-time, dual-beam** ultrasonic method:

Two ultrasonic sensors are mounted diagonally along the flow tube. Each sensor alternates as sender and receiver. An ultrasonic pulse sent **with** the flow travels faster than one sent **against** it. The meter measures both transit times (TAB: sensor A→B, and TBA: sensor B→A) continuously. The **time difference (TBA − TAB)** is directly proportional to the mean flow velocity (Vm). Flow rate = Vm × cross-sectional area of the flow tube.

This principle means:
- Measurement is completely non-intrusive — nothing crosses the flow path
- The meter is inherently **bi-directional** (forward and reverse equally accurate)
- Low flows are detectable because even small time differences are measurable electronically
- **Air in the pipe causes signal loss** — the sensors cannot transmit through air-water interfaces reliably

*Source: Arad Octave Datasheet Release 4.01 (Netafim, 2017); Arad Installation Manual 24573010 Rev04 05/2023, Section 6.0*

### 1.3 Product Variants / Line-Up

There are four distinct Octave sub-lines:

| Sub-line | Body | Sizes | Connection | Typical Use |
|----------|------|-------|------------|-------------|
| **Octave (Grid/Standard)** | Cast iron, epoxy coated | DN50–DN300 (2"–12") | Flanged ISO/BS/ANSI | Grid, agricultural, large commercial |
| **Octave District (Polymer)** | Highly reinforced polymer | DN40, DN50 (1½"–2") | Threaded NPT/BSP | Apartment buildings, small district |
| **Octave Industrial (Stainless Steel)** | AISI 316 stainless steel | DN50–DN200 (2"–8") | AWWA ANSI flanges only | Industrial, aggressive water, mining |
| **Octave High Flow** | Stainless steel AISI 316 | DN80–DN200 (3"–8") | ISO/ANSI/BS floating flanges | High-volume transfer — Q3 is 2.5× standard |

**Note on High Flow:** The Octave High Flow is a separate product line characterised by its stainless steel body and significantly higher Q3 (permanent flow rate). For example, a DN100 High Flow has Q3 = 250 m³/h vs Q3 = 100 m³/h on the standard DN100.

*Source: Arad Group product pages (arad.co.il, retrieved 2026-07-16); Arad Octave Datasheet Release 4.01 (2017)*

### 1.4 Key Specifications

**Environmental / Mechanical:**

| Parameter | Value |
|-----------|-------|
| Maximum Working Pressure | 16 bar (232 psi) |
| Liquid Temperature | 0.1°C to 50°C (32°F to 122°F) |
| Ambient Operating Temperature (display) | −25°C to +55°C |
| Environmental Protection | IP68 (submersible) |
| Pressure Loss | ΔP 0.16 bar at Q3 (varies by size — see head loss curves) |
| Severity: Mechanical | Class M1 |
| Severity: Electromagnetic | Class E1 |
| Power Source | 2 × D-size Lithium batteries, up to 15 years life |
| Configuration | Compact — display built into the meter body |
| Data Logger | 48KB, 4,130 data points (volumes + alarms) |

**Standards / Certifications:**
- MID 2014/32/EU (OIML R49:2013, EN 14154, ISO 4064:2014) — EU Declaration of Conformity signed 17/04/2023, valid to 14 Aug 2030
- AWWA C750
- WRAS (UK)
- NSF / ACS / KTW W-270 / AS/NZS 4020 / FM
- CE marked

**Precision / Accuracy — ISO 4064 rev.2014, Accuracy Class 2:**

The Q3/Q1 ratio (also called R-value) is **500:1** for all standard sizes DN40 through DN300. This is exceptionally high for a bulk meter and is one of the Octave's headline claims.

*Note: The older 2017 datasheet cites ISO 4064 rev.2005 Accuracy Class 2. The 2023 Installation Manual (24573010 Rev04) cites ISO 4064 rev.2014. The product is certified to the current 2014 revision. Confidence HIGH.*

### 1.5 Flow Rate Table by Size (ISO 4064)

From Arad Octave Datasheet Release 4.01 (primary source):

| Size | Q1 Min (m³/h) | Q2 Transition (m³/h) | Q3 Permanent (m³/h) | Q4 Overload (m³/h) | Q3/Q1 (R) | Starting Flow (m³/h) |
|------|--------------|---------------------|--------------------|--------------------|-----------|----------------------|
| DN40 Threaded | 0.160 | 0.256 | 40 | 50 | 250 | 0.025 |
| DN50 Threaded | 0.080 | 0.125 | 40 | 50 | 500 | 0.025 |
| DN50 | 0.080 | 0.125 | 40 | 50 | 500 | 0.025 |
| DN65 | 0.125 | 0.200 | 63 | 80 | 500 | 0.025 |
| DN80 | 0.200 | 0.320 | 63 | 80 | 500 | 0.025 |
| DN100 | 0.200 | 0.320 | 100 | 125 | 500 | 0.025 |
| DN150 | 0.500 | 0.800 | 250 | 313 | 500 | 0.200 |
| DN200 | 0.800 | 1.280 | 400 | 500 | 500 | 0.200 |
| DN250 | 2.000 | 3.200 | 1000 | 1250 | 500 | 0.500 |
| DN300 | 2.000 | 3.200 | 1000 | 1250 | 500 | 0.500 |

**Note on DN40:** R-value is 250, not 500. All other sizes are R500.

*Source: Arad Octave Datasheet Release 4.01 (Netafim AU, 2017) — Confidence HIGH*

### 1.6 Physical Dimensions (Cast Iron, Flanged)

| Size | L (mm) | W (mm) | H (mm) | Weight (kg) |
|------|--------|--------|--------|-------------|
| DN50 | 200 | 165 | 194 | 9 |
| DN65 | 200 | 185 | 210 | 11.5 |
| DN80 | 225 | 200 | 210 | 13 |
| DN100 | 250 | 220 | 223 | 15 |
| DN150 | 300 | 285 | 282 | 32 |
| DN200 | 350 | 340 | 332 | 45 |
| DN250 | 449 | 406 | 383 | 68 |
| DN300 | 499 | 489 | 456 | 96 |

Polymer DN40/DN50 (threaded): 300mm × 113mm × 155mm, 1.4–1.45 kg.
Stainless Steel (AWWA flanges): DN50 = 254mm long, 5.5 kg; DN200 = 508mm long, 51 kg.

*Source: Arad Octave Datasheet Release 4.01 (2017) and Arad Installation Manual 24573010 Rev04 (2023) — Confidence HIGH*

---

## 2. Configuration & Programming

### 2.1 Configuration Software

**Software name: Arad Smart Meters**

- Runs on **Windows PC** (version not specified in available documentation)
- Available from Arad directly; not a publicly downloadable consumer tool
- Used for all Arad ultrasonic meter configuration (not just Octave — also used with Sonata Pulse and others)

*Source: Arad Octave Configuration Manual (ManualsLib manual #2164668, retrieved 2026-07-16) — Confidence HIGH*

### 2.2 Physical Interface — NFC Reader

The Octave uses **NFC (Near Field Communication)** as its primary field configuration interface.

**Connection procedure:**
1. Fasten the NFC reader to the plastic adapter (A)
2. Clip the adapter + NFC reader onto the Octave display housing (B)
3. Connect the USB end of the NFC reader to the PC running Arad Smart Meters
4. The Link LED on the NFC reader illuminates **green** when properly connected
5. Double-click the Arad Smart Meters shortcut to launch the software
6. Log in (administrator-level Windows account required)
7. When connected, the meter's current configuration is read and saved as a timestamped file

**Critical warnings:**
- Meter output is **disabled** while connected to Arad Smart Meters — do not leave connected in-service
- Always click **"Disconnect"** within the software before removing the NFC reader; failure to do so leaves the meter in connected state with output disabled
- Initial configuration should ideally be completed **before** installation (not mandatory but recommended)

**Alternative: RS-232 Serial Connection**
A serial RS-232 communication module with USB-to-serial converter can be used as an alternative to NFC. Configured via the Connection tab in Arad Smart Meters (set correct COM port number).

*Source: Arad Octave Configuration Manual, pages 9–11 (ManualsLib #2164668, retrieved 2026-07-16) — Confidence HIGH*

### 2.3 Known Access Passwords

From the Scribd Octave Configuration Guide (2019-12, retrieved 2026-07-16):

| Mode | Password |
|------|----------|
| Programming mode | `arad1941` |
| Flow simulation mode | `sim2017` |

**Important caveat:** These passwords were found in a Scribd-hosted document (third-party distribution of what appears to be an Arad configuration guide). They could be outdated or version-specific. Verify against the current Arad Smart Meters version in use. Confidence: MEDIUM.

The software also notes: "The logged-in user should be an administrator user with full permissions to all folders" (Windows OS requirement, not meter-specific password).

Special functions pages (p.55+) are marked "intended for supervising technicians only" — suggesting a tiered access system exists but the exact mechanism is not fully documented in publicly available sources.

### 2.4 Configurable Parameters

Based on the Configuration Manual table of contents and individual page extractions:

**Display Settings (Chapter 3, pages 14–18):**
- Volume display units: m³, GAL, Ft³, A.F. (acre-feet), IGAL, A.I. (acre-inches), barrels
- Flow rate display units: m³/h, L/s, GPM, IGPM, BPM, Lt/m — must be selected as paired unit set
- Number of digits after decimal point (resolution)
- Accumulator mode: Net (Forward less Reverse), Forward Only, Reverse Only, Forward & Reverse alternating
- Temperature display: °C or °F, or Off
- Sleep mode threshold (time to sleep after empty pipe / no flow detection)

**Output Settings (Chapter 4, pages 19–43):**

*No Output* — display only, no electrical output

*Pulses mode:*
- Pulse 1 and Pulse 2 independently configurable
- Measuring units (can differ from display units)
- Pulse resolution (volume per pulse)
- Pulse width (milliseconds) — directly affects battery life on SSR module
- Forward pulses only, or reverse pulses, or one of each
- Alarm frequency output option (Pulse 2 can be assigned as alarm output)

*4-20mA + Pulse:*
- 4mA = zero flow (factory set)
- 20mA = programmable to any flow ≤ Q4 (defaults to max safe flow rate for the meter size, printed on sticker below LCD)
- Programmable for forward or reverse flow

*Encoder (Sensus protocol):*
- Protocol: UI1203 or UI1204 (Sensus/AMCO/Neptune-compatible)
- Optional additional pulse output

*Extended Encoder, CZ Module:* Variants for specific AMR network types (Confidence MEDIUM — limited detail in accessible docs)

*Modbus (RS485):*
- Slave address: 1–247
- Baud rate: up to 9600 BPS
- Supply voltage: 5–24 Vdc
- Max cable length: 1,000 metres
- Readable registers: Alarms (battery, empty pipe), AMR serial number, RTC, Volume units, Flow rate units, Current flow, Flow direction, Forward and reverse volumes, Flow/volume resolution
- Mode: Modbus only, or Modbus + Pulse (SSR)

*M-Bus:*
- Protocol version: M-Bus V2.1 module
- M-Bus voltage: 24–36 Vdc
- Max baud rate: 9600 BPS
- Max cable length: 3 metres (from module to bus connection point — this is a very short run; bus itself can be much longer via concentrator)
- Slave address and device ID configurable
- Transmission period configurable
- Readable: alarms, AMR serial, RTC, volumes, flow rates, direction

*LoRaWAN / 9xx MHz (Dialog3G):*
- Arad's proprietary AMR/AMI protocol family
- Dialog3G operates on 9xx MHz sub-GHz band
- LoRaWAN option available as separate register/module
- Configuration of communication interval (hours)
- Shabbat mode (see Section 3.5) — interval-based transmission during Sabbath

**Alarm Thresholds (Chapter 5, pages 44–46):**

*General:*
- Activation Quantity: volume of water that must pass before alarm detection activates (prevents false alarms at startup/commissioning)
- Alarms appear in meter logs AND on display; some types appear only in logs

*Flow Rate Alarm:*
- Threshold: minimum flow rate to trigger (must be ≥ Q1)
- Start Duration: time (minutes) above threshold before alarm activates
- End Duration: time (minutes) below threshold before alarm deactivates
- **Note: Flow Rate Alarms are NOT shown on the LCD — they appear in logs only**

*Leakage Alarm:*
- Threshold: minimum sustained low flow rate
- Start Duration (hours): time above threshold to trigger
- End Duration (minutes): time below threshold to clear
- Displayed in logs

*Pipe Burst Alarm:*
- Threshold: high flow rate indicative of burst
- Configuration similar to Flow Rate Alarm
- Appears in logs

*Reverse Flow Alarm:*
- Monitors reverse flow events
- Configurable threshold and duration
- Displayed in meter logs

**Meter Logs (Chapter 6, pages 47–49):**
- 48KB capacity, 4,130 data points
- Records volumes (periodic) and alarm events
- Configurable logging interval
- System events included: watchdog, critical change, low battery

**Advanced / Special Functions (Chapter 7, pages 51–62):**
- Clock Settings (RTC)
- LCD Test
- Totalizer Data (cumulative volume management)
- Special Functions (supervising technicians only — details not publicly documented)
- Application Settings: recording mode (manual/auto), output folder, base filename
- Shabbat mode configuration (on/off + interval)
- Flow Simulation mode (password-protected: `sim2017`) — allows simulated flow for testing pulse/4-20mA outputs without real flow; clears simulated volume on disconnect

### 2.5 Configuration Workflow — Step by Step

Standard field configuration sequence (before installation):

1. Install Arad Smart Meters on Windows PC
2. Clip NFC reader onto meter display; connect USB to PC
3. Launch Arad Smart Meters; verify green Link LED
4. Log in (admin account)
5. Software reads meter — saves timestamped configuration file automatically
6. Navigate to **Display Settings** → set volume units, flow rate units, decimal precision, accumulator mode
7. Navigate to **Output Settings** → select output type (Pulse/4-20mA/Encoder/Modbus/M-Bus), configure all parameters
8. Navigate to **Alarm Thresholds** → configure leakage, pipe burst, flow rate, reverse flow thresholds and durations
9. Navigate to **Meter Logs** → set logging interval
10. (Optional) Set clock under Advanced → Clock Settings
11. **Save** configuration to meter
12. Wait ~60 seconds for output module to activate with new settings
13. Click **Disconnect** in software before removing NFC reader
14. Verify display shows expected units and mode icons

*Source: Arad Smart Meters Configuration Manual (ManualsLib #2164668); Scribd Configuration Guide (2019-12) — Confidence HIGH for steps 1–13, MEDIUM for exact menu structure as screens may vary by software version*

---

## 3. Communication & Outputs

### 3.1 Output Module Overview

All electrical outputs are provided via a **plug-in output module** that attaches to the side of the meter body (Allen key 3mm, 2 N·m torque, o-ring sealed). The module is replaceable in the field without disturbing the meter's plumbing (see Section 7, Module Replacement). The module type must be ordered at time of purchase or sourced separately.

### 3.2 Pulse Outputs

**Three pulse output module types available:**

| Module Type | Notes | Max Voltage | Max Current | Requires External Power |
|-------------|-------|-------------|-------------|------------------------|
| Open Drain (Open Collector) | Single reading device only; no isolation | 35 VDC | 200 mA | No |
| Solid State Relay (SSR) | Multiple reading devices; isolated outputs; bidirectional | ±400 V | 120 mA | Optional (5–35 VDC) |
| Dry Contact (Mechanical Relay) | Multiple devices; isolated; mechanical contacts | 5–35 VDC | 15W max | Yes (5–35 VDC) |

**Pulse wiring (Open Drain — long cable):**
- Red: Pulse Out #1
- Green: Pulse Out #2
- Black: GND

**Pulse wiring (SSR/Dry Contact — long cable):**
- Red + Orange: Out #1
- Brown + Black: Out #2
- Short cable (Red): 5–35V+, (Black): 5–35V−, (Yellow, Dry Contact only): Earth

Cable supplied with all modules: 1.5m (Arad manual) / 5 feet (Netafim manual)
Maximum cable length: 500m (Arad manual) / 1,640 feet (Netafim manual)

**Pulse resolution:** Configurable. Resolution and pulse width shown on LCD display for each pulse output separately. Higher frequency/finer resolution pulses consume more battery — see battery life calculation tables (Section 5.3).

**Dry Contact recommendation:** For low-resolution applications only (10 to 100 gallons/pulse). Mechanical life: 10⁹ cycles.

*Source: Arad Installation Manual 24573010 Rev04 (2023), Section 14; Netafim Octave Installation & User Guide (OCT-MAN 05/23) — Confidence HIGH*

### 3.3 Encoder Output (Sensus/HRI-Style)

- Serial communication protocol using **UI1203 or UI1204** (Sensus protocol)
- Compatible with Sensus/AMCO/Mueller/Neptune AMR head-end systems
- Additional pulse output available as an option alongside encoder
- Enables integration into existing AMR systems using Sensus-compatible walk-by or drive-by readers

*Source: Arad Octave Datasheet Release 4.01; Installation Manual 24573010 Rev04 — Confidence HIGH*

### 3.4 4-20mA Analog Output

- Passive current loop: 4–20mA
- Loop supply voltage: 12–24 VDC (supplied by reading device or external PSU)
- Output impedance: 25 MΩ typical
- 4mA = zero flow (fixed)
- 20mA = configurable (default: maximum safe flow rate for meter size, printed on sticker below LCD)
- Programmable for forward or reverse flow
- Outdoor installation: surge protector Bourns 1669-03 recommended, mounted within 100mm of module
- Wiring: Red = current loop+, Black = current loop−, Shield = earth

*Source: Arad Installation Manual 24573010 Rev04, Section 14.4; Netafim Octave Installation & User Guide — Confidence HIGH*

### 3.5 Modbus (RS485)

- Module: Octave Modbus v2.0
- Physical interface: RS485, 2-wire
- Cable: CAT5 2xTP recommended
- Max baud rate: 9600 BPS
- Supply voltage: 5–24 VDC
- Max power consumption: 80mW
- Max cable length: 1,000 metres
- Wiring: Blue = D0/A/Tx+, White/Blue = D1/B/Tx−, Orange = 5–24V, White/Orange = GND
- Optional pulse output alongside Modbus

Available Modbus registers (readable): Alarms (battery, empty pipe), AMR serial number, Real Time Clock, Volume units, Flow rate units, Current flow, Flow direction, Forward volume, Reverse volume, Flow resolution, Volume resolution.

*Source: Arad Installation Manual 24573010 Rev04, Section 14.5 — Confidence HIGH*

### 3.6 M-Bus

- Module: Octave M-Bus V2.1
- M-Bus bus voltage: 24–36 VDC
- Max baud rate: 9600 BPS
- Max power consumption: 80mW
- Cable from module to bus connection: 3 metres (note: this is the pigtail length — M-Bus network itself can be longer via concentrator)
- Wiring: Red = BUSL1, Black = BUSL2
- Optional pulse output alongside M-Bus

*Source: Arad Installation Manual 24573010 Rev04, Section 14.6 — Confidence HIGH*

### 3.7 LoRaWAN / 9xx MHz / Dialog3G AMR

Arad's AMR/AMI ecosystem:
- **Dialog3G** is Arad's proprietary 9xx MHz sub-GHz wireless platform, supporting walk-by, drive-by, and fixed-network reading
- **LoRaWAN** is available as a separate register module (Dialog3G Interpreter Register)
- The Octave encoder output (UI1203/UI1204, Sensus) interfaces with Dialog3G units
- **Shabbat Mode:** A unique feature for Israeli utility compliance. When enabled: transmission occurs at a configurable interval in hours (e.g. every 4 hours) during the Jewish Sabbath, rather than on-demand. Factory-configured; identifiable by sticker on display.

*Source: Arad Group product pages (arad.co.il, retrieved 2026-07-16); Configuration Manual (ManualsLib #2164668) — Confidence MEDIUM (LoRaWAN/Dialog3G integration detail is sparse in public docs)*

### 3.8 Data Logging

- Onboard: 48KB, 4,130 data points
- Records: periodic volume readings + alarm events
- System events logged: watchdog resets, critical configuration changes, low battery, empty pipe detections
- Logs downloadable via Arad Smart Meters (NFC connection)
- Log interval configurable in Meter Logs section of software

---

## 4. Display & Normal Operation

### 4.1 Hardware Versions

There are **two distinct hardware/display versions**:

**Version 3** (manufactured before June 2017):
- Smaller display icon set
- Displays: Volume units (GAL), Flow rate units (GPM), Battery level icon, Flow direction arrow, Alarm/Error triangle, Output mode icon
- Does NOT show: water temperature, pulse resolution, communication mode icon, accumulator mode text

**Version 4** (June 2017 onwards — all current production):
- Expanded display — adds additional measuring units, water temperature readout, pulse output resolution display, sleep mode, communication mode icon
- This is the current version; Version 3 is legacy

*Source: Netafim Octave Installation & User Guide (OCT-MAN 05/23), Hardware Versions section — Confidence HIGH*

### 4.2 LCD Layout (Version 4 — Current)

The display is a vacuum-sealed (IP68) multiline LCD. Screen elements:

**Main number area (top):**
- 9-digit accumulator volume (12 digits in some descriptions) with programmable decimal point
- Volume units symbols: `bl` / `m³` / `IGAE` / `ft³` (shown in top-right corner)

**Secondary row (middle):**
- 5-digit flow rate with automatic floating decimal
- Flow rate units: `m³/h` / `L/s·L/m` / `IGPM`
- Accumulator mode: `FWD` / `NET` / `BCK`

**Icon/status row:**
- Flow direction arrow (up = forward, down = reverse)
- Pulse #1 resolution value
- Pulse #2 resolution value
- 4-20mA / AMI TYPE indicator
- Communication mode icon
- `LOW BATT.` banner
- System error triangle (Δ / △)
- Water temperature (°C/°F)
- Output mode code
- Shabbat-mode indicator (`שבת` — Hebrew characters)

**Sleep mode display:**
- When meter enters sleep (after ~24h of empty pipe/no flow, or configurable interval): all accumulator digits show `0.00.000.000` and the word `SLEEP` appears in the flow rate area, with the NET accumulator mode symbol visible and the system error triangle lit.

*Source: Arad Octave Datasheet Release 4.01 (2017), Digital Display section; Arad Installation Manual 24573010 Rev04 (2023), Section 10.0; Netafim Installation & User Guide (2023) — Confidence HIGH*

### 4.3 Display Icons — Meaning

| Icon | What It Means |
|------|---------------|
| Arrow (up) | Flow is in forward direction |
| Arrow (down) | Flow is in reverse direction |
| `m³/h` / `L/s/L/m` / `IGPM` | Flow rate measurement unit in use |
| `FWD` | Accumulator shows forward volume only |
| `NET` | Accumulator shows net (forward minus reverse) |
| `BCK` | Accumulator shows reverse volume only |
| Communication icon (radio waves) | NFC reader connected / communication active |
| `4-20mA` / `AMI TYPE: n` | Output module type installed (n = 0–3 or letter code) |
| `LOW BATT.` banner | Battery voltage low — service required |
| Triangle / Δ (System Error) | A system error condition is present — check logs |
| `188` with `°C°F` | Water temperature reading |
| `bl m³ IGAE ft³` (volume units) | Volume unit currently displayed |
| `Pulse #1: nnnnn` / `Pulse #2: nnnnn` | Configured pulse resolution for each output |
| `שבת` (Hebrew) | Shabbat mode is active |
| `SLEEP` | Meter is in sleep mode (empty pipe/no signal for configured period) |

### 4.4 Reading the Meter

Normal operation reading sequence:
1. Open the lid (lid should remain closed except when reading)
2. Top number = **cumulative totaliser** in configured volume units
3. Middle number = **current flow rate** in configured flow rate units
4. Flow direction arrow indicates direction of flow
5. Check for any alarm icons (LOW BATT., triangle, SLEEP)
6. Output mode icon confirms which module type is installed

---

## 5. Troubleshooting

### 5.1 Error Codes / Alarm Indicators on Display

The Octave LCD does **not** show numeric error codes. It uses symbolic indicators:

| Display Indicator | Meaning | Action |
|------------------|---------|--------|
| `LOW BATT.` banner illuminated | Battery voltage below threshold — meter approaching end-of-battery-life | Contact Arad service. Battery not user-replaceable. Meter must be returned to factory or authorised service centre. |
| Triangle / System Error icon (Δ) | A metering alarm or system fault has been detected | Connect Arad Smart Meters via NFC; review Meter Logs to identify specific alarm type and time-stamp |
| `SLEEP` on display, zeroes on accumulator | Meter has entered sleep mode — no valid flow measurement (usually empty pipe) | Check pipe is full of water. Ensure no air in pipe. Open downstream valve. Check air vents. Once pipe re-fills and flow resumes, meter wakes automatically. |
| Display completely blank | Battery exhausted OR display disconnected internally | If battery life was near end, return to service. If meter is newly installed and display blank, check for internal fault — return to Arad. |
| Flow rate shows zero when flow is expected | Empty pipe (sensors not wetted), or air in pipe | Ensure pipe is full. Check installation for air pockets. Verify back pressure (0.5–0.7 bar downstream). Confirm control valve is downstream not upstream. |
| `שבת` icon | Shabbat mode active | Normal operation if meter is configured for Shabbat mode. Transmission occurs at set intervals, not continuously. |

**Important:** Flow Rate Alarms, Leakage Alarms, Pipe Burst Alarms, and Reverse Flow Alarms are **logged in meter memory but do NOT appear as visual indicators on the LCD**. The only visible alarm indication for these is the system error triangle (Δ). Reading the logs via Arad Smart Meters is necessary to identify what triggered it.

*Source: Arad Octave Datasheet Release 4.01; Arad Installation Manual 24573010 Rev04; Configuration Manual (ManualsLib #2164668) — Confidence HIGH for display indicators; MEDIUM for log-only alarm behaviour (inferred from configuration manual alarm section)*

### 5.2 Software / Configuration Error Messages

These appear in **Arad Smart Meters software** (not on the meter LCD):

| Error Message | Meaning | Remedial Action |
|--------------|---------|-----------------|
| "Error: Connection" | Cannot establish communication with meter | Check NFC reader LED; reposition NFC reader on display; verify USB cable connected; check Windows Device Manager recognises device; ensure Demonstration mode is OFF; for RS-232, verify correct COM port |
| "Error: Send Command to Meter" | Communication interrupted mid-session | Verify NFC reader USB cable properly connected; ensure NFC reader's groove and protrusion match the display housing correctly |
| "Error: Illegal Input Value" | Invalid data entered during login or command | Re-enter correct credentials; check that the value entered is within allowed range |
| "Error: Time out" | Meter did not respond within expected window | Retry connection; reposition NFC reader; check for interference sources nearby |

*Source: Arad Octave Configuration Manual, page 62 (ManualsLib #2164668, retrieved 2026-07-16) — Confidence HIGH*

### 5.3 Common Field Problems and Fixes

**Problem: Display shows SLEEP or zero flow when water is flowing**
- Cause 1: Pipe not completely full — air in measuring section causes loss of ultrasonic signal. Non-wetted sensors cannot measure and display zero.
- Cause 2: No downstream back pressure (pipe open at far end). Octave requires 0.5–0.7 bar downstream back pressure to maintain full pipe.
- Cause 3: Meter installed at a high point — air collects at high points. Re-install at lowest available point.
- Cause 4: Meter installed on pump suction side — negative pressure causes cavitation and air entrainment.
- Fix: Install Combination Air/Vacuum Release Vent upstream of meter (position: 3"–4" meters → vent 12–18" before meter; 6"–8" meters → 18–24" before; 10"–12" meters → 30–36" before). Install check valve downstream to maintain back pressure. Control valves must be downstream, not upstream.

**Problem: Inaccurate reading / meter under-reads**
- Cause 1: Air in pipe causing intermittent signal loss and missed pulses
- Cause 2: Insufficient straight pipe length upstream — turbulent/swirling flow profile
- Cause 3: Installation immediately downstream of a pump without required straight length (10 DN upstream minimum from pump)
- Cause 4: Installation on pump suction side
- Cause 5: Excessive vibration from unsupported pipeline
- Fix: Address root cause per above. Ensure pipeline is supported on both sides of meter. Confirm minimum straight lengths (see Section 6).

**Problem: No pulse output / pulses not reaching SCADA/data logger**
- Cause 1: Output module not firmly seated (o-ring not sealed, screws not torqued to 2 N·m)
- Cause 2: Wrong output type module for application (e.g. Open Drain used with multiple reading devices — only SSR/Dry Contact supports this)
- Cause 3: For SSR/Dry Contact: external 5–35 VDC power supply not connected or insufficient
- Cause 4: Signal polarity error (polarity is mandatory — warning in both manuals)
- Cause 5: Cable too long for module type, or incompatible cable impedance
- Cause 6: Meter still in "connected" state (Arad Smart Meters connected via NFC, output disabled)
- Cause 7: ~60 second delay after saving configuration before output module activates
- Fix: Check module seating, power supply, polarity, cable specifications. Disconnect NFC if connected.

**Problem: 4-20mA output reads incorrectly**
- Cause 1: 20mA point programmed to wrong value — check the "SAFE MAX FLOW" sticker below the LCD and confirm 20mA is set to appropriate value
- Cause 2: Loop supply voltage outside 12–24 VDC range
- Cause 3: Surge damage (outdoor installation without surge protector)
- Fix: Reconfigure 20mA endpoint via Arad Smart Meters. Verify supply voltage. Add Bourns 1669-03 surge protector for outdoor runs.

**Problem: M-Bus / Modbus not responding**
- Cause 1: Slave address conflict on bus
- Cause 2: Baud rate mismatch
- Cause 3: M-Bus pigtail cable > 3 metres
- Cause 4: Module not correctly installed (o-ring, torque)
- Fix: Verify address settings in Arad Smart Meters match master configuration. Check baud rate (max 9600 BPS). Keep M-Bus pigtail to within 3m.

**Problem: Display settings change not reflected on output module**
- Cause: There is a ~60 second delay between saving configuration and output module activating with new settings.
- Fix: Wait 60 seconds after saving before testing output.

**Problem: Configuration save not appearing after reconnect**
- Cause: Demonstration mode is enabled in Arad Smart Meters settings.
- Fix: Go to Settings (bottom-right of login page) → Connection tab → uncheck "Demonstration mode".

*Source: Arad Installation Manual 24573010 Rev04 (2023); Netafim Octave Installation & User Guide (OCT-MAN 05/23); Arad Octave Configuration Manual (ManualsLib #2164668) — Confidence HIGH*

### 5.4 Installation Faults That Cause Measurement Errors

These are the most common root causes of reported meter problems — all preventable at installation:

| Installation Fault | Effect | Standard Requirement |
|-------------------|--------|---------------------|
| Insufficient upstream straight length | Turbulent/swirling profile → inaccurate reading | Minimum 2 DN upstream from elbow, valve, tee. 10 DN from pump. |
| Insufficient downstream straight length | Distorted profile | Minimum 2 DN downstream of meter |
| Meter at a high point in pipe | Air accumulation → empty pipe / sleep mode | Install at lowest available point in system |
| No downstream back pressure | Pipe not full → zero reading / SLEEP | Require 0.5–0.7 bar. Use check valve downstream. |
| Control valve upstream of meter | Cavitation / turbulent inlet | Always install control valves downstream |
| Meter on pump suction | Cavitation, negative pressure, air | Never install on suction side |
| No air vent upstream | Air pockets cannot escape → signal loss | Install Combination Air/Vacuum Release Vent per placement guidance |
| Vertical downward flow | Not recommended | Install horizontal or vertical upward flow only |
| Excessive vibration | Measurement errors | Support pipeline both sides of meter |
| Parallel pipe connections (tee bypass not isolated) | Unmeasured flow bypass | Ensure all flow passes through meter |
| Polymeric meter in middle of system | Mechanical load damage to body | Install near system end; use PVC/plastic connection on at least one side |

*Source: Arad Installation Manual 24573010 Rev04 (2023), Sections 12.2, 7.0; Netafim Octave Installation & User Guide (2023) — Confidence HIGH*

### 5.5 Battery — End of Life Behaviour

**Key facts:**
- Batteries: 2 × D-size Lithium, rated up to 15 years
- **Not user-replaceable** — both manuals state explicitly "there are no operator-serviceable parts inside this product"
- Low battery warning: `LOW BATT.` banner appears on LCD; also logged as a system event in meter logs
- Actual battery life depends heavily on pulse output configuration — see SSR battery life table:

| Meter Size | Outputs | Q4 (m³/h) | Pulse Resolution (m³/pulse) | Pulse Width (ms) | Battery Life (years) |
|-----------|---------|-----------|---------------------------|-----------------|----------------------|
| DN50 | 2 | 50 | 0.01 | 30 | 11.4 |
| DN80 | 2 | 80 | 0.01 | 20 | 10.7 |
| DN100 | 2 | 125 | 0.01 | 12 | 11.4 |
| DN50 (high freq.) | 2 | 50 | 0.001 | 7 | 5.1 |

- When `LOW BATT.` appears: contact Arad Ltd. or authorised distributor for meter replacement or factory service. There is no field battery replacement procedure.
- The SSR module is battery-powered internally; external 5–35 VDC can supplement for certain pulse parameter combinations and extends operation.

*Source: Arad Installation Manual 24573010 Rev04 (2023), Section 14.3 (SSR battery table); Netafim Octave Installation & User Guide (2023), General Information — Confidence HIGH*

---

## 6. Installation Requirements

### 6.1 Orientation

- **Recommended:** Horizontal installation, with the meter body axis horizontal and the display assembly facing upward or to the side.
- **Acceptable:** Vertical installation with flow going **upward**. Two pipe diameters of straight pipe required before and after elbows in vertical installations.
- **NOT recommended:** Vertical installation with downward flow (flow direction below horizontal plane).
- The meter is bi-directional — however, the flow direction arrow on the display and body must be confirmed to match the actual flow direction for proper accumulation mode.
- The size and flow direction are cast in raised letters on the outer surface of the meter body.

*Source: Arad Installation Manual 24573010 Rev04 (2023), Section 12.2; Netafim Octave Installation & User Guide (2023) — Confidence HIGH*

### 6.2 Straight Pipe Length Requirements

**Arad's official guidance** (from Installation Manual 24573010 Rev04):

> "For upstream & downstream straight pipes please use as much as the installation site will allow (the longer the better)."
> "When installing the Octave downstream of any hydraulic component (valve, pump) the recommended installation requirements are no less than the drawings recommendations."

Specific minimum requirements illustrated in both manuals:

| Installation Scenario | Upstream (before meter) | Downstream (after meter) |
|----------------------|------------------------|--------------------------|
| 90° elbow | 2 DN | 2 DN |
| Valve or tee connection | 2 DN | 2 DN |
| Pump (Arad manual) | 10 DN | 2 DN |
| Pump (Netafim manual) | 5 DN | 2 DN |
| Strainer | — | 2 DN (after strainer) |
| Pressure breaker after meter | — | ≥ 2 DN |

**Note on pump upstream distance:** The Arad Installation Manual 24573010 shows 10 DN from pump; the Netafim Installation & User Guide shows 5 DN. The Arad figure (10 DN) is more conservative and should be used where space allows. Confidence MEDIUM — two sources disagree; use Arad primary guidance.

### 6.3 Strainer Requirements

The Arad Installation Manual does not specify a mandatory strainer requirement or strainer mesh size. The illustrations show meters installed downstream of strainers with 2 DN straight pipe after the strainer.

The Netafim manual notes: "AWWA length Octaves may be bolted directly to a strainer" — implying strainers are commonly used but not mandatory per the Arad standard specification.

Best practice recommendation (based on good metering practice, not explicitly stated in Arad docs): Install a strainer upstream on systems where debris is expected, to protect sensor faces from fouling.

*Confidence LOW on strainer mesh specification — not specified in available documentation.*

### 6.4 Air Vents

**Mandatory for reliable operation.** Air in the pipe causes signal loss, zero readings, and sleep mode.

Netafim manual specifies:
- Install Combination Air/Vacuum Release Vent **or** Continuous Acting Air Vent upstream of meter
- Placement distances before meter:
  - 3" and 4" meters: vent 12–18" (300–450mm) before meter
  - 6" and 8" meters: vent 18–24" (450–610mm) before meter
  - 10" and 12" meters: vent 30–36" (760–915mm) before meter
- Air vent can be placed on a 6"–12" riser to evacuate larger air volumes
- Netafim warranty for 5-year coverage requires Netafim-branded air vent installation

Arad manual states: "Since air collects at the highest point of the system, installation of the flow meter should be at the lowest point."

### 6.5 Back Pressure

**Critical — often overlooked:**

From Arad Installation Manual 24573010 Rev04, Section 12.2:
> "Note: The Octave needs to operate with downstream back pressure of minimum 0.5–0.7 Bar. Do not install the meter with a fully open downstream pipe (with no back pressure)."

Means for achieving back pressure:
- Install a check valve downstream of the meter
- Ensure a downstream pressure-reducing or control valve maintains sufficient pressure
- In irrigation systems: the system pressure naturally provides back pressure when operating

### 6.6 Counter/Pipe Flanges

- Pipe flanges must be parallel to each other (flange faces coplanar)
- Install meter inline with pipe axis
- Permissible length deviation: Lmax − Lmin = 0.5mm (0.02")
- For gaskets: refer to standard dimensional drawings
- Flanges: ISO, BS 10, ANSI 150 for standard cast iron; AWWA ANSI flanges only for stainless steel

### 6.7 Module Replacement

Field-replaceable procedure (Section 15.0 of Arad Installation Manual):
1. Dry the connector area thoroughly
2. Remove seal cover from screws (sharp tool)
3. Remove screws using Allen key 3mm
4. Remove old module
5. Dry connector area again
6. Check/insert o-ring; lubricate with silicone grease
7. Attach new module
8. Hand-tighten screws, then torque to 2 N·m with torque wrench (apply symmetrically)
9. Replace seal cover on screws

---

## 7. Official Documentation

All documents listed below were located and cross-referenced during this research (2026-07-16):

### 7.1 Primary Arad Documents

| # | Document | URL | Date | Notes |
|---|----------|-----|------|-------|
| 1 | Octave Brochure / Datasheet (Release 4.01) | https://www.netafimusa.com/globalassets/local/au/pdf-content-files/arad-octave-2017.pdf | February 2017 | Full specs, flow table, display diagram, outputs. Older but still accurate for core specs. |
| 2 | Octave Brochure / Datasheet (Release 4.02) | https://www.arad.co.il/wp-content/uploads/Octave_2019_EN.pdf | 2019 (URL 404 at time of research) | Supersedes 4.01. Check arad.co.il for current version. |
| 3 | Octave Installation Manual (24573010 Rev04 05/2023) | https://www.arad.co.il/wp-content/uploads/OCTAVE-Installation-Manuel-EN-web.pdf | May 2023 | **Most current primary Arad installation document.** Covers all outputs, dimensions, wiring, EU DoC. |
| 4 | Octave Installation Manual (older, pre-NFC branding) | https://www.arad.co.il/wp-content/uploads/OCTAVE-Installation-Manuel-EN.pdf | Pre-2023 | Earlier version — superseded by Rev04 |
| 5 | Octave Configuration Manual | https://www.manualslib.com/manual/2164668/Arad-Octave.html | Not dated (ManualsLib hosted) | 73 pages. Full software guide for Arad Smart Meters. Primary reference for configuration. |
| 6 | Octave Configuration Guide (Scribd) | https://www.scribd.com/document/667168225/2019-12-Octave-Configuration-guide | December 2019 | 9-page field configuration quick guide. Contains simulation mode passwords. |
| 7 | Octave High Flow brochure | https://www.arad.co.il/wp-content/uploads/Octave-high-flow_NEW-4.pdf | Not dated | High Flow variant specs |
| 8 | Octave Floating Flanges Installation Guide | https://www.arad.co.il/wp-content/uploads/Floating-flanges-Manuel_270318_2_compressed.pdf | March 2018 | Stainless steel floating flange variant |
| 9 | Arad Downloads page (master list) | https://www.arad.co.il/downloads/ | Retrieved 2026-07-16 | Lists all available documents in multiple languages |

### 7.2 Distributor / Third-Party Documents

| # | Document | URL | Date | Notes |
|---|----------|-----|------|-------|
| 10 | Netafim Octave Installation & User Guide | https://www.netafimusa.com/bynder/B7E58843-6A81-4C27-B4FEBD5D4849A1BD-oct-man-octave-manual.pdf | May 2023 (OCT-MAN 05/23) | Full installation guide incl. hardware versions, outputs, wiring diagrams — US market |
| 11 | Netafim AU Octave Configuration Guide | https://www.netafim.com.au/contentassets/23e09c1593144653a560133529034ec7/octave-configuration-guide.pdf | Not dated | Config guide for Netafim Australia market |
| 12 | Arad Octave DN50 Installation Manual (ManualsLib) | https://www.manualslib.com/manual/2014209/Arad-Octave-Dn-50.html | Not dated | DN50-specific installation manual |
| 13 | Arad Octave Installation Manual (ManualsLib, older) | https://www.manualslib.com/manual/1419549/Arad-Octave.html | Not dated (pre-2017) | Older version |
| 14 | Arad Octave Datasheet Scribd (Release 4.02) | https://www.scribd.com/document/576570906/ARAD-Octave-Data-Sheet-Rel-4-02-2019 | 2019 | Community-uploaded scan of Release 4.02 datasheet |
| 15 | MWA Technology Octave Product Page | https://www.mwatechnology.com/products/arad-octave-ultrasonic-water-meter/ | Retrieved 2026-07-16 | Flow table by model number; useful cross-reference |
| 16 | Pipersberg Modbus Module SRS | https://www.pipersberg.de/wp-content/uploads/2021/09/OCTAVE-Handbuch-Modbus-Modul.pdf | 2021 | German-market Modbus module documentation |

### 7.3 Certification Documents

- EU Declaration of Conformity: issued 17/04/2023 by Arad Ltd., signed by Nastiya Rubin (Product Certification Manager). Certificate SK 20-MI001-SMU062 revision 3, issued 09/01/2023, valid until 14/08/2030. Notified Body 1781 Slovak Institute of Metrology. Included in Arad Installation Manual 24573010 Rev04 (p.18).

---

## 8. Gaps / Needs Verification

The following items could not be fully confirmed from publicly available documentation and should be verified against the full Arad Smart Meters software or direct contact with Arad technical support:

| Gap | What's Unknown | How to Verify |
|-----|---------------|---------------|
| Full alarm code taxonomy | Individual alarm codes/types visible in meter logs (beyond Flow Rate, Leakage, Pipe Burst, Reverse Flow) are not fully documented in public sources | Access Arad Smart Meters software; review Meter Logs → Alarms section |
| Firmware versions | Version numbers for Arad Smart Meters software and meter firmware are not in public docs | Check "About" page in Arad Smart Meters; Meter Info → Software tab shows firmware version on connected meter |
| Password validity | `arad1941` (programming) and `sim2017` (simulation) found in a 2019 Scribd document — may be version-specific or outdated | Test against installed Arad Smart Meters version; request from Arad |
| Special Functions (p.55+) content | Marked "for supervising technicians only" — not detailed in any public document | Requires Arad authorised technician access; contact Arad service |
| Numeric error register in Modbus | Specific register addresses and error bit meanings for Modbus | Request Modbus register map from Arad (separate technical document) |
| K-factor / flow correction | Whether the Octave supports a field-adjustable K-factor or correction coefficient is not confirmed | Consult Arad Smart Meters Special Functions or contact Arad |
| Strainer mesh specification | No mesh size or strainer type specified in available Arad docs | Contact Arad; for UK water applications, follow WRAS guidance |
| LoRaWAN configuration detail | Integration with LoRaWAN networks described only at product level — no NwkSKey/AppKey configuration procedure found | Consult Dialog3G LoRaWAN Interpreter Register documentation |
| Battery replacement service cost/lead time | Not in any public document | Contact Arad Ltd. or UK distributor directly |
| Stainless Steel Octave specific installation notes | SS variant has AWWA flanges only and different sealing requirements — dedicated installation manual not retrieved | Use Arad floating flanges manual (#8 above) |

---

## Sources Summary

| # | Source | URL | Date | Reliability |
|---|--------|-----|------|-------------|
| 1 | Arad Octave Datasheet Release 4.01 (Netafim AU) | https://www.netafimusa.com/globalassets/local/au/pdf-content-files/arad-octave-2017.pdf | Feb 2017 | High |
| 2 | Arad Octave Installation Manual 24573010 Rev04 | https://www.arad.co.il/wp-content/uploads/OCTAVE-Installation-Manuel-EN-web.pdf | May 2023 | High |
| 3 | Arad Octave Configuration Manual (ManualsLib) | https://www.manualslib.com/manual/2164668/Arad-Octave.html | Unknown (current) | High |
| 4 | Octave Configuration Guide (Scribd, 2019-12) | https://www.scribd.com/document/667168225/2019-12-Octave-Configuration-guide | Dec 2019 | Medium |
| 5 | Netafim Octave Installation & User Guide | https://www.netafimusa.com/bynder/B7E58843-6A81-4C27-B4FEBD5D4849A1BD-oct-man-octave-manual.pdf | May 2023 | High |
| 6 | Arad Group Octave product page | https://www.arad.co.il/products/bulk-water-meters/octave-ultrasonic-water-meter/ | Retrieved 2026-07-16 | High |
| 7 | Arad Group Octave High Flow page | https://www.arad.co.il/products/bulk-water-meters/octave-high-flow/ | Retrieved 2026-07-16 | High |
| 8 | Arad Downloads page | https://www.arad.co.il/downloads/ | Retrieved 2026-07-16 | High |
| 9 | MWA Technology Octave page | https://www.mwatechnology.com/products/arad-octave-ultrasonic-water-meter/ | Retrieved 2026-07-16 | Medium |
| 10 | Arad Octave Datasheet Scribd (Release 4.02) | https://www.scribd.com/document/576570906/ARAD-Octave-Data-Sheet-Rel-4-02-2019 | 2019 | Medium |
| 11 | ManualsLib — Arad Octave DN50 | https://www.manualslib.com/manual/2014209/Arad-Octave-Dn-50.html | Unknown | Medium |
| 12 | ManualsLib — Arad Octave (older) | https://www.manualslib.com/manual/1419549/Arad-Octave.html | Pre-2017 | Medium |

---

## Confidence Assessment

- **Overall confidence: MEDIUM-HIGH**

**HIGH confidence (verified across 2+ primary sources):**
- Core specifications (pressure, temperature, IP68, battery life, body materials)
- Flow rate table Q1–Q4 by size, R-value of 500 (DN50+)
- All six output module types and their wiring specifications
- NFC reader as primary configuration interface; Arad Smart Meters software
- Display icons and their meanings (Version 3 vs Version 4 distinction)
- Installation requirements (orientation, back pressure, air vents, straight lengths)
- Battery non-serviceability
- Module replacement procedure

**MEDIUM confidence (single source or partially extracted):**
- Software passwords (`arad1941`, `sim2017`) — from 2019 third-party document
- Exact configurable parameter detail (some screens not fully accessible)
- Alarm threshold parameter detail (partially extracted from ManualsLib page summaries)
- LoRaWAN/Dialog3G integration specifics
- Pump upstream distance (two sources disagree: 5 DN vs 10 DN)

**LOW confidence / unverified:**
- Full Modbus register map
- K-factor / correction coefficient availability
- Special Functions content (technician-only, not in public docs)
- Strainer mesh requirements

**What would significantly improve this research:**
1. Full Arad Smart Meters software installation to browse all configuration screens
2. Arad technical support contact for Modbus register map
3. Request the current Arad Smart Meters user manual (separate from the Configuration Manual on ManualsLib)
4. Physical access to a connected Octave meter for first-hand display and software documentation

---

*Manufacturer: Arad Ltd., Dalia 1923900, Israel · www.arad.co.il*
*All specifications subject to change — check www.arad.co.il for most current documentation*
