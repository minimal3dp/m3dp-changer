# CxChanger printed 6.11 — CAD integration update

This fit-prototype set is for six tools on a standard Voron 2.4r2 350, with Chaoticlab CNC TAP V2, ASA parts, and M3 inserts measuring 5 mm OD ×4 mm long. It retains the stock closed enclosure and accepts reduced Y print area.

## Included changes

- An 11 mm TAP adapter at the original head height, an integrated top-mounted 4020 blower carrier, and a side-fed duct retaining the original nozzle jets. The obsolete lower-switch holes are sealed. The native generator now applies the original duct's part-to-assembly placement explicitly.
- Left/right supports for a new 400 mm 2020 rail on the moving gantry. The matching layout has modeled door, physical-bed and upper-frame margins; these are not measured printer clearances.
- Three raised two-station dock modules, with 34 mm spacing within each pair and 38 mm between pairs. The nominal dock-body span is 216 mm; the fan-retainer ears extend it to 221 mm. Six 2510 fan cages use nine removable M3 retainers.
- An upper tool/filament detector mount seated on the existing motor ear, with checked fastener envelopes. The proposed switch truth table is true only with both tool and filament; its physical actuation still needs testing.
- The earlier integral-pillar P1, reinforced P3/P4, two-insert P5, printed P8 arm and six hotend holders remain in the active set.
- The selected insert bore is now **Ø4.6 mm (`4p6`)** at the two P5 seats, three TAP-adapter seats, three fan-retainer seats per paired dock and the matching two-seat 2510 cage coupon. The 4.3–4.7 mm comparison coupon set is preserved.

The active print manifest contains **15 designs, 28 printed pieces and nine fit coupons**. P2, the original rear-blower duct, old 30 mm-pitch dock and old rail coupon are preserved under reference-only directories and excluded from that manifest. Do not mix intermediate 6/9 mm adapters or old support geometry with this 11 mm layout.

## Digital validation

For the 4.6 mm insert-bore revision, [insert-bore-4p6-validation.json](insert-bore-4p6-validation.json) is the authoritative validation record and supersedes affected earlier geometry checks. Consult its recorded status and scope; the following describes the baseline integration checks.

Native FreeCAD models were built, saved and reopened; editable dimensions were changed and restored. STEP readback and independent STL checks verify closed solids, connected watertight meshes and consistent winding. The new duct has an enclosed path from the fan inlet through the plenum to both nozzle jets. Assembly checks cover both XY joints, sampled TAP travel, retained detector hardware, parked neighbors and sampled docking poses.

The duct's default mass-property integration varies slightly across native and STEP representations. The verifier records bounded volume/area/centroid tolerances and retains the 0.0001 mm bidirectional sampled-surface limit. The measured surface agreement is substantially tighter. Geometric air connectivity is not an airflow-performance test.

## Fit and commissioning

The user favored `4p6` cold, reported `4p5`/`4p6` best after heat-setting and cooling with easy screw travel, and selected `4p6`. **Next print one `stl/coupons/chaoticlab-v2-interface-fit-gauge.stl`**, followed by the gantry, rail-saddle and fan-cage coupons, then one holder and one dock pair. Inspect slicer supports, precision seats and the duct interior; no inaccessible internal duct support is acceptable.

The conservative modeled Y print depth is about 324 mm, subject to actual fitting, cabling and travel calibration. Do not copy this value into Klipper as a calibrated limit. Keep the low parked nozzle pads outside the physical bed; a slicer exclusion alone does not prevent collision.

Hardware notes now allocate 32 ordinary M3 nuts and 14 production inserts. Rail-clamp lengths depend on the actual extrusion and T-nuts. Verify the specified small countersunk heads, TAP screw engagement, fan body and PC4 fitting/collar clearances before assembly.

The physical evidence is limited to the reported insert-coupon fit and screw travel. No torque/pullout, repeat on a second selected coupon, assembled-printer fit, load, probe-repeatability, airflow, warm-chamber creep or automatic-tool-change result has been reported. Loaded/hot operation remains unqualified. No live printer settings were changed.
