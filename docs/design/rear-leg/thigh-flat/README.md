# Thigh option 3 — one piece, tapered, printed on the cup-floor plane (owner, 2026-09-19)

**Adopted the same day as production `thigh` v2 and `shank` v2** with a rounding pass and
DEC-60's hip spacing (which makes the shank's flush face fall out of the geometry); see the
revision log in `cad-integrated-design.md` and `part-design-review.md`. **Slice the production
exports**, `hardware/build/stl/thigh_{left,right}.stl` and `shank_{left,right}.stl` (v2, already
in their print orientations), not the study STLs named below. What follows is the study as it
was reviewed.

The owner's choice after seeing [options 1 and 2](../thigh-options/README.md) in the
viewer: keep the DEC-58 thigh as **one print**, take option 2's body form (the
idler-side cheek thickened out to the cup-floor plane so cheek and cup floor share
the bed), keep the drive-side cheek in the same part, and replace the step from the
thick cheek to the idler pad with **one flat taper along the owner's red line**
(marked on a viewer screenshot of the option 2 body). Print it on that plane with
**tree (organic) support** under the drive-side cheek and both pads; the owner knows
from SO-ARM101 that tree support works on this printer.

Geometry: `links.rear_thigh_flat`, spec `option_thigh_flat`, parameter
`THIGH_CHAMFER_Z` (27.5 mm). The taper is tangent to the idler pad's outer top edge
and to the join's outer face and reaches the cheek's outer face 27.5 mm down the
link, so pad, join and cheek read as one surface. Volume 46.2 cm³ (+4.7 on DEC-58).
Joint centres, pads, cup, knee clocking, window, the 45° root mount and the
straight servo insertion are unchanged. Both legs use it in the rear-leg viewer
(`uv run python -m koala_hardware.rear_leg_review --thigh-flat`).

Print orientation `Rot(X=-90)`: bed contact 1986 mm², height 73 mm, geometry
screen ≈57 cm³ of support ([screen](../thigh-options/print-orientations.png),
bottom row); tree support will use less and is the owner's call. The taper face
itself is a 67° overhang on the bed side. STLs in the print orientation:
`hardware/build/rear-leg-review/thigh_flat_{left,right}.stl` (SHA-256 a3ba9056 R,
7b69bf15 L, 2026-09-19 export). **Slicing waits for the printer**: plate 1 (root
sockets) is printing and nothing is sliced on printhub during a print
(3d-printing rule 1). Slice one part at a time with the Flathub 2.9.6 slicer
(organic support; its `--merge` crashes, single parts are fine) and the
`petg_fig_tree`-style organic settings plus koala's 4 perimeters / 30 % gyroid or
grid — settings to be fixed when sliced and recorded in `test-log.md`.

## Shank: motor moved inboard 2.25 mm (owner, 2026-09-19)

The DEC-58 shank prints on its outer face, but that face has a 2.25 mm step:
the motor-mount face stands proud of the drive fork's outer face, so the fork
pads sit in a recess. The owner asked for the motors to move inboard by that
step. `SHANK_MOTOR_INSET` (2.25, derived) does that in `links.motor_shank` and
`motor_face`; spec `option_shank_flush`. The outer face is now one plane:
bed contact 1821 → 2612 mm², overhang 2241 → 1457 mm², height 51 → 49 mm,
volume 36.5 cm³ (the outer step and its R2 return disappear). STLs:
`hardware/build/rear-leg-review/shank_flush_{left,right}.stl` (SHA-256 7288b0da R,
505c949a L). **Consequences:** the bought motor stack moves with the face, so the
rear wheel track narrows from **220 to 215.5 mm** and the neutral motor end gap
from 36 to 31.5 mm; the inward-roll stop is motor against motor, so it moves
too: **−5.5° → −4.5° in quadruped and −5° → −4.25° upright** (review of 2026-09-19 with the flush shank on both legs; every other check unchanged and passing, `flush_motor_insertion_*` and `flush_motor_driver_*` in `clearance.json` at 0). The main assembly keeps 220 mm
until the owner adopts this; the review carries it on both legs with the moved
motors, hubs, wheels and screw heads.

## Checks

Run 2026-09-19, both legs option 3, all passing: roll −30..30° every degree
against the carrier and B's cases; knee 0..120° every degree against the shank;
horn bores, heads and drivers on both pads; knee ear access; straight C insertion
(0/5/15/25/50 mm); motor insertion; all 16 assembly samples clear; every viewer
endpoint and both combined samples clear in solid CAD (`viewer-endpoints.json`,
`all_passed: true`). Sampled travel identical to the DEC-58 rear-leg viewer on
every axis in both poses except inward roll, which the moved motors reduce by 1° and 0.75° (above). Screenshots (with the flush shank): [quadruped](viewer-quadruped.png) ·
[upright](viewer-upright.png) · [parts tab](viewer-parts.png). These are CAD
clearances, not walking limits; nothing is sliced or printed.
