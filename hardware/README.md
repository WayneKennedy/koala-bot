# hardware/

Parametric build123d CAD, CERN-OHL-S-2.0. **DEC-34 is a digital lower-body
prototype, not an accepted structural robot.** The previous structural
builders have been deleted; they remain recoverable in git. Design and
acceptance record: [`../docs/cad-restart-design.md`](../docs/cad-restart-design.md).

## Layout

| Path | Role |
|---|---|
| `src/koala_hardware/params.py` | Dimensions and provenance; `RESTART_*` study assumptions and `V2_*` implemented layout are distinct |
| `servo_iface.py` | Shared SO-101 cradle, collar, two horn plates and socket access envelopes |
| `parts/pelvis.py`, `parts/links.py`, `parts/e_tray.py` | New pelvis, orthogonal hips, thighs, knees, shanks, wheel-feet and tray |
| `parts/joint_rig.py` | Five `coupon_socket_*` parts for the first physical gate |
| `parts/coupons.py` | Retained motor, hole/insert and seam coupons; old enclosing cradle coupon removed |
| `leg_sizing.py` | Analytical height, motor-width and knee-load study, independent of CAD |
| `assembly.py`, `viewer.py`, `viewer.html` | Posed assembly and browser inspection with separate hip/knee pivots |
| `audit.py`, `validation.py` | Nominal solid intersections, selected hardware access and hole probes, shared layout datums |
| `export.py`, `printability.py` | STL/renders, bed/surface screens, generated printed/fastener BOM |
| `slice_remote.py` | Printer-host slicing, only when idle |
| `vendor/so-arm100/` | Apache-2.0 upstream reference CAD |
| `vendor/st3215/` | STS3215 case model used by `servo_iface.case_model()` for clearance checks; licence to record (see its README) |
| `build/` | Ignored outputs: STL, renders, viewer scene, manifest and hash-matched slice cache |

Source paths in the table are relative to `src/koala_hardware/` after the
first row. All shell commands below run from `hardware/`.

## Build and review

```sh
uv run python -m koala_hardware.export
uv run python -m koala_hardware.audit
uv run python -m unittest discover -s tests
uv run python -m koala_hardware.leg_sizing
uv run python -m koala_hardware.assembly
uv run python -m koala_hardware.viewer       # http://localhost:8017
```

`viewer --build` regenerates data without serving; `--serve` serves existing
data; `--port N` changes the port. Hip and knee sliders are **inspection poses,
not control limits**. The nominal stance is hip 15°, knee 30°, roll 0°.

**Always-on instance (DEC-35):** the reference workstation `blake` runs the
viewer as a user service, reachable within the tailnet at
<https://blake.tail13a0c0.ts.net:8443/> (Tailscale Serve → `127.0.0.1:8017`;
configured 2026-09-08). The unit is [`systemd/koala-viewer.service`](systemd/koala-viewer.service);
its header has the install steps. **The scene is not live**: the server only
serves `build/viewer/scene.json`, rebuilt when the service (re)starts. After a
CAD change on blake, `systemctl --user restart koala-viewer` (the rebuild took
6 s on 2026-09-08) and reload the tab; or run `viewer --build` and reload.

The Parts tab shows declared print orientation, quantity and assembly notes;
it is not a packed print plate.

With the viewer running:

```sh
uv run --with playwright python tests/viewer_smoke.py
```

Use an installed Playwright Chromium or set `PLAYWRIGHT_CHROMIUM`. The check
compares browser-posed left/right mesh bounds to CAD, including knee motion.

A full export regenerates the printed-parts **and fastening** tables in
[`../docs/bom.md`](../docs/bom.md); never hand-edit the generated block.
Handed cores, cradles and collars produce explicit `_left`/`_right` STLs.
Per-side quantities come from the builders. Removed outputs are pruned.
Cached slice figures count only when their SHA-256 matches the current STL.

The build rejects disconnected printable bodies (except the two-piece seam
coupon), bed bounds over 200 mm, bed contact below 300 mm², and flagged
overhang area above 800 mm². These surface tests are **screens**, not proof of
support-free manufacture or strength. The audit samples 27 local and 81
opposing-leg poses; it is not a continuous or tolerance-expanded sweep.

## Print order and remaining checks

The maintainer confirms ST3215 fit in SO-101 parts in both PLA+ and PETG
(DEC-33); repeat gauging and calipers are not prerequisites. `SOCKET_CLEAR=0`
applies to that pocket. Generic non-servo fits remain separate.

1. When the printer is idle, slice and inspect **only the five
   `coupon_socket_*` rig parts first**. The cradle's shelf, collar's open-bottom
   cable slot and horizontal screw bores need layer inspection. Do not assume
   a green overhang-area result proves them printable.
2. Print and fit one complete joint, log insertion/removal, all screw
   engagements, both horn fits, free motion without axial preload and cable
   access in `docs/test-log.md`. The new parts have not inherited physical
   acceptance merely by adopting upstream nominal dimensions.
3. Resolve motor boss/body fits with the retained coupons. Then one leg,
   the pair, and quantified load/creep tests under OQ-11/13. The front/rear
   orientation of actual connectors and both handed sockets remain fit checks.

The five rig STL names begin `coupon_socket_`; `export coupon_socket` filters
export output. It does not slice, pack or start a print. **Never slice on the
printer host while a print is running.** On 2026-09-07 it reported `printing`,
so this redesign did not run the slicer or start a print.

The remaining motor/insert coupons are fit ladders: choose the smallest size
that accepts the real part on the calibrated reference printer. Record every
result, including no change, in the test log; store the value and provenance
in `params.py`. Generic coupon results are not universal material tolerances.

## Design rules retained from the reviews

Keep case and horn datums distinct. Design the carrier, driven link, hardware
stack and access path together. Use real metal threads; no plastic sliding
threads. Flat cheeks and motor plates keep their principal bending loads in
the layer plane. Crossbars and tapered socket supports print from broad ends;
root tension, creep and side loading still need physical tests. Keep head
pockets open in the print orientation. Proud internal fasteners require
clearance; exposed fasteners and pinch points require guards before child use.
