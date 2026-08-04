# Changelog

All notable changes to this project are documented in this file.

The format loosely follows [Keep a Changelog](https://keepachangelog.com/).

---

# v1.0.0

## Added

- Initial Git repository.
- Modular Klipper configuration structure.
- Project documentation framework.
- BTT SKR Mini E3 V3 mainboard support.

## Changed

- Replaced the Creality v4.2.2 mainboard with the BTT SKR Mini E3 V3.

---

# v1.1.0 - 2026-07-25

## Added

- Modular hardware configuration files.
- Dedicated `extruder.cfg`.
- SSH-based Git workflow from Raspberry Pi.
- Initial commissioning documentation.
- Hardware documentation.
- Known Issues documentation.

## Changed

- Corrected Y-axis motor direction.
- Corrected Z-axis motor direction.
- Measured and configured CR Touch probe offsets.
- Updated `safe_z_home` configuration.
- Reduced stock hotend maximum temperature to **250°C**.

## Fixed

- Resolved homing issues preventing successful `G28`.
- Verified CR Touch operation under Klipper.

---

# v1.2.0 - 2026-07-28

## Added

- 5 × 5 bed mesh calibration.
- Hotend PID calibration.
- Heated bed PID calibration.
- Extruder rotation distance calibration.
- Probe repeatability validation.
- Project commissioning records for Sessions 4 and 5.

## Changed

- Moved `rotation_distance` from hardware configuration to `calibration/rotation.cfg`.
- Standardised calibration file layout.
- Updated Klipper from **v0.13.0-707** to **v0.13.0-708**.
- Updated KlipperScreen.

## Fixed

- Confirmed final Safe Z Home behaviour using nozzle coordinates.
- Verified probe calibration remained valid following configuration changes.

## Session 9

### Added

- Pressure Advance calibration
- PREHEAT_PLA macro
- Direct Moonraker upload from PrusaSlicer
- Improved START_PRINT sequence

### Changed

- Created dedicated Klipper PrusaSlicer profile
- Removed unsupported Marlin G-Code commands
- START_PRINT now waits for bed temperature before homing
- Flow calibration completed

### Calibrations

Pressure Advance:
0.055

Flow:
1.00