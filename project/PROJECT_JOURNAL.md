# Ender 5 Pro Project Journal

This journal records the engineering decisions, implementation work and lessons learned throughout the project.

The current verified state of the printer is recorded separately in `COMMISSIONING.md`.

---

# Session 1

## Objectives

- Define the project scope.
- Establish the upgrade roadmap.
- Select the firmware platform.

## Completed

- Planned the complete printer rebuild.
- Selected Klipper as the firmware platform.
- Designed the printer enclosure.
- Defined the long-term hardware upgrade roadmap.

---

# Session 2

## Objectives

- Build the software platform.
- Install the Klipper ecosystem.

## Completed

- Installed Debian.
- Installed KIAUH.
- Installed Klipper.
- Installed Moonraker.
- Installed Mainsail.
- Installed KlipperScreen.

### Engineering Notes

- Adopted Raspberry Pi as the dedicated printer controller.
- Established a clean software foundation before beginning printer commissioning.

---

# Session 3 — 2026-07

## Objectives

- Install the new control electronics.
- Bring the printer online under Klipper.
- Establish project documentation and version control.

## Completed

- Installed the BTT SKR Mini E3 V3.
- Compiled and flashed Klipper firmware.
- Verified USB communication.
- Created the project repository.
- Initialised Git version control.
- Designed the modular configuration architecture.

### Engineering Decisions

- Adopted a modular configuration layout to separate hardware, machine geometry and calibration values.
- Decided to rebuild the motion subsystem using the official Klipper reference configuration rather than continuing with manually reconstructed settings.

### Next Session

- Rebuild the motion subsystem.
- Commission printer motion.

---

# Session 4 — 2026-07-25

## Objectives

- Commission the motion subsystem.
- Verify CR Touch operation.
- Complete Git workflow.

## Completed

- Configured SSH authentication for Git.
- Enabled direct GitHub pushes from the Raspberry Pi.
- Completed modularisation of the printer configuration.
- Separated the extruder into an independent configuration file.
- Completed probe configuration.
- Rebuilt the motion subsystem using the Klipper reference configuration.
- Commissioned printer motion and homing.

### Engineering Decisions

- Adopted the official Klipper configuration as the baseline for future maintenance.
- Confirmed that separating hardware configuration into dedicated include files significantly improves maintainability and future hardware upgrades.

### Lessons Learned

- `safe_z_home` uses nozzle coordinates rather than probe coordinates.
- Correct probe positioning therefore requires compensation using the measured probe offsets.
- Initial assumptions regarding Safe Z Home behaviour were incorrect and required verification against the Klipper documentation.

### Next Session

- Begin printer calibration.
- Validate probe behaviour.
- Investigate bed mesh configuration.

---

# Session 5 — 2026-07-28

## Objectives

- Begin printer calibration.
- Validate configuration architecture.
- Investigate bed mesh implementation.

## Completed

- Validated the modular configuration architecture.
- Investigated Klipper's configuration parser behaviour.
- Completed PID tuning for both the hotend and heated bed.
- Generated the first production bed mesh.
- Verified extruder rotation calibration.
- Updated Klipper from v0.13.0-707 to v0.13.0-708.
- Created a Git checkpoint before firmware updates.

### Extruder Rotation Distance Verification

Following PID calibration, the extruder rotation distance was verified to confirm that commanded extrusion matched physical filament movement.

Due to Klipper's manual extrusion safety limit, the verification was performed using two consecutive 50 mm extrusion commands.

| Parameter             |                     Value |
| --------------------- | ------------------------: |
| Filament              | Elegoo PLA+ Black 1.75 mm |
| Initial Mark Position |                  120.0 mm |
| Commanded Extrusion   |                  100.0 mm |
| Remaining Distance    |                   20.0 mm |
| Actual Extrusion      |                  100.0 mm |

**Result:** ✅ PASS

The configured `rotation_distance` was confirmed to be correct. No adjustment was required.

The calibrated value is stored in:

```text
calibration/rotation.cfg
```

