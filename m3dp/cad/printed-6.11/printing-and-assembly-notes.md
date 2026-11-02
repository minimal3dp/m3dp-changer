# M3DP Changer: printing and assembly

This build keeps the corrected 6.11 mechanism and adapts selected parts for printing. It does not use the historical printed 4.25 assembly. The purchased heat-set inserts are **M3, 5 mm outside diameter × 4 mm length**. Original CNC files remain references. The primary set uses integral printed pillars on P1, a rear through-bolt on P5 and matching reinforced P3/P4 covers. Use the four matching adapted parts together; the earlier metal-spacer arrangement is a work-only fallback, not the primary build.

## Part selection

| Original part reference | Use in this build |
|---|---|
| p1, top magnet plate | Use **p1-magnet-plate-integral-pillars**. Both installed source posts are integrated into P1, with M3 clearance bores and metal through-bolts/nuts. Do not install Ø5 × 4 inserts in these pillars. The remaining thin plate sections are not broadly strengthened. |
| p2, spring support plate | **Omit.** This belongs to the CNC arm alternative and overlaps the selected printed P8 arm. The source/export is retained for reference only. |
| p3/p4, left/right covers | Use **p3-cover-left-clamp-web** and **p4-cover-right-clamp-web**, with Ø7 mm support through each existing clamp web and Ø3.4 mm clearance holes. These preserve all original mating/bearing planes. Their remaining thin regions still need print/stiffness verification. Do not substitute unmodified source covers at the two through-bolts. |
| p5, Trident backplate | Use **p5-backplate-two-inserts-through-bolt**. Its front pair use the purchased Ø5 × 4 inserts; the rear clearance hole/countersink takes the long through-bolt through P1’s second pillar. It is not a ready-made TAP carriage adapter. |
| p6/p7, outer/inner CNC swing levers | Omit these alternatives when using the printed one-piece arm. |
| p8, printed one-piece swing arm | Print **one** of this 6.11 alternative, exported unchanged. Use its single bearing, gear and fastener set; do not duplicate hardware from the omitted CNC alternative. |
| Hotend holders | Print **six** matching corrected 6.11 holders, one per tool. Source geometry is exported unchanged. |
| 4020 cooling duct | Use the new top-blower duct with its matching TAP adapter/carrier. The original rear-blower duct is reference only. See `voron-integration/tap/`. |
| Cx tool/filament detector | Use the prototype upper switch mount adapted from the earlier 6.11 assembly, in `voron-integration/detector/`. The existing printed arm is the candidate actuator; the binary switch response in the three physical conditions remains unverified. |
| Dock | Use three raised-rail **two-station modules**, each on a 72 mm pitch, to provide six tools. The station pitch is 34 mm within pairs and 38 mm between pairs. Fit the new saddle and fan-cage coupons first. The old 30 mm-pitch and fixed racks are historical references, not verified alternatives. |

The full STEP displays alternatives simultaneously. For the actual chosen head, two 36-tooth extruder gears are used rather than the three displayed across both arm alternatives. The duplicated 683ZZ bearing, small washer, M3×8 screw and M3 nut likewise belong to alternate arms. The extra 10 mm M4 post and source M3×16 countersunk screw belong to the omitted CNC arm, not the selected printed arm. Consult the selected-arm assembly rather than totaling every displayed occurrence.

## Primary through-bolt fastening

The pillars contain clearance holes, **not plastic threads**. Clamp each joint with a metal countersunk screw, washer and nut. Use the matching revised covers so the washers bear on a full nominal support face.

| Joint | Through-bolt | Lower hardware | Nominal stack |
|---|---|---|---|
| P1 pillar, original 10 mm post position | **M3×20**, 90° countersunk, actual head Ø≤5.6 mm | One M3 nut, 5.5 mm across flats ×2.4 mm thick; one M3 washer, 3.2 mm ID, **OD≤7 mm**, 0.5 mm thick | Head 0.1 mm recessed in Ø5.8 mm mouth; bolt tip 1.7 mm beyond nut |
| Rear connection, original 14 mm post position | **M3×30**, 90° countersunk, actual head Ø≤5.6 mm | Same nut and washer | Head 0.3 mm recessed in Ø6.2 mm mouth; bolt tip 1.9 mm beyond nut |

Countersunk screw length includes the head. Check complete head profile, actual length, threaded length at the nut and seating; a nominal 90° cone does not capture every manufactured rim or tolerance. The nut/washer dimensions are part of the stack. A thicker washer, taller locking nut or different screw head changes engagement and clearance. Do not use the prior short top/bottom screw arrangement with these integral pillars.

