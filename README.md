# M3DP Changer

A six-tool hotend changer for the Voron 2.4, derived from [CxChanger](https://github.com/cx330-TXY/CxChanger).

M3DP Changer is the Minimal3DP adaptation of the corrected CxChanger 6.11 mechanism for a **Voron 2.4r2 350**. It combines printed structural parts, a Chaoticlab CNC TAP V2 interface and top blower, and three paired docks on a raised 400 mm 2020 rail attached to the moving gantry. The target is a closed stock enclosure with reduced Y print area.

**Status: prototype — assembly and automatic tool-change validation in progress.** CAD and export checks are documented, but the full mechanism has not yet passed physical assembly, thermal or automatic-operation acceptance. The Klipper files are commissioning drafts and require machine-specific settings.

## Start here

| What you need | Where to find it |
|---|---|
| Current STL files, quantities and print order | [STL print guide](stl/README.md) |
| Part identification, orientation and hardware stacks | [Illustrated B1 assembly guide](m3dp/cad/printed-6.11/assembly-guide/README.md) · [Printable PDF](output/pdf/CxChanger-B1-illustrated-assembly-guide.pdf) |
| Editable CAD, STEP exports and validation records | [Printed mechanism and Voron integration](m3dp/cad/printed-6.11/README.md) |
| Electronics, wiring and commissioning | [Klipper configuration guide](m3dp/klipper/README.md) · [Wiring plan](m3dp/klipper/wiring-plan.md) |
| Offline firmware regression checks | [Test instructions](m3dp/klipper/tests/README.md) |
| Hardware and purchasing | [BOM](m3dp/bom/README.md) · [Mechanism hardware notes](m3dp/cad/printhead-6.11-hardware.md) |

## Build and validation progress

- The selected insert bore is **4.6 mm (`4p6`)**, following heat-set and cool-down coupon tests.
- The 2510 fan body and installed retainers fit; the TAP interface gauge and raised saddle's fit over the actual 2020 were also confirmed.
- The eight-piece B1 head batch has been printed: P1, P3, P4, P5, P8, the detector mount and two hotend holders.
- **Next: inspect and dry-assemble the B1 head and T0/T1 holders** using the illustrated guide. Check free gear/arm movement, hardware clearance and repeatable holder seating. The P8 gear shaft seating/retention check remains open.
- Before the full rail/dock batch, complete the front-gantry coupon's mounted fit and belt-clearance check and the saddle's M3 T-nut clamp check. Full TAP travel, detector operation, airflow, hot retention and automatic changing remain to be tested.

The [STL guide](stl/README.md) is the detailed progress and print-order record. The active six-tool set has 15 designs and 28 assembly pieces, plus nine fit coupons. Parts under `reference-only/` are excluded from that set. CAD dimensions are not calibrated printer pickup coordinates.

## Project layout and development

The canonical repository is [minimal3dp/m3dp-changer](https://github.com/minimal3dp/m3dp-changer), with `main` as the development baseline. The existing `m3dp/` paths and working STL/configuration filenames are retained so the build instructions and firmware includes remain usable.

Use [m3dp/README.md](m3dp/README.md) for the development workflow and folder map. [Project transition notes](docs/PROJECT-TRANSITION.md) explain the preserved Git history and the relationship to CxChanger. The [repository layout](docs/REPOSITORY-LAYOUT.md) separates the active build from [retained CxChanger references](reference/cxchanger/README.md). Unused upstream archives, photos and older panel/BOM copies have been removed from the working tree and remain recoverable from Git history.

## Attribution and license

The mechanism is derived from **CxChanger by cx330-TXY**. Its coupling and latch interfaces remain the basis of this build; the selected P8 arm and hotend holder are unchanged source exports. Minimal3DP adaptations include printed pillar/clamp structures, Voron mounting and cooling, paired raised docks, calibrated insert bores, and build-specific configuration and documentation.

Retain the [GPLv3 license](LICENSE), original notices, [CAD source provenance](m3dp/cad/printed-6.11/source-provenance.json), and the third-party reference attributions for [Voron rail geometry](m3dp/cad/printed-6.11/voron-integration/rail/REFERENCE-ATTRIBUTION.md) and the [TAP interface](m3dp/cad/printed-6.11/voron-integration/tap/REFERENCE-ATTRIBUTION.md). The [original CxChanger README](reference/cxchanger/README-original.md) is preserved for reference.