This completes commissioning of the extruder drive system and provides a verified baseline for subsequent flow calibration, pressure advance tuning and print quality optimisation.

### Engineering Decisions

- Confirmed that calibration values should remain separate from permanent hardware configuration.
- Decided to move `rotation_distance` into the calibration configuration alongside probe offset, PID values and pressure advance.
- Confirmed that calibration files should be considered disposable and regenerated whenever hardware changes occur.

### Lessons Learned

- Klipper merges repeated configuration sections for most modules but not for generated sections such as `[bed_mesh]`.
- `[bed_mesh]` must remain a single atomic configuration because mesh geometry and generated mesh values share the same section.
- The `SAVE_CONFIG` block should never be edited manually. If corruption occurs, remove the entire generated block and allow Klipper to recreate it.
- Separating permanent hardware configuration from generated calibration values produces a much cleaner and more maintainable repository structure.
- Klipper limits manual extrusion commands to 50 mm as a safety feature; a standard 100 mm extrusion calibration should therefore be performed using two consecutive 50 mm extrusion moves.

### Next Session

- Perform first-layer validation across the full build area.
- Optimise probe calibration, bed mesh and Z offset.
- Begin dimensional accuracy verification once a consistent first layer has been achieved.

# Session 6 – First Layer Calibration Completed

## Objectives
- Resolve inconsistent first layer despite bed mesh compensation.
- Configure SKR Mini E3 V3 cooling fans.
- Re-run probe and bed mesh calibration.
- Improve mechanical bed tram using Klipper screw tilt adjustment.
- Validate complete first layer across the printable area.

## Work Completed

### Hotend Investigation
During first layer testing the printer stopped extruding despite the nozzle appearing to be at the correct Z height.

Investigation found:

- Filament jammed within the heatbreak / Capricorn tube.
- Hotend cooling fan was not operating.
- Heat creep caused filament to soften above the melt zone resulting in a blockage.

Actions:

- Completely disassembled the hotend.
- Removed blocked filament.
- Cleaned heatbreak and nozzle.
- Reassembled hotend.
- Verified unrestricted manual filament movement.

### Fan Configuration

Configured both SKR Mini E3 V3 fan outputs.

Hotend heatsink fan:

- MCU Pin: `PC7`
- Operates automatically whenever the hotend exceeds the configured temperature threshold.

Part cooling fan:

- MCU Pin: `PB15`
- Controlled by slicer (M106).

Both fans verified operational.

### PID Calibration

Following restoration of the heatsink fan:

- Re-ran hotend PID calibration.
- Updated configuration with new PID values.

This ensures tuning reflects the printer's normal operating cooling conditions.

### Probe Configuration

Resolved long-standing SAVE_CONFIG issue.

Previous configuration prevented Klipper updating:

- BLTouch Z offset
- Bed Mesh

Solution:

- Allowed SAVE_CONFIG to own calibration values.
- Hardware configuration now contains only static probe parameters.
- Z offset and mesh are now written directly into printer.cfg.

Calibration workflow now operates normally.

### Screw Tilt Adjustment

Implemented Klipper screw tilt adjustment.

Initial probing positions required correction because screw coordinates must reference probe position rather than nozzle position.

Adjusted probe positions using probe offsets.

Mechanical tramming completed to approximately:

- Base screw
- Xmax/Ymin : 1 minute adjustment
- Xmax/Ymax : 2 minute adjustment
- Xmin/Ymax : 1 minute adjustment

Bed is now mechanically much closer to level before mesh compensation.

Reference note:

Counter-clockwise instruction from Klipper corresponds to:

- Bed moving away from nozzle.
- Tightening the bed spring.
- Clockwise rotation of the adjustment wheel when viewed from above.

### Bed Mesh

Following screw adjustment:

- Re-ran PROBE_CALIBRATE.
- Re-ran BED_MESH_CALIBRATE.
- Saved new mesh.

Mesh quality improved significantly compared with earlier sessions.

### First Layer Validation

Repeated Teaching Tech first layer tests.

Final observations:

