# Hardware Configuration

## Printer

Creality Ender 5 Pro

## Mainboard

BTT SKR Mini E3 V3

MCU:

STM32G0B1

## Probe

CR Touch

Measured offsets:

X = -44 mm

Y = -9 mm

## Extruder

Stock Creality metal extruder

Direct drive conversion

## Hotend

Stock Creality hotend

Current maximum temperature:

250°C

Future upgrade:

Phaetus Dragonfly

## Bed

Creality glass bed

Future:

Flexible PEI spring steel

## Controller

BigTreeTech SKR Mini E3 V3

MCU

STM32G0B1

---

## Probe

Creality CR Touch

Measured offsets

X = -44

Y = -9

## Fan Assignments

| Function | Header | MCU Pin | Configuration |
|----------|--------|---------|---------------|
| Part Cooling Fan | FAN2 | PB15 | `[fan]` |
| Hotend Heatsink Fan | FAN1 | PC7 | `[heater_fan heatbreak_cooling_fan]` |
| Spare | FAN0 | PC6 | Unused |

### Heater Fan Configuration

```ini
[heater_fan heatbreak_cooling_fan]
pin: PC7
heater: extruder
heater_temp: 50.0
fan_speed: 1.0
```

### Part Cooling Fan

```ini
[fan]
pin: PB15
```