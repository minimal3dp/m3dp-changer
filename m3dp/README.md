# M3DP Changer — build sources and documentation

This directory contains the Minimal3DP adaptation for a six-tool Voron 2.4r2 350.
It includes work derived from CxChanger and other credited projects; retain the
licenses and source-provenance records with the CAD and configurations.

Start with the [project overview](../README.md), [print set](../stl/README.md),
and [illustrated B1 assembly guide](cad/printed-6.11/assembly-guide/README.md).
The project is a prototype undergoing assembly and automatic tool-change validation.

## Branches and remotes

| Name | Purpose |
|---|---|
| `origin` | [minimal3dp/m3dp-changer](https://github.com/minimal3dp/m3dp-changer), the active project repository |
| `main` | M3DP Changer development and documented build state |
| `upstream` | [cx330-TXY/CxChanger](https://github.com/cx330-TXY/CxChanger), the original project; fetch only, with pushing disabled |
| `upstream-*` tags | Historical upstream snapshots retained for comparison |

The former `main`-as-upstream-mirror / `m3dp`-as-build-branch workflow is retired.
Make project changes on branches based on this repository's `main`.

## Review upstream changes

Run `m3dp/tools/sync-upstream.sh` from the repository to fetch the upstream `main`
reference and report commits not yet in our `main`. Despite its retained filename,
the script does **not** merge, switch branches, push, or move tags. The former
`--no-merge` option remains accepted for existing commands.

The `upstream-watch` GitHub Action is manual (`workflow_dispatch`) and places the
same report in its run summary. It has read-only repository permission and does
not open issues or update branches.

Review useful upstream changes individually on a development branch. Check their
effect on the adapted geometry, configuration and instructions, then record any
adopted changes in [UPSTREAM-CHANGELOG.md](UPSTREAM-CHANGELOG.md). Keep upstream
credit and provenance when incorporating changes.

## Folder map

- `cad/` — source references, editable models, generators and validation records;
  [CAD layout](cad/README.md) distinguishes current models from source references.
- `bom/` — [BOM notes](bom/README.md). The linked Google Sheet is the working BOM;
  `CxChanger_BOM_6tool.xlsx` retains its original filename as a 2026-09-30 snapshot.
- `build-log/` — dated build notes (copy `_template.md`).
- `klipper/` — [six-tool configuration and commissioning instructions](klipper/README.md).
- `voron/` — retained printer configuration references and credited macro sources.
- `tools/` — upstream review and STEP translation utilities.
- `UPSTREAM-CHANGELOG.md` — historical upstream changes and their build impact.

Existing STL, native CAD and Klipper filenames are retained so print records,
validation receipts and configuration includes continue to match.
