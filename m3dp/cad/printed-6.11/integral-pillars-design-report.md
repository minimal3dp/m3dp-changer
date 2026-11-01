# Integral printed pillars — four matched mounting parts

This selected adaptation removes both installed metal spacers from the selected 6.11 head with the one-piece printed p8 arm. Both pillars become part of **P1**, not P5. The head is clamped with two long M3 through-bolts, washers and metal nuts; **there are no printed threads**.

The other 10 mm M4 spacer visible off to the side in the source assembly belongs to the unused CNC arm alternative. It is not installed in this selected head.

## Print the matching set

| Part / export stem | Change | Proposed print orientation |
|---|---|---|
| `p1-magnet-plate-integral-pillars` | Integral 10 mm and 14 mm hex pillars; Ø3.2 clearance bores; small countersunk head seat retained | Broad assembly Z−7 face down; pillars point upward |
| `p5-backplate-two-inserts-through-bolt` | Two front insert seats; rear clearance/countersink for the long through-bolt | Broad assembly Z0 face down |
| `p3-cover-left-clamp-web` | Full-depth Ø7 washer-support web, Ø3.4 bolt clearance | Outer assembly Z−22.5 face down |
| `p4-cover-right-clamp-web` | Full-depth Ø7 washer-support web, Ø3.4 bolt clearance | Outer assembly Z−25.5 face down |

Use the explicitly named **`-print-flat.stl`** files. The STEP and `-assembly.stl` files retain assembly coordinates. P1/P5 rotate 180° about X for printing; P3/P4 retain their orientation. Every print export is translated onto Z0. Inspect the slicer preview and verify the printed bores, seating faces and pillar ends before assembly.

Do not combine the integral P1 with the old unmodified lower covers: their approximately Ø3.05 holes and interrupted washer footprints were the reason for adapting P3/P4. The two cover supports fill the existing clamping web, rather than adding a thin unsupported flange below it.

## Exact geometry and hardware map

All coordinates are in the original assembly frame, in millimeters. The fastening axes are parallel to Z.

| Stack | Axis X,Y | Integral pillar | Lower cover support | Required through-bolt |
|---|---|---|---|---|
| Left P1 | 1.728227, −33.760903 | 6 mm across-flats hex, Z−20 to Z−10, Ø3.2 bore | P3: Ø7, Z−22.5 to Z−20, Ø3.4 bore | **M3×20**, 90° flat head, measured head OD ≤5.6 |
| Rear P5/P1 | 26.78, −36.45 | 6 mm across-flats hex, Z−23.5 to Z−9.5, Ø3.2 bore | P4: Ø7, Z−25.5 to Z−23.5, Ø3.4 bore | **M3×30**, same head requirement |

The pillar outer hexagons reproduce the original spacer envelopes; both have 1.4 mm nominal minimum wall between the Ø3.2 bore and a flat. No root fillet expands into the adjacent moving parts. The native model uses editable hexagonal Prism features with 30° rotation and circumradius 6/√3 mm.

The now-unused rounded hex pocket reliefs at the two pillar roots are filled to eliminate zero-width corner slits. These fills are clipped to the original plate's exterior profile, span the existing 0.5 mm left and 1.0 mm rear pocket depths, and add approximately 0.3464 mm³. The added material has no modeled neighbor overlap and remains 0.825 mm from the compound gear and 0.833 mm from the fixed gear. The bore axes and mating faces are unchanged.

For each lower end, use **one M3 washer, ID 3.2 mm, OD no more than 7 mm, thickness 0.5 mm**, and **one standard M3 hex nut, 5.5 mm across flats and 2.4 mm thick**. The new Ø7 support webs give a complete nominal footprint for a Ø7 washer. Larger/thicker washers or locknuts have not been checked. Reuse owned nuts/washers only if the measured dimensions match; this design does not establish what hardware has already arrived.

Nominal stack with a 5.6 mm, 90° head:

