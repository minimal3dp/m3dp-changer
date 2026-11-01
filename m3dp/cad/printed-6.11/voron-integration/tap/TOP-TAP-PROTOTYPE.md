# M3DP Changer / Chaoticlab CNC TAP V2 integration prototype

This source set is the **11 mm adapter / original head-height** revision. It combines the TAP adapter, an elevated 4020 blower carrier, and a side-fed replacement duct retaining the original two nozzle jets. The adapter/carrier and duct remain fit prototypes; their printing, load testing, TAP probing, powered cooling and printer operation have not been reported.

**The baseline 11 mm revision passed native generation/reopen, dependency-edit restoration, STEP readback and independent STL checks.** Its two parts were valid closed single solids and all four meshes were watertight single components with consistent winding. The selected 4.6 mm insert-bore revision uses [insert-bore-4p6-validation.json](../../insert-bore-4p6-validation.json) as its authoritative validation record, superseding affected earlier geometry checks; consult that record for current status and scope. Use this revision together with the matching lowered front-rail supports. The earlier 6 mm and 9 mm exports are superseded. Physical qualification remains outstanding.

To regenerate, run `BuildTopTapPrototype.FCMacro` in FreeCAD, `ValidateTopTapAir.py` with a PythonOCC environment, then `VerifyTopTapPrototype.FCMacro` in FreeCAD. The existing bundled Python on this Mac can run the independent validator. The final verifier checks its receipt against exact export hashes; do not reuse a receipt after rebuilding. It preserves the frozen preflight reference and applies only the three selected Ø4.6 mm insert cutters before comparing the adapter. The current bore-revision record above separately documents the change from the previous exports. Both macros record progress/results before optional display work.

## Parts and datum

Generate one adapter/carrier and one duct. Keep the separately validated integral P1, P3, P4 and P5 plates, selected printed arm, original hotend holders, and the separate corrected detector prototype. The original CNC P2 spring plate is not an additional part with the selected printed arm.

The source Cx coordinate transform into the MGN12 front mounting-face/hole-pattern center is:

`X = CxX − 19.95; Y = CxZ − 24.52053; Z = −CxY − 13.5`.

The nozzle is `(0, −42.22161593, −69)` in that frame. Use the matching **11 mm lowered front-rail support revision**. At the modeled docking position, MGN is `(0, −424.15338596, −0.0865699)` in the rear-crossbar frame; rail center is `(0, −482.530002, 48.91343)`. These are CAD reference coordinates, not commissioned Klipper positions.

The TAP reference is the user's Chaoticlab CNC TAP V2. Manufacturer instructions establish the four outer attachment holes; a third-party measured V2 reconstruction supplies approximate clearance geometry. Its internal parts and 3 mm travel are reference assumptions requiring physical confirmation. Licensed V2 bodies are not embedded in the deliverable model.

## Hardware and assembly

| Interface | Hardware | Modeled fit |
|---|---|---|
| Upper TAP pair | 2 × M3×6 socket-head screws | Seat at Cx Z8.3, TAP face at Z11: 3.3 mm engagement |
| Lower TAP pair, shared with duct | 2 × M3×14 socket-head screws | Duct seat at Z−0.5: 2.5 mm engagement in TAP |
| Adapter to P5 | 3 × M3 heatsets, 5 mm OD × 4 mm long | Front entry Z0; selected Ø4.6 × 5.1 mm seat, then Ø3.3 relief |
| P5 upper two axes | 2 × M3×10 socket-head screws | Install into the adapter inserts; check actual seating and engagement |
| P5 lower-right axis | 1 × M3×8 socket-head screw | Install into the third adapter insert |
| Top blower | Reuse 3 × M3×22 button-head screws; add 3 × M3 nuts and 3 × Ø7 × 0.5 mm washers | 12.75 mm fan mounting flange + 3 mm carrier + 0.5 mm washer + 2.4 mm nut = 18.65 mm stack; 3.35 mm tip projection |

The fan has an approximately 19 mm total body thickness, but its three screw seats clamp the measured **12.75 mm mounting flange**. All three modeled Ø3.3 fan bore axes coincide with the carrier axes after relocation. Confirm the actual fan has this same flange and under-head plane before reusing M3×22; a different fan housing needs a fresh stack check. The final build count is **32 M3 nuts**: 28 for the prior integral-head/six-hotend build, one detector anchor nut, and three blower nuts. The recorded 55-piece pack covers that count if all nuts are actually available.

**TAP interface gauge fit passed (2026-10-31):** the user reported that `stl/coupons/chaoticlab-v2-interface-fit-gauge.stl` fits well. This confirms gauge fit only, not full TAP assembly or operation. **Next print one `stl/coupons/front-gantry-fit-coupon.stl`** and check the right-side gantry mating face, bolt stack and unobstructed Z-belt fork.

