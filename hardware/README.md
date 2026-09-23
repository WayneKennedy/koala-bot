# hardware/

Parametric build123d CAD, CERN-OHL-S-2.0. Current 2026-09-19 CAD implements
recessed **roll → pitch → elbow** front limbs and **pitch → roll → knee** rear
limbs, with rear ankle drives and replaceable TPU front pads. Design, assembly,
dimensions and remaining acceptance gates:
[cad-integrated-design.md](../docs/cad-integrated-design.md).

**2026-09-21:** the first build uses four TPU feet (DEC-62). `foot_shank` v1
replaces each complete wheeled rear shank at the existing knee; the same
`front_contact_pad` v1 fits all four feet. The default viewer configuration is
`walking`; `quadruped` and `upright` retain the wheeled geometry.
[Print files, assembly and evidence](../docs/design/walking/README.md).

## Current CAD

The torso now wraps the front A volume, with a **10 mm socket-lip recess**,
removable front-access shoulder cassettes and a cap at body Z183.5; the
hip-to-shoulder axis separation remains **150 mm**. The front carrier, upper arm
and forearm apply the rear redesign's broad print planes, open forks and
accessible supports. Front B/C shafts are parallel. The main assembly carries
DEC-61's **45° rear pitch socket mount**, with rear driver corridors through the
actual torso. [Front revision and evidence](../docs/design/front-redesign/README.md).

`params.py` supplies body/interface dimensions. `servo_iface.py` implements the
measured four-ear SO-101 saddle and horn references. `parts/links.py` carries the
rear links/carriers; `parts/front.py` implements the front chain,
`parts/shoulder_mount.py` its independent cassettes, and `parts/pelvis.py` the
unchanged proven root socket. `parts/torso.py` and `parts/e_tray.py` complete the
chassis. `parts/neck_space.py` reserves small STS3032M neck-servo space and a
cartridge interface; it does not build an accepted 3-RPS mechanism or neck print.
`body_plan.py` and `assembly.py` share the declared pose geometry; front and rear
use different serial joint transforms.

Source paths above are relative to `src/koala_hardware/`. All commands below
run from `hardware/`:

```sh
uv run python -m koala_hardware.export
uv run python -m koala_hardware.assembly
uv run python -m koala_hardware.audit
uv run python -m koala_hardware.audit --fallback --nominal-only
uv run python -m unittest discover -s tests
uv run python -m koala_hardware.body_plan --output ../docs/design --cad
uv run python -m koala_hardware.viewer --build
uv run python -m koala_hardware.mjcf          # MuJoCo model -> sim/koala_walking.xml + meshes/ (--crude: capsule visuals); docs/architecture.md
```

Exports: `build/stl/`, `build/step/`, `build/renders/`, `build/manifest.txt`.
`sim/` holds the generated MuJoCo model: one visual STL per rigid body in `sim/meshes/` (2.7 MB,
committed; regenerate after any CAD change), explicit per-body inertia from the BREP, and the
assumptions in the XML header. `mjcf_check.py` loads it from any venv that has MuJoCo (not a
dependency here) and reports masses, CoM against the feet, a 3 s stand and a render.
Full assemblies are `build/step/koala-walking.step`, `koala-quadruped.step` and `koala-upright.step`.
Every handed print has explicit left/right files. Removed part outputs are
pruned. The exporter regenerates the printed and fastening blocks in
[the BOM](../docs/bom.md); never hand-edit them. Slice results count only when
their SHA-256 matches the current STL.

Every structural print must be one valid solid, export a watertight positive-volume
STL and fit the 200 mm bed in its
stated orientation. Local supports/brims are explicit under DEC-39; flagged
surface areas remain visible in the manifest/BOM and need layer inspection.
They are not a reason to reintroduce unnecessary structural seams.

`audit.py` checks the measured interface, selected screw/tool paths, motor
insertion, real frame contacts and sampled full assemblies including nominal
fastener heads. `--fallback` uses the conservative stepped case instead of the optional
local STEP. Reports are `build/audit.json` and `build/audit-fallback.json`.
Samples are not continuous motion, loaded operating limits or physical fit.
Head placement and mounting are undecided; the placeholder is omitted from
structural CAD/viewer. Neck, complete battery/electronics packaging and
harness/guards remain open. `leg_sizing.py` retains the explicitly historical
DEC-32 analytical study; it does not size the current robot.

