# Ender 5 Pro Commissioning Log

This document records the commissioning, calibration and validation of the printer.

Hardware installation history is recorded separately in `MACHINE_CHANGELOG.md`.

---

# Overall Status

| Stage | Status |
|------|--------|
| Firmware Bring-up | ✅ Complete |
| Motion Commissioning | ✅ Complete |
| CR Touch Commissioning | ✅ Complete |
| Initial Calibration | 🟡 In Progress |
| Reliable PLA Printing | ⬜ Pending |
| Reliable ABS Printing | ⬜ Pending |

---

# Session 1 – Machine Bring-up

**Date:** 2026-07

## Firmware

| Component | Version |
|-----------|----------|
| Klipper | v0.13.0-708 |
| Moonraker | Installed |
| Mainsail | Installed |
| KlipperScreen | Installed |

---

## Motion System

### Verification

| Test | Result |
|------|--------|
| X Axis | PASS |
| Y Axis | PASS |
| Z Axis | PASS |

### Motor Configuration

| Axis | Configuration |
|------|---------------|
| X | Default |
| Y | `dir_pin: PB2` |
| Z | `dir_pin: !PC5` |

---

## CR Touch

### Configuration

| Parameter | Value |
|----------|------:|
| X Offset | -44 mm |
| Y Offset | -9 mm |
| Samples | 3 |
| Sample Result | Median |
| Sample Tolerance | 0.020 mm |
| Sample Retries | 3 |

---

## Commissioning Outcome

**Status:** PASS

---

# Session 2 – Z Probe Calibration

## Probe Z Offset

### Calibration

Command:

```
PROBE_CALIBRATE
```

Final value:

```
z_offset: 0.390
```

Stored in:

```
calibration/probe.cfg
```

### Verification

Probe calibration completed successfully.

### Result

- PASS

---

## Commissioning Outcome

**Status:** PASS

---

# Session 3 – Motion Commissioning

## Motion Verification

### Axis Movement

| Axis | Result |
|------|--------|
| X | PASS |
| Y | PASS |
| Z | PASS |

Motion directions verified against the official Klipper reference configuration.

---

## Homing

| Function | Result |
|----------|--------|
| X Home | PASS |
| Y Home | PASS |
| Z Home | PASS |

---

## Safe Z Home

### Configuration

```
home_xy_position: 110,110
```

### Verification

- Probe homes at the physical centre of the bed.
- Nozzle correctly compensates for probe offsets.
- `PROBE_CALIBRATE` operates at the same physical location.
- Behaviour verified against the Klipper documentation.

### Result

- PASS

---

## Commissioning Outcome

**Status:** PASS

---

# Session 4 – Initial Calibration

## Probe Accuracy

### Acceptance Criteria

- Standard deviation < 0.010 mm

### Measured Result

```
maximum:             0.012500
minimum:            -0.005000
range:               0.017500
standard deviation:  0.006614
```

### Result

- PASS

---

## Probe Calibration Verification

### Configuration

```
z_offset: 0.390
```

### Verification

Existing calibration confirmed.

### Result

- PASS

---

## Hotend Cooling Verification

Before any calibration involving a heated nozzle:

- Heat nozzle to 60°C.
- Confirm heatsink fan starts automatically.
- Heat to printing temperature.
- Confirm manual extrusion is possible.
- Cool hotend.
- Verify heatsink fan remains running until temperature falls below 50°C.

Failure of the heatsink fan can cause heat creep during extended calibration sessions, leading to filament swelling inside the heatbreak and false first-layer diagnosis.

## Hotend PID

### Configuration

Target temperature:

```
220°C
```

Final values:

```
pid_Kp=25.744
pid_Ki=1.244
pid_Kd=133.227
```

Stored using:

```
SAVE_CONFIG
```

### Result

- PASS

---

## Heated Bed PID

### Configuration

Target temperature:

```
60°C
```

Final values:

```
pid_Kp=70.251
pid_Ki=1.082
pid_Kd=1140.694
```

Stored using:

```
SAVE_CONFIG
```

### Result

- PASS

---

## Bed Mesh

### Configuration

| Parameter | Value |
|----------|------:|
| Grid Size | 5 × 5 |

Stored using:

```
SAVE_CONFIG
```

> **Note**
>
> The `SAVE_CONFIG` block is managed exclusively by Klipper. Do not manually edit or partially delete this block. If it becomes corrupted, remove the entire generated block (including the `#*# <---------------------- SAVE_CONFIG ---------------------->` marker) and allow Klipper to regenerate it.

### Result

- PASS

---

## Extruder Rotation Distance

### Acceptance Criteria

- 100.0 ±0.2 mm extrusion

### Measured Result

| Parameter | Value |
|----------|------:|
| Filament | Elegoo PLA+ Black 1.75 mm |
| Hotend Temperature | 220°C |
| Mark Position | 120.0 mm |
| Commanded Extrusion | 100.0 mm |
| Remaining Distance | 20.0 mm |
| Actual Extrusion | 100.0 mm |

Current `rotation_distance` verified.

Configuration stored in:

```
calibration/rotation.cfg
```

### Result

- PASS

---

## Commissioning Outcome

**Status:** IN PROGRESS

**Next Stage**

- PLA first-layer validation
- Calibration cube
- Flow calibration
- Temperature tower
- Retraction calibration
- Pressure Advance
- Input Shaper
- Performance optimisation
- ABS validation

## Stage 6 — First Layer Calibration ✅ COMPLETE

### Tasks Completed

- [x] Configure hotend cooling fan
- [x] Configure part cooling fan
- [x] Re-run hotend PID calibration
- [x] Resolve heat creep blockage
- [x] Configure automatic heatsink fan control
- [x] Calibrate probe Z offset
- [x] Perform screw tilt adjustment
- [x] Re-run bed mesh calibration
- [x] Save probe offset using SAVE_CONFIG
- [x] Validate first layer across full printable area

### Result

Printer now produces a consistent first layer across the majority of the build area.

Residual variation is minimal and suitable for normal printing.

Future calibration should only require occasional:

- PROBE_CALIBRATE
- BED_MESH_CALIBRATE

without significant mechanical adjustment.

## Dimensional Accuracy Verification

**Status:** ✅ Complete

### Test Model

Teaching Tech 20 mm XYZ Calibration Cube

### Results

| Axis |   Target | Measured |    Error |
| ---- | -------: | -------: | -------: |
| X    | 20.00 mm | 19.83 mm | -0.17 mm |
| Y    | 20.00 mm | 19.99 mm | -0.01 mm |
| Z    | 20.00 mm | 20.18 mm | +0.18 mm |

### Assessment

Following correction of the Z-axis `rotation_distance`, dimensional accuracy is now within acceptable tolerances for a commissioned FDM printer.

No software axis compensation has been applied.

---

## Flow Calibration

**Status:** ✅ Complete

### Test Model

Teaching Tech Single-Wall Flow Calibration Cube

### Results

| Target Wall |     Measured |
| ----------- | -----------: |
| 0.40 mm     | 0.40–0.41 mm |

### Assessment

Measured wall thickness matched the intended extrusion width within measurement tolerance.

No adjustment to the extrusion multiplier was required.

### Commissioning Outcome

The printer has now demonstrated:

* Correct motion scaling
* Correct extruder calibration
* Correct dimensional accuracy
* Correct extrusion flow

Flow calibration is therefore considered complete.
