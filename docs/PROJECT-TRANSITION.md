# Transition to M3DP Changer

Date: 2026-11-01

M3DP Changer is an independently maintained derivative of [CxChanger](https://github.com/cx330-TXY/CxChanger), published at [minimal3dp/m3dp-changer](https://github.com/minimal3dp/m3dp-changer). The project is at the prototype assembly-validation stage; the name change does not establish physical or firmware qualification.

## History and provenance

The transition joins two existing histories in a merge:

- `9c964d3`: the previous `minimal3dp/CxChanger` build branch (`m3dp`), including its CxChanger ancestry.
- `1bf18a2`: the initial commit of the new `minimal3dp/m3dp-changer` repository.

The existing `upstream-2026-09-29` tag retains the upstream snapshot at `f5e88ce87f0204d034d888ffd2aa6d259816f5d3`. The migration also captures the reviewed, previously uncommitted CAD, print files, configuration, tests and assembly-guide deliverables from the build workspace.

The original CxChanger checkout is left unchanged. Its root README is preserved in [README-CxChanger-upstream.md](../README-CxChanger-upstream.md). Existing licenses, source-provenance records and reference attributions remain with the files they describe.

## Repository policy

`main` now represents the M3DP Changer build. It is no longer a pristine mirror of upstream CxChanger. The `upstream` remote is a fetch-only reference; upstream changes are reviewed and adopted selectively. The retained `sync-upstream.sh` entry point and GitHub workflow report changes for review rather than merging or pushing them into this project's branches.

The active `m3dp/`, `stl/` and `output/pdf/` paths are retained during this transition. In particular, STL names, `cxchanger.cfg`, `CX_*` macro names and the existing assembly-PDF filename remain compatible with the documented print and firmware workflow. Historical CxChanger names inside CAD documents and provenance records identify the source or saved artifact; they are not instructions to use the old repository.

## Included build material

- Native CAD, generator scripts/macros, source references, STEP/STL exports and geometry-validation records.
- The active STL set, labeled reference-only parts, coupons and physical fit records.
- The illustrated B1 assembly guide, CAD illustrations and printable PDF.
- Klipper commissioning examples, build-specific macros, wiring notes and offline regression tests.
- Four Voron include dependencies: `mainsail.cfg`, `KNOMI.cfg`, `stealthburner_leds.cfg` and `klipper_backup.cfg`. See the [snapshot notes](../m3dp/voron/README.md).

Temporary PDF renders, caches, local tool state, and redundant dated printer backups are excluded from the new repository. Personal host/service configuration and the original live-printer snapshot are retained only in the old local workspace. The inactive optional macro-library checkout is not required by the commissioning template and is not included.

## Migration verification

- All 157 CAD/mesh files (59 STEP, 17 FCStd, 63 STL and 18 BREP), 20 configuration files and four license files match the original workspace byte for byte. The three spreadsheets and two source archives are also unchanged.
- Two FreeCAD macros now resolve their source paths relative to the project instead of the old checkout's absolute path. Geometry and print filenames are unchanged.
- The ten-page assembly PDF and its cover preview were rebuilt with M3DP Changer branding; the cover was visually checked. Existing CAD illustrations are unchanged.
- The offline Klipper suite passed with **110 passed and six expected failures** against Klipper `7f822f3a5c27743b3e49a8e0d7b9d81bc3176f17`, using Python 3.13.18, pytest 9.1.1 and Jinja2 3.1.6. The expected failures document unchanged upstream defects; this is not a physical printer test.
- All 64 local Markdown links in the reviewed active guides resolve. The upstream review script and workflow shell passed syntax checks.

Existing CAD audit files and release checksum manifests are preserved as historical records of the artifacts they originally tested. Documentation, path-resolution edits and the rebranded PDF can differ from those earlier checksums; the migration does not claim to rerun geometric or physical qualification.

## Continued build work

The B1 head batch is printed and awaits inspection and dry assembly. Front-gantry mounted fit, saddle clamping and the remaining integration checks are still open. Continue from the [STL progress record](../stl/README.md) and [illustrated assembly guide](../m3dp/cad/printed-6.11/assembly-guide/README.md); preserve their distinction between completed fit tests and untested full operation.
