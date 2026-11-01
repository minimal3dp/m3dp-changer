# Voron integration dependency snapshot

These four files were copied from the supplied Voron configuration for the M3DP Changer commissioning template and its offline integration tests:

| File | Role |
|---|---|
| `mainsail.cfg` | Mainsail client and pause/resume definitions |
| `KNOMI.cfg` | Display status and command wrappers |
| `stealthburner_leds.cfg` | Existing LED configuration and status macros |
| `klipper_backup.cfg` | Optional configuration-backup command wrappers |

Retain the original notices and comments in these files. This folder is a selected dependency snapshot, not a complete printer configuration or a new implementation of those integrations. The original `printer.cfg`, dated printer backups, saved-variable state and host/service configuration were not published in this migration.

[../klipper/printer.cfg.example](../klipper/printer.cfg.example) includes these files by relative path. Preserve the sibling `klipper/` and `voron/` layout when deploying. Follow the [commissioning guide](../klipper/README.md); the example retains settings from the supplied machine and must be reviewed for the actual hardware.

`klipper_backup.cfg` calls an external `~/klipper-backup/script.sh` through the `gcode_shell_command` extension. The extension and script are not bundled here. Keep that include only if the backup integration is installed and intended; otherwise omit it from the deployed main configuration. Offline tests inspect the definitions without executing shell commands.

The old `macros.cfg` and optional `klipper-macros/` library are not included or enabled. The M3DP Changer macros replace the relevant print lifecycle and probing behavior; adding another macro library requires a fresh include/conflict review.
