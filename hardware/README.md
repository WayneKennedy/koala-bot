# hardware/

Parametric build123d CAD, CERN-OHL-S-2.0. **DEC-49/50 implements enclosing sockets, rounded links, rear ankle drives
and flat-section forearms with replaceable TPU contact pads**, retaining the DEC-41
pitch → roll joints. Knee-wheel relocation is deferred. Design,
assembly, dimensions and remaining acceptance gates:
[cad-integrated-design.md](../docs/cad-integrated-design.md).

## Current CAD

`params.py` supplies the body and interface dimensions. `servo_iface.py`
implements the four-ear SO-101 saddle, flat horn interfaces and hardware
references. `parts/links.py` builds integrated upper/lower links and orthogonal
carriers; `pelvis.py`, `torso.py` and `e_tray.py` complete the present chassis.
The root chain is pitch → roll → knee/elbow (DEC-41); the pitch carrier holds
the roll servo, and upper links have perpendicular end axes.
`body_plan.py` supplies the same joint centres to schematics and `assembly.py`.

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
```

Exports: `build/stl/`, `build/step/`, `build/renders/`, `build/manifest.txt`.
Full assemblies are `build/step/koala-quadruped.step` and `koala-upright.step`.
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
heads. `--fallback` uses the conservative stepped case instead of the optional
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
The search uses 0.25° samples and a 1° reserve before the first obstruction;
these are not calibrated servo or loaded operating limits. Ground contact and
complete harnesses are outside the search. Initial BREP endpoint checks are in
`docs/design/manufacturing/travel-endpoints.json`.

[Blake viewer](https://blake.tail13a0c0.ts.net:8443/) is the canonical instance
(DEC-35), served by [systemd/koala-viewer.service](systemd/koala-viewer.service).
It serves a static build. After source changes, run `viewer --build` on blake
and reload; a service restart also rebuilds. The body selector switches between
quadruped and upright snapshots. Sliders apply joint adjustments, **not a
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
There is no repeat-gauge/caliper prerequisite. Start with the **two**
`coupon_socket_*` prints: four-ear saddle and integrated double fork.
Check insertion/removal, all M2/M3 engagements, centre-head/boss clearance,
Back washers, axial preload and real connector access. Log the fit in
[the test log](../docs/test-log.md) before a full leg is printed.

Next: one rear leg, the pair, front limbs, documented load/creep and transition
checks. The additional drive units require an updated measured mass/CoM and
power budget. No digital check closes these gates.

`slice_remote.py` must not run on the printer host while printing is active.
This CAD update does not slice or start a print. Generic motor/hole/insert
coupons remain available; record results, including no change, in the test log
and store calibrated constants in `params.py`.

## Local manufacturing slices

`uv run python -m koala_hardware.manufacturing_slices` uses local PrusaSlicer,
reads the shared printer profile from the sibling 3d-printing checkout and adds
`print/manufacturing-*.ini` project settings. It records exact STL hashes and
layer-path images in `docs/design/manufacturing/`. It never submits a print.
Every current design is `assumed`; none is physically `proven` at this revision.
TPU settings are provisional until matched to the actual spool.
