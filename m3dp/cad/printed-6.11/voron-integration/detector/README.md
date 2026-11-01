# Upper tool/filament detector mount — fit prototype

This adapts the upper microswitch mount from the earlier CxChanger 6.11 assembly. The corrected assembly omitted it. It retains the existing printed arm as the candidate switch actuator; no separate actuator is invented or required by this CAD export. The lower source Z-endstop switch is omitted because this build uses TAP.

The mount retains its original seating face against the motor mounting ear, adds a 3.4 mm M3 anchor clearance, and adds 2.2 mm M2 pivot/arc-slot clearances. Do not add a spacer or boss under this face; the retained motor ear occupies that space. The switch-hole centers are 6.5 mm apart; the slot retains the source angular adjustment. Use one of the already purchased D2F-01F switches.

| Hardware | Quantity | Modeled stack |
|---|---:|---|
| M2×18 socket-head screw | 2 | 3.8 mm maximum head diameter, 2 mm head height |
| M2 nut | 2 | 1.6 mm thick; modeled circumscribed diameter 4.62 mm |
| M2 washer | 4 | 5 mm OD, 0.4 mm thick; one on each side of the joint |
| M3×22 button-head anchor screw | 1 | Replaces the corrected assembly's shorter M3×16 at this location |
| M3 nut | 1 | 5.5 mm across flats, 2.4 mm thick; no added washer in this checked stack |

Keep the existing M3 nut below P5 that retains the hollow-bolt mechanism. The second nut goes above the detector mount; the M3×22 screw has 0.6 mm nominal protrusion past its 2.4 mm nut. The two M2×18 screws have 0.75 mm nominal protrusion past the modeled washers and nuts, with the front washer seated against the switch’s outer 5.85 mm body envelope. The extra M3 nut raises the base head/module total from 28 to 29; the three top-blower nuts bring the complete final11 build to **32 ordinary M3 nuts**. The dock-fan retainers use inserts, not additional nuts. Reuse purchased stock where it matches these dimensions. Check thread protrusion and screw engagement physically; do not substitute thicker washers or locknuts without recalculating the stack.

The exported STL is oriented with its main flat face down. Inspect the small bore/slot and support interface in the slicer. The FCStd contains the embedded upstream mount and native editable features. The seating correction passed independent retained-part and fastener clearance checks. The corrected native build, distinct-copy reopen/edit, STEP readback and independent watertight-mesh checks passed on 2026-10-26. The obsolete seating boss is absent from the saved native model.

**Switch actuation is not qualified by those checks.** Adjust it by hand and test empty head, tool with filament, and tool without filament across the full arm stroke. This is one binary switch, not three independent electrical states: the current firmware requires detected only for a mounted tool with filament; empty and mounted-without-filament must both report not detected. The source model places the printed arm against the switch plunger, but it contains only one arm pose and does not prove that truth table or safe overtravel. Do not bottom the plunger or infer tool presence from an untested signal. Only enable automatic tool changing after those results repeat reliably. The [Omron D2F datasheet](https://components.omron.com/sites/default/files/datasheet_pdf/B036-E1.pdf) is the electrical/mechanical component reference; it does not verify this printed linkage.

Source attribution and assembly hash are recorded in `source-provenance.json`; the CxChanger GPL-3.0 license is retained in the parent printed-parts folder.
