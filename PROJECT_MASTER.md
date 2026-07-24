---
## PROJECT_JOURNAL.md
---

# Ender 5 Pro Project Journal

## Session 1

Initial planning.

Established project objectives.

Selected Klipper.

Created enclosure design.

...

## Session 2

Installed Debian.

Installed KIAUH.

Installed Klipper.

Installed Moonraker.

Installed Mainsail.

Installed KlipperScreen.

...

## Session 3

Installed SKR Mini E3 V3.

Compiled firmware.

Flashed firmware.

Verified USB communication.

Created modular project structure.

Initialised Git.

Identified that motion subsystem should be rebuilt using official Klipper reference files rather than reconstructed manually.

Next session:

• Rebuild motion.cfg
• Commission motion system

---
## PROJECT_STATUS.md
---

# Project Status

Version
-------
v1.0.0 (Commissioning)

Current Stage
-------------
Hardware Commissioning

Completed
---------
✔ Raspberry Pi 4 installed
✔ Debian 13 installed
✔ Klipper installed
✔ Moonraker installed
✔ Mainsail installed
✔ KlipperScreen installed
✔ Crowsnest installed

✔ SKR Mini E3 V3 installed
✔ Firmware compiled
✔ Firmware flashed
✔ USB communication verified

✔ Modular configuration structure created

✔ Git repository initialised

Current Hardware
----------------
Printer:
Ender 5 Pro

Controller:
BTT SKR Mini E3 V3

Probe:
CR Touch

Filament Sensor:
BTT Smart Filament Sensor

Extruder:
Creality metal extruder
Unitak3D direct-drive bracket
RTelligent 42Ncm motor

Hotend:
Stock Creality

Bed:
Glass

Enclosure:
Aluminium extrusion enclosure

Known Issues
------------
Motion configuration currently being rebuilt from official Klipper reference configurations.

Next Milestone
--------------
Complete motion subsystem.

---
## TODO.md
---

# TODO

## High Priority

☐ Rebuild motion.cfg
☐ Verify X axis
☐ Verify Y axis
☐ Verify Z axis
☐ Verify extruder

☐ Configure CR Touch
☐ Verify probe operation

☐ Configure thermistors
☐ Verify temperatures

☐ Configure heaters
☐ PID tune hotend
☐ PID tune bed

☐ Configure fans

☐ Configure LCD

☐ Configure filament sensor

## Calibration

☐ Extruder rotation distance

☐ Probe offsets

☐ Bed mesh

☐ Pressure advance

☐ Input shaping

## Future

☐ Dragonfly hotend

☐ Hero Me Gen6

☐ PEI sheet

☐ Chamber sensor

☐ Nevermore filter

☐ Moonraker PSU relay

☐ Automatic backups

☐ GitHub Actions config validation

---
## DECISIONS.md
---


---
## CHANGELOG.md
---

v1.0.0

Added

- SKR Mini E3 V3
- Git repository
- Modular configuration
- Documentation structure

Changed

- Removed Creality 4.2.2 board

Planned

- Motion commissioning
