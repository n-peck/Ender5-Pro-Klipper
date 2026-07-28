# Engineering Decisions

This document records significant engineering and architectural decisions made throughout the project.

Measured calibration values are recorded in `COMMISSIONING.md`.

---

# Repository

## Decision

GitHub is the project's single source of truth.

### Reason

Maintains a single authoritative copy of the project, provides full version history, and eliminates configuration drift between development machines.

---

# Configuration Architecture

## Decision

Split the Klipper configuration into logical modules.

```
hardware/
machine/
calibration/
```

### Reason

Separates permanent hardware configuration from machine geometry and measured calibration values, improving readability, maintainability and future hardware upgrades.

---

## Decision

Store measured values within the `calibration` directory.

### Reason

Calibration values are expected to change throughout the life of the printer and should be regenerated whenever hardware changes occur. Permanent hardware configuration should remain independent of printer tuning.

---

## Decision

Treat calibration files as disposable.

### Reason

Following major hardware changes (hotend, extruder, probe, etc.) the calibration directory can be regenerated without modifying the underlying hardware configuration.

---

## Decision

Use the official Klipper reference configuration as the baseline.

### Reason

Reduces configuration errors, simplifies troubleshooting and ensures compatibility with future Klipper releases.

---

## Decision

Retain a unified `[bed_mesh]` configuration.

### Reason

Klipper does not merge repeated `[bed_mesh]` sections across included configuration files. Geometry settings and generated mesh data must therefore remain within a single configuration section.

---

## Decision

Allow Klipper to manage generated calibration data using `SAVE_CONFIG`.

### Reason

Generated calibration values should not be maintained manually. If the generated block becomes corrupted, remove the entire block and allow Klipper to recreate it automatically.

---

# Version Control

## Decision

Commit all verified commissioning milestones.

### Reason

Provides known-good recovery points before major configuration changes, firmware upgrades or hardware modifications.

---

# Future Decisions

- Manage bed mesh generation through an external tooling workflow if configuration modularity becomes a limitation.
- Review configuration architecture following future hardware upgrades (Dragonfly hotend, Hero Me Gen 6, CAN bus, etc.).