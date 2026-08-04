# Calibration Guide

This document defines the recommended calibration sequence and records the latest calibration results.

Current verified calibration values are recorded in `COMMISSIONING.md`.

---

# Calibration Order

Perform calibration in the following order after any major hardware changes.

| Step | Calibration | Status |
|------|-------------|--------|
| 1 | Probe Accuracy | ✅ |
| 2 | Probe Z Offset (`PROBE_CALIBRATE`) | ✅ |
| 3 | Hotend PID | ✅ |
| 4 | Heated Bed PID | ✅ |
| 5 | Bed Mesh | ✅ |
| 6 | Extruder Rotation Distance | ✅ |
| 7 | PLA First Layer | ⬜ |
| 8 | Calibration Cube | ⬜ |
| 9 | Flow Calibration | ⬜ |
| 10 | Temperature Tower | ⬜ |
| 11 | Retraction Calibration | ⬜ |
| 12 | Pressure Advance | ⬜ |
| 13 | Input Shaper | ⬜ |
| 14 | Performance Optimisation | ⬜ |
| 15 | ABS Validation | ⬜ |

---

# Probe Accuracy

Command:

```
PROBE_ACCURACY
```

## Run 1

```
maximum:             0.015000
minimum:             0.007500
range:               0.007500
average:             0.011500
median:              0.012500
standard deviation:  0.002550
```

## Run 2

```
maximum:            -0.005000
minimum:            -0.017500
range:               0.012500
average:            -0.012500
median:             -0.015000
standard deviation:  0.004743
```

Result:

- PASS

---

# Probe Z Offset

Command:

```
PROBE_CALIBRATE
```

Calibration stored using:

```
SAVE_CONFIG
```

---

# Hotend PID

Command:

```
PID_CALIBRATE HEATER=extruder TARGET=220
```

## Run 1

```
pid_Kp=26.134
pid_Ki=1.351
pid_Kd=126.423
```

## Run 2

```
pid_Kp=25.744
pid_Ki=1.244
pid_Kd=133.227
```

Calibration stored using:

```
SAVE_CONFIG
```

---

# Heated Bed PID

Command:

```
PID_CALIBRATE HEATER=heater_bed TARGET=60
```

## Run 1

```
pid_Kp=70.251
pid_Ki=1.082
pid_Kd=1140.694
```

Calibration stored using:

```
SAVE_CONFIG
```

---

# Bed Mesh

Generate a 5 × 5 bed mesh.

Calibration stored using:

```
SAVE_CONFIG
```

> **Important**
>
> The `SAVE_CONFIG` block is managed exclusively by Klipper.
>
> Never manually edit or partially delete the generated block.
>
> If corruption occurs, remove the entire generated block (including the `#*# <---------------------- SAVE_CONFIG ---------------------->` marker) and allow Klipper to regenerate it.

---

# Extruder Rotation Distance

Procedure:

- Heat the hotend to 220°C.
- Mark filament at 120 mm.
- Extrude 100 mm (two 50 mm moves due to Klipper safety limits).
- Measure the remaining distance.

Latest verification:

| Parameter | Value |
|----------|------:|
| Filament | Elegoo PLA+ Black 1.75 mm |
| Mark Position | 120.0 mm |
| Commanded Extrusion | 100.0 mm |
| Remaining Distance | 20.0 mm |
| Actual Extrusion | 100.0 mm |

Result:

- PASS
- No adjustment required.

Configuration:

```
rotation_distance
```

is stored in:

```
calibration/rotation.cfg
```

# Printer Power Management

- Raspberry Pi GPIO17 configured for PSU relay control
- Automatic relay activation during Raspberry Pi boot
- Moonraker power device configured
- Printer power controllable directly from Mainsail
- Verified automatic SKR startup after Raspberry Pi reboot

**Status:** ✅ Complete

## Dimensional Accuracy Calibration

### Objective

Verify that the printer produces dimensionally accurate parts following mechanical calibration.

### Test Model

Teaching Tech 20 mm XYZ Calibration Cube

### Results

| Axis |   Target | Measured |
| ---- | -------: | -------: |
| X    | 20.00 mm | 19.83 mm |
| Y    | 20.00 mm | 19.99 mm |
| Z    | 20.00 mm | 20.18 mm |

### Outcome

PASS

The previous Z-axis scaling error was resolved following correction of the Z-axis `rotation_distance`.

Measured dimensions are considered acceptable without applying software compensation.

---

## Flow Calibration

### Objective

Verify that the configured extrusion rate produces the intended wall thickness.

### Test Model

Teaching Tech Single-Wall Flow Calibration Cube

### Results

Target wall thickness:

```
0.40 mm
```

Measured wall thickness:

```
0.40–0.41 mm
```

### Outcome

PASS

Measured wall thickness matched the expected extrusion width within measurement tolerance.

No flow multiplier adjustment was required.

These results confirm that the previously calibrated extruder `rotation_distance` and extrusion settings remain correct.

# Pressure Advance

Method:
Klipper TUNING_TOWER

Final value:
pressure_advance: 0.055

Calibration performed using:
SET_VELOCITY_LIMIT ACCEL=3000 SQUARE_CORNER_VELOCITY=5

TUNING_TOWER COMMAND=SET_PRESSURE_ADVANCE PARAMETER=ADVANCE START=0.03 FACTOR=0.001

Over-compensation first observed at approximately 25.2mm.

Pressure Advance calculated as:
0.030 + (25.2 × 0.001)

Final configured value:
0.055

---

# Flow Calibration

Method:

Single wall cube

Target wall thickness:
0.40mm

Measured:
0.40
0.41

Average results within tolerance.

No extrusion multiplier adjustment required.

Final extrusion multiplier:
1.00