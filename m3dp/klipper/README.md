# M3DP Changer configuration — six-tool Voron 2.4 350

This is the build-specific configuration for the confirmed **Manta M8P V1.1**,
existing RP2040 head-controller pin mapping (`EBBCan`, matching SB2209 CAN
RP2040), installed TAP, and two new
EBB36 CAN V1.2 boards. The new 350 W / 24 V supply powers the toolchanger through
four external DC heater switches and the two EBB36s. See [wiring-plan.md](wiring-plan.md).

The candidate preserves the supplied Voron motion setup and existing CAN identities.
It is **not ready to load unchanged**: new CAN IDs, the pickup switch polarity,
HGX motor calibration, delivered thermistor types, dock positions and thermal
calibration require physical verification. No printer commands have been sent.
The required peripheral includes are preserved in `../voron/`; see its
[snapshot notes](../voron/README.md). Personal printer backups and host settings
remain in the original checkout. Upstream examples are isolated in
[reference/cxchanger/klipper](../../reference/cxchanger/klipper/) for reference
and regression tests. The `cxchanger.cfg` filename and
`CX_*` commands are retained for compatibility.

## Prepare the candidate

The files are arranged as sibling `klipper/` and `voron/` folders. Keep that layout
when copying to the printer, or adjust the explicit `../voron/` include paths.

1. Copy `printer.cfg.example` to `printer.cfg` **in this folder** and use it as
   Klipper's main configuration. Do not include it from the old printer.cfg: it
   replaces that main file and carries its retained bed/probe `SAVE_CONFIG` data.
2. Copy `hardware.cfg.example` to `hardware.cfg` and `hotends.cfg.example` to
   `hotends.cfg`. Resolve every `REPLACE_*` value in all three files. Keep
   `cxchanger.cfg` after the existing UI/peripheral includes.
3. Follow the wiring plan before enabling outputs. The bed SSR control moves from
   HE1/PB5 to BED/PB7; the case light must be disconnected from HE2/PB6. HE0–HE3
   now drive the **control inputs** of four compatible external DC heater switches.
   Their heater load power comes from the new supply. Never join the two +24 V rails.
4. Keep the original `~/printer_data/config/variables.cfg` store and its measured
   offsets. Identify the two new EBB36 UUIDs individually. Verify the proposed
   pickup-switch input and its polarity with `QUERY_FILAMENT_SENSOR
   SENSOR=cx_tool_sensor`; detected must mean a seated tool with filament present.
5. Confirm the actual HGX gears, motor step angle/current and extrusion distance.
   The old Stealthburner ratio and rotation distance do not calibrate the new drive.
   Check motor direction with supervised, short moves after the mechanical setup.
6. Verify the delivered heater voltage/power, thermistor type and temperature
   rating. Check each sensor and heater channel separately before PID calibration.
   Replace temporary `control: watermark` with each hotend's measured PID gains.
   If using `SAVE_CONFIG`, remove conflicting control/PID entries from the include
   before saving; otherwise record the measured gains directly in `hotends.cfg`.

The candidate uses the supplied Mainsail, KNOMI, LED and backup definitions. Its
local `nevermore.cfg` corrects heater selection for T0–T5 while retaining bed-fan
behavior. M3DP Changer definitions replace the existing pause and probing wrappers.
The original printer's `macros.cfg` and `klipper-macros/` library are not part of
this deployment: their print macros are replaced, and the fixed-height
`PARK`/`G32` sequence is not used. Do not also include upstream CxChanger macros.
Recheck integration if those includes change.

The hotend templates use `min_temp: 0` and `min_extrude_temp: 180`. The 300 °C maximum
is an upper commissioning limit; lower it to the lowest applicable component rating.
No fabricated PID gains are supplied. The old hotend PID is removed from the
candidate; the existing bed PID is retained. Probe Z offset and input shaping must
be recalibrated for the assembled head.

## TAP and first homing

T0 is the reference nozzle for Z homing, QGL and bed mesh. The new mechanism must
retain TAP travel and trigger reliably with a securely seated nozzle. After
checking that physically, set `_CX_TAP_CONFIG.mount_verified: True` in `tap.cfg`.
This separate gate allows supervised homing before automatic docks are commissioned.

After a restart the tool state is unknown and the shared motor is detached.
Manually seat clean T0 with filament present, then run:

```gcode
CX_CONFIRM_TOOL TOOL=0
G28
```

The switch must agree with the observed tool. TAP operations reject an empty head,
T1–T5, unknown state, or a missing pickup signal. They explicitly cool T0 to the
installed TAP probing limits and check the sensor again after waiting. Existing
`safe_z_home` remains in use. `G9928` is an internal implementation alias; use
`G28` in normal macros and the UI so the TAP guard runs.

Re-run `PROBE_CALIBRATE` with T0; the inherited -0.896 mm value is old setup data,
not a calibration of M3DP Changer. Then verify repeatability, QGL and mesh. Eddy is
not configured in this build.

## Docks, offsets and recovery

