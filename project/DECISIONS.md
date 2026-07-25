## Repository

Decision

GitHub is the source of truth.

Reason

Eliminates Windows copy becoming stale.

---

## Configuration

Decision

Split printer configuration into logical modules.

Reason

Simplifies maintenance and future upgrades.

---

## Motion

Decision

Invert Y direction.

Reason

Motor moved opposite to commanded direction.

---

Decision

Invert Z direction.

Reason

Motor moved opposite to commanded direction.

---

## Probe

Decision

Measure physical probe offsets.

Result

X = -44

Y = -9

---

Decision

safe_z_home configured to:

66,101

Reason

Current Klipper build homes the nozzle to home_xy_position rather than compensating for probe offsets.