- (0,0): Slightly close.
- (0,200): Good.
- (110,110): Good.
- (200,0): Slightly far.
- (200,200): Slightly far.

Variation is now small and considered acceptable for commissioning.

### Custom Diagnostic Print

Developed initial prototype of a custom first layer diagnostic print intended to replace the Teaching Tech calibration pattern.

Future improvements planned:

- Continuous serpentine path.
- Double-line raster.
- Faster fault identification.
- Coordinate-referenced diagnostics.

## Outcome

First layer calibration considered complete.

Remaining tuning can be performed through minor probe offset adjustments rather than mechanical correction.

Commissioning can now proceed to normal print validation.

# Session 7 - Z-Axis Calibration Root Cause Analysis

**Date:** 2 August 2026

## Objectives

- Resolve persistent dimensional inaccuracies in Z.
- Verify mechanical configuration following SKR Mini E3 V3 migration.
- Complete investigation into first layer and layer height issues.

---

## Summary

Following successful first layer calibration during Session 6, a 20 mm XYZ calibration cube revealed a major dimensional error.

### Observed behaviour

- First layer printed successfully.
- Print progressively scraped across previous layers.
- Extruder clicked and nozzle dragged through printed material.
- 20 mm calibration cube measured approximately 11 mm tall.

This indicated the problem was no longer related to first layer calibration, bed mesh or probe offset, but instead affected every subsequent Z move.

---

## Investigation

The following checks were completed:

### Stepper configuration

Current configuration:

```ini
microsteps: 16
rotation_distance: 8
```

This matched the generic BTT SKR Mini E3 V3 reference configuration.

---

### Mechanical verification

A physical movement test was performed.

Procedure:

```
G28
G92 Z0
G1 Z40 F300
```

Results:

- Leadscrew rotated exactly five complete revolutions.
- Bed travelled approximately 20 mm.

Measured travel:

```
20 mm / 5 revolutions = 4 mm per revolution
```

This conclusively proved the installed leadscrew has a **4 mm lead**.

---

## Root Cause

The installed Ender 5 Pro Z leadscrew provides:

- 4 mm travel per revolution

However Klipper was configured for:

```
rotation_distance: 8
```

As a result every commanded Z movement was approximately doubled internally while the mechanics only moved half the expected distance.

Consequences included:

- 20 mm cube printed approximately 11 mm tall.
- Progressive nozzle scraping.
- Incorrect layer spacing.
- Bed mesh compensation applied using incorrect Z scaling.
- Difficult first layer tuning despite mechanically level bed.

---

## Resolution

Updated Z configuration:

```ini
rotation_distance: 4
```

Following this change:

- Z travel matched commanded movement.
- Probe calibration repeated.
- Bed tramming repeated using SCREWS_TILT_CALCULATE.
- Bed mesh regenerated.
- SAVE_CONFIG updated successfully.

---

## Bed Tramming

Final screw adjustment:

| Screw | Adjustment |
|-------|------------|
| Xmin Ymin | Base |
| Xmax Ymin | 3 minutes CCW |
| Xmax Ymax | 5 minutes CCW |
| Xmin Ymax | 3 minutes CCW |

Reference:

Counter-clockwise (viewed from above)

- moves bed away from nozzle
- compresses spring
- tightens adjustment wheel

---

## Final Bed Mesh

Mesh statistics:

```
Average: +0.01 mm
Range:
Minimum -0.051 mm
Maximum +0.081 mm
Total variation 0.132 mm
```

This represents approximately a 50% improvement over previous measurements and is considered an excellent result for a stock Ender 5 Pro glass bed.

---

## Lessons Learned

- Never assume board manufacturer example configurations match the installed printer mechanics.
- Always verify actual mechanical travel experimentally.
- Rotation distance should always be validated after controller replacement.
- Mechanical measurement is more reliable than reference configuration examples.
- Probe calibration and bed mesh should always be repeated after changing Z kinematics.

---

## Current Status

### Completed

