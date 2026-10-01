# 20.8 mm footed links and bend travel — unprinted, 2026-10-01

Owner selected the full-depth profile after comparing its elbow contact with
the benchmark and rejecting the removal-only trial. The owner then visually
accepted the maximum-fold robot pose: no additional fold travel is needed or
wanted. Forearm v3, foot shank v2 and matching pad v2 are the accepted current
CAD revision. This is design acceptance, not a physical print result. Owner also reports visual
inspection of SO-ARM models showing the same servo-pocket travel constraint;
that observation does not establish Koala's physical fit or loaded travel.
[Revision log](../../cad-integrated-design.md#revision-log).

- `forearm` **v3**, 100 mm elbow-to-pad reach; `foot_shank` **v2**, 90 mm
  knee-to-pad reach. Fork spacing stays 36.4 mm. Both broad faces now continue
  at 20.8 mm depth through fork, stem and key.
- `front_contact_pad` **v2** has the matching wider cavity. Key engagement is
  3.5 mm, allowing the longer tapered cavity roof while retaining the pad's
  outer surface and fixing positions. Pad v1 does not fit the revised key.
- All three are **unknown/unprinted**. Physical strength, key retention,
  support removal, traction and creep remain unverified. Neither wider geometry
  nor the CAD travel checks establish print strength.
- The upper arms, rear thighs, horn interfaces and joint centres are retained.
  The removal-only variants remain [rejected historical studies](../flat-link-removal/README.md).

## Bend limits and pose conventions

Canonical values: [`bend_limits.py`](../../../hardware/src/koala_hardware/bend_limits.py).
Angles are native X rotation from straight upper/lower links. Front anatomical
flexion is negative; rear anatomical flexion is positive because the assemblies
bend opposite ways. The rear servo pocket is clocked 90°.

| Joint | CAD inspection interval | First obstructed samples outside interval |
|---|---|---|
| Front elbow | −112.75° to +112.75° | −115° / +115° |
| Rear footed knee | −22.75° to +121.25° | −25° / +123.5° |

Each endpoint retains 2° inside the last clear quarter-degree sample. These
are sampled geometric bounds, not the exact tangency angles, calibrated motor
limits or permission to combine arbitrary hip/shoulder positions. The viewer's
shared bend slider intersects its scene-dependent search with these local bounds.
The simulation applies the local bend ranges relative to its walking home pose.

[Clearance report](bend-clearance.json): 226 front and 145 rear interior/endpoint
samples, 1° interior and 0.25° near each stop; pads, pad fixings and horn heads
included. Obstacles include the owning print, supplier servo case, parametric
case and ear heads. Three whole-robot endpoint combinations pass with each case
model. These are static samples, not continuous swept volumes; full cables,
manufacturing tolerances, deflection and loaded movement remain open.

Reproduce with:

```sh
hardware/freecad-run -m koala_hardware.bend_clearance
hardware/freecad-run -m unittest discover -s hardware/tests
```

## Inspection poses

The normal walking, quadruped and upright references remain inside the new bend
bounds. Three additional FreeCAD assemblies hold hip/shoulder positions at the
walking reference and pose both left/right lower limbs at their respective stops:

- **max-fold:** both front elbows at −112.75°, both rear knees at +121.25°.
- **bend-min:** front −112.75°, rear −22.75°.
- **bend-max:** front +112.75°, rear +121.25°.

These are **suspended inspection poses**, not grounded stances or balance/gait
claims. Each has native feature history and a matching archived Python replay.
The conversion benchmark remains immutable at Git `9e6ded8` and in its original
FreeCAD source snapshot. [Approved maximum-fold view](max-fold.png).

| Model | Version | Python | FreeCAD |
|---|---|---|---|
| `forearm_right` | v3 | [Python](../../../hardware/freecad/parts/forearm/v3/aeb4e11ef28feee4/forearm_right.py) | [FCStd](../../../hardware/freecad/parts/forearm/v3/aeb4e11ef28feee4/forearm_right.FCStd) |
| `forearm_left` | v3 | [Python](../../../hardware/freecad/parts/forearm/v3/aeb4e11ef28feee4/forearm_left.py) | [FCStd](../../../hardware/freecad/parts/forearm/v3/aeb4e11ef28feee4/forearm_left.FCStd) |
| `foot_shank_right` | v2 | [Python](../../../hardware/freecad/parts/foot_shank/v2/aeb4e11ef28feee4/foot_shank_right.py) | [FCStd](../../../hardware/freecad/parts/foot_shank/v2/aeb4e11ef28feee4/foot_shank_right.FCStd) |
| `foot_shank_left` | v2 | [Python](../../../hardware/freecad/parts/foot_shank/v2/aeb4e11ef28feee4/foot_shank_left.py) | [FCStd](../../../hardware/freecad/parts/foot_shank/v2/aeb4e11ef28feee4/foot_shank_left.FCStd) |
| `front_contact_pad` | v2 | [Python](../../../hardware/freecad/parts/front_contact_pad/v2/aeb4e11ef28feee4/front_contact_pad.py) | [FCStd](../../../hardware/freecad/parts/front_contact_pad/v2/aeb4e11ef28feee4/front_contact_pad.FCStd) |
| `koala-walking` | — | [Python](../../../hardware/freecad/assemblies/aeb4e11ef28feee4/koala-walking.py) | [FCStd](../../../hardware/freecad/assemblies/aeb4e11ef28feee4/koala-walking.FCStd) |
| `koala-quadruped` | — | [Python](../../../hardware/freecad/assemblies/aeb4e11ef28feee4/koala-quadruped.py) | [FCStd](../../../hardware/freecad/assemblies/aeb4e11ef28feee4/koala-quadruped.FCStd) |
| `koala-upright` | — | [Python](../../../hardware/freecad/assemblies/aeb4e11ef28feee4/koala-upright.py) | [FCStd](../../../hardware/freecad/assemblies/aeb4e11ef28feee4/koala-upright.FCStd) |
| `koala-walking-max-fold` | — | [Python](../../../hardware/freecad/assemblies/aeb4e11ef28feee4/koala-walking-max-fold.py) | [FCStd](../../../hardware/freecad/assemblies/aeb4e11ef28feee4/koala-walking-max-fold.FCStd) |
| `koala-walking-bend-min` | — | [Python](../../../hardware/freecad/assemblies/aeb4e11ef28feee4/koala-walking-bend-min.py) | [FCStd](../../../hardware/freecad/assemblies/aeb4e11ef28feee4/koala-walking-bend-min.FCStd) |
| `koala-walking-bend-max` | — | [Python](../../../hardware/freecad/assemblies/aeb4e11ef28feee4/koala-walking-bend-max.py) | [FCStd](../../../hardware/freecad/assemblies/aeb4e11ef28feee4/koala-walking-bend-max.FCStd) |

## Validation

All 81 Python tests and the viewer joint-order/bend-limit regression pass.
[Nominal assembly audit](nominal-audit.json) passes all three reference poses;
[endpoint clearance](bend-clearance.json) passes all three review poses with
both servo case models. The [viewer bounds](viewer-limits.json) were rebuilt,
and both MuJoCo variants [load with matching joint ranges](simulation-check.json).
All 11 new native documents passed save/reopen/full recompute.
[Archive and source verification](validation.json) confirms the benchmark is
unchanged and the new frozen Python matches current generators.
Exports, the version ledger and generated BOM are current.

## Visual review

Renewed four-view inspection passes: continuous broad faces, intact horn-pocket
rims, open forks, retained rounded roots and a tapered pad cavity. “Does it look
stupid?” **No.** [Forearm](../parts/forearm-views.png) ·
[rear shank](../parts/foot_shank-views.png) · [TPU pad](../parts/front_contact_pad-views.png).
Physical printability remains unknown; earlier slices do not validate these versions.
