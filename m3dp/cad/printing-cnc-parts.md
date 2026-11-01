# Printing the CNC-designed parts

Build-specific 6.11 adaptations are now in [printed-6.11](printed-6.11/README.md): two-station dock modules for a 2020 rail, integral spacer pillars, matching reinforced covers, and two front P5 insert seats. Use the part selection in that guide. The table below describes the original CNC source files, not the adapted print set. The active guide now includes TAP, gantry-rail, dock-fan and detector fit prototypes. Physical fit, airflow, warm-chamber loading and the remaining thin regions still require validation.

Decision (2026-10-01): print instead of CNC. The CNC quote was over $300.
Measurements are from the files in this folder (m3dp_cnc_6_p1–p8), read 2026-10-01.

| File | Part | Size (mm) | Print notes |
|---|---|---|---|
| p1 | Top magnet plate | 3.5 × 28.3 × 34.8 | Thin. 5 × Ø6 magnet pockets, 1.5 mm pin holes. Print flat, 100% infill or 6+ walls. |
| p2 | Spring support plate | 6.1 × 8.5 × 16 | **Omit with P8.** CNC-arm alternative; it overlaps the selected printed arm. |
| p3 | Cover, left | 6.5 × 18 × 23.2 | Use the matching reinforced cover; validate clamp loading. |
| p4 | Cover, right | 3.0 × 18 × 23.2 | Use the matching reinforced cover; validate clamp loading. |
| p5 | Back plate (Trident) | 7.5 × 49.9 × 63 | Carries the whole head on the MGN12H. ASA is selected for the adapted build; use the revised geometry and validate fit, clamping and warm-chamber behavior. PC-CF/PA-CF is not an automatic upgrade. |
| p6 + p7 | Swing lever outer/inner (CNC) | 5.0 / 3.8 × 13.5 × ~41 | **Don't print these.** Too thin for plastic at a bearing pivot. |
| p8 | Swing arm, one-piece printed version | 12.9 × 19.5 × 41.9 | **Use this instead of p6 + p7.** Upstream designed it for printing. |
| dock 6.11 | Four-station hotend rack (CNC) | 21.2 × 76.3 × 130 | Four stations at 30 mm pitch; **do not print six racks**. The original 30 mm pitch has loaded-neighbor interference in this build. Use three raised 34/38 mm two-station modules and their matching gantry brackets in `printed-6.11`. Docked hotends stay hot, so ASA/ABS only, and keep the dock fans. |

## Changes needed for plastic

1. **Tapped M3 holes (Ø2.5 in the CNC files):** choose fastening treatment per hole.
   Enlarging diameter alone does not make the ordered inserts fit: p1 has only 3.0 mm
   of local support at its relieved hole, and p5's two top holes have 2.8 mm.
   Neither supports a fully contained 4 or 5 mm-long insert. Verify the purchased
   insert dimensions and surrounding clearance; use a suitably short insert, a
   clearance-checked boss/protrusion, or validate the self-threading option with a
   test piece. The adapted P5 front pair now has 5 mm-deep support for the confirmed Ø5 × 4 mm inserts and the selected Ø4.6 mm bore; see the [recorded coupon result](printed-6.11/insert-coupon-guidance.md). The other two joints use integral printed pillars and through-bolts with metal nuts. Printed strength and warm-chamber behavior still require testing.
2. **Bearing seats and Ø1.5 / Ø3 pin holes:** do a test print of one hole first and tune hole compensation;
   pins should press in, bearings should press in without cracking the part.
3. **Material:** ASA is selected for the adapted set. Use the same ASA and settings for coupons and final parts; verify dimensional fit and behavior under the actual loads and warm-chamber conditions. Follow the `printed-6.11` guide for the current build.
4. **Settings to start from:** 4–6 walls, 40%+ infill, 0.2 mm layers; orient so screw and pin loads are not across layer lines.