The two M3 metal standoffs are **not required for this primary version**. Both pillars attach to P1 at the original post locations; do not extend a separate pillar from P5 across the original gap. The purchased M4 spacers remain spare stock. The third source 10 mm post belonged to the unselected CNC arm. The base six-tool mechanism needs **28 M3 nuts**, before the new detector and top-blower mounting hardware: 24 in the six modules, two in the selected head and two added for these through-bolts. Adding one detector-anchor nut and three top-blower nuts gives **32 ordinary M3 nuts for the complete final11 build**. The M3/M5 rail T-nuts and two M2 detector nuts are separate counts. The saved BOM records a 55-piece nut pack and 100-piece washer pack; locate and measure those before buying replacements. The printed-arm washer retains its own 3.2×6×0.5 mm requirement. The two cover washers must be 0.5 mm thick with OD no greater than 7 mm; 6 mm and 7 mm envelopes were checked. Verify adequate nut bearing and the actual fit rather than substituting arbitrary tiny washers.

[Würth’s manufacturer catalogue](https://www.wuerth.ee/kataloogom/wuerth_tootekataloog/219/) lists M3 DIN 965 screws in 20 and 30 mm lengths with Ø5.6 mm heads. This is a dimensional example, not evidence that the user’s ordered screws match. The order PDF shows M3×16 DIN 7991 screws, not these long through-bolts. Do not substitute unspecified ISO 10642 M3: its head can reach Ø6.72 mm. [Böllhoff dimensions](https://eshop.boellhoff.de/out/media/pdf/ISO_10642_Stahl_10.9___en.pdf).

## Fit limits at the revised joints

P1’s Ø5.8 mm countersink mouth has a small interrupted lip at a nearby opening: the original outer boundary is approximately 2.86–2.87 mm from the axis, versus the 2.9 mm mouth radius. The modeled ≤5.6 mm head cone is supported below the lip and has about 0.837 mm clearance from a conservative rotating 17T gear envelope. The rear head has only 0.3 mm nominal motor clearance. Check that both real screws remain recessed.

The covers gain support through the existing clamp-web thickness: P3 2.5 mm, P4 2 mm. All original mating and lower bearing faces remain fixed. There is **no added 0.6 mm underside flange** in the selected geometry. The rear Ø7 mm web and maximum-size washer have only 0.33 mm clearance to the modeled hotend holder. A Ø7 mm, 12 mm long socket approach clears the modeled parts, but actual nut-driver/handle fit and all mechanism positions must be checked.

Inspect the final cover clearance holes and printed pillar bores. The source covers had Ø3.05 mm holes; the revised covers target Ø3.4 mm, and the pillar bores target Ø3.2 mm. Verify free insertion of the actual bolt rather than forcing it into plastic. Dry-fit a screw through the complete stack before tightening. Ensure no bolt, nut or washer contacts the hotend module or moving arm through its complete travel.

Geometric fit does not establish clamp strength or a tightening torque. Confirm that the pillars, covers and plate sit squarely without bending, cracks, separated layers or slipping. Do not overtighten to compensate for a weak or poorly seated print. Recheck clamp condition after supervised warm operation. The metal-spacer version remains a work-only fallback if the integral version does not pass physical testing.

## Print setup and inspection

**ASA is the user's selected material for this build.** Voron supports ASA alongside ABS, which makes ASA a reasonable starting material for this enclosed printer. This does not qualify the newly adapted Cx parts for their actual clamp loads, temperatures or sustained use. [Voron material guidance](https://docs.vorondesign.com/materials.html).

CxChanger upstream specifies ABS, four walls and 60% infill (`reference/cxchanger/README-original.md:98`, `reference/cxchanger/README-English.md:97`). Use that as the documented geometry/process baseline while following the selected ASA manufacturer's temperature, drying and chamber guidance. The integral pillars, clamp webs and insert supports need intact local walls in the slicer; an infill percentage alone does not establish strength. Use the **same ASA, nozzle, layer height, wall count and dimensional-compensation settings** for each fit coupon and its matching final parts.

Voron's statement that its own parts include ABS/ASA shrinkage compensation does **not** establish that these CNC-derived Cx shapes include it. Measure the actual Cx coupons and parts; do not import a blanket shrinkage correction or scale the entire assembly to fix one hole.

PC or a PC blend is not an automatic upgrade. Voron notes the tradeoff between higher temperature capability and stiffness/cracking risk, while acknowledging some toolhead use. Consider a specific alternative only if the ASA prototype fails the required thermal or sustained-clamp tests, then revalidate dimensions, stiffness and ductility. No PC/PC-CF purchase is added to this build. [Voron PC discussion](https://docs.vorondesign.com/materials.html#polycarbonate).

Orient the parts so the magnet/coupling reference faces stay flat and the insert holes remain measurable. Check slicer previews for unsupported ceilings, missing thin walls and support contact inside pin/bearing seats. Print orientation and supports need to match the final adapted geometry; the source assembly's world coordinates are not print orientations.

Inspect the finished part before installing hardware. Reject cracked walls, separated layers, warped coupling faces and lost small features. Remove burrs without enlarging precision pin/bearing seats indiscriminately. Fit a spare pin/bearing and an insert coupon before committing the complete set. Do not scale the whole part to repair one undersized hole.

## Insert installation

The user selected **Ø4.6 mm (`4p6`)** after comparing cold fit and fit after heat-setting/cooling, with easy screw travel reported. This bore applies to the P5 front pair, three TAP-adapter seats and dock fan-retainer seats, including the matching cage coupon. See `insert-coupon-guidance.md` for the recorded evidence; torque/pullout, repeat-coupon and thermal-performance results remain unreported. Use the insert maker's installation guidance if available. Verify actual maximum knurl diameter and length with calipers. Distinguish insert length from available bore depth and from screw clearance beyond the insert.

Install with a suitable temperature-controlled tip while supporting the part squarely. Stop at the designed seating face, let it cool without loading, then test the intended screw and engagement. Do not use the screw to pull a hot insert into alignment. The insert must not protrude into a gear, bearing, magnet pocket or mating face. A fit coupon establishes the process, not the loaded assembly's strength.

For P5's front pair, the first reviewed Ø10 mm support envelopes clear the modeled parts, but the closest MGN12H clearance is only 0.4 mm. Confirm the **final** geometry and actual print clear that rail carriage before tightening. The rear P5 insert proposal was also rejected: a full boss interfered with nearby parts, while the reduced support left roughly 0.5 mm of plastic beyond a Ø5 insert near its entry. Use the revised rear through-bolt and integral P1 pillar instead.

## Mechanical assembly checks

1. Dry-fit the four matching revised parts, through-bolts and selected printed arm. Rotate the gear train through full turns by hand and move the arm through its complete release/clamp stroke. Check screws and inserts for contact throughout the sweep, not only at the STEP's saved position.
2. Install magnets and locating pins according to the original coupling geometry. Upstream requires the spherical pins to contact their cylindrical-pin grooves while the opposing magnets retain a small gap. A magnet contacting its counterpart defeats the locating arrangement (`reference/cxchanger/README-original.md:101`).
3. Use magnetic heads for the actual **M3×10 docking hooks** in the corrected 6.11 assembly. Their axes are 15 mm apart and match the dock keyholes; the transverse M3×22 pair clamps the hotend. Upstream calls for grade 12.9 cap-head hooks; 304 stainless screws may not provide the intended magnetic retention (`reference/cxchanger/README-original.md:102`). Check the actual M3×10 screw and dock magnet together.
4. Fit every hotend to the head and every dock station manually. Check positive seating, arm release, nozzle-plug compression, cable/PTFE clearance and removal without snagging. Fit and adjust the prototype Cx detector mount, then confirm repeatable empty/tool-with-filament/tool-without-filament state changes before enabling automatic changes.
5. Establish dock cooling and validate fan mounting before any parked hotend is heated. Six configured fan loads do not establish that their mounting brackets and airflow are complete.
6. Only after the mechanical checks pass, commission coordinates and thermal operation one tool at a time using the separate wiring/configuration checklist.

## Scope still outside this CAD adaptation

The changed holes/supports solve selected fastening conflicts. They do **not** turn every CNC-derived plate into a qualified printed structural part. P1 retains thin sections; P3/P4 gain local clamp support but their other regions are unchanged. The pillars and rest of the head still need print-orientation, local wall, stiffness, creep and loaded-fit validation. Do not describe the complete head as print-ready based on these edits.

The `voron-integration/` folder adds fit prototypes for the TAP interface/top blower, raised gantry rail supports, paired dock fan retention, and upper detector mount. Their native/export checks establish CAD integrity; physical travel, airflow, retention, detector operation and warm-chamber loading remain acceptance tests.

The supplied backplate is named for Trident/MGN12H. The new Chaoticlab V2 adapter uses a measured reconstruction as an interface reference; its fit, stiffness and complete probe travel still require physical verification. Modeled printer/nozzle/dock clearances are documented in the integration notes. The upstream design uses a fixed microswitch with the hotend removed; it does not provide an existing TAP integration (`reference/cxchanger/README-original.md:22,66`). A dock attached to a Voron 2.4 must retain its alignment to the moving gantry across gantry leveling and Z travel. The actual bracket/extrusion placement must be checked on this machine.

Neither a valid STEP solid, an STL export nor a successful insert coupon establishes stiffness, heat resistance, tool retention or safe automatic changing. The generated-part manifest should state which checks have actually been completed.
