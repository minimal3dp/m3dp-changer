# Repository layout

The working tree is organized around the M3DP Changer build. The original CxChanger checkout and this repository's Git history remain intact.

| Folder | Contents |
|---|---|
| [`stl/`](../stl/README.md) | Printable parts, fit coupons, quantities and current print progress |
| [`m3dp/cad/`](../m3dp/cad/README.md) | Editable CAD, generators, exports, illustrations and required source geometry |
| [`m3dp/klipper/`](../m3dp/klipper/README.md) | Current commissioning templates, wiring plan and offline tests |
| [`m3dp/voron/`](../m3dp/voron/README.md) | Retained printer configuration dependencies |
| [`m3dp/bom/`](../m3dp/bom/README.md) | Working BOM link and six-tool spreadsheet snapshot |
| `m3dp/build-log/`, `m3dp/tools/`, `m3dp/refs/` | Build-note template, development utilities and reference notes |
| [`output/pdf/`](../output/pdf/) | Printable illustrated assembly guide |
| [`reference/cxchanger/`](../reference/cxchanger/README.md) | Upstream assembly documentation, diagram and original regression configurations |
| `docs/` | Repository history and organization notes |

## Cleanup on 2026-11-01

The following unused or duplicate material was removed from the current working tree:

- Root `CAD/`: original source archives; active generators use retained embedded sources and the translated assembly.
- Root `img/`: seven unreferenced photos.
- `5.5版本bom.xlsx` and `EN-translation/bom_v5.5.xlsx`: old 5.5 BOM copies.
- `拼版（5.5和5.1版本）/` and `m3dp/cad/panels-5.5-5.1-EN/`: old panel exports and translated copies.
- `EN-translation/klipper/`: unused translated configuration examples.
- `m3dp/cad/printhead-6.11-corrected-EN.zip`: exact duplicate of the retained expanded English STEP.
- `m3dp/translations/README.md`: an unused placeholder.

The two upstream READMEs and English coordinate diagram moved into `reference/cxchanger/`; the original root `klipper/` examples moved into `reference/cxchanger/klipper/`. The regression test resolver and documentation links were updated. Retained CAD, STL and configuration contents were not changed.

The cleanup removes 26 unused files, about 31.8 MiB, from the working tree. Git history still contains those files, so this is not a reduction in historical repository size. Physical print/test status is unchanged.

## Recovering historical files

The complete pre-cleanup tree is preserved in commit `06b1a171de5f6fdf35802d782ec9ee03c5c41643`. For example, from the repository root:

```sh
git show '06b1a171de5f6fdf35802d782ec9ee03c5c41643:CAD/打印头6.11修正.zip' > /tmp/cxchanger-original-printhead.zip
```

Use that commit to inspect other removed paths. Original upstream content is also retained at tag `upstream-2026-09-29`. Historical source-provenance records keep their original paths; they describe the sources used at the time rather than requiring removed files to exist in the current working tree.
