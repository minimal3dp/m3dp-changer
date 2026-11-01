# Insert-fit coupon for M3 × Ø5 × L4 inserts

**Material for this build: ASA, as selected by the user.** Print the coupons and matching final parts with the same ASA and settings. These coupons establish insert fit only; they do not certify pillar strength, thermal performance or creep resistance.

The user has confirmed **5 mm outside diameter and 4 mm length** and selected **4.6 mm nominal CAD bore (`4p6`)** after the coupon comparison below. The maker's pilot-hole recommendation is not yet available; this selection is based on the user's printed samples. Do not infer hole diameter from the `M3×4×5` product shorthand.

## Recorded selection

The user preferred `4p6` for cold fit. After heat-setting all five inserts and allowing them to cool, the user reported `4p5` or `4p6` as the best fit and that the screws went all the way through easily. The user then explicitly selected `4p6` for the models and STLs.

Apply the selected Ø4.6 mm bore to the two front P5 insert supports, three TAP-adapter seats, three fan-retainer seats per paired dock and the two matching seats in the 2510 cage coupon. These parts have different surrounding geometry; the sleeve results do not establish retention strength in all of them. No torque/pullout result, repeat on a second selected coupon or thermal-performance test has been reported. Actual printed bore measurements, installation temperature and seating-depth measurements were not supplied.

[insert-bore-4p6-validation.json](insert-bore-4p6-validation.json) is the authoritative geometry-validation record for this revision and supersedes affected earlier geometry checks; its status does not expand the physical evidence above. The next print is **one `stl/coupons/chaoticlab-v2-interface-fit-gauge.stl`**.

## Coupon geometry

The supplied coupon consists of five separate **Ø10 mm × 5 mm-high sleeves**, with trial through-bores of **4.3, 4.4, 4.5, 4.6 and 4.7 mm**. These are an exploratory range, not manufacturer specifications. They have no floor, shared base, entry chamfer or embossed text. Print the sleeves individually and label them manually before testing so the hole sizes cannot be confused.

The native file is `insert-fit-coupon.FCStd`; `insert-fit-coupon.step` contains the same five sleeves in left-to-right order 4.3, 4.4, 4.5, 4.6, 4.7 mm. Individual STEP and STL files are:

| Trial bore | File stem (both `.step` and `.stl`) |
|---|---|
| 4.3 mm | `insert-coupon-4p3` |
| 4.4 mm | `insert-coupon-4p4` |
| 4.5 mm | `insert-coupon-4p5` |
| 4.6 mm | `insert-coupon-4p6` |
| 4.7 mm | `insert-coupon-4p7` |

These sleeves match the initial P5 front support's outer diameter and overall depth. If the final part uses a different entry profile, blind floor or wall geometry, test that representative feature too; a plain sleeve does not reproduce those changes.

Keep the supplied specimens separate. Do not add a thick common base underneath the holes: that would test a different support condition. Provide enough room around the selected specimen to use the same installation tip and fixture as the real part.

P1 and rear P5 use the revised integral P1 pillars and metal through-bolts/nuts, not inserts or separate metal spacers. This sleeve coupon represents the two front P5 insert supports; the selected bore is also used in the TAP adapter and dock/cage parts, whose own seating and clamping still need checking. It is not evidence for countersink fit or whole-head strength.

## Test procedure

1. Measure an actual insert's maximum knurl diameter, body length and tip/lead-in shape. Record supplier/lot if known. Record the chosen material and slicer hole compensation.
2. Print all five with the intended material, orientation, layer height and wall settings. Measure the unheated bores where possible and record nominal versus printed dimensions.
3. Install one insert in each specimen using the maker's process if supplied. Otherwise, develop the process on the coupon with a controlled tip, square support and a depth stop; do not assign a universal temperature from the CAD file.
4. After complete cooling, inspect for split walls, lifted material, ovality and seating-height error. Thread the intended M3 screw by hand and check that it neither binds nor bottoms prematurely.
5. Tighten the intended joint in a representative test assembly and check for insert rotation, pullout or local deformation. Repeat insertion on a second specimen of the selected bore so a single successful attempt is not treated as a reliable process. Recheck after representative warm-chamber exposure before using the structural part.
6. Record the selected nominal CAD bore, measured printed bore, seating depth, process settings and observed result. Apply that result only to the tested geometry/material/process combination.

Do not install an oversized insert by forcing it into an undersized production hole. If every specimen fails, revise the range or the surrounding support; do not select the least-bad failure. Keep screw torque and thermal settings tied to the actual material, insert and joint rather than inventing numerical limits.
