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

# Session 6 – First Layer Investigation

## Objective
Investigate inconsistent first layer despite successful bed mesh generation.

## Initial Symptoms
- First layer appeared acceptable near X=0.
- Centre slightly over-squashed.
- Prints at X≈200 appeared to fail, initially believed to be nozzle contacting the bed.

## Investigation Performed
- Verified probe offsets were correct.
- Confirmed bed mesh probed the expected physical locations.
- Verified active mesh using `BED_MESH_OUTPUT`.
- Confirmed mesh compensation was active using manual paper tests across the X axis.
- Confirmed glass bed had not moved between probing and printing.

## Root Cause Found
Further investigation showed the nozzle was **not** contacting the bed.

Instead:
- No filament was being extruded.
- Filament could not be manually pushed through the hotend at 220°C.
- Filament also could not be withdrawn.
- Heat sink cooling fan was found not to be operating.

The hotend cooling fan had been connected to FAN1 on the SKR Mini E3 V3 but no Klipper fan configuration had yet been created.

This resulted in heat creep during repeated calibration sessions, causing PLA to soften inside the heatbreak and Capricorn tube.

## Corrective Actions
- Removed hotend assembly.
- Cleared filament blockage.
- Reassembled hotend.
- Configured Klipper heater fan.
- Configured part cooling fan.

## New Fan Configuration

```ini
[heater_fan heatbreak_cooling_fan]
pin: PC7
heater: extruder
heater_temp: 50.0
fan_speed: 1.0

[fan]
pin: PB15
```

## Status
✔ Heater fan now automatically operates above 50°C.

✔ Part cooling fan responds correctly to M106/M107.

Next session:
- Verify reliable manual extrusion.
- Re-run bed mesh.
- Resume first layer commissioning.