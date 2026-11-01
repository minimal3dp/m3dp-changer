# Independent audit: proposed integral P1 pillars

Status: integral pillars with full-thickness cover clamp webs selected as primary; native CAD validation and physical testing remain separate checks. The checked metal-spacer version remains the fallback. No CAD was edited by this audit.

## Proposed arrangement

Both original post envelopes attach to P1, rather than adding a bridge through the gap from P5:

| Joint | Axis in source assembly | Pillar Z extent | Top fastener |
|---|---|---|---|
| P1 / source post 52 | X1.72822729, Y−33.76090259 | −20 to −10 mm | M3×20 countersunk, 90°, actual head ≤5.6 mm; top at Z−7.1 |
| Rear / source post 53 | X26.78, Y−36.45 | −23.5 to −9.5 mm | M3×30 countersunk, 90°, actual head ≤5.6 mm; top at Z−0.3 |

Retain the original 6 mm across-flats outer envelopes, but provide clearance bores rather than printed threads. Each long metal bolt passes through the pillar and cover to a metal washer and nut. Final union, bore continuity and attachment to P1 are the CAD agent's checks.

Matching P3/P4 covers now receive Ø7 mm support through the existing clamp web and Ø3.4 mm clearance bores. P3 support: Z−22.5 to −20 (2.5 mm); P4 support: Z−25.5 to −23.5 (2 mm). Original mating and lower bearing faces stay fixed. The lower washers are Ø7/ID3.2 ×0.5 mm, immediately below the original cover face. M3 nuts are modeled 5.5 mm across flats ×2.4 mm thick, ending at Z−25.4 and Z−28.4. Nominal bolt tips end at −27.1 and −30.3, leaving 1.7 and 1.9 mm beyond the nuts. Chamfers, thread runout, screw tolerances and actual head seating remain physical checks; sufficient threaded length must reach each nut.

## Independent clearance results — full-thickness cover clamp webs

The source assembly was checked with posts 52/53 and old screws 56/58 removed. The adapted P1/P5 bores were excluded from the shank comparison because this audit loads their original shapes. Own-cover contact is excluded for the added pad; the CAD agent must validate the final pad-to-cover union and bore continuity.

- Ø7 mm support through the existing clamp-web thickness: no retained-part volumetric collision; rear hotend-holder clearance **0.330 mm**.
- Ø7/ID3.2 ×0.5 mm washers immediately below pads: no volumetric collision; rear hotend-holder clearance **0.330 mm**.
- M3 nut conservative cylinders (diameter 5.5/cos30°): no collision; rear hotend-holder clearance 0.820 mm. These enclose every angular orientation of the ideal hex nut.
- Ø7 mm socket approach, 12 mm below each washer: no collision; rear hotend-holder clearance 0.594 mm. This does not guarantee that every commercial nut driver or handle fits.
- Nominal Ø3 mm bolt shafts: no retained-part collision. Original cover bores were Ø3.05 mm; the proposed Ø3.4 mm holes must be verified in the final native CAD and actual prints.

Evidence: `integral-pillar-fullweb-cover-audit.json` and `audit_fullweb_cover_fasteners.py`. The separate 0.6 mm underside-flange proposal in `integral-pillar-padded-cover-audit.json` was superseded. The original fastener positions were retained in this full-web design.

## Support and print limitations

Before the cover revision, the lower covers did not support the entire outer washer circumference. At a plane 0.01 mm inside the cover's bearing face, sampled material is complete around P1 at radius 2.5 mm and rear at radius 2.0 mm. Larger sampled rings intersect the existing outside edge/opening. This also affects the original screw-head bearing region. The full-thickness supports provide a nominal full bearing face for the modeled washers without a thin extra flange. Their connection to the rest of the cover and the resulting clamp-load capacity are still untested; a valid solid and collision test do not establish strength.

Do not solve a weak seat by increasing tightening torque. Verify that the actual cover, pillar and plate seat squarely without bending, layer separation or creep, and that the nuts remain secure. The CAD does not establish a safe torque, preload or sustained chamber-temperature rating. Retain the metal-spacer fallback if printed-pillar load testing is unsatisfactory.

Evidence: `cover-washer-support.json`. Angular sampling is 1°; this is a material-presence check, not a stress analysis.

## Stock reconciliation

The order PDF shows only M3×16 DIN 7991 countersunk screws, not the proposed M3×20/30 small-head through-bolts. The saved BOM records 55 M3 nuts and 100 small washers; those entries are absent from the PDF, so locate the packs before buying. Nuts must be the actual measured thickness used in the stack; nylock or other taller nuts change the required length.

M3 DIN 965 screws with Ø5.6 mm heads are documented in 20 and 30 mm lengths by [Würth's manufacturer catalogue](https://www.wuerth.ee/kataloogom/wuerth_tootekataloog/219/). This establishes a possible dimensional family, not current local stock, a price or a purchase. Confirm the complete head profile, drive access and threaded length for the actual selected screws.

Do not buy the two M3 metal standoffs for the selected primary version. Use two long through-bolts plus two suitable nuts/washers, rather than the previous four separate top/bottom screws and two metal standoffs. The other source M4 10 mm post belongs to the unselected CNC arm alternative and is omitted with that arm. Both metal posts installed in the selected printed-arm head are replaced by the integral pillars.
