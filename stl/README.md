# M3DP Changer — six-tool ASA fit-prototype set

This set combines the selected printed P8 mechanism with a Chaoticlab CNC TAP V2 adapter, top-mounted 4020 blower, paired docks on a new 400 mm 2020 gantry rail, dock-fan retainers, and an upper detector mount. The layout targets a standard Voron 2.4r2 350 with closed stock doors and reduced Y print area. **These are fit prototypes: CAD checks do not qualify loaded, hot or automatic operation.**

The active set has **15 designs, 28 printed pieces for six tools, and nine fit coupons**. Files in `reference-only/` are excluded. In particular, omit P2 with the printed P8 arm, and use the new TAP duct instead of the original rear-blower duct.

## Print and measure the coupons first

Use the same ASA, nozzle, layer height, walls and dimensional settings for coupons and their final parts. The upstream baseline is four walls and 60% infill; inspect local walls and follow the filament manufacturer's settings. Do not scale the entire mechanism to fix an individual hole.

| Coupon | Quantity | Check |
|---|---:|---|
| `coupons/insert-coupon-4p3.stl` through `insert-coupon-4p7.stl` | 1 each | Comparison completed; user selected `4p6` (4.6 mm nominal bore) for the actual M3 inserts, 5 mm OD ×4 mm long |
| `coupons/chaoticlab-v2-interface-fit-gauge.stl` | 1 | Four TAP mounting-hole positions; use suitable short screws without bottoming |
| `coupons/front-gantry-fit-coupon.stl` | 1 | Stock front-idler bolt stack and unobstructed Z-belt fork |
| `coupons/raised-2020-saddle-fit-coupon.stl` | 1 | Actual 2020 exterior, M3 T-nuts, screw engagement and clamping |
| `coupons/2510-cage-fit-coupon.stl` | 1 | Actual 2510 fan body, cable exit and retainer fit |

**2510 fan body fit confirmed (2026-10-30):** the user printed the [build123d 4p6 cage coupon](../m3dp/cad/printed-6.11/voron-integration/dock/build123d/2510-cage-fit-coupon-build123d-4p6.stl) and reported that the fan fit perfectly. **Installed retainer fit confirmed (2026-10-31):** the user reported that the cage retainers fit great. Insert retention, clamping strength, torque/pullout, cable exit clearance, and heated operation remain unreported. See the [coupon record](../m3dp/cad/printed-6.11/voron-integration/dock/build123d/README.md).

**TAP interface gauge fit passed (2026-10-31):** the user reported that `coupons/chaoticlab-v2-interface-fit-gauge.stl` fits well. This records gauge fit only; full TAP assembly and operation remain untested.

**Gantry and saddle coupons printed (2026-10-31):** the user supplied bench photos (`IMG_0429`, `IMG_0430`, `IMG_0431`, `IMG_0433`) and confirmed that the raised saddle fits the actual 2020. This passes the saddle's extrusion fit only; M3 T-nut clamping, screw engagement and bottoming remain unreported. The gantry coupon's mounted fit remains unreported. Its fork underside has loose, curled strands in `IMG_0431`; inspect after removing support/debris. If part layers or the belt-opening edge remain distorted, reprint with supports beneath the raised arms before judging clearance.

**Outstanding coupon check: fit the printed front-gantry coupon at the right-front gantry clamp.** Check the seated mating face, bolt stack and unobstructed Z-belt fork, then finish the saddle's M3 clamp check before printing the full rail supports. See [rail fit directions](../m3dp/cad/printed-6.11/voron-integration/rail/front-rail-support-notes.md) and [saddle hardware](../m3dp/cad/printed-6.11/modular-dock-notes.md#raised-rail-and-fastening).

**B1 prints completed (2026-10-31):** after receiving the eight-piece batch list, the user confirmed printing complete: P1, P3, P4, P5, P8 and detector mount, one each, plus two hotend holders. Print quality and assembly fit remain unreported. **Next inspect these parts and dry-fit the head and T0/T1 holders** using the [assembly notes](../m3dp/cad/printed-6.11/printing-and-assembly-notes.md). Complete the affected outstanding coupon checks and this dry-fit before the B2 rail-support/dock batch.

