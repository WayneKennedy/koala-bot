# hardware/

Parametric code-CAD (DEC-09: `build123d`, body-as-source-code) for the printable
parts. Licence: `CERN-OHL-S-2.0` (see [`../LICENSING.md`](../LICENSING.md));
`vendor/` contains third-party Apache-2.0 reference CAD (see its README).

## Layout

| Path | What |
|------|------|
| `src/koala_hardware/params.py` | **All dimensions** (mm), tagged by provenance (`[STEP]`/`[VENDOR]`/`[STD]`/`[VERIFY]`) |
| `src/koala_hardware/fasteners.py` | DEC-23 joint primitives (M3 insert bosses, clearance holes, registration keys) |
| `src/koala_hardware/servo_iface.py` | STS3215 pocket / horn-drive / retention geometry (measured from vendor STEP) |
| `src/koala_hardware/parts/` | Builders by subassembly; `hip_bracket` is a private integral pelvis root, not a print |
| `src/koala_hardware/printability.py` | Bed contact / overhang geometry screen, not a manufacturing proof |
| `src/koala_hardware/validation.py` | Neutral motor clearance and wheel-track datum checks |
| `src/koala_hardware/audit.py` | Sampled posed-solid and selected screw-head checks, full-depth horn-hole probes |
| `src/koala_hardware/export.py` | Build pipeline: STL + 4-view renders + **DEC-09 bed-fit + DEC-24 checks** |
| `src/koala_hardware/assembly.py` | Posed lower-body render for proportion/collision eyeballing |
| `vendor/so-arm100/` | SO-ARM100 STEP reference models (Apache-2.0) |
| `build/` | Outputs (gitignored): `stl/`, `renders/`, `manifest.txt` |

## Build

```sh
cd hardware
uv run python -m koala_hardware.export     # all parts -> build/
uv run python -m koala_hardware.export thigh   # name filter
uv run python -m koala_hardware.assembly   # assembly sanity render
uv run python -m koala_hardware.viewer     # interactive 3D viewer on :8017
uv run python -m koala_hardware.audit      # sampled mechanical regressions
uv run python -m unittest discover -s tests
```

Optional browser regression (with the viewer running):
`uv run --with playwright python tests/viewer_smoke.py`. Install Playwright's
Chromium or set `PLAYWRIGHT_CHROMIUM` to an existing compatible binary.

`koala_hardware.viewer` rebuilds `build/viewer/scene.json` from the current
CAD, copies the checked-in `viewer.html` beside it, and serves both on
`http://localhost:8017`. `--build` regenerates the data without serving,
`--serve` serves without rebuilding, `--port N` moves it. Any harness can
refresh the geometry and the browser tab picks it up on reload. It shows the
posed assembly (printed parts, bought parts, nominal servo references) and every
printed part in its declared print orientation. Click a row to isolate a part,
shift-click to hide it. **The viewer is an eyeball check on proportion and
packaging only**. Pitch and symmetric-roll sliders inspect geometry, not safe
operating limits. The Parts tab shows bed orientation, layer/load-path notes
and surface-screen metrics. All validation scope and remaining gates are in
[the DEC-29 redesign record](../docs/cad-redesign.md).

A full run also regenerates the printed-parts table in
[`../docs/bom.md`](../docs/bom.md) and prunes outputs for renamed parts. Parts
marked `handed` export **both** `_right` and `_left` STLs — mirroring in the
slicer is too easy to forget.

Measured slice figures are accepted only when their cached SHA-256 matches the
current STL. A geometry change therefore falls back to a clearly labelled
solid-volume upper bound until `koala_hardware.slice_remote` is run again.

The export **fails** if any part exceeds 200x200 mm in its declared print
orientation (DEC-09/DEC-23), or if it fails the surface geometry screen:
bed contact under 300 mm2, or overhang area over 800 mm2. On failure it prints
the better orientations it measured. It also fails on critical assembly-layout
errors that part-local checks cannot see, including overlapping neutral drive
motors or inconsistent wheel track. Printable parts must also be one connected
solid unless explicitly declared as a multi-piece coupon.

### Designing a part that passes

- **Features on one face only.** A plate with bosses up *and* structure hanging
  down needs its actual bed orientation examined. The integrated pelvis prints
  deck-top-down with its roots growing upward; no separate flange is required.
- **No closed cavity floors** — a floor becomes a bridged ceiling when the part
  is flipped. Let cavities open through.
- **Choose layer direction from the load path.** The roll/thigh cheeks print
  separately and flat, not standing as the tines of a one-piece fork.
- **When two features want different orientations, add a seam** (DEC-23) — the
  new thigh uses flat plates and compression spacers. There is no old motor-clamp seam.
- **Cap heads stand proud; never countersink printed plastic** (DEC-25). Reach
  for `fasteners.m3_counterbore` only where a proud head fouls a mating face or
  a moving part, and put that face up so the pocket prints as open air.

## Print order — coupons first

Existing `coupon_*` parts cover selected fits, not every `[VERIFY]` constant
or the new case clamp. **Print and fit-check the applicable coupons before
any structural part**, adjust the constants, regenerate. Material: PETG.

*("Coupon" is the materials-engineering term — from French *couper*, to cut —
for a small sample made alongside the real thing and tested in its place. Here:
a cheap print that answers one dimensional question before you commit filament
and hours to a structural part.)*

### Reading a coupon result

A coupon measures **the design's clearance and the printer's error together**,
so keep them apart:

- **Fit tests, not measurements.** Each coupon offers a ladder of sizes and the
  answer is *the smallest that accepts the real part* — an M3 screw, the servo,
  the 37D's face boss. Judge it by fit, not by calipers against nominal; a
  caliper reading only tells you your printer's shrinkage, which is not what
  the constant is for.
- **Calibrate the printer first.** Flow / extrusion multiplier and XY
  dimensional accuracy must be settled *before* a coupon result is folded into
  `params.py`. Otherwise the design silently absorbs one machine's error and
  every other builder inherits it.
- **Constants here are reference-printer values** (DEC-14), not universal
  truths. That is exactly why the coupons ship with the design: another builder
  re-runs them on their own machine and re-derives their own numbers.

Record what a coupon actually showed — including "no change needed" — in
[`../docs/test-log.md`](../docs/test-log.md), so the next person knows the
constant was tested rather than guessed.

## Status

Draft **v1** lower body, **not ready for structural printing or assembly**.
DEC-29 replaces the [reviewed defects](../docs/cad-review.md) with an integrated
pelvis, open bolted hip carrier and flat twin-cheek thighs. Bed-fit, full-depth
horn holes and sampled nominal collisions are checked. Physical servo/idler
fits, sliced layers, clamp retention and structural print validation remain
outstanding. See [cad-redesign.md](../docs/cad-redesign.md) before printing.