- ✓ Hotend cooling configuration
- ✓ Heat creep issue resolved
- ✓ PID recalibrated
- ✓ Probe calibration completed
- ✓ Screw tilt calibration completed
- ✓ Bed mesh calibration completed
- ✓ First layer calibration completed
- ✓ Root cause of incorrect Z motion identified

### Next Steps

- Verify dimensional accuracy using 20 mm XYZ cube.
- Calibrate extrusion multiplier / flow.
- Calibrate pressure advance.
- Calibrate input shaping.
- Begin print quality optimisation.

# Session 8 — 2026-08-02

## Objectives

* Integrate printer power management into Moonraker.
* Validate dimensional accuracy following Z-axis calibration.
* Verify extrusion flow accuracy.
* Continue commissioning towards production-ready operation.

## Completed

* Configured Raspberry Pi Host MCU.
* Configured automatic PSU relay activation during Raspberry Pi startup.
* Migrated printer power management from a Klipper `output_pin` to a Moonraker Power Device.
* Added native printer power controls to Mainsail.
* Verified automatic printer power-up after Raspberry Pi reboot.
* Verified dimensional accuracy using the Teaching Tech 20 mm XYZ calibration cube.
* Confirmed the corrected Z-axis `rotation_distance` resolved the previous height error.
* Completed single-wall flow calibration.
* Confirmed extrusion flow accuracy without requiring adjustment.

## Raspberry Pi GPIO Power Control

### Overview

Printer PSU control was migrated from a Klipper `output_pin` implementation to Moonraker Power Devices.

### Engineering Rationale

Although Klipper can drive Raspberry Pi GPIOs, once printer power is removed the printer MCU immediately disconnects, placing Klipper into a shutdown state. This prevents Klipper from reasserting the relay to restore power.

Moonraker operates independently of the printer MCU and therefore remains capable of controlling Raspberry Pi GPIOs regardless of printer power state.

### Raspberry Pi Host MCU

Configured a Linux Host MCU for future GPIO expansion.

```ini
[mcu rpi]
serial: /tmp/klipper_host_mcu
```

Although the Host MCU is available for future functionality, printer power is now managed directly by Moonraker.

### Automatic Power-On

Configured Raspberry Pi firmware to assert GPIO17 during boot:

```text
gpio=17=op,dh
```

This energises the PSU relay before Moonraker or Klipper start, ensuring the SKR controller is powered during system startup.

### Moonraker Integration

Configured a Moonraker GPIO Power Device using GPIO17.

Benefits include:

* Native printer power controls within Mainsail.
* Reliable remote printer power-on and power-off.
* Printer can be powered on from a completely de-energised state.
* Ready for future Home Assistant integration.
* Eliminates dependency on Klipper for PSU control.

### Result

**PASS**

Power management is now fully integrated into Moonraker and verified through successful cold boot and shutdown testing.

---

## Dimensional Accuracy Verification

Following correction of the Z-axis `rotation_distance`, the Teaching Tech 20 mm XYZ calibration cube was reprinted.

### Results

| Axis |  Nominal | Measured |    Error |
| ---- | -------: | -------: | -------: |
| X    | 20.00 mm | 19.83 mm | -0.17 mm |
| Y    | 20.00 mm | 19.99 mm | -0.01 mm |
| Z    | 20.00 mm | 20.18 mm | +0.18 mm |

### Result

**PASS**

The previous issue producing approximately half-height parts was completely resolved by correcting the Z-axis `rotation_distance`.

Overall dimensional accuracy is considered acceptable for a commissioned FDM printer. No software axis compensation has been applied, as the remaining deviations fall within expected printing tolerances.

---

## Flow Calibration

A Teaching Tech single-wall flow calibration cube was printed to verify extrusion accuracy.

### Results

| Target Wall Thickness |     Measured |
| --------------------: | -----------: |
|               0.40 mm | 0.40–0.41 mm |

### Result

**PASS**

Measured wall thickness matched the intended extrusion width within measurement tolerance.

No flow multiplier adjustment was required.

---

## Engineering Assessment

The printer has now successfully demonstrated:

