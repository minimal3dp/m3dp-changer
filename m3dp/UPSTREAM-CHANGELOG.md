# Upstream changelog (cx330-TXY/CxChanger)

Newest first. One entry per sync.

## 2026-09-30 — synced to upstream `f5e88ce` (2026-09-29)

**Design is now v6.11. The BOM file is still v5.5 (last changed 2026-05-25 upstream).**

- Added `CAD/打印头6.11修正.zip` (printhead 6.11, corrected; one ~32 MB STEP inside).
- Added `CAD/热端停靠坞6.11改.STEP` (hotend dock 6.11, revised).
- Deleted all older STEP files: printhead 4.24/4.25 (printed + CNC), 5.1, 5.5 (duct fix), 6.11 (original), dock set 5.5.
- 6.11 adds tool-change-failure + filament-runout detection → `[filament_switch_sensor tool_sensor]` (pin PC14) in `klipper/toolchange.cfg` (Aug 2026). Needs one extra switch on the head. Added to BOM.
- `klipper/printer.cfg` has `[heater_fan dock_fan]`. README: enclosed printers use one axial fan per dock. Added 6 dock fans to BOM (size TBD from dock STEP).
- Upstream config ships T0–T3 only. T4/T5 macros + `extruder4/5` sections are mine to write.
- Thermistor in config: `ATC Semitec 104GT-2`. Bambu clone heaters are NTC 3950. Match `sensor_type` to what you buy.

BOM impact: see `bom/CxChanger_BOM_6tool.xlsx`.
