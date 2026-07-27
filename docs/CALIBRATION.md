# Calibration

Order

1. PROBE_CALIBRATE
2. SAVE_CONFIG
3. PID Hotend
4. PID Bed
5. Bed Mesh
6. Extruder Rotation Distance
7. Flow
8. Retraction
9. Pressure Advance
10. Input Shaper

Current Status

1. PROBE_ACCURACY 2026/07/27 2:29pm

RUN1 (PROBE_ACCURACY) =
probe accuracy results: maximum 0.015000, minimum 0.007500, range 0.007500, average 0.011500, median 0.012500, standard deviation 0.002550

RUN2 = 
probe accuracy results: maximum -0.005000, minimum -0.017500, range 0.012500, average -0.012500, median -0.015000, standard deviation 0.004743

3. PID Hotend

RUN1 (PID_CALIBRATE HEATER=extruder TARGET=220) =
PID parameters: pid_Kp=26.134 pid_Ki=1.351 pid_Kd=126.423

RUN2 = 
PID parameters: pid_Kp=25.744 pid_Ki=1.244 pid_Kd=133.227

4. PID Bed

RUN1 (PID_CALIBRATE HEATER=heater_bed TARGET=60) =
PID parameters: pid_Kp=70.251 pid_Ki=1.082 pid_Kd=1140.694
