# Raised front rail supports — fit prototype

The support pair carries a **400 mm length of 2020 extrusion** on the moving gantry of a standard Voron 2.4r2 350. It retains the stock front idlers and upper Z-belt clamps. Two forked brackets pass around the vertical Z belts, then support the new rail from its top face. Two ribs on each bracket brace the top clamp and tall column.

The original Cx latch and nozzle-pad geometry faces forward. Tool pickup withdraws toward the rear of the printer. The rail is raised and moved inward so that the original nozzle pads remain outside the physical bed while the stock front doors can close. This location requires the **11 mm TAP adapter stand-off and original source head height** used by the integrated head design.

## Parts and hardware

| Item | Quantity | Specification |
|---|---:|---|
| Left support |1|`front-rail-support-left.stl`|
| Right support |1|`front-rail-support-right.stl`|
| Gantry fit coupon |1 first|`front-gantry-fit-coupon.stl`; checks the right-side bolt stack and belt fork before printing/installing the supports|
| New crossrail |1|2020 extrusion cut to 400 mm; ends square and deburred|
| Replacement gantry screws |4|M5×40 button-head screws replacing the four reference M5×16 screws; the bracket adds exactly 24 mm under the heads|
| Rail clamp screws |4|M5 button heads; length must match the actual T-nut recess and engagement through the 6 mm clamp plus washer|
| Rail T-nuts |4|M5 nuts compatible with the purchased 2020 profile|
| Rail washers |4|M5, up to 1 mm thick and 10 mm outside diameter in the checked envelope|

Do not add a washer to the existing-clamp M5×40 stack unless screw engagement is recalculated. The modeled top-rail screw heads are 9.5 mm diameter and 2.75 mm high. The exact top-rail screw length is deliberately not frozen without the actual T-nut/profile pair. No internal slot-width key is used.

The STL orientation keeps the vertical gantry screw bores upright. Slicer supports are needed below the raised arms. Inspect the coupon's mating face, bolt fit and unobstructed belt path before loading the full support pair.

## Reference fit and motion

Coordinates below use the center of the original rear gantry crossbrace: X across the printer, +Y rearward, +Z upward. They are **physical CAD datums, not Klipper coordinates**.

- Rail center: `(0, −482.530002, 48.913430)` mm; length 400 mm.
- In original dock coordinates, the rail occupies `Y 65..85`, `Z−11.5..+8.5`; its axis follows dock X.
- Parked nozzle Y: −466.375002 mm. The lowest pad material is 7.3 mm below the nozzle, so the entire pad must remain outside the physical bed even if a slicer exclusion area is set.
- With the modeled 350 mm plate, the rear edge of that low pad clears the physical front bed edge by 3.870 mm.
- The bare rail clears the closed front-door inner face by 3.476 mm. Hanger/fan hardware must not project farther forward than the rail's front face.
- Top clamp, 1 mm washer and M5 button head clear the front upper frame bar by 4.240 mm at the existing configured Z 310 limit.
- The arm-to-vertical-belt gap is approximately 2.06 mm in the reference geometry. The modeled front XY-joint stop has a 4 mm pre-contact margin.

With the 11 mm adapter and the same 2 mm rear mechanical margin, the modeled rear nozzle limit is approximately Y −112.355 mm, while the physical 350 mm bed reaches Y −106.006 mm. That leaves approximately 6.35 mm of the rear bed outside the modeled nozzle reach. This is the rear limit only, not the total Y-area loss. A conservative separation of the complete moving-head and parked-dock envelopes puts the front print boundary at Y −437.345 mm for 3 mm clearance. That excludes approximately 18.66 mm at the front and leaves approximately 324.99 mm of Y depth between the modeled front/rear bounds. Using the existing 30 mm withdrawal plane, Y −436.375 mm, increases that separation to 3.97 mm and leaves approximately 324.02 mm of Y depth. This envelope check ignores X/Z separation, so it is sufficient rather than the tightest possible front limit; it includes the source tools, raised modules, fans, retainers, coupling pins and modeled fasteners. Cables, connectors, PTFE loops, flexible-pad deflection and the actual purchased nozzle geometry remain physical checks. Treat these as commissioning estimates, not ready-to-use slicer or Klipper limits.

The gantry interfaces, bolt heads, washers, rail and support ribs were checked against the official idlers, XY-joint motion, Z-belt runs, frame, doors and top panel. The enclosure sweep covers configured Z −5..310. These checks do not qualify the user's physical machine or prove the complete 350 mm print area. Measure the actual bed edge, panel position, T-nut engagement and all cable loops; establish the final nozzle travel limits after installing the complete TAP/head/duct assembly. The stock Klipper endstop value 350 is not a measured coordinate for the new nozzle.

## Reproduction

Run `BuildFrontRailSupports.FCMacro` in FreeCAD with `front_bracket_geometry.py` beside it. It creates separate FCStd, STEP and STL files for the pair and coupon. The native projects use boxes, cylinders, sketches, extrusions and Boolean operations; no custom proxy is required. The native operation tree remains editable.

Run `VerifyFrontRailSupports.FCMacro` separately. It opens unique copies of the saved files, edits/restores a bore and checks that the originals remain unchanged. `preflight_front_brackets.py`, `check_enclosure_and_bed.py` and `validate_front_support_exports.py` provide independent OCC, export and mesh checks using PythonOCC and the local `cad_checks.py` helper. Preflight reference BREP files are extracted from the official assembly.

Source: [official Voron 2.4 CAD](https://github.com/VoronDesign/Voron-2/tree/Voron2.4/CAD) and [official configurator](https://vorondesign.com/voron2.4). The downloaded STEP archive has Git blob SHA `142a355c22f6e488deb0aac4104cc2073bc31321`. Its assembly is the 250 reference; the 350 geometry uses the configurator's 100 mm length/placement increments without scaling hardware. The standard 350 frame is 530 mm tall. The new rail cross-section is copied from the original HFSB5-2020 profile; its exterior envelope is also checked as a conservative solid 20×20 mm box.
