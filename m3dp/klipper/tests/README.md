# Offline Klipper macro regression tests

These tests use actual Klipper Python implementations, not a reimplementation of
Jinja evaluation or coordinate transformations:

- `gcode.GCodeDispatch`: parsing, nested command dispatch, error propagation
- `extras.gcode_macro`: Jinja2 environment, whole-macro render timing and status snapshots
- `extras.gcode_move`: absolute/relative modes, extrusion origin, offsets, save/restore
- `extras.pause_resume`: pause and resume behavior
- `kinematics.extruder.PrinterExtruder`: temperature commands, active-extruder changes,
  and extrusion safety checks

The printer service, movement endpoint, temperature changes, filament switch,
shared-motor queue, and heater waits are simulated. No MCU or printer is connected.
These tests cannot validate wiring, physical switch polarity, thermal response,
steps/mm, actual dock coordinates, mechanical clearance or real-time MCU behavior.

## Run

Use Python with `jinja2` and `pytest` available and an existing Klipper checkout:

```sh
cd /path/to/m3dp-changer/m3dp/klipper
KLIPPER_SOURCE=/path/to/klipper CXCHANGER_SOURCE=/path/to/m3dp-changer python -m pytest -q tests
```

The test run during development used Klipper commit
`7f822f3a5c27743b3e49a8e0d7b9d81bc3176f17`, Python 3.12.12,
Jinja2 3.1.6, and pytest 9.0.3.

`test_original_regressions.py` asserts the intended safe behavior against the
untouched original examples. Its six strict expected failures document the
baseline defects. To see the actual failing assertions:

```sh
KLIPPER_SOURCE=/path/to/klipper CXCHANGER_SOURCE=/path/to/m3dp-changer python -m pytest --runxfail --tb=short tests/test_original_regressions.py
```

The original examples are read only. Temporary fixtures and saved-variable state
stay in memory or pytest's temporary directory.

`test_toolchange.py` and `test_print_lifecycle.py` run the staged or installed
macros one directory above `tests/`. The sensor fixture supplies physical pickup
and release outcomes immediately before verification, and asserts that actual
macro execution has first completed `M400` plus a settling `G4`.
`test_calibration.py` supplies synthetic contact-probe results; it verifies
sequencing, result validation, storage and failure propagation, not the external
probe plugin's hardware implementation.

`test_tap.py` verifies the installed TAP policy: confirmed T0 must remain present
for Z homing, gantry leveling and bed meshing. It executes the exact `[probe]`
`activate_gcode` from `tap.cfg` through Klipper's `TemplateWrapper`, including
explicit T0 temperature control and the second sensor check after cooling.
Homing/probing endpoints are still simulated; these tests do not establish TAP
mounting compatibility, trigger accuracy, nozzle seating strength or probe offset.

`test_merged_config.py` builds a temporary deployment mirror with sibling
`m3dp/klipper` and `m3dp/voron` directories. Klipper's `ConfigFileReader` resolves
the actual include order; its autosave parsing keeps main-file saved values with
Klipper's duplicate-field precedence. The fixture copies hardware/hotend examples
without replacing their deliberately invalid commissioning placeholders. A
`PrinterPins`-based ownership check resolves aliases and flags physical pin
collisions separately from the unresolved GPIO21 switch-polarity placeholder.
The macro run then verifies the final Nevermore, KNOMI, Mainsail, TAP and CxChanger
bodies together, including named-heater routing, fans, layer pauses and cancellation.

A successful structural audit is not a complete connected Klipper startup test:
MCU identities, heater sensor types, motor parameters, switch polarity and other
commissioning values still require the delivered hardware. No MCU dictionary,
serial connection, real probe, heater or motor is used by this suite.
