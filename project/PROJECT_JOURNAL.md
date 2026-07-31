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

### Engineering Decisions

- Confirmed that calibration values should remain separate from permanent hardware configuration.
- Decided to move `rotation_distance` into the `calibration` configuration alongside probe offset, PID values and pressure advance.
- Confirmed that calibration files should be considered disposable and regenerated whenever hardware changes occur.

### Lessons Learned

- Klipper merges repeated configuration sections for most modules but not for generated sections such as `[bed_mesh]`.
- `[bed_mesh]` must remain a single atomic configuration because mesh geometry and generated mesh values share the same section.
- The `SAVE_CONFIG` block should never be edited manually. If corruption occurs, remove the entire generated block and allow Klipper to recreate it.
- Separating permanent hardware configuration from generated calibration values produces a much cleaner and more maintainable repository structure.

### Next Session

- Perform PLA first-layer validation.
- Print the first dimensional calibration cube.
- Begin extrusion and print quality tuning.

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