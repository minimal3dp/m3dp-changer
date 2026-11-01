# M3DP Changer wiring plan — six-tool Voron 2.4 350

Prepared 2026-10-25 from the live BOM, supplied Voron configuration, user corrections and manufacturer schematics. The target is the **existing M8P V1.1**, confirmed by the user, with its existing `EBBCan` toolboard and TAP retained for the first integration. The V2 belongs to another printer. The new LRS-350-24 is intended to power the toolchanger. The user selected four external DC heater switches so the new supply powers the toolchanger while existing board/motion feeds remain. The document is an installation plan, not a record of installed wiring.

## Verified hardware and limits

| Item | Established choice | Still to verify physically |
|---|---|---|
| Controller | Existing M8P V1.1, confirmed; supplied pins agree | Inspect actual terminal labels and existing feeds before wiring |
| Existing toolboard | Retain `EBBCan`, UUID `f2c8dad996fc`, for shared motor, head fans, X endstop, TAP and ADXL | Label, new motor coil pairs/current and gearing |
| Added controllers | Two EBB36 CAN V1.2 without MAX31865, T4/T5 | Labels, new unique UUIDs and locations |
| Hotends | Six Sirol TZ2 X1-style kits plus one spare | Delivered heater/sensor specifications |
| Heater basis | 24 V, 48 W each; NTC 100K 3950 | BOM specification, not a measurement |
| Fans | 24 V 4020 head blower and seven 24 V 2510 fans including six dock fans | Voltage, running/startup current and connector ratings |
| Added PSU | LRS-350-24, 24 V / 14.6 A / 350.4 W | Label, temperature derating and full load budget |
| Hotend cable | 4-core 22 AWG, nominally 1.5 m per tool | Cable/flex specification and ratings |
| CAN cable | Mellow 3 m combined power/data | Conductor sizes and end-to-end continuity |

