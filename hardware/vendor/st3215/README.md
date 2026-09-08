# Vendor CAD — Feetech STS3215 servo (third-party)

`STS3215_c.step` — a FreeCAD-authored model of the STS3215 with both horns,
case screws, the two Molex connectors and the label (STEP header: FreeCAD,
Open CASCADE 7.8, 2026-06-08; part labels `Middle`/`Top`/`Bottom` for the case
halves, `Freetech_sts3215` for the label plate). Supplied by the maintainer on
2026-09-08 from `~/Code/ST3215-CAD` on ivory. **Author and licence: not yet
recorded — see below.** `sts3215_view2.jpg` is one of the renders that came
with it.

## Why it is here

It is the first servo model whose *shape* matches the physical ST3215: the
centred raised pads that the printed pocket grips, the ear plane, the recessed
connector bay on the Back, the seat pads and the Top-end step are all present
and in the right places. `koala_hardware.servo_iface.case_model()` loads its
three case solids as the collision/clearance reference for every joint.

## What is NOT taken from it

Its horn stack is wrong against calipers, so the horns, idler, boss and screw
head in the reference come from measured constants in `params.py`, not from
this file. Nothing about retention or pockets derives from it either: pockets
come from the SO-101 printed parts (`docs/soarm-joint-pattern.md`).

## Model against calipers (2026-09-08, cheap calipers ±0.3)

Servo-face words per `docs/soarm-joint-pattern.md`: Front = drive horn, Back =
idler and connectors, Bottom = the end it stands on. Heights from the Bottom.

| Feature | This model | Measured | Verdict |
|---|---|---|---|
| Case length | 45.22 | 45.4 (spec 45.23) | ok |
| Output axis from the Top | 10.11 | 10.2 | ok |
| Side to Side | 24.72 | 24.7 | ok |
| Widest faces, Front ↔ Back | 34.7–35.0 | 34.8 | ok |
| Ear faces (M2 holes) | 32.0 | 31.8 | ok |
| Horn / idler seats | 29.4 | 28.8 | 0.6 thick, conservative |
| Drive horn thickness | 4.5 | 4.3–4.5 | ok |
| Idler thickness | 3.35 | 3.1 | 0.25 thick |
| **Clevis span, horn face to idler face** | **37.25** | **36.4** | **wrong by 0.85 — not used** |
| Back pad, width / height band | 17.9 / 5.5–18.5 | 18.5 / 5.3–18.8 | ok |
| Connector bay, height band | 18.7–23.6 | 18.8–24.5 | ok |
| Front case screws (model) | at 2.4 and 42.2, Z ±10 | printed parts use 5.8 on the Front | differs — the model shows case-assembly screws, not the SO-101 mounting holes |

## Licence

Unknown at the time of vendoring. The repository's own hardware licence
(CERN-OHL-S-2.0, `../../../LICENSING.md`) does not cover third-party files in
`vendor/`; this file must not be redistributed under it. **Record the source
URL and licence here before the repository is published or this file is
pushed.**
