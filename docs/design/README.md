# Engineering drawings and CAD — DEC-49/50

**DEC-49/50 common carriers and asymmetric sockets:** [SO-101 templates and comparison images](so101/README.md)
and [part-by-part critique and printability tags](../part-design-review.md).
[Front-carrier flat-back comparison](front-carrier/comparison.png) ·
[Study notes and STEP](front-carrier/README.md). The overall layout below
is accepted; the revised details are implemented. [Slice evidence and layer
images](manufacturing/README.md) support `assumed` printability for every part.

Current assets show rear ankle drives and fixed rounded front feet.
[Design and assembly](../cad-integrated-design.md).

**Historical knee packaging study, deferred by DEC-43:**
[PNG](knee-packaging.png) · [SVG](knee-packaging.svg) ·
[Results](knee-packaging.json) · [Interpretation](../knee-drive-packaging.md).
This records the rejected knee-wheel detour and is not the current structure.

These PNGs open directly in the iPad Files app. Copies are kept in this same
repo path on blake.

| View | Quadruped | Upright |
|---|---|---|
| Dimensioned body master | [PNG](body-quadruped.png) | [PNG](body-upright.png) |
| Scalable body master | [SVG](body-quadruped.svg) | [SVG](body-upright.svg) |
| Actual structural CAD, side | [PNG](cad-quadruped-side.png) | [PNG](cad-upright-side.png) |
| Actual structural CAD, perspective | [PNG](cad-quadruped.png) | [PNG](cad-upright.png) |
| Kinematic STEP reference | [STEP](body-quadruped.step) | [STEP](body-upright.step) |

The master drawings and detailed CAD share their joint centres: 70 mm upper
arms, 75 mm forearms plus 25 mm hand extensions to Ø32 mm ball centres,
85/90 mm rear links, 150 mm torso, 450 mm upright height and 220 mm rear track.
Front ball centres are 149 mm apart and 260 mm ahead of the rear wheels in
supported stance. Only the rear Ø80 wheels are driven. Hip and shoulder
joints retain pitch → roll (DEC-41). The body-master head outline is a sizing allocation only; it is omitted from
the structural CAD and viewer because position and mounting are undecided.

[Joint coordinates](body-plan.json) · [Design and assembly](../cad-integrated-design.md) ·
[Digital validation](cad-validation.json) · [Body-layout rationale](../body-layout.md).

## Individual structural prints

These four-view images show the exported print orientation; they are not packed
plates. Left/right STL and STEP files are generated separately where needed.

| Print | Image |
|---|---|
| Independent pelvis socket | [PNG](parts/pelvis_socket_right.png) |
| Independent shoulder socket | [PNG](parts/shoulder_socket_right.png) |
| Common hip/shoulder carrier (two per hand) | [PNG](parts/root_carrier_right.png) |
| Drive/idler socket slots | [PNG](so101/socket-slot-comparison.png) |
| Thigh, 85 mm | [PNG](parts/thigh_right.png) |
| Upper arm, 70 mm | [PNG](parts/upper_arm_right.png) |
| Shank, 90 mm | [PNG](parts/shank_right.png) |
| Flat-section forearm and keyed hand end | [PNG](parts/forearm_right.png) |
| Replaceable Ø32 TPU contact | [PNG](parts/front_contact_pad.png) |
| Rigid torso frame | [PNG](parts/torso_frame.png) |
| Electronics tray | [PNG](parts/e_tray.png) |
| Two-print acceptance rig | [Saddle](parts/coupon_socket_saddle.png) · [Fork](parts/coupon_socket_fork.png) |

Full structural STEP assemblies are generated in
`hardware/build/step/koala-quadruped.step` and `koala-upright.step`; the current
part STL/STEP sets are in `hardware/build/stl/` and `hardware/build/step/`.
These build outputs also exist on blake. Original upstream reference STEPs
remain unchanged in `hardware/vendor/`; they are not koala prints.

## Regenerate

From `hardware/`:

```sh
uv run python -m koala_hardware.export
uv run python -m koala_hardware.manufacturing_slices
uv run python -m koala_hardware.assembly
uv run python -m koala_hardware.audit
uv run python -m koala_hardware.audit --fallback --nominal-only
uv run --with playwright python -m koala_hardware.body_plan --output ../docs/design --cad --png
uv run python -m koala_hardware.viewer --build
```

PNG rendering requires Playwright Chromium, or `PLAYWRIGHT_CHROMIUM` set to an
installed binary. CAD scene PNGs come from the browser regression captures;
individual print PNGs come from the exporter. No image is evidence of slicing,
physical fit, continuous collision clearance, strength or a validated rise.