- **Left:** head top Z−7.1; bolt tip Z−27.1. Washer Z−23 to Z−22.5; nut Z−25.4 to Z−23. The bolt projects **1.7 mm** beyond the nut.
- **Rear:** head top Z−0.3; bolt tip Z−30.3. Washer Z−26 to Z−25.5; nut Z−28.4 to Z−26. The bolt projects **1.9 mm** beyond the nut.

Countersunk bolt length includes the head. Ensure the threaded portion covers the entire nut and confirm actual projection after assembly; actual head profile and printed seating tolerances affect these values. The upper head must remain recessed, especially next to the motor. Fit the upper bolts before surrounding components obstruct access, then hold the lower nuts while tightening. Do not force the printed pillars to shorten to compensate for a mismatched stack.

A primary supplier catalogue lists DIN 965 M3×20 and M3×30 with a 5.6 mm head diameter and 1.65 mm head height: [Würth catalogue, printed page 215](https://www.wuerth.ee/kataloogom/wuerth_tootekataloog/219/). This is dimensional/availability evidence, not a purchase, stock or price claim. Do not substitute a generic M3 socket countersunk screw without checking its head; some M3 countersunk standards are larger than these pockets permit.

## Inserts remain only at the two front P5 locations

Within these four mounting parts, the purchased M3 inserts (5 mm OD ×4 mm long) are used only at X2.45/Y3 and X37.45/Y3. Each boss is Ø10, spans Z−5 to Z0, and has an open-ended Ø4.6 bore selected by the user after the `4p6` coupon comparison. Insert from Z0 toward negative Z. The 5 mm support length includes 1 mm beyond the nominal insert. The user reported easy screw travel after heat-setting and cooling; no torque/pullout, repeat-coupon or thermal-performance result has been reported. See [insert results](insert-coupon-guidance.md).

P1 and the rear P5/P1 stack do not take heat-set inserts. Their gear/arm clearances are why through-fastening is used instead.

## What has been checked

- The independent CAD build produces four valid single solids, including P1 as one connected body with both pillars.
- The new cover webs, nominal shafts, washers and nuts have no positive-volume collision with retained modeled components. Unused CNC arm hardware and the two replaced spacers/screws are excluded.
- Tight static clearances remain at the rear: **0.33 mm** between the Ø7 support/washer envelope and the hotend holder, **0.82 mm** for the conservative nut envelope, and **0.594 mm** for a Ø7×12 mm nut-driver approach. A larger driver or a different holder position needs a new check.
- The P5 front bosses retain approximately **0.40 mm** clearance to the MGN12H model. Check the actual print and rail block.
- The P1 countersink still approaches a source edge only 2.86–2.87 mm from its axis. Its Ø5.8 mouth has a small interrupted upper lip. The recessed Ø5.6 nominal head has circumferential conical seating material, but the narrow upper edge is not a demonstrated strength margin.

The final native reopen/STEP correspondence and mesh reports are separate generated artifacts. [insert-bore-4p6-validation.json](insert-bore-4p6-validation.json) is the authoritative record for the selected 4.6 mm revision and supersedes affected earlier geometry checks. These digital checks do not establish hardware performance; the physical sleeve-coupon evidence is recorded separately above.

## Prototype limits

A through-bolt clamps the printed pillar in compression but does not establish its long-term resistance to creep, cracking or lateral loading. The original thin plate webs remain, and this change does not qualify the entire CNC-derived head for printing. Test actual material, layer bonding, seating, clamping, chamber temperature exposure and tool-change motion before use. No clamp torque, service life, TAP load capacity or dynamic stiffness has been validated.

`BuildIntegralPillars.FCMacro` builds the complete variant from the four original P1/P3/P4/P5 STEP files in `source/`, preserving them as references. New pillars, supports, bores and countersinks remain native editable features. `CxChanger6_11IntegralPillars.FCStd` is the resulting model.
