# Assembly-guide source and validation notes

This guide covers the selected corrected-6.11 head with the one-piece printed P8 arm and the adapted integral-pillar P1/P3/P4/P5 set. The user reported the B1 prints complete; that report does not establish assembled bearing, shaft, fastener, detector or loaded-head performance. The order shown is a bench assembly aid derived from the saved geometry and project notes, not a verified upstream workshop procedure.

## Geometry sources

- Full assembly: `m3dp/cad/printhead-6.11-corrected-EN.STEP`, SHA-256 `d3ff5474d634279f90d272693b034265914b97b85cbf893dd8ee97b5c1a4284c`.
- Adapted plates: `../p1-magnet-plate-integral-pillars.step`, `../p3-cover-left-clamp-web.step`, `../p4-cover-right-clamp-web.step`, and `../p5-backplate-two-inserts-through-bolt.step`. These retain the source assembly datum. Their `-print-flat.stl` counterparts do not.
- Exact P8 and holder definitions: `../unchanged-printables/source/p8-printed-bearing-arm.step` and `../unchanged-printables/source/hotend-holder.step`. These are local part definitions and need their assembly occurrence transforms.
- Detector: `../voron-integration/detector/tool-detector-mount.step`. This export retains the earlier 6.11 detector's installed datum and motor-ear seating face. The corrected full assembly omits this detector.

The adapted plate geometry and fastening data come from `../BuildIntegralPillars.FCMacro`, `../integral-pillars-design-report.md` and `../printing-and-assembly-notes.md`. Detector data come from its `README.md`, `BuildToolDetectorMount.FCMacro` and `source-provenance.json`. Local-definition provenance is recorded in `../unchanged-printables/source-selection.json`.

## Full-assembly child selection

Indices below are **zero-based direct children of this exact imported full STEP**, not permanent part numbers. Confirm labels when changing importer or source revision. The STEP occurrence number is index + 1 for these direct children.

| Children | Identity and treatment |
|---|---|
| 18, 31, 32, 39 | Original P1, P3, P4 and P5; replace with the four adapted STEP solids. |
| 49 | Selected one-piece printed P8 arm. |
| 0 | Retained HGX 17/44T compound gear. |
| 1, 53 | Selected fixed and P8-arm 36T gears respectively; two installed gears total. |
| 4 | Fixed-gear Ø3×16 pin. |
| 26 | P8 pivot Ø3×24 pin. |
| 5, 10, 25 | Retained MR63ZZ bearings; all three belong to the selected head. |
| 50, 51, 52, 54 | P8 M3×8 screw, 683ZZ bearing, 3.2×6×0.5 washer and M3 nut. |
| 3, 6, 7, 8, 27, 28 | Six Ø1.5×5 cylindrical coupling pins. |
| 9, 11, 21 | Three head-side 6×4 magnets. |
| 12, 15, 16, 17 | Motor, hollow bolt, compression spring and M4 lock nut. |
| 22, 38 | Retained M3×15 motor-side screw and existing M3 nut below P5. |
| 58 | Original M3×16 button-head anchor; replace with M3×22 for the detector stack. |
| 14 | Hotend-module subassembly; its child 0 is the holder. Preserve the parent transform when extracting individual module components. |
| 19, 20, 41–48 | Omitted CNC-arm alternative: P2, its 36T gear, CNC arms and associated bearing/fastener/spacer set. |
| 29, 30, 33, 35 | Old installed spacers and lower cover screws; superseded by integral pillars and the long through-bolts. |
| 2 | Second Ø3×16 pin, saved at the CNC alternative's gear location; see the source omission below. |

Original fans, rear duct, probe, carriage and their mounting hardware are outside this B1 mechanism illustration. Their omission from a figure is not a complete final-build hardware exclusion list; the selected TAP/top-blower and dock layouts are documented separately.

## Placement and orientation

Do not place local part definitions beside installed solids without their occurrence transforms. In particular, extracting a child of the hotend module requires applying **`module_parent.location` to the child**; do not assume the extracted child already has global coordinates. Equally, do not apply the parent transform twice to an already flattened global shape.

Reference transforms from the STEP relationships:

- P8 local definition 210387: translation `(34.28, -36.45, -19)`; local X maps to `(0.999751526, -0.022290943, 0)`, local Y to `(-0.022290943, -0.999751526, 0)`, and local Z to `(0, 0, -1)`.
- Holder local definition 283614: composed global translation `(19.95, 7.3, -11.8260859311)` with rotation −90° about X. This includes both holder-to-module and module-to-head transforms.
- Detector STEP: already in the installed head datum. Its original Z=2 seating face contacts the motor ear; no spacer belongs below that face.

