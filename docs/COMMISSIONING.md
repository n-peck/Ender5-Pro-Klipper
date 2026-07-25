# Commissioning Log

## Session 1

### Motion

Verified all axes move correctly.

Final direction configuration:

- X: unchanged
- Y: dir_pin: PB2
- Z: dir_pin: !PC5

Motion limits currently:

- Max velocity: 300 mm/s
- Max acceleration: 3000 mm/s²
- Max Z velocity: 15 mm/s
- Max Z acceleration: 100 mm/s²

---

### CR Touch

Measured probe offsets.

Final values:

x_offset: -44
y_offset: -9

Probe repeatability settings:

- samples = 3
- samples_result = median
- samples_tolerance = 0.02

---

### Safe Z Home

Observed behaviour:

Klipper development build:

v0.13.0-707-gf604aeee

did not automatically compensate BLTouch offsets when using safe_z_home.

Required configuration:

home_xy_position: 66,101

This positions the probe at the physical bed centre.

This behaviour should be revalidated after future Klipper upgrades.

---

### Git

Repository now used as source of truth.

Pi authenticates to GitHub using SSH keys.

Workflow:

git pull
edit
git commit
git push

## Motion Commissioning

Verified

- X movement
- Y movement
- Z movement

Final motor directions

Y

dir_pin: PB2

Z

dir_pin: !PC5

---

## Probe Commissioning

Measured offsets

X = -44

Y = -9

Probe repeatability

samples = 3

median

tolerance = 0.02

---

## Homing

G28

PASS

Notes

safe_z_home required nozzle coordinates:

66,101

to place the probe over bed centre.