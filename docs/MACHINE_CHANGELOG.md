# Ender 5 Pro Machine Changelog

This document records physical modifications made to the printer.

Calibration activities are recorded separately in `COMMISSIONING.md`.

---

# Current Configuration

## Printer

- Creality Ender 5 Pro

## Controller

- BTT SKR Mini E3 V3

## Firmware

- Klipper
- Moonraker
- Mainsail
- KlipperScreen

## Probe

- Creality CR Touch

## Filament Sensor

- BTT Smart Filament Sensor

## Extruder

- Creality Metal Extruder
- Direct Drive Conversion

## Hotend

- Stock Creality Hotend

## Build Surface

- Creality Glass Bed

## Enclosure

Custom aluminium extrusion enclosure.

Approximate dimensions:

- 560 × 560 mm
- 600 mm tall

Ceramic tile base.

Filament supplied from external EIBOS dryer.

---

# Modification History

## 2026-07

### Electronics

- Installed BTT SKR Mini E3 V3
- Installed Klipper firmware
- Installed KlipperScreen

### Probe

- Installed CR Touch

### Filament

- Installed BTT Smart Filament Sensor

### Motion

- Converted to direct drive

### Software

- Migrated configuration to modular repository structure

---

# Planned Upgrades

## Cooling

- Hero Me Gen 6

## Hotend

- Phaetus Dragonfly BMS

## Resonance

- ADXL345 Accelerometer

## Chamber

- Heated chamber
- Chamber temperature monitoring

## Toolhead

- Final production wiring
- Connector pass-through panel

## Print Profiles

- PLA
- PETG
- ABS

---

# Notes

The Git commit history records software configuration changes.

This document records only physical machine changes.

### Probe geometry correction

Corrected CR Touch XY offsets after discovering the sign convention had been reversed during commissioning.

Old:

x_offset = -44
y_offset = -9

New:

x_offset = 44
y_offset = 9

Returned safe_z_home to the physical bed centre (110,110).

Recalibrated Z probe offset:

z_offset = 0.108