Use functional orientation labels in the guide: **carriage side**, **coupling/module side**, and **nozzle direction**. Source Z is not printer-up. The final11 source-to-printer reference is `(X−19.95, Z−24.52053, −Y−13.5)`. P5's broad source Z=0 face is on the carriage side; it contains the insert entrances and rear countersunk head. P1's coupling face meets the removable holder. P3/P4 outer washer faces are source Z=−22.5/−25.5.

## Checked hardware relationships

- P5: two M3 inserts, nominal 5 mm OD ×4 mm long, in the selected 4.6 mm bores. Insert from source Z=0 inward. P1 pillars and the P5 rear joint use clearance bores, not inserts.
- Left clamp: M3×20 countersunk screw → P1 integral 10 mm pillar → P3 → washer → M3 nut.
- Rear clamp: M3×30 countersunk screw → P5/P1 integral 14 mm pillar → P4 → washer → M3 nut.
- Both clamp screws require a 90° head with actual OD ≤5.6 mm. Each cover washer is 3.2 mm ID, OD ≤7 mm and 0.5 mm thick; each ordinary nut is 5.5 mm across flats and 2.4 mm thick. Fit the countersunk screws before nearby motor/gears obstruct access. These dimensions do not establish a tightening torque.
- P8 roller: M3×8 screw head → 683ZZ bearing → 3.2×6×0.5 washer → printed arm → M3 nut. Keep this set distinct from the omitted CNC-arm duplicate.
- Detector: M3×22 anchor replaces the shorter source screw. Retain the existing nut below P5 and add the specified nut above the detector. The switch uses two M2×18 screws, two M2 nuts and four M2 washers, one washer on each side of each joint. The checked stack has no added M3 washer or seating spacer.
- Each module: M3×22 transverse screws clamp the hotend; the separate M3×10 cap-head pair are docking hooks. Three round-head pins contact the head's three cylindrical-pin grooves. Opposing magnets retain a gap rather than becoming locating stops.

### Final guide connection audit

- The P5 insert-pair axes `(2.45, 3)` and `(37.45, 3)` match original blower screws (source children 55 and 36). The current top-blower layout relocates all three original blower M3×22 button-head screws. No active B1 attachment to the P5 insert pair is documented; the guide therefore leaves these seats unused during the dry-fit. Existing installed inserts may remain. The later TAP attachment uses different P5 axes and two M3×10 plus one M3×8 socket-head screws into three inserts in the adapter, not these P5 seats.
- Retain the left motor M3×15 socket-head screw (child 22), with its head seated against P1 and its shaft pointing toward P5/motor. The source has no additional left motor nut. Motor-ear Ø2.5 geometry does not establish actual thread engagement or tightening torque. The right joint is the longer detector anchor already documented above.
- MR63ZZ children 5 and 10 share the compound-gear axis `(9.47823, -36.9009)` at source Z centers `-1.15` and `-17.25`, seating in P5 and P3. Child 25 seats in P4 at the P8 pivot axis `(34.28, -36.45)`, Z center `-23.75`. P3's other bore receives the fixed-gear pin. The guide explicitly distinguishes these seats from screw joints.

The resulting PDF has ten pages. Its first page is also saved as `images/guide-preview.png`. `build_guide.py` composes the PDF using ReportLab; it does not generate or modify geometry. The PNGs are build123d MCP renders of the source selections described above, with labels and leader arrows added during PDF composition.

## Known source omission and physical checks

The saved full assembly places the second Ø3×16 pin (child 2) at approximately `(60.8883, −16.9527)` beside the CNC alternative. The selected P8 gear (child 53) instead has its axis at approximately `(29.1756, −23.1329)`. No separate installed shaft is saved at that P8-gear axis. The P8 definition has a Ø3.2 bore there, and the gear has a Ø3.1 bore. Any illustration showing the second pin relocated to P8 must identify that relocation as an assembly interpretation requiring a bench fit check, not an unchanged source occurrence or a validated retention result.

Rendered geometry establishes part identity and saved orientation. It does not establish insertion access, pin retention, bearing fit, gear freedom under clamp load, magnetic seating, spring adjustment or detector actuation. Those checks remain physical work. The detector must repeatably report detected only for a mounted tool with filament; empty and mounted-without-filament both need to report not detected. Printing completion alone does not close those tests.