Source: [live BOM rows 10–13 and 35–50](https://docs.google.com/spreadsheets/d/1XKfhXYksS0HXqKZEymX-_Pp8U7Hs6pY4Yzv2Vwxhv8M/edit#gid=1794676540&range=C10:M50). The repository XLSX predates the live choices.

## Selected architecture: four external DC heater stages

The M8P has **no separate hotend-only power input**. HE0–HE3 share its main POWER/VBB rail with regulators, host/core-board supply and fan voltage selectors. To retain all existing board/motion power while using the new PSU for all six hotend heaters, the selected design uses **four external DC heater-switch channels**, one driven by each M8P HE output. T4/T5 use the two new EBB heater outputs directly. This adds hardware. Four Sensata/Crydom D1D07 units are the documented example recommended below; no purchase has been made.

```text
Existing PSU --> existing M8P POWER / motion / BED-control arrangement
              --> retained EBBCan power branch

M8P HE0 pair --> external DC switch T0 CONTROL input
M8P HE1 pair --> external DC switch T1 CONTROL input (after bed SSR move)
M8P HE2 pair --> external DC switch T2 CONTROL input (after light removal)
M8P HE3 pair --> external DC switch T3 CONTROL input

New 24 V PSU --> protected distribution
                +-- protected load branch --> DC switch T0 --> T0 heater
                +-- protected load branch --> DC switch T1 --> T1 heater
                +-- protected load branch --> DC switch T2 --> T2 heater
                +-- protected load branch --> DC switch T3 --> T3 heater
                +-- protected branch -------> EBB T4 VIN --> T4 heater
                +-- protected branch -------> EBB T5 VIN --> T5 heater
                +-- rated dock-fan supply/control arrangement
```

Each external stage must accept the M8P's **switched 24 V heater-output pair** as its control input and switch a **24 V DC resistive load** of nominally 2 A continuously, with adequate thermal margin, connector ratings, PWM response and an off state when the control signal is absent. A bare logic-input MOSFET board cannot be connected to 24 V control without a compatible input circuit. An AC-output SSR is unsuitable for these DC heaters. Prefer documented isolation between control and load circuits; verify the chosen module's actual terminal topology and leakage/off behavior before wiring it. Its manufacturer's connection diagram must complete this block diagram.

Do not connect new-PSU positive to an M8P HE positive terminal: that terminal is already connected to the old POWER rail. The M8P HE pair goes to the external module's control terminals only. Thermistors remain on the M8P TH inputs. The new EBBs each receive their own protected power branch, not power through each other or through the M8P CAN connector. Never parallel the two PSU positive outputs. Define the common DC reference needed by the non-isolated CAN nodes; protective earth and DC return have separate functions.

Cable sizes, fuse values, connector part numbers and the final purchase choice remain open pending their actual ratings, loads and installation. Both supplies must be present for normal operation. With the old/controller supply off and the new supply on, the external stages must remain off; verify this explicitly with a safe test load before connecting heaters.

The verified V1.1 schematic shows HE0–3 on the shared VBB rail, the independent motor rail and the separate BED+ input. Retaining the existing supply feeds avoids changing those allocations. [V1.1 schematic, pages 6–8](https://github.com/bigtreetech/Manta-M8P/blob/master/V1.0_V1.1/Hardware/BIGTREETECH%20MANTA%20M8P%20V1.1-SCH.pdf).

### Documented external-switch example

Recommended example: **4 × Sensata/Crydom D1D07**, standard screw/clamp version. Its DC MOSFET output supports 24 V / 2 A; control accepts 3.5–32 VDC at up to 15 mA. Manufacturer isolation is 3750 Vrms input/output/base, switching time at most 100 microseconds, and PWM limit 5 kHz. Klipper's 0.100 s heater cycle (10 Hz) is within that specification. These are specifications, not a test of the installed circuit. [Manufacturer datasheet, pages 1–3](https://www.sensata.com/sites/default/files/a/sensata-1-dc-series-40-dc-output-panel-mount-ssr-datasheet.pdf).

Repeat this terminal wiring independently for T0–T3:

```text
M8P HEn positive/VBB ------------ D1D07 input 3 (+)
M8P HEn switched negative ------- D1D07 input 4 (−)

New PSU +24 V -- branch fuse -- heater -- D1D07 output 2 (+)
New PSU 0 V ---------------------------- D1D07 output 1 (−)
```

Follow the actual relay labels and datasheet diagram. Its control input does not share a terminal with its load circuit. Keep 22 AWG hotend leads out of these output clamps: the datasheet specifies **20 AWG minimum output wire**. Use a rated transition to appropriately sized terminal leads. Check mounting, enclosure temperature and the derating curve; the no-heatsink curve requires the metal base exposed to free ambient air. Prices and mounting hardware are not included in the present BOM totals. [Datasheet, pages 2 and 5](https://www.sensata.com/sites/default/files/a/sensata-1-dc-series-40-dc-output-panel-mount-ssr-datasheet.pdf).

## Reclaim the occupied HE1 and HE2 outputs

The supplied base uses HE1/PB5 for the bed SSR and HE2/PB6 for the caselight. Both connections must be physically removed before those outputs control T1/T2.

**Bed SSR:** move its low-voltage control pair from HE1 to the dedicated BED OUT pair and change the configured output to **PB7**. Preserve its bed sensor PA0, sensor type, temperature limits and PID. Confirm the installed SSR's DC input voltage/polarity/current specification and the actual BED output voltage first. Its control supply remains from the existing PSU. The V1.1 independent BED POWER input needs a compatible reviewed feed from that same existing PSU if it is currently unpowered. The actual bed heater's supply and SSR load-side wiring remain unchanged; this plan does not specify mains work.

**Caselight:** disconnect and insulate its leads from HE2, and disable its output section in the candidate until a suitable unused channel is verified. Removing the config alone is insufficient: a light left on HE2 would be driven by the T2 heater control. FAN3/PE5 is occupied by Nevermore and must not be reused. FAN4/PE4 is a possible two-wire output only after lamp current, voltage and startup demand are checked. No caselight channel is assigned here.

## Thermal pin map

These HE/TH and BED/TB GPIO assignments are common to the official V1.0 and V1.1 samples. They stay on the existing primary `[mcu]`, UUID `20a6cbafd015`; no extra M8P is introduced.

| Tool / heater | Physical control and sensor | Heater/control pin | Sensor pin |
|---|---|---|---|
| T0 / extruder | HE0 to DC stage T0; TH0 | PE3 | PA1 |
| T1 / extruder1 | HE1 to DC stage T1; TH1 | PB5 | PA2 |
| T2 / extruder2 | HE2 to DC stage T2; TH2 | PB6 | PA3 |
| T3 / extruder3 | HE3 to DC stage T3; TH3 | PE1 | PA4 |
| T4 / extruder4 | EBB T4 HE0 / TH0 | ebb_t4:PB13 | ebb_t4:PA3 |
| T5 / extruder5 | EBB T5 HE0 / TH0 | ebb_t5:PB13 | ebb_t5:PA3 |
| Bed, after physical move | BED OUT / TB | PB7 | PA0 |

References: [V1.0 sample](https://raw.githubusercontent.com/bigtreetech/Manta-M8P/master/V1.0_V1.1/Firmware/Klipper/generic-bigtreetech-manta-m8p-V1_0.cfg), [V1.1 sample](https://raw.githubusercontent.com/bigtreetech/Manta-M8P/master/V1.0_V1.1/Firmware/Klipper/generic-bigtreetech-manta-m8p-V1_1.cfg), [EBB V1.2 sample](https://github.com/bigtreetech/EBB/blob/master/EBB%20CAN%20V1.1%20and%20V1.2%20%28STM32G0B1%29/sample-bigtreetech-ebb-canbus-v1.2.cfg). Do not substitute EBB V1.1's PA2 heater pin for the ordered V1.2 PB13.

Move the old hotend thermal assignment off EBBCan:gpio7/gpio27 when adopting T0. Preserve that board's shared motor, driver and other retained functions. Label each heater/control/sensor T0–T5 at both ends. A crossed heater/sensor can appear plausible at room temperature while heating the wrong assembly.

Use Generic 3950 only after confirming the delivered 100K 3950 thermistor. Normal NTC configuration uses a 4.7-kohm pull-up without PT1000 selection. The new HGX-LITE motor/gearing needs verified current, coil pairs and extrusion calibration; do not copy the old 50:10 gear ratio, 22.979 rotation distance or 0.65 A driver current without checking. [M8P sensor settings](https://global.bttwiki.com/M8P.html#100k-ntc-or-pt1000-setting), [EBB sensor settings](https://neo.bttwiki.com/en/docs/board-docs/ebb-series/ebb-36/ebb-36-hardware#ntc-100k-or-pt1000).

## CAN data and power are separate

The V1.1 schematic shows **two parallel two-pin CAN connectors**, J16 and J18. Pin 1 is CANH/P; pin 2 is CANL/N. Neither supplies 24 V/GND. PD12/PD13 on the pinout identify MCU RX/TX signals, not extra connector positions. Verify connector orientation on the actual board. [V1.1 CAN schematic, page 3](https://github.com/bigtreetech/Manta-M8P/blob/master/V1.0_V1.1/Hardware/BIGTREETECH%20MANTA%20M8P%20V1.1-SCH.pdf).

Retain the working host interface and existing mcu/EBBCan nodes. Extend the physical CAN bus in a line for ebb_t4 and ebb_t5; do not create a star because two parallel headers are available. Match the existing bitrate and firmware mode. Exactly two 120-ohm terminations belong at the complete bus's physical ends; disable termination on intermediate nodes. With all supplies removed, H–L should measure approximately 60 ohms. [Klipper CAN](https://www.klipper3d.org/CANBUS.html), [wiring guidance](https://www.klipper3d.org/CANBUS_Troubleshooting.html).

Trace H, L, VIN+ and VIN− through the combined cable by continuity. Split data to CAN and power to each EBB's separately protected branch. Do not route both heater currents through one JST-XH power pair: the heaters alone total 4 A, while JST rates XH at 3 A with AWG22. [JST XH specification](https://www.jst-mfg.com/product/pdf/eng/eXH.pdf).

## Cooling and retained TAP

Keep head blower EBBCan:gpio13 and heatbreak fan EBBCan:gpio14 where the replacement head permits; associate heatbreak cooling with all six heaters. The existing M8P channels are FAN0/PE6 and FAN1/PE0 electronics cooling, FAN2/PC12 exhaust, and FAN3/PE5 Nevermore. Preserve those allocations. Expand electronics fan heater associations if a parked tool can heat while T0/bed/motors are idle.

FAN4/PE4 is the remaining M8P V1.1 two-wire output and is reserved as a possible caselight channel pending the load check. FAN5/PB8 and FAN6/PB9 are four-wire control interfaces; their PWM pins are not switched 24 V outputs for arbitrary two-wire loads. Do not connect the dock fan bank or caselight to those PWM pins as though they were heater/fan power terminals.

The proposed dock-fan assignment is three 24 V 2510 fans on EBB T4 FAN0/`ebb_t4:PA0` and the other three on EBB T5 FAN0/`ebb_t5:PA0`. These boards and fan banks use the new supply. Mounting the EBBs near the gantry-mounted docks would shorten these leads, but their physical positions are not yet confirmed.

Each three-fan bank must have a verified combined continuous current below the 1 A fan-output rating, with startup demand below the documented 1.5 A peak and adequate margin; its wiring and splitter must also be rated. Do not infer this from fan dimensions. If a bank does not fit, distribute it between FAN0/PA0 and FAN1/PA1 on that same EBB (for example two plus one), validating each channel and the 6 A total board-input limit including its 2 A heater and electronics. If the loads still fail those limits, use a suitably rated external fan controller. Do not install a splitter before these checks.

Configure every dock-fan bank, including any PA1 split bank, as a heater fan associated with **all six** hotends: `extruder, extruder1, extruder2, extruder3, extruder4, extruder5`. All six dock fans must run while any hotend is hot or commanded to heat, regardless of which heater happens to be attached to the EBB controlling that fan bank. The proposed two-channel allocation remains gated on the fan current and wiring checks. [EBB V1.2 PA0/PA1 sample](https://raw.githubusercontent.com/bigtreetech/EBB/master/EBB%20CAN%20V1.1%20and%20V1.2%20%28STM32G0B1%29/sample-bigtreetech-ebb-canbus-v1.2.cfg).

Published limits: M8P fan output 1 A, heater output 5.5 A, stated heater/driver/fan aggregate below 12 A; EBB36 board input 6 A, heater output 5 A and fan output 1 A. A cable, splitter or added stage may have a lower limit. [M8P specifications](https://global.bttwiki.com/M8P.html#specifications), [EBB specifications](https://github.com/bigtreetech/EBB#hardware).

TAP remains on !EBBCan:gpio22. Homing/probing requires a mounted, verified nozzle and temperature protection for the selected hotend. The old single-extruder activation macro must be adapted; retaining its wire does not make empty-carriage Z homing valid. Eddy remains an uninstalled future option.

The proposed Cx sensing contact uses the retained SB2209 RP2040 **Probe** connector's GPIO21 signal and adjacent GND. The connector is P9: pin 5 is PROBE/GPIO21, pin 4 GND, pin 3 GPIO22/TAP, pin 2 +5 V and pin 1 GND. GPIO21 is behind Schmitt buffer U13, with no connector-side pullup. Klipper `^` cannot pull up the contact through that buffer. For a passive contact to ground, provide an external pullup, for example 4.7 kohms from P9 pin 5 to pin 2 +5 V, with the contact between pins 5 and 4. Confirm the delivered sensor is a passive contact before using this arrangement; measure both states and set inversion accordingly. Preserve the TAP connections. [Official pinout](https://github.com/bigtreetech/EBB/blob/master/EBB%20SB2209%20CAN%20%28RP2040%29/Hardware/EBB%20SB2209%20CAN%20V1.0%EF%BC%88RP2040%EF%BC%89-Pin.pdf), [schematic, page 1](https://github.com/bigtreetech/EBB/blob/master/EBB%20SB2209%20CAN%20%28RP2040%29/Hardware/BIGTREETECH%20EBB%20SB2209%20CAN%28RP2040%29%20V1.0-SCH.pdf).

## New-supply load budget

| Load | Nominal power | Current at 24 V |
|---|---:|---:|
| T0–T3 heaters | 192 W | 8 A |
| T4 heater | 48 W | 2 A |
| T5 heater | 48 W | 2 A |
| Six heaters total | 288 W | 12 A |
| LRS-350-24 nameplate | 350.4 W | 14.6 A |
| Capacity remaining before overhead | 62.4 W | 2.6 A |

For the selected external-stage architecture, add both new EBBs, external-stage losses, dock fans and any other load assigned to the new supply. Existing motion, M8P/host, retained toolboard and bed load stay on their current feeds. The bed SSR control move does not move the bed heater load. Check ambient-temperature derating and all individual component limits before simultaneous heating. If the budget fails, revise distribution/capacity or heating concurrency. [Mean Well LRS-350 specification](https://www.meanwell.com/Upload/PDF/LRS-350/LRS-350-SPEC.PDF).

## Verification sequence

1. Inspect the confirmed V1.1 board and existing feeds. Confirm SSR input, external-switch model/diagram, fan/light ratings, load ownership, cable/connector ratings and branch protection.
2. With all power removed, inspect all existing positive feed jumpers. Verify positive rails remain separate, intended common DC returns, polarity, continuity, strain relief and CAN termination.
3. Move the SSR control to verified BED OUT, disconnect the caselight from HE2, label every tool/control/sensor, and keep heater loads disconnected.
4. Prove each added switch's control voltage, polarity and off behavior with the actual module and a safe test load, including old/control supply absent. Then bring up all MCUs and sensible room-temperature sensor readings; identify new EBBs individually.
5. Test the bed SSR response after its move. Test one matched hotend/sensor at a time under supervision, confirming only its sensor rises and cooling runs. A nominal 24 V/48 W heater is about 12 ohms; this does not identify the thermistor curve.
6. Calibrate six heater PIDs and validate the completed load budget before concurrent heating. Test dock/electronics cooling against every hotend individually, especially T1–T5.
7. Complete mounted-nozzle TAP, dock geometry and clearance commissioning before automatic tool changes. Electrical verification does not establish motion safety.

No live printer configuration, firmware or wiring has been changed by this plan.
