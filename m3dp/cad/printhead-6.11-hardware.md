# Printhead 6.11 — hardware pulled from the CAD (upstream f5e88ce, 2026-09-29)

This is the upstream occurrence inventory. For the printed adaptation, use the joint-specific hardware changes in [printed-6.11](printed-6.11/README.md); its integral pillars and matching covers replace two metal spacers and their paired short screws with through-bolts, nuts and washers. Do not order this table as an additional full kit.

Source: `CAD/打印头6.11修正.zip` (SolidWorks 2024 STEP), assembly tree parsed 2026-10-01; the original archive remains in Git history at `upstream-2026-09-29`.
Retained English assembly: [printhead-6.11-corrected-EN.STEP](printhead-6.11-corrected-EN.STEP), with translated names and unchanged geometry; see its [name map](printhead-6.11-name-map.csv). The redundant ZIP copy has been removed.
The model has **1 hotend module**; multiply those lines by the tool count.
The head inventory below counts CAD occurrences, including both alternative swing
arms. It is not an installed-quantity list until one arm is selected. In particular,
the selected arrangement uses two 36T drive gears; the third belongs to the other
arm. The paired 683ZZ bearings, M3×8 screws and small washers also include both
alternatives; count the chosen arm only, or label the extra items as spares.

The current final11 installation uses **32 ordinary M3 nuts**: 24 in the modules, two in the selected head, two at the integral-pillar through-bolts, one at the detector and three at the top blower. It also uses **14 heat-set inserts**: two P5, three TAP-adapter and nine fan-retainer inserts. These selected totals supersede the occurrence totals below for purchasing. Six M3 rail T-nuts, four M5 rail T-nuts and two M2 detector nuts are separate hardware categories.

## Printhead (×1)

| Qty | Part | Chinese name |
|---|---|---|
| 4 | Button head screw M3×22 (ISO 7380) | 半圆头螺栓_M3*22 |
| 1 | Button head screw M3×16 (ISO 7380) | 半圆头螺栓_M3*16 |
| 1 | Countersunk screw M3×16 (DIN 7991) | 沉头螺栓_M3*16 |
| 2 | Socket head cap screw M3×15 (DIN 912) | 圆柱头螺栓_M3*15 |
| 2 | Socket head cap screw M3×8 (DIN 912) | 圆柱头螺栓_M3*8 |
| 2 | Socket head cap screw M2.5×14 (DIN 912) | 圆柱头螺栓_M2.5*14 |
| 3 | M3 hex nut | M3螺母 |
| 2 | Washer 3.2×6×0.5 | 垫圈_3.2*6*0.5 |
| 1 | M4 lock nut (anti-loosening) | 百瑞特防滑螺母_M4 |
| 1 | M4 hollow through-hole bolt | M4带孔螺栓 |
| 2 | M4 hex standoff 10 mm | M4六角隔离柱10 |
| 1 | M4 hex standoff 14 mm | M4六角隔离柱14 |
| 2 | Dowel pin Ø3×16 | 直径3长16圆柱销 |
| 1 | Dowel pin Ø3×24 | 直径3长24圆柱销 |
| 6 | Dowel pin Ø1.5×5 (coupling V-grooves) | 圆柱销外径1.5长5 |
| 3 | Bearing 3×6×2.5 (MR63ZZ) | 轴承外径6内径3厚2.5 |
| 2 | Bearing 3×7×3 (683ZZ) — **new vs 5.5 BOM** | 轴承_3x7x3 |
| 3 in CAD; 2 installed | 36T extruder drive gear — third belongs to alternate arm | 36齿挤出齿轮 |
| 1 | HGX 17/44T compound gear | 17 44双联齿轮 |
| 3 | N52 magnet 6×4 | N52磁铁 6 4 |
| 1 | Compression spring | 压簧 |
| 1 | NEMA14 36 mm pancake stepper | 36圆饼步进电机 |
| 1 | 2510 fan | 2510风扇 |
| 1 | 4020 blower | 4020离心风扇 |
| 1 | Eddy-current leveling probe (BTT Eddy style) | 涡流调平 |

Printed/CNC parts in the model: top magnet plate, spring support plate, back plate CNC (Trident),
swing lever CNC (outer + inner) **and** a printed one-piece swing arm (alternatives — build one),
simplified covers L/R, part-cooling duct, hotend holder.

## Per hotend module (× tools)

| Qty | Part | Chinese name |
|---|---|---|
| 1 | Bambu P1P hotend assembly (heatsink, nozzle+heatbreak, ceramic heater, silicone sock) | 拓竹P1P热端组件 |
| 2 | Socket head cap screw M3×22 (DIN 912) — transverse hotend clamp screws | 圆柱头螺栓_M3*22 |
| 2 | Socket head cap screw M3×10 (DIN 912) — docking hooks; use magnetic heads as required by README | 圆柱头螺栓_M3*10 |
| 4 | M3 hex nut | M3螺母 |
| 3 | N52 magnet 6×4 | N52磁铁 6 4 |
| 3 | Round head pin Ø3×4 (coupling balls) | 圆头销外径3长4 |

## Dock (× tools) — not in the dock STEP; from README

1 × female-threaded round head pin M3 Ø5×20, 1 × N52 magnet 6×4, 1 × fan (enclosed printers).
Dock 6.11 holes: Ø3.05, Ø3.2 (M3 clearance), Ø5.2 (pin bore), Ø5.5.

## 6-tool CAD totals (head alternatives + 6 modules + 6 dock stations)

These totals retain both arm alternatives; reconcile the selected arm before ordering.
The dock STEP contains four stations in one rack, not one printable dock per tool.

M3×22 SHCS 12 · M3×10 SHCS 12 · M3×15 SHCS 2 · M3×8 SHCS 2 · M2.5×14 SHCS 2 ·
M3×22 button 4 · M3×16 button 1 · M3×16 countersunk 1 · M3 nut 27 · M3 washer 2 · M4 lock nut 1 ·
magnets 27 · round head pins 18 · threaded dock pins 6.