Fit the adapter to TAP before attaching P5; the lower two screws pass through the duct tabs and adapter together. The user selected the Ø4.6 bore (`4p6`) after sleeve-coupon heat-setting and cooling, with easy screw travel reported. This is not a supplier-qualified hole specification or an adapter retention-strength result; check installation in the adapter's own seats. The top carrier is an open frame; route wiring without obstructing the blower intake or TAP travel.

The model reserves a straight Ø4 mm PTFE route with 1 mm radial clearance above the filament axis. **The purchased PC4-M6 fitting body and collar position are not known/modelled.** Check fitting clearance, collar release access and a practical tube bend on the actual assembly before printing the full carrier or enabling motion.

## Geometry evidence and limits

Independent OpenCascade checks cover valid single solids, retained head parts, detector and conservative detector-fastener envelopes, both XY joints at nozzle X±175, TAP travel samples at 0/1.5/3 mm, and the blower mounting axes. Separate dock checks cover both adjacent parked tools, entry/latched/retreat snapshots and the 0.85 mm axial press allowance. Minimum new-duct clearance at maximum press is about 0.776 mm to a neighboring coupling pin and 0.806 mm to a dock actuator pin. These small margins need a physical fit test. The closed source arm bearing contacts the original dock at maximum press; that is an articulated mechanism, not a rigid-body clearance pass.

The duct has a defined 153 mm² neck and approximately 171.5 mm² rounded side port. Its unchanged jets total 54.2829 mm², so the neck is 2.82 times the combined jet area. The longer path and extra bends can still change pressure loss and cooling distribution; section area is not an airflow-performance claim. The original intake is capped, unused Eddy holes are filled, and two obsolete lower-switch holes are sealed flush with 2 mm material. A temporary-cap air-volume test must demonstrate one enclosed cavity connecting the inlet neck, side port, original plenum and both jets, separate from outside air.

The loft profiles expand 1.2 mm outward to form the duct wall; that is a construction dimension, not a demonstrated uniform minimum thickness through every transition. Inspect the sliced walls and bridges. The supplied print orientations require external support; do not put support inside the airway. No strength, creep, vibration or heat resistance qualification is implied.

Before printer use, verify all screw seats without bottoming, insert pullout and adapter stiffness under coupling/release forces, fan vibration, full TAP travel/return and trigger repeatability, closed-door and bed clearance across the usable range, filament/harness routing, and powered airflow at both jets. Use the separate commissioning instructions for actual tool offsets and reduced motion limits.

## Generated filenames

- `CxChangerTopTapPrototype.FCStd`
- `tap-adapter-top-fan-carrier-PROTOTYPE.step`
- `tap-top-fan-duct-PROTOTYPE.step`
- Each part also has `-assembly.stl` and `-print-with-external-supports.stl` exports.
- `top-native-build.json` and `top-native-validation.json` record the successful native run.
- `top-independent-export-validation.json` records independent STEP/STL checks.
- `top-export-airway-validation.json` records independent air-path checks on both actual duct exports; `ValidateTopTapAir.py` regenerates it.

The original corrected 6.11 duct is retained in part-local STEP and assembly-frame BREP forms under `source/cx/`; the latter supplies the diagnostic jet caps. See `REFERENCE-ATTRIBUTION.md` for provenance. Other source/reference CAD remains outside this deliverable. Do not redistribute the third-party V2 reconstruction with it.

Native cylinders, boxes, extrusions and Booleans remain editable. Stored outline/loft ControlPoints are descriptive metadata, not a GUI constraint system; change those profiles in the macro and regenerate.

The native verifier limits bidirectional sampled boundary differences to 0.0001 mm. The measured preflight/native difference is 0.00000000442 mm for the duct; both native/STEP differences are below 0.000000000009 mm. Rewriting trimmed B-spline faces changes the default numerical mass integration: the duct showed 0.932 mm³ volume, 0.123 mm² area and 0.00317 mm center differences. Its guards are therefore 1.0 mm³, 0.15 mm² and 0.004 mm, alongside the unchanged strict boundary check; the adapter retains tighter mass guards. Independent adaptive Gauss–Kronrod integration reduced the duct volume disagreement to 0.0777 mm³. This is numerical validation evidence, not a manufacturing tolerance.

The independent PythonOCC airway test uses coplanar-face refinement and a 0.000001 mm Boolean tolerance for temporary caps because raw cap operations produced inconsistent air partitions. Both actual exports passed: exactly two positive, disjoint air solids and one enclosed cavity joining all five stages. No printed geometry is changed by the diagnostic operations. The native verifier checks the independent receipt and exact file hashes; it does not claim FreeCAD performed the air-volume Boolean test.
