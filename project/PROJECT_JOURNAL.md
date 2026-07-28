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

## Session 4 - 2026-07-25

Objectives

- Commission motion system
- Verify CR Touch
- Configure Git workflow

Completed

- Git SSH authentication configured
- Raspberry Pi now pushes directly to GitHub
- Extruder configuration separated
- Probe configuration completed
- Motion directions verified
- Probe offsets measured
- Successful homing achieved

Lessons Learned

safe_z_home required manual compensation using the nozzle coordinates rather than probe coordinates.

Next Session

Printer calibration.

## Session 5 — 2026‑07‑28

Objectives

- Validate probe offsets
- Confirm Z‑home behaviour
- Begin calibration workflow
- Investigate bed mesh configuration structure

Completed

- Verified probe offsets remain correct (X‑44, Y‑9)
- Confirmed safe_z_home behaviour and nozzle‑based homing
- Validated modular configuration structure
- Identified Klipper’s non‑merging behaviour for repeated section names
- Determined that bed mesh must be managed as a unified section
- Deferred bed mesh implementation to external tooling workflow

Lessons Learned

- Klipper overwrites repeated section names rather than merging them; bed mesh geometry and calibration cannot be split across multiple files.
- Modular configuration remains viable, but certain sections (e.g., [bed_mesh]) must be atomic.
- Bed mesh values should be managed via a dedicated tool to avoid parser conflicts.

Next Session

- PID tuning (hotend + bed)
- Extruder rotation distance calibration
- Begin PLA first‑layer validation

2026-07-28 — Created Git checkpoint before updating Klipper (v0.13.0-707 → v0.13.0-708) and KlipperScreen. Current printer operational with completed probe calibration and 5×5 bed mesh under investigation. Awaiting verification of SAVE_CONFIG behaviour after update.

Important: The SAVE_CONFIG block at the end of printer.cfg is managed exclusively by Klipper. Do not manually edit or partially delete this block. If it becomes corrupted, remove the entire block (including the #*# <---------------------- SAVE_CONFIG ----------------------> marker) and allow Klipper to regenerate it with SAVE_CONFIG.