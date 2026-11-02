# CAD layout

Start with [printed-6.11](printed-6.11/README.md) for the current printed mechanism, Voron integration, generators, STEP exports and validation records. Use the repository's [STL guide](../../stl/README.md) to select prints.

| Location | Purpose |
|---|---|
| `printed-6.11/` | Current printed adaptation and assembly guide |
| `printed-6.11/source/` | Embedded source geometry used by the adaptation generators |
| `printed-6.11/voron-integration/` | Dock, rail, detector, TAP and cooling adaptations, with their required source/reference files |
| `printed-6.11/reference-only/` | Superseded designs retained for comparison; excluded from the active print set |
| `printhead-6.11-corrected-EN.STEP` | Full original assembly with English names, retained for part identification and assembly-guide provenance |
| `m3dp_cnc_6*.step`, `dock-6.11-EN.STEP` and name maps | Original translated geometry, historical measurements and generator fallback inputs; not the current print set |

The [hardware inventory](printhead-6.11-hardware.md) and [CNC conversion notes](printing-cnc-parts.md) explain the source design. The printed adaptation's joint-specific instructions take precedence when choosing hardware for M3DP Changer.

The English assembly ZIP duplicated the expanded STEP and was removed. Older 5.1/5.5 panel exports were also removed; recovery is documented in the [repository layout](../../docs/REPOSITORY-LAYOUT.md). Source-provenance and validation records retain their original paths and checksums as historical evidence.
