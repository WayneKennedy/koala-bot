# Vendor CAD — SO-ARM100 (third-party)

STEP files from [TheRobotStudio/SO-ARM100](https://github.com/TheRobotStudio/SO-ARM100),
licensed **Apache-2.0** (text in [`../../../LICENSES/Apache-2.0.txt`](../../../LICENSES/Apache-2.0.txt)),
redistributed here unmodified per DEC-21 (SO-ARM-compatible servo mounting).

**Provenance (verified 2026-09-02):** both files are byte-identical (sha256) to
`STEP/SO100/` upstream at commit
[`7629d2a`](https://github.com/TheRobotStudio/SO-ARM100/tree/7629d2ad9853d10fb903093a33ef6114099d97e5).

| File | What | Use |
|------|------|-----|
| `STS3215_03a.step` | Feetech STS3215 servo model | measured reference for `params.py` [STEP] constants and pocket geometry |
| `Rotation_Pitch_08i.step` | SO-ARM100 joint bracket | dimensional reference only — nothing in `params.py` derives from it |

## SO-100 vs SO-101 (checked 2026-09-02)

Upstream deprecates **SO-100** in favour of **SO-101**. The repo kept its original
name, so `SO-ARM100` in the URL above is the *repository*, not the revision — it
ships both, under `STEP/SO100/` and `STEP/SO101/`.

**The servo model is revision-independent.** `STS3215_03a.step` exists only under
`STEP/SO100/`; upstream ships no SO-101 counterpart, because the servo itself did
not change (the 100->101 changes were wiring routing, assembly, and *leader*-arm
gear ratios). Every `[STEP]` constant in `params.py` derives from this file, so
all of them stand.

**The bracket did change**, and SO-101 renames it `Rotation_Pitch_SO101.step`:

| | SO-100 `08i` | SO-101 |
|---|---|---|
| Bounding box (mm) | 59.80 x **85.90** x 46.00 | 59.80 x **84.20** x 46.00 |
| Volume | 68.60 cm3 | 68.81 cm3 |
| Cylindrical faces | 89 | 63 |

A refinement rather than a redesign: X and Z are identical, volume is within
0.3 %, and **28 features coincide exactly** once a uniform **+1.7 mm Y shift** is
applied — the part lost 1.7 mm off one end in Y and was simplified, with many
small r=1.0 / r=2.0 features removed. That is consistent with upstream's stated
goal of easier assembly (no gear removal).

**Consequence for koala-bot: none.** The bracket is a reference only; no constant
is taken from it. If a future joint does take dimensions from it, pull
`STEP/SO101/Rotation_Pitch_SO101.step` and vendor that alongside instead.
