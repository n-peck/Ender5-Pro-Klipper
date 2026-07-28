# Ender 5 Pro Commissioning Log

This document records the commissioning, calibration and validation of the printer.

Hardware installation history is recorded separately in `CHANGELOG.md`.

---

# Session 1 – Initial Bring-up

Date: 2026-07

## Firmware

- Klipper installed
- Moonraker installed
- Mainsail configured
- KlipperScreen installed
- Repository structure created
- Configuration modularised

---

## Motion System

### Verification

| Test | Result |
|------|--------|
| X Axis | PASS |
| Y Axis | PASS |
| Z Axis | PASS |

### Final Motor Configuration

| Axis | Configuration |
|------|---------------|
| X | Default |
| Y | `dir_pin: PB2` |
| Z | `dir_pin: !PC5` |

---

## Motion Limits

Safe commissioning limits configured.

| Parameter | Value |
|----------|------:|
| Max Velocity | 300 mm/s |
| Max Acceleration | 3000 mm/s² |
| Max Z Velocity | 15 mm/s |
| Max Z Acceleration | 100 mm/s² |
| Square Corner Velocity | 5 mm/s |
| Minimum Cruise Ratio | 0.5 |

These values are intentionally conservative and will be increased after resonance testing.

---

## CR Touch

### Probe Offset

Measured nozzle-to-probe offsets.

| Parameter | Value |
|----------|------:|
| X Offset | -44 mm |
| Y Offset | -9 mm |

### Repeatability

| Setting | Value |
|---------|------:|
| Samples | 3 |
| Result | Median |
| Tolerance | 0.02 mm |
| Retries | 3 |

---

## Safe Z Homing

### Verification

`G28`

**PASS**

### Observation

Printer firmware:

```
Klipper v0.13.0-707-gf604aeee
```

did **not** automatically compensate for the configured BLTouch XY offsets when using `safe_z_home`.

Correct operation required:

```
home_xy_position: 66,101
```

This places the probe at the physical bed centre (110,110).

This behaviour should be revalidated following future Klipper upgrades.

---

## Git Repository

Repository adopted as the project's single source of truth.

Workflow:

```
git pull
edit
git commit
git push
```

SSH authentication configured and verified.

---

# Session 2 – Repository Refactor

Configuration reorganised into logical groups.

```
hardware/
machine/
calibration/
```

## Hardware

Electrical configuration only.

## Machine

Physical printer geometry and operating limits.

## Calibration

Generated calibration values only.

This structure separates permanent hardware configuration from values expected to change during printer tuning.

---

# Session 3 – CR Touch Z Calibration

## Probe Calibration

`PROBE_CALIBRATE`

Measured probe offset:

```
z_offset: 0.390
```

Result committed to:

```
calibration/probe.cfg
```

### Notes

Probe calibration completed successfully.

First-layer validation still required during initial print calibration.

---

# Future Commissioning

- [ ] Hotend PID
- [ ] Bed PID
- [ ] Bed Mesh
- [ ] Extruder Rotation Distance
- [ ] PLA Calibration Cube
- [ ] Flow Calibration
- [ ] Temperature Tower
- [ ] Retraction Calibration
- [ ] Pressure Advance
- [ ] Input Shaper
- [ ] Performance Limit Optimisation
- [ ] ABS Validation

## Safe Z Home

Probe offsets verified.

Final values:

- x_offset = 44
- y_offset = 9

safe_z_home:

home_xy_position: 110,110

Result:

- Probe homes at physical bed centre.
- PROBE_CALIBRATE performs automatic probing and manual nozzle calibration at the same physical location.
- Behaviour matches Klipper documentation.

## Session 4 - PIR and Bedmesh

Important: The SAVE_CONFIG block at the end of printer.cfg is managed exclusively by Klipper. Do not manually edit or partially delete this block. If it becomes corrupted, remove the entire block (including the #*# <---------------------- SAVE_CONFIG ----------------------> marker) and allow Klipper to regenerate it with SAVE_CONFIG.
