> Active-build selection: P8 arm and six hotend holders are retained. P2 is a CNC-arm alternative and must be omitted; the original 4020 duct is replaced by the TAP top-blower duct. This folder preserves source exports and their historical checks.

# Remaining corrected-6.11 printed parts

These four designs complete the available unchanged printed-component set alongside the separately adapted head plates and dock. Hardware and the alternate CNC swing arms are excluded.

| STL | Quantity for six tools | Placement / preparation |
|---|---:|---|
| `p2-spring-support-plate.stl` | 1 | Broad flat lower face on the bed. |
| `p8-printed-bearing-arm.stl` | 1 | Broad flat lower face on the bed; inspect internal overhangs and bearing/pin fits. |
| `hotend-holder.stl` | 6 | Broad coplanar rear faces on the bed; inspect supports and mating pockets in the slicer. Print and fit one before the other five. |
| `4020-part-cooling-duct.stl` | 1 | Source orientation lowered to the bed. **Orientation and support strategy still require slicer review.** Its thin source membrane is retained. |

The corrected assembly contains one occurrence of each listed design and one hotend module. The holder quantity is multiplied by six because it belongs to the removable hotend module. The spring plate, arm and duct remain on the common carriage.

Geometry comes from `m3dp/cad/printhead-6.11-corrected-EN.STEP`. The duct definition contained two overlapping solids; export uses their Boolean union, without adding a bridge or changing their material envelope. All other selected definitions are unchanged apart from rigid placement. Individual STEP sources and their source product IDs/hash are included for reproducibility.

`build-unchanged-printables.FCMacro` builds `unchanged-printables-6.11.FCStd`, four individual STL files and STEP files in print placement. It uses the adjacent `source/` folder. Run `verify-unchanged-printables.FCMacro` separately to check reopening, then run `validate-unchanged-printables.py` with PythonOCC for independent geometry and watertight-mesh checks.

The corrected assembly has an Eddy reference but no microswitch mount or detector actuator. The earlier uncorrected June model contains different detector parts; they are not mixed into this set. No TAP adapter, dock-fan mount or new gantry-rail bracket is invented here. Those physical integration parts remain unresolved rather than being represented by unrelated reference hardware.