Keep the printed left and middle fan retainers for the final dock if they remain sound; they count toward the three required of each design. The insert sleeves, cage coupon, TAP gauge, gantry coupon and saddle coupon are test pieces, not installed assembly parts. Keep them labeled for future fit comparisons.

Use the [illustrated B1 assembly guide](../m3dp/cad/printed-6.11/assembly-guide/README.md) to identify the eight head-batch prints and follow their orientation and hardware stacks. It includes a printable PDF with labeled CAD views.

The selected 4.6 mm insert bore applies to the two front P5 seats, three TAP-adapter seats, three fan-retainer seats in each dock and the two matching seats in `2510-cage-fit-coupon.stl`. The user favored `4p6` cold, found `4p5`/`4p6` best after heat-setting and cooling, and reported easy screw travel. Torque, pullout, a second coupon and thermal performance have not been reported. See [insert results](../m3dp/cad/printed-6.11/insert-coupon-guidance.md) and the authoritative [4p6 geometry validation record](../m3dp/cad/printed-6.11/insert-bore-4p6-validation.json), which supersedes affected earlier geometry checks. The original 4.3–4.7 mm comparison coupons remain available.

## Print quantities

| Active STL filename | Quantity |
|---|---:|
| `p1-magnet-plate-integral-pillars-print-flat.stl` | 1 |
| `p5-backplate-two-inserts-through-bolt-print-flat.stl` | 1 |
| `p3-cover-left-clamp-web-print-flat.stl` | 1 |
| `p4-cover-right-clamp-web-print-flat.stl` | 1 |
| `p8-printed-bearing-arm.stl` | 1 |
| `hotend-holder.stl` | 6 |
| `two-station-dock.stl` | 3 |
| `fan-retainer-left.stl` | 3 |
| `fan-retainer-middle.stl` | 3 |
| `fan-retainer-right.stl` | 3 |
| `tap-adapter-top-fan-carrier-PROTOTYPE.stl` | 1 |
| `tap-top-fan-duct-PROTOTYPE.stl` | 1 |
| `front-rail-support-left.stl` | 1 |
| `front-rail-support-right.stl` | 1 |
| `tool-detector-mount-PROTOTYPE.stl` | 1 |

Use the four revised P1/P3/P4/P5 parts together. P1 includes clearance-bored printed pillars, with metal M3 through-bolts and nuts; no metal M3 standoffs or printed threads are used. The two bolts are M3×20 and M3×30, 90° countersunk, actual head diameter ≤5.6 mm. Follow the documented nut/washer stack.

The docks have **34 mm station pitch within a pair and 38 mm between pairs**. Three modules occupy 216 mm; fan-retainer ears extend the full plastic envelope to 221 mm. These are CAD dimensions, not Klipper pickup coordinates. Label and measure every station separately. Eight-tool permutations are not qualified on this six-tool installation.

Review every slicer preview. The head plates are oriented flat. The tall rail supports, dock fingers and TAP/carrier/duct parts require external-support review. Keep support out of the cooling airway and precision seats; do not accept missing thin walls or inaccessible support inside the duct. Print one dock pair and one holder, then dry-fit the whole motion before duplicating them.

## Acceptance before powered changing

1. Check TAP mounting, full probe stroke and return, fitting/push-collar access, cable/PTFE routing, gear and arm motion, and all fastener heads/thread ends.
2. With the printer unpowered, check pickup and release at every station, both travel ends, bed edges, closed doors, belts and the full intended Z range. Keep the low nozzle pads outside the physical bed; a slicer exclusion alone does not prevent a first-layer collision.
3. Verify switch operation for empty head, tool with filament and tool without filament using the intended sampling sequence. Check hotend retention and nozzle-pad compression by hand.
4. Test blower and dock-fan airflow, then supervised warm-chamber stiffness, creep and repeated changes. Set measured machine travel/dock coordinates only after these checks.

See [CAD and assembly documentation](../m3dp/cad/printed-6.11/README.md) for editable sources, hardware stacks, provenance and the exact scope of validation. The existing firmware is not recalibrated by installing these files.
