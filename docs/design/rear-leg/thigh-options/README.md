# Thigh print-form options — 2026-09-19 review

Two ways to make the DEC-58 rear thigh printable, modelled side by side for the
owner to judge in the [rear-leg viewer](https://blake.tail13a0c0.ts.net:8443/rear-leg/)
(Tailscale; rebuilt with `uv run python -m koala_hardware.rear_leg_review --thigh-options`).
**Left leg = option 1, right leg = option 2.** Screenshots: [quadruped](viewer-quadruped.png) · [upright](viewer-upright.png) · [parts tab](viewer-parts.png). Everything else is DEC-57/58: joint
centres, 85/90 mm links, pads, cup, knee clocking, the yoke window and the
45° root mount. The main assembly, BOM and the DEC-58 exports are untouched;
`rear_leg_review` without the flag rebuilds the DEC-58 viewer.

Why: the DEC-58 thigh is a C-yoke whose parallel cheeks are 50 mm cantilevers in
every lying orientation, and its knee pocket opens toward the bed
([orientation study](../thigh-orientation-study.png), owner review 2026-09-18).
The socket cannot be centred under the bridge (the shaft fixes it) and a wedge
under the bridge would occupy the case's own space, so both options change the
knee end instead. [Print-orientation screen](print-orientations.png).

## Option 1 — one print, closed knee-end frame (left leg)

`thigh_frame`, `links.rear_thigh_frame`. A **4 mm foot** runs from the bridge down
to the cup's return plane on the drive-pad side and a **1.7 mm bar** runs along
that plane to the cup wall, 0.3 mm off the case's Side face
(`THIGH_FOOT_T`, `THIGH_BAR_CLEAR`). The part **stands on the knee socket**: both
cheeks and both pads are vertical, bed contact 1718 mm², height 110 mm. What is
left to print: one **45.9 mm span** bridged under the bridge across the empty case
space (2 mm above where the case will sit) and the horn-bore roofs. The screen
counts that span as ≈45 cm³ of support because it cannot see bridging; if the
slicer bridges it, support is near zero, otherwise it is one block open from
both X sides. Volume 44.7 cm³ (+3.2 on DEC-58).

Consequences: servo C cannot slide straight out past the foot, so it enters
**sideways (X) at its 17 mm pre-insertion offset**, 1.65 mm clear of the foot,
then slides into the pocket; checked in `clearance.json`
(`frame_C_sideways_*`). Layers lie across the cheeks' bending load. Strength,
bridging quality and support removal are unverified.

## Option 2 — two prints, bolted cheek (right leg)

`thigh_body` + `thigh_cheek`, `links.rear_thigh_split`. The drive-side cheek,
with its pad, join and the bridge end, is a **separate piece** with a **5 mm lip**
over the bridge's knee-end face. It mates on an L (cheek inner face against the
bridge end, lip on the bridge's outer face) with **two M3 into captive nuts**
entered from the window face: one along Z through the lip
(`THIGH_LIP_SCREW_Y`), one along Y through the cheek with its head counterbored
flush (`THIGH_END_SCREW_Z`, `THIGH_END_NUT_Y`). The body's idler-side cheek is
**thickened out to the cup-floor plane** so the body lies flat on that plane:
bed 2258 mm², height 67 mm, ≈10 cm³ of support (one block under the idler
pad's free part). The cheek piece lies on its outer face: bed 1013 mm², height
20 mm, ≈2.5 cm³ under the drive pad. Volumes 38.6 + 9.7 cm³.

Consequences: servo C is fitted **before** the cheek piece, so the straight
insertion path is unchanged. The drive-horn torque passes through two M3 and
the L faces: unverified. An earlier variant with a 5 mm outer lap plate
**failed the 0–120° knee check at 117°** (shank against the plate, 3.1 mm³);
the lip-only joint stays inside the DEC-58 envelope and passes. The screw
heads sit on the lip and in the counterbore only.

## Results, 2026-09-19

All checks below pass for both options in the same run. The viewer's sampled
travel is **identical to the DEC-58 rear-leg viewer** on every axis in both
poses (quadruped pitch −51..173.75°, roll −5.5..180°, knee −96.5..56.25°;
upright pitch −125.5..99.5°, roll −5..180°, knee −91.25..61.5°); the knee
stop on the right leg now names the cheek piece alongside the body. Every
endpoint and both combined samples clear in solid CAD
(`viewer-endpoints.json`, `all_passed: true`). The frame's bar needed
`THIGH_BAR_CLEAR` (0.3 mm) because a bar lying exactly on the case's Side
plane registered the reference case's ~0.05 mm oversize outside the allowed
pocket-contact zone. Viewer engine change (`mechanical_limits.js`,
`viewer.py`): a servo's exempt contact partner may now be a list, so a fork
split across two prints keeps its designed horn contact exempt; the main
viewer was rebuilt against the new engine hash with unchanged limits.

## Checks (`clearance.json`, `viewer-limits.json`, `viewer-endpoints.json`)

Local, every degree, both options and the fixings: roll −30..30 against the
carrier and B's cases; knee 0..120 against the shank. Horn bores, heads and
drivers on every pad; knee ear access; C insertion (straight for the body,
sideways then straight for the frame); motor insertion. Assembly samples and
the viewer's sampled travel with both legs, all rear hardware and the 45°
mount. These are CAD clearances, not walking limits. Nothing is sliced or
printed; both options are `unknown` printable until one is chosen and printed.
