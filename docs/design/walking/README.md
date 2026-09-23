# Walking first build — interchangeable rear shanks

**2026-09-21, DEC-62.** `foot_shank` v1 replaces each complete wheeled `shank`
at the existing knee. It has no motor mount or drive hardware and uses the
**unchanged `front_contact_pad` v1**: four identical Ø32 TPU feet on the first
robot. Wheeled shank v2 remains the V1 end goal.

[Four-view shape review](../parts/foot_shank-views.png) ·
[Assembly](assembly.png) · [Side](assembly-side.png) ·
[Walking schematic](../body-walking.png) · [SVG](../body-walking.svg) ·
[Main viewer](https://blake.tail13a0c0.ts.net:8443/) (opens in “Walking · four TPU feet”).

## Parts and exchange

| Print | Qty for walking | Files |
|---|---:|---|
| `foot_shank_left` v1, PETG | 1 | [STL](../../../hardware/build/stl/foot_shank_left.stl) · [STEP](foot_shank_left-v1.step) |
| `foot_shank_right` v1, PETG | 1 | [STL](../../../hardware/build/stl/foot_shank_right.stl) · [STEP](foot_shank_right-v1.step) |
| `front_contact_pad` v1, TPU | 4 total | [STL](../../../hardware/build/stl/front_contact_pad.stl) |

STLs are generated local build outputs; run the exporter after cloning.
The full structural assembly is
[`koala-walking.step`](../../../hardware/build/step/koala-walking.step).
The generated [BOM](../../bom.md) counts **28 physical prints walking** and
**26 wheeled**, excluding coupons and unfitted alternatives from each total.

Each rear foot is 90 mm from knee axis to ball centre; front reach stays
100 mm. Native X is the knee shaft, +Z points toward the pad. The rear knee's
36.4 mm horn span, square holes, head recesses and driver paths are retained.
No new ankle joint or structural seam is introduced. The front v2 geometry
and all existing part versions are unchanged; the ledger adds `foot_shank` v1.

Insert the captive M3 nut from the shank's side before fitting the keyed pad.
Use the same recessed M3×20 screw and plain washer as the front foot. Mount
the fork on the knee's drive/idler horns using the existing eight square
screws, drive-centre retention and four idler washers. For conversion,
support the robot, isolate power and exchange the whole handed lower links
at those horn interfaces; the knee servos stay in the thighs. Fit the
retained motor/hub/wheel packages to wheeled shank v2 and use the matching
kinematics, calibration and mass model.

## Stance and clearance scope

The walking CAD reference retains the supported torso and front limb pose.
Rear contact X remains −55 mm; pad centres are Z16 instead of the wheel
axles' Z40. Rear knees are re-solved for the retained 85/90 mm links. All four
TPU surfaces touch Z0. Neutral rear foot spacing is **132.6 mm**; front foot
spacing is 190.23 mm. **220 mm is the wheeled track**, not walking-foot spacing.
The `walking` reference is a standing configuration, not a trained gait.

- Four-view shape gate passed before export: short front-style taper, open
  fork and broad flat print face; no leftover motor bracket.
- Both handed exports are connected, valid solids with closed positive-volume
  meshes; each fits within **49.0 × 103.4 × 20.8 mm** in its print orientation.
- Regression checks cover common horn interfaces/driver paths, identical
  keyed terminal geometry, nut access, pad/head clearance and per-build BOM
  counts. The full Python suite passed 71 tests; the JavaScript transform
  regression also passed.
- The complete shank **and pad** clear the adjacent thigh and knee case at
  **0–120° bend in 10° increments**, with imported and conservative cases.
  This local check is separate from whole-robot slider travel.
- [Assembly samples](assembly-samples.json): 27 shared-control combinations
  at −5/0/+5° roll/pitch/bend plus four opposed-left pitch/bend samples pass.
  [Nominal audit](assembly-audit.json) and
  [conservative-case audit](assembly-audit-fallback.json) include all three
  configurations and the existing mounting/access checks.
- [Viewer endpoints](viewer-endpoints.json): all six initial walking slider
  endpoints pass independent solid-CAD checks with both case models. Browser
  checks cover walking and both retained wheeled poses, left/right motion,
  pad/shank tags, backdrop alignment and resetting the controls.
  [Validation record](validation.json) lists the commands and results;
  [source/export manifest](manifest.json) records the reviewed version and hashes.

These are discrete, nominal CAD checks. They do not prove continuous travel,
floor clearance during slider motion, cable routing, loaded gait, strength or
safe servo limits. Ground reactions, training setup and physical foot/load
acceptance remain OQ-16/17/19.

## Print approach and local slices

`foot_shank` v1 is **unknown / unprinted**. Print with its broad native −Y face
on the bed. The existing fork bores/head reliefs and nut-slot roof need
accessible local supports. The new rear part inherits the front construction,
not physical proof of fit or strength.

[Slice records and hashes](slices.json) ·
[Left layers](foot_shank_left-layers.png) ·
[Right layers](foot_shank_right-layers.png).

Both handed v1 exports were sliced with the recorded shared PETG profile and
Koala's `manufacturing-petg-tree.ini`: organic support from the bed only,
0.2 mm layers, four perimeters, 30% infill, 4 mm brim. Each has 104 layers,
zero reported slicer diagnostics and approximately **3 hours / 30 g PETG**.
Selected layers show a continuous shaft/taper and open support access at the
fork and key; they do not prove every layer start or physical removal.
The unchanged TPU pad retains its existing slice record; material grade,
retention, traction and wear remain unverified. Nothing was printed.

From `hardware/`, regenerate CAD and checks:

```sh
uv run python -m koala_hardware.render_views foot_shank
uv run python -m koala_hardware.export
uv run python -m koala_hardware.assembly
uv run python -m koala_hardware.audit --nominal-only
uv run python -m koala_hardware.audit --fallback --nominal-only
uv run python -m unittest discover -s tests
uv run python -m koala_hardware.body_plan --output ../docs/design --cad --png
uv run python -m koala_hardware.viewer --build
```

For either exported shank, the local slice command is:

```sh
prusa-slicer --load ../../3d-printing/reference/ender5s1_petg_koala.ini \
  --load print/manufacturing-petg-tree.ini --threads 2 --export-gcode \
  --output build/manufacturing/foot_shank_right-v1-tree.gcode \
  build/stl/foot_shank_right.stl
```

Use `left` for the other hand. The recorded run used the temporary extracted
PrusaSlicer executable named in `slices.json`; no host installation or printer
connection was required.
