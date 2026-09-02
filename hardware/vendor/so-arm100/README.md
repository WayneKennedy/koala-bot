# Vendor CAD — SO-ARM100 (third-party)

STEP files from [TheRobotStudio/SO-ARM100](https://github.com/TheRobotStudio/SO-ARM100),
licensed **Apache-2.0** (text in [`../../../LICENSES/Apache-2.0.txt`](../../../LICENSES/Apache-2.0.txt)),
redistributed here unmodified per DEC-21 (SO-ARM-compatible servo mounting).

| File | What | Use |
|------|------|-----|
| `STS3215_03a.step` | Feetech STS3215 servo model | measured reference for `params.py` [STEP] constants and pocket geometry |
| `Rotation_Pitch_08i.step` | SO-ARM100 joint bracket | dimensional reference for bracket-style joints — **see the revision caveat below** |

## Revision caveat (DEC-21, checked 2026-09-02)

TheRobotStudio now **deprecates SO-100 in favour of SO-101**. The repo kept its
original name, so `SO-ARM100` in the URL above is the *repository*, not the
revision — it hosts both designs.

**Which revision these two files came from was never recorded.** They were
vendored in `1c1b65a` (2026-09-01) with attribution but no upstream revision or
commit, and the filenames do not say. What that means for each:

- **`STS3215_03a.step` is unaffected either way.** SO-101 uses the same servo —
  the 100→101 changes were wiring routing, assembly, and *leader*-arm gear ratios,
  none of which touch the servo body. Every `[STEP]` constant in `params.py`
  stands regardless of which revision this came from.
- **`Rotation_Pitch_08i.step` is unverified.** Neither its source revision nor
  whether bracket geometry changed across 100→101 has been checked. It stays valid
  as the reference for the joints already designed against it; **re-check it
  against current SO-101 CAD before trusting it for a new joint** — and record the
  upstream revision when you do.
