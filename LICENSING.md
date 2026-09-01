# Licensing

koala-bot is a mixed hardware / software / documentation project and uses a
**tri-licence**, standard for open-source hardware:

| Area | Covers | Licence | SPDX |
|------|--------|---------|------|
| **Hardware** | CAD, mechanical designs, PCB, printable parts (`hardware/`) | CERN Open Hardware Licence v2 – Strongly Reciprocal | `CERN-OHL-S-2.0` |
| **Software** | Firmware, host software, tooling (`firmware/`, `software/`) | MIT | `MIT` |
| **Docs & media** | Documentation, diagrams, build guides, models-as-media (`docs/`) | Creative Commons Attribution-ShareAlike 4.0 | `CC-BY-SA-4.0` |

**Exception:** `hardware/vendor/` redistributes third-party reference CAD under its
own licence (**Apache-2.0**, from SO-ARM100) — see that directory's README.

Each source file SHOULD carry an `SPDX-License-Identifier:` header naming its licence.

All three full licence texts are included verbatim in `LICENSES/` (fetched from their canonical sources).
