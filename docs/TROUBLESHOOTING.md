## Symptom

No filament extrudes after multiple calibration cycles.

### Possible Cause

Hotend heatsink fan not operating.

### Typical Symptoms

- Extruder clicking.
- No extrusion.
- Filament cannot be manually pushed through.
- Filament cannot be withdrawn.
- Printer appears to scrape the bed despite correct Z calibration.

### Cause

Heat creep causes filament to soften inside the heatbreak or Capricorn tube.

### Resolution

1. Verify heatsink fan operation.
2. Heat nozzle to 240°C.
3. Remove blockage.
4. Reassemble hotend.
5. Verify manual extrusion.
6. Repeat first layer calibration.

## Symptom

First layer inconsistent despite apparently good bed mesh.

### Possible Causes

- Heat creep caused by non-operational hotend cooling fan.
- Mechanical bed not sufficiently trammed.
- Probe calibration not saved correctly.
- Bed mesh generated before final probe calibration.
- Bed mesh not loaded before print.

### Resolution

1. Verify heatsink fan operation.
2. Perform PROBE_CALIBRATE.
3. SAVE_CONFIG.
4. Restart Klipper.
5. Perform SCREWS_TILT_CALCULATE.
6. Mechanically tram the bed.
7. Run BED_MESH_CALIBRATE.
8. SAVE_CONFIG.
9. Verify mesh loads before every print.