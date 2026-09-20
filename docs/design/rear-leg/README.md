# Production rear-leg review — 2026-09-19

This review shows **thigh v3, shank v2 and the complete torso frame v5** with
DEC-61's 45° rear pitch sockets and the retained hip carriers. It uses the same
production geometry as the main assembly. Front limbs and shoulder cassettes,
neck envelopes, electronics, cables and guards are omitted from this rear-only
viewer.

[Live review over Tailscale](https://blake.tail13a0c0.ts.net:8443/rear-leg/) ·
[Quadruped view](rear-leg-quadruped.png) · [Upright view](rear-leg-upright.png) ·
[30° outward roll](rear-leg-roll-30.png) · [Thigh v3](rear-leg-thigh-v3.png) ·
[Structural sections](sections.png).

## Geometry and manufacture

The **85 mm thigh**, **90 mm shank**, **220 mm neutral rear track** and both
bought ankle drives are retained.

- **Thigh v3 — `unknown` printable:** the stepped yoke, R6.3 fork roots and
  knee case clocked 90° about its unchanged shaft remain. The idler-side cheek
  reaches the cup-floor plane through one flat taper. R2 outer rounding and
  R1.5 cup rounding now accumulate correctly: later successful fillet groups
  no longer restore earlier sharp edges. Horn seats and driver paths remain
  intact. Print on the cup-floor plane with accessible tree support beneath
  the drive-side cheek and pads. Current left/right slices have zero diagnostics;
  inspected layers retain access for support removal. Physical removal and
  loaded testing are still required.
- **Shank v2 — `assumed` printable:** the extended open knee fork, R6.3 fork
  roots and R5 motor-support roots remain. Its motor-mount outer face and
  drive-fork outer face share one print plane. Fit the motor axially from
  inboard and install all six face screws before the hub and wheel. Support
  beneath the idler fork and motor-bore roof remains to be reviewed physically.

Both revisions are **unprinted**. Thigh v3 has hash-matched
[slice records](../front-redesign/slices.json) and inspected
[left](../front-redesign/thigh_left-layers.png) /
[right](../front-redesign/thigh_right-layers.png) layers. Shank v2 has
[earlier recorded bed-only organic slices (OQ-22)](../../open-questions.md)
matching the current STL hash prefixes; check its unsupported motor-bore roof
for sag when printed.
The separately recorded
[root socket v1 print](../../test-log.md) does not establish their fit or strength.
[Current exported STL hashes, dimensions and surface metrics](manufacturing.json)
record watertight, positive-volume meshes in their declared print orientations;
these metrics are not a slicing or physical-print result.

[Thigh right STEP](thigh-right.step) · [Thigh left STEP](thigh-left.step) ·
[Shank right STEP](shank-right.step) · [Shank left STEP](shank-left.step).
These part exports are already on the bed.
[Quadruped assembly STEP](rear-leg-quadruped.step) and
[upright assembly STEP](rear-leg-upright.step) contain only project geometry.
The viewer distributes measured case/horn envelopes; the local vendor servo
STEP is used for independent checks and is not redistributed.

## Clearance evidence

[Solid-CAD checks, part versions and source hashes](clearance.json) record:

- **61 local thigh-roll samples, −30° to +30° at 1°:** thigh against its carrier
  and both imported and conservative measured B case references.
- **121 local knee-flexion samples, 0° to 120° at 1°:** shank against the thigh
  and both C case references.
- Horn bores, head/washer pockets and straight driver approaches; C's ear
  fixings, cable corridor and sampled case-insertion positions; axial motor
  insertion and all six motor-face driver paths.
- Broader rear-assembly samples with both legs, motors, wheels, nominal
  hardware and the actual torso. Each sample records its own collisions;
  local ranges do not establish whole-assembly travel.

Of the sixteen exploratory assembly samples, fifteen clear. Quadruped hip
pitch −45° intersects the torso at both thighs (903.890 mm³ per side); the
viewer limits that direction to **−28.25°**. The colliding exploratory pose is
outside the accepted viewer range.

The [viewer limits](viewer-limits.json) use 0.25° mesh samples with a 2° reserve
before the first obstruction. Hidden parts and the opposite leg remain
obstacles. [Independent endpoint checks](viewer-endpoints.json) check its twelve
initial bounds and four combined configurations against solid CAD with imported
servo cases. [Browser checks](browser.json) cover both cached poses, motion,
current part versions and printability tags.

Any ±180° bound is the search ceiling, not a confirmed physical stop. Ground
contact, omitted front/neck/electronics components, cables, physical indexing,
tolerances and loaded transitions remain outside this review. Use the main
viewer when checking the complete modelled chassis.

## Earlier studies and reproduction

The [orientation study](thigh-orientation-study.png),
[frame-versus-bolted-cheek comparison](thigh-options/README.md) and
[one-piece tapered-thigh study](thigh-flat/README.md) are historical evidence.
Their archived files remain unchanged; the production viewer displays the
current rounded thigh v3. The earlier
[socket-angle comparison](../carrier-orientation/README.md) records the origin
of the accepted 45° mount.

From `hardware/`:

```sh
uv run python -m koala_hardware.export
uv run python -m koala_hardware.rear_leg_review
```

The review command refreshes `hardware/build/viewer/rear-leg/`, clearance and
endpoint records, project STEP exports, native sections and metrics for the
preceding main-export STLs. Browser screenshots and `browser.json` are captured
with `uv run --with playwright python tests/rear_viewer_smoke.py` after the viewer
is served. Set `VIEWER_URL` and `PLAYWRIGHT_CHROMIUM` for another server or local
browser executable. Do not use `--thigh-options` or
`--thigh-flat` when refreshing production evidence.