The six docks must follow the moving Voron 2.4 gantry. The original dock STEP is a
**four-station rack**. The printed adaptation in `../cad/printed-6.11` uses three
two-station modules on a new 2020 rail: 34 mm spacing inside each pair and 38 mm
between butted modules. Do not derive all six positions from a single 34 mm pitch.
Complete the rail brackets and full clearance checks before measuring each dock
coordinate; CAD pad centers are not carriage pickup positions.

`_CX_CONFIG.commissioned` starts `False`; all six XY pairs start `None`. Measure
and enter each dock position, X latch shift, approach distances and required Z
clearance in `toolchange.cfg`. This movement pattern assumes **front docks, with
positive Y exiting the docks**. A different orientation requires a reviewed path.
Check the whole path throughout gantry Z travel, then set `commissioned: True` for
supervised trials. A tool change refuses to move if its full Z clearance cannot fit.
Reserve that clearance when setting the slicer's usable build height.

`T0`–`T5` change tools and return to the logical print position with the new nozzle
offsets. `UNTOOL` parks the nozzle and leaves the carriage at the dock exit with Z
raised. For supervised pickup/offset calibration before offsets exist:

```gcode
CX_CHANGE_TOOL TOOL=1 RETURN=0
```

`RETURN=0` stays at the dock exit in machine coordinates. Normal printing with
T1–T5 requires measured `tN_offset_x`, `tN_offset_y`, `tN_offset_z` values in the
saved-variable store. T0 is the reference. Never enter zero offsets just to bypass
this check. The macros preserve coordinate/extrusion modes, live babystepping and
pressure advance routing to the single physical motor.

A failed release or pickup turns off heaters, detaches the motor, and aborts the
enclosing operation. Cancel, inspect the mechanism, physically identify the tool,
then reconcile with `CX_CONFIRM_TOOL TOOL=-1` (empty) or `TOOL=0` through `TOOL=5`.
Restart the abandoned job rather than resuming a failed tool-change sequence.
Ordinary filament runout can resume after restoring filament and temperature.

## Slicer setup

Configure six tools with a one-to-one filament/tool mapping, T0–T5. Use this
OrcaSlicer start command (one line):

```gcode
PRINT_START BED=[bed_temperature_initial_layer_single] INITIAL_TOOL=[initial_tool] T0_TEMP={nozzle_temperature_initial_layer[0]} T0_USED={is_extruder_used[0]} T1_TEMP={nozzle_temperature_initial_layer[1]} T1_USED={is_extruder_used[1]} T2_TEMP={nozzle_temperature_initial_layer[2]} T2_USED={is_extruder_used[2]} T3_TEMP={nozzle_temperature_initial_layer[3]} T3_USED={is_extruder_used[3]} T4_TEMP={nozzle_temperature_initial_layer[4]} T4_USED={is_extruder_used[4]} T5_TEMP={nozzle_temperature_initial_layer[5]} T5_USED={is_extruder_used[5]}
```

Start requires confirmed, mounted T0 even when the print uses only another tool.
It heats the bed, homes, runs QGL, homes Z again and probes the mesh with T0. It then
parks T0, heats the used tools, primes them and leaves the initial tool active.
An unused T0 is turned off after probing. Measure the clear priming strip in
`_CX_PRINT_CONFIG` before printing. After `PRINT_END`, the carriage is empty;
with valid homing you can pick up T0 using `CX_CHANGE_TOOL TOOL=0 RETURN=0` before
the next start. After lost homing or restart, manually seat and confirm T0 instead.

Tool-change G-code:

```gcode
M104 S{nozzle_temperature[next_extruder]} T{next_extruder}
T{next_extruder}
```

End G-code is `PRINT_END`. The slicer owns retraction/compensation; these macros do
no hidden pickup extrusion or retraction. Remove any old extra 3 mm pickup
compensation. Other primed tools are turned off, so preheat the next tool before
selecting it. `SET_PRESSURE_ADVANCE` applies to the shared physical extruder motor.

Inspect exported G-code for all six tools before printing, including the first
move following startup/tool changes. These snippets have not been tested with a
live OrcaSlicer profile. Variable semantics follow the
[OrcaSlicer placeholder documentation](https://github.com/OrcaSlicer/OrcaSlicer/wiki/Built-in-placeholders-variables/6c8293fa7bbc061734288c258f75569f226fdab4).

## Optional nozzle-offset fixture

`calibration.cfg` stays excluded by default. It requires a separate XYZ contact
fixture and the [tools_calibrate extension](https://github.com/viesturz/klipper-toolchanger/blob/main/tools_calibrate.md).
TAP or an ordinary Eddy bed probe does not substitute for this fixture. Measure
its approach point and clearance before enabling `_CX_CALIB_CONFIG.enabled`.
Home with T0 first, then park it; calibration starts with an empty, homed carriage.
`CALIBRATE_ALL_TOOLS` establishes T0 then measures T1–T5. Re-establish T0 after moving
the fixture or restarting. Independently measured offsets can be used instead.

## Verification

[tests/README.md](tests/README.md) describes the reproducible offline regressions.
They use actual Klipper parsing, macro evaluation, coordinate handling and
extruder checks, with simulated hardware responses. They cannot prove electrical
ratings, TAP compatibility, retention, clearance, thermal performance or physical
calibration. Commission the assembled machine in the sequence in the wiring plan.
