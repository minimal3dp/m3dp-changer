# M3DP Changer — printed adaptation of CxChanger 6.11 for Voron 2.4r2 350

The active build uses the corrected 6.11 mechanism with its printed P8 arm, integral P1 pillars, matching reinforced P3/P4 covers and P5 insert supports. It adds a Chaoticlab CNC TAP V2 adapter/top blower and a raised 400 mm 2020 dock rail on the moving gantry. The target is the stock closed enclosure with reduced Y print area. ASA and M3 inserts measuring 5 mm OD ×4 mm long are the selected materials/hardware.

**This is a fit-prototype release.** Native models and exports were checked; actual printer fit, airflow, stiffness, hot retention, detector operation and automatic changing still require physical acceptance.

Use the [active STL print guide](../../../stl/README.md) for quantities and coupon order. The active six-tool set contains 15 printable designs and 28 pieces, plus nine coupons. The old P2 spring support belongs to the CNC arm alternative and overlaps P8. The original rear-blower duct and 30 mm-pitch dock are reference only, not alternatives for this installation.

See [this integration update](integration-release-notes.md) and [export verification](integration-export-verification.json) for the final release scope.

## Design and assembly notes

- [Illustrated B1 assembly guide](assembly-guide/README.md): labeled CAD views, exploded layout and hardware order for the eight-piece head batch; includes the printable PDF.
- [Printed plates, integral pillars and through-bolt stacks](printing-and-assembly-notes.md).
- [Insert fitting](insert-coupon-guidance.md): the user selected the 4.6 mm nominal bore (`4p6`) after coupon heat-setting and cooling; this is not a supplier-qualified value or a retention-strength result.
- [Raised paired docks and fan retention](modular-dock-notes.md): 34 mm within-pair pitch, 38 mm between pairs; 216 mm nominal span for six tools, 221 mm including the fan-retainer ear.
- [TAP interface, top blower and duct](voron-integration/tap/README.md).
- [Rail-to-gantry supports](voron-integration/rail/front-rail-support-notes.md).
- [Upper tool/filament detector mount](voron-integration/detector/README.md).

The original latch/pin/nozzle-pad interfaces are retained. The raised rail allows those low pads to remain outside the physical bed while the front doors close. The modeled bed/door/upper-frame margins are in the integration notes. They depend on the matching head adapter and bracket geometry; do not mix intermediate versions or derive machine coordinates directly from CAD datums.

The insert coupon comparison is complete and the selected bore is 4.6 mm for the two P5 seats, three TAP-adapter seats, three fan-retainer seats per dock and matching 2510 cage coupon. The user reported that the TAP interface gauge fit passed on 2026-10-31; full TAP assembly and operation remain untested. The gantry and saddle coupons were also printed on 2026-10-31, and the saddle's fit over the actual 2020 was confirmed. **Next inspect the gantry coupon's rough fork underside and check its right-front mounting, bolt stack and belt clearance**, then check the saddle's M3 T-nut clamping and finish the remaining cage checks listed in the active STL print guide before the full assembly. Gantry fit and saddle clamping have not yet been reported. Then fit one holder and one paired dock before duplicating them. Use the four revised head plates together. Their integral pillars use M3 clearance holes and metal through-bolts/nuts, not plastic threads. The smaller countersunk head limit and washer stack remain mandatory; see the assembly notes.

**B1 progress (2026-10-31):** the user confirmed printing the eight-piece first head batch: P1/P3/P4/P5, P8, detector mount and two holders. The next head step is print inspection and dry assembly; no head/holder fit result has yet been reported. The outstanding coupon checks above still apply before the rail/dock batch. See the active STL guide for the current combined progress record.

## Editable sources and validation

`CxChanger6_11IntegralPillars.FCStd` contains the four revised head parts; `insert-fit-coupon.FCStd` contains the insert samples. The `voron-integration/` subfolders contain the new native FreeCAD projects, their generator macros, STEP/STL exports and validation records. The native trees use ordinary Part features, primitives and Boolean operations; they do not recreate the original SolidWorks sketch history.

Reopen tests for the new head, dock, rail and detector use distinct saved disk copies and exercise an editable dimension before restoring it. Export checks inspect closed single solids, mesh connectivity/winding, STEP readback and modeled assembly clearances. For the selected 4.6 mm bore revision, [insert-bore-4p6-validation.json](insert-bore-4p6-validation.json) is the authoritative validation record and supersedes affected earlier geometry checks; consult its recorded status and scope. Historical checks for unchanged parts remain applicable to those exports; superseded dock checks are isolated in `reference-only/superseded-30mm-dock/`. No valid-solid report establishes physical strength or a complete motion proof.

The selected P8 arm and hotend-holder source exports are in `unchanged-printables/`. That folder also preserves P2 and the original duct for traceability; its historical all-source export list is not the active build list. `source/` holds unchanged Cx references.

## Physical commissioning still required

Check actual TAP and gantry interfaces, screw engagement, probe travel, PTFE/fitting/cable clearance, arm movement and docking paths. Confirm the detector's state sequence and cooling performance. Establish the usable print area and station coordinates on the assembled machine; this release does not change the live printer or certify the previous 350 mm travel limits.

Warm-chamber clamp, creep and retention testing is required for the ASA plates, pillars, rail supports and tall dock hangers. The remaining thin source regions have not been globally thickened or structurally qualified. Airway cross-section and geometric clearance do not establish blower performance.

## Provenance

Cx source geometry is from [CxChanger 6.11](https://github.com/cx330-TXY/CxChanger); retain the included GPL-3.0 license and `source-provenance.json`. Rail interfaces use the [official Voron 2.4r2 CAD](https://github.com/VoronDesign/Voron-2/tree/Voron2.4/CAD) with 350 mm configurator dimensions. TAP interface measurements use the user's [unofficial Chaoticlab V2 reconstruction](https://www.printables.com/model/1853271-cnc-voron-tap-v2-unofficial-cad-reconstruction-ste/related), checked against the official V2 guide. Third-party TAP reference bodies are not embedded in the released native models.