* Correct X, Y and Z motion scaling.
* Correct extruder calibration.
* Accurate first-layer performance.
* Correct single-wall extrusion.
* Reliable dimensional accuracy.
* Fully integrated Moonraker power management.
* Stable system startup and shutdown behaviour.

The printer is now considered mechanically commissioned and suitable for general-purpose printing. Remaining commissioning work is focused on print quality optimisation rather than hardware calibration.

---

## Engineering Decisions

* Moonraker Power Devices adopted as the permanent PSU control solution.
* Raspberry Pi GPIO17 reserved for printer power relay control.
* Retained the Linux Host MCU for future GPIO expansion and accessory control.
* No axis compensation applied following dimensional verification.
* No flow multiplier adjustment required following flow calibration.

---

## Lessons Learned

* Printer power should be managed independently of the printer MCU to allow recovery from a fully powered-off state.
* Raspberry Pi firmware GPIO initialisation provides a reliable method of energising external relays before application startup.
* Mechanical calibration should always be verified before considering software compensation.
* Flow calibration should only be adjusted when repeated measurements consistently deviate from the intended extrusion width.

---

## Commissioning Status

The following commissioning activities are now complete:

* ✅ Motion system verification
* ✅ Endstop verification
* ✅ Z-axis calibration
* ✅ Extruder rotation calibration
* ✅ Probe calibration
* ✅ Probe accuracy verification
* ✅ Screw tilt adjustment
* ✅ Bed mesh calibration
* ✅ First-layer validation
* ✅ PID tuning
* ✅ Dimensional accuracy verification
* ✅ Flow calibration
* ✅ Moonraker power management integration

---

## Next Session

* Print a PLA temperature tower.
* Perform retraction tuning.
* Print a Benchy as the primary commissioning validation model.
* Complete a tolerance test to verify dimensional repeatability and part fit.
* Begin pressure advance tuning.

# Session 9 - Print Accuracy Calibration

## Objectives

Following completion of printer commissioning, this session focused on print accuracy, extrusion tuning and workflow improvements.

## Completed

### Pressure Advance

Pressure Advance was calibrated using Klipper's `TUNING_TOWER`.

Initial test:
- START=0.000
- FACTOR=0.0025

The initial range produced minimal visible change, indicating the test conditions were not sufficiently stressing the extrusion system.

A second test was performed using a narrower range:
SET_VELOCITY_LIMIT ACCEL=3000 SQUARE_CORNER_VELOCITY=5

TUNING_TOWER COMMAND=SET_PRESSURE_ADVANCE PARAMETER=ADVANCE START=0.03 FACTOR=0.001

The first signs of over-compensation (small gap after corners) appeared at approximately 25.2mm.

Calculated Pressure Advance:
0.030 + (25.2 × 0.001) = 0.0552

Final configured value:
pressure_advance: 0.055

---

### Flow Calibration

Flow calibration was completed using a single wall cube.

Nominal wall width:
0.40mm

Measured wall thickness:

- 0.40mm
- 0.41mm

Measurements were taken at three locations on each wall.

Results were within measurement tolerance and no adjustment to extrusion multiplier was required.

Final value:
Extrusion Multiplier = 1.00

---

### PrusaSlicer

A dedicated Klipper printer profile was created.

Changes include:

- Klipper G-Code flavour
- Direct Moonraker upload
- START_PRINT macro
- END_PRINT macro
- Removed Marlin acceleration commands (M201/M203/M205)

Printing can now be started directly from PrusaSlicer without exporting G-Code manually.

---

### START_PRINT improvements

START_PRINT now:

- Loads saved bed mesh
- Starts heating bed
- Waits for bed temperature
- Homes printer after bed reaches operating temperature
- Heats nozzle to print temperature
- Continues with purge sequence

This ensures homing is always performed with the printer at thermal equilibrium.

---

### Macros

Added:

- PREHEAT_PLA

Future additions:

- PREHEAT_PETG
- LOAD_FILAMENT
- UNLOAD_FILAMENT
- COOL_DOWN

---

## Outcome

Printer commissioning is now considered complete.

The printer has transitioned from commissioning into performance tuning and production readiness.