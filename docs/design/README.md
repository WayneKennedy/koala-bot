# Engineering drawings and CAD

**2026-09-21 addition:** [walking first build](walking/README.md), with four
identical TPU feet and interchangeable `foot_shank` v1 rear links. The main
viewer opens in this configuration; the wheeled snapshots remain selectable.

**Current 2026-09-19 revision:** [recessed roll-first front limbs](front-redesign/README.md),
[small-servo neck provision](neck-provision.md),
[design and assembly](../cad-integrated-design.md), and
[part-by-part printability](../part-design-review.md). The torso wraps the front
A modules while retaining 150 mm hip-to-shoulder spacing. New front parts and
changed torso/thigh remain unprinted; older slices validate only matching hashes.

The [rear-leg record](rear-leg/README.md) documents DEC-57/58's origins and later
print-form studies. DEC-61's inclined rear mount is now implemented in the main
assembly. Current thigh v3 corrects rounding; shank v2 is unchanged. Earlier
[carrier-orientation alternatives](carrier-orientation/README.md) and
[front-carrier flat-back study](front-carrier/README.md) are historical, not
competing current mounts.

[SO-101 source templates and interface comparison](so101/README.md) retain the
measured construction reference. [Manufacturing records](manufacturing/README.md)
distinguish local slices from physical proof; root socket v1 is proven with its
recorded ear-hole caveat.

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
Unrolled front ball centres are now 190.23 mm apart and 260 mm ahead of the
rear wheels in supported stance. Only the rear Ø80 wheels are driven. Front
shoulders are roll → pitch; rear hips remain pitch → roll. The body-master head outline is a sizing allocation only; it is omitted from
the structural CAD and viewer because position and mounting are undecided.

[Joint coordinates](body-plan.json) · [Design and assembly](../cad-integrated-design.md) ·
[Digital validation](cad-validation.json) · [Body-layout rationale](../body-layout.md).

## Individual structural prints

Exporter PNGs show the print orientation; files ending `-views.png` show native
CAD coordinates for shape review. Current [layer plots](front-redesign/README.md#local-slicing-and-support-review)
show the chosen bed faces. Left/right STL and STEP files are generated separately.

| Print | Image |
|---|---|
| Proven root socket v1 (four physical prints) | [PNG](parts/root_socket_right.png) |
| Recessed shoulder cassette v1 | [Four views](parts/shoulder_mount-views.png) |
| Roll-first shoulder carrier v3 | [Four views](parts/shoulder_carrier-views.png) |
| Rear hip carrier v1 | [PNG](parts/hip_carrier_right.png) |
| Drive/idler socket slots | [PNG](so101/socket-slot-comparison.png) |
| Corrected thigh v3, 85 mm | [Four views](parts/thigh-views.png) |
| Upper arm v2, 70 mm | [Four views](parts/upper_arm-views.png) |
| Shank v2, 90 mm | [PNG](parts/shank_right.png) |
| Footed rear shank v1, 90 mm | [Four views](parts/foot_shank-views.png) |
| Forearm v2 and keyed hand end | [Four views](parts/forearm-views.png) |
| Replaceable Ø32 TPU contact | [PNG](parts/front_contact_pad.png) |
| Extended torso v5 | [Four views](parts/torso_frame-views.png) |
| Electronics tray | [PNG](parts/e_tray.png) |
| Two-print acceptance rig | [Saddle](parts/coupon_socket_saddle.png) · [Fork](parts/coupon_socket_fork.png) |

Full structural STEP assemblies are generated in
`hardware/build/step/koala-walking.step`, `koala-quadruped.step` and `koala-upright.step`; the current
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