## Viewer and independent images

**DEC-46/48:** sliders use pose-dependent mechanical-clearance ranges for the
printed parts and nominal hardware. The static build warms geometry/engine-hashed
caches using Node.js. A browser worker recomputes bounds after each change.
The search uses 0.25° samples and a 2° reserve before the first obstruction;
these are not calibrated servo or loaded operating limits. Ground contact and
complete harnesses are outside the search. Current main-viewer browser and
solid-CAD endpoint checks are in the
[front revision evidence](../docs/design/front-redesign/README.md#digital-evidence-and-limits).
The earlier `docs/design/manufacturing/travel-endpoints.json` predates the
current links; each report validates only its recorded revision.

Build the separate rear-leg review with `uv run python -m koala_hardware.rear_leg_review`
(add `--thigh-options` for the 2026-09-19 thigh print-form comparison, left leg
option 1, right leg option 2: [record](../docs/design/rear-leg/thigh-options/README.md);
`--thigh-flat` for the owner's chosen one-piece tapered thigh on both legs:
[record](../docs/design/rear-leg/thigh-flat/README.md));
the existing server then exposes it at
[rear-leg/](https://blake.tail13a0c0.ts.net:8443/rear-leg/).

[Blake viewer](https://blake.tail13a0c0.ts.net:8443/) is the canonical instance
(DEC-35), served by [systemd/koala-viewer.service](systemd/koala-viewer.service).
It serves a static build. After source changes, run `viewer --build` on blake
and reload; a service restart also rebuilds. The body selector switches between
walking, wheeled quadruped and wheeled upright snapshots. Sliders apply joint adjustments, **not a
validated rise trajectory or safe operating limits**.

For a local viewer:

```sh
uv run python -m koala_hardware.viewer --serve --no-open --port 8020
```

For browser/CAD parity, with Playwright Chromium installed or
`PLAYWRIGHT_CHROMIUM` set:

```sh
uv run --with playwright python tests/viewer_smoke.py
```

Independent PNG/SVG drawings and structural views are in
[docs/design/](../docs/design/README.md), including copies on blake for iPad
Files. Refresh the kinematic PNGs with:

```sh
uv run --with playwright python -m koala_hardware.body_plan --output ../docs/design --cad --png
```

The Parts tab shows per-part `printable` tags, materials, print orientations and assembly notes;
it is not a packed print plate. Bought references are not printable parts.

## Physical acceptance

The maintainer confirms ST3215 fit in SO-101 parts in PLA+/PETG (DEC-33).
There is no repeat-gauge/caliper prerequisite. The two `coupon_socket_*`
designs remain available to investigate a specific new fit issue. Check the
current assembly's insertion/removal, M2/M3 engagement, centre-head/boss
clearance, Back washers, axial preload and real connector access. Log results
by exact print version in [the test log](../docs/test-log.md).

Root socket v1 is physically proven with its recorded ear-hole support caveat;
hip carrier v1 has plate 2 slices but no recorded physical result. Continue with version-specific fitting,
one rear leg, the pair, front limbs and documented load/creep/transition checks.
Actual masses, CoM and power budgets remain open. No digital check closes these gates.

`slice_remote.py` must not run on the printer host while printing is active.
Local slicing does not submit or start a print. Generic motor/hole/insert
coupons remain available; record results, including no change, in the test log
and store calibrated constants in `params.py`.

## Local manufacturing slices

`uv run python -m koala_hardware.manufacturing_slices` uses local PrusaSlicer,
reads the shared printer profile from the sibling 3d-printing checkout and adds
`print/manufacturing-*.ini` project settings (support from the bed only, never off the part:
the house rule, learned on plate 1; `-tree.ini` for organic support, one part per job). It records exact STL hashes and
layer-path images in `docs/design/manufacturing/`. It never submits a print.
Changed torso v5, shoulder mount v1, front carrier v3, upper arm/forearm v2 and
thigh v3 remain `unknown`; local toolpaths alone do not establish physical
printability. Root socket v1 is `proven` with its documented caveat; unchanged
parts retain their recorded tags. See [the part review](../docs/part-design-review.md).
TPU settings are provisional until matched to the actual spool.
