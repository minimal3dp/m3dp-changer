# Reference geometry and license

This prototype was developed for the CxChanger build on 2026-10-25. The forked support pair, gussets, rail clamps and fit coupon are new additions; they are not official Voron parts and have not been physically qualified.

The retained printer geometry comes from the [VoronDesign/Voron-2](https://github.com/VoronDesign/Voron-2/tree/Voron2.4) project, licensed under the GNU General Public License version 3. The unmodified repository license is included as `reference/VORON-LICENSE`. CxChanger source and adaptation licensing is retained in the parent printed-parts folder.

Reference source: `CAD/Voron_2.4r2_Assembly_STEP.zip`, Git blob SHA `142a355c22f6e488deb0aac4104cc2073bc31321`. The archive contains the official 250-size assembly. The 350-size reference applies the [official configurator](https://vorondesign.com/voron2.4) length and placement differences of 100 mm without scaling bearings, fasteners or printed parts.

The normalized frame has its origin at the center of the rear gantry crossbrace, X across the machine, +Y rearward and +Z up. Original assembly coordinates `(sX,sY,sZ)` become `(sY+163, -sX-8.49958338, sZ-33.40599583)`. The right/left XY joints move +50/-50 mm along X for the 350 configuration; front idlers additionally move -100 mm along Y. These datums are not Klipper coordinates.

Minimal retained BREP references:

- `placed-9.brep` and `placed-20.brep`: original left/right XY-joint assemblies, used to check their motion against the new supports.
- `Front-Idler-A-350.brep` and `Front-Idler-B-350.brep`: front idler assemblies transformed to the 350 reference.
- `new400mm-raised-rail.brep`: an illustrative 400 mm extrusion using the source HFSB5-2020 cross-section. Clearance checks also use a conservative solid 20×20 mm envelope; the purchased profile's T-nuts and slot details still require fit checking.

The editable FCStd projects, native FreeCAD generator, geometric parameters and independent validators accompany the exported STEP/STL files. No custom FreeCAD proxy is required.
