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
| `src/koala_hardware/parts/` | One module per part: `pelvis`, `hip_bracket`, `hip_link`, `thigh`, `e_tray`, `coupons` |
| `src/koala_hardware/printability.py` | **DEC-24 support-free check**: bed contact, overhang area, orientation ranking |
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
```

A full run also regenerates the printed-parts table in
[`../docs/bom.md`](../docs/bom.md) and prunes outputs for renamed parts. Parts
marked `handed` export **both** `_right` and `_left` STLs — mirroring in the
slicer is too easy to forget.

The export **fails** if any part exceeds 200x200 mm in its declared print
orientation (DEC-09/DEC-23), or if that orientation needs support (DEC-24):
bed contact under 300 mm2, or overhang area over 800 mm2. On failure it prints
the better orientations it measured.

### Designing a part that passes

- **Features on one face only.** A plate with bosses up *and* structure hanging
  down has no printable orientation — split it (that is why the pelvis is a bare
  deck with separate `hip_bracket`s).
- **No closed cavity floors** — a floor becomes a bridged ceiling when the part
  is flipped. Let cavities open through.
- **Forks print axis-horizontal**, so both tines stand on the bed; axis-vertical
  leaves the far tine bridging air.
- **When two features want different orientations, add a seam** (DEC-23) — the
  thigh splits into `thigh_upper` + `motor_clamp` for exactly this reason.

## Print order — coupons first

Every `[VERIFY]` constant in `params.py` has a matching test coupon
(`coupon_*` in the build output). **Print and fit-check the coupons before
any structural part**, adjust the constants, regenerate. Material: PETG.

## Status

Draft **v1** lower body: pelvis deck, hip brackets + hip links (2-DOF hips),
thigh upper + motor clamp (motor-in-thigh, wheel-at-knee, DEC-17), electronics
tray (first torso element). All parts pass bed-fit and support-free checks;
geometry reviewed in renders; **not yet test-printed**, and five `[VERIFY]`
constants still rest on datasheet figures.
