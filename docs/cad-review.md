# Lower-body CAD review — revision a3f265c

**Disposition: not ready for structural printing or assembly.** The current
solids have reproducible joint interference and blocked fastener paths. Bed-fit,
connected-solid and surface-angle checks pass, but do not establish a working
mechanism, support-free manufacture, or adequate FDM strength.

This is a review, not an adopted replacement design. CAD source and generated
parts were left unchanged. Proposed changes remain pending under OQ-13.

## What the commits establish

| Commit | Change | Review implication |
|--------|--------|--------------------|
| `1c1b65a` | Initial integrated pelvis, hip links, thighs and tray | A dimensional lower-body draft, without structural validation |
| `c329e3e` | Split pelvis/brackets and thigh/clamp; add printability heuristic | Original pelvis stood on tray bosses. Removing those bosses fixed the flat-face problem, but the same commit also split off the brackets. The current separation is not required by that original problem |
| `0bc6372`, `7515b14` | Correct horn screw sizing and add the idler bolt pattern | Useful interface corrections; not proof of screw access through later geometry |
| `ed41a58` | Compact the hip, move pitch servo aft/outboard, lengthen thigh | Its stated collision sweep covers link/pitch servo against bracket/roll servo. It does not cover the pitch-driven thigh against its carrier. The sweep is not retained as a reproducible repo check |
| `ef8ee9c` | Widen stance, reconnect solids, change thigh profile, extend clamp ribs | Fixes real packaging/connectivity issues but leaves collisions and creates a 44 mm seam screw passage without updating the 16 mm fasteners or providing head access |
| `a3f265c` | Add interactive viewer | Improves inspection; introduces no motion or structural validation |

The intended V1 is still the knee-wheeled, two-axis-hip companion in
`concept.md`: forces must pass from wheel/motor through thigh, pitch horn,
pitch-servo case and retention, hip link, roll horn, roll-servo case and
retention, then pelvis. A snug pocket with no verified retention leaves this
load path incomplete. The checked-in SO-ARM bracket is explicitly only a
reference; the custom joints have not inherited a validated bracket design
merely by using its servo dimensions.

## Findings

### 1. Hip link and thigh physically overlap at neutral — blocking

An OpenCascade boolean intersection of the actual printed solids gives
**7,041.21 mm³ per hip at neutral**. This excludes servo ghosts, screws and
clearance padding: two printed parts occupy the same space.

| Thigh pitch about its own Y axis | Printed link/thigh intersection (mm³) |
|---------------------------------|--------------------------------------|
| −30° | 9,285.73 |
| −10° | 7,261.30 |
| 0° | 7,041.21 |
| +10° | 7,250.43 |
| +30° | 8,696.99 |

These are sampled poses, not an exhaustive continuous sweep or an approved
operating range. Neutral interference alone is enough to reject the assembly.

`parts/hip_link.py` subtracts `servo_envelope()` from its cradle, clearing the
metal horn at roughly 10 mm radius. The thigh's rotating printed fork plates
have 15 mm radius, plus the attached beam and eventual screw heads. Their
occupied and swept volumes were never reserved. Filleting the carrier cannot
resolve this architectural conflict; the carrier and driven fork need designing
together around the same motion and access envelopes.

### 2. Four roll-horn screw holes are blind — blocking

In `parts/hip_link.py`, the circular fork plates are 5 mm thick, but the legs
overlapping their lower halves are 6 mm thick. The final cutters still use
`drive_hole_cutters(FORK_T)`, including only 0.1 mm overshoot.

Probing with a 3 mm diameter screw cylinder through the full thickness confirms
**0.9 mm of residual plastic** at both lower holes on each roll-fork face:
four blocked paths per hip link. Each probe intersects 6.36 mm³ of material.
The openings visible from the servo side are therefore not through-holes.
Clearing the screw shaft alone would still leave head seating, tool approach,
thread engagement and assembly order to verify.

### 3. Motor-clamp seam has no validated fastening arrangement — blocking

`parts/thigh.py` now runs seam ribs from wheel-local Z=18 to Z=62:
**44 mm through the rib**, before any engagement in the upper thigh. The bought
BOM still lists M3×16 for this seam. The full-depth clearance cutters remain,
but no intermediate head seats or driver-access pockets were added.

A nominal M3 cap placed immediately below each rib at Z=18 intersects the
motor-clamp solid (49–55 mm³ per head in the tested positions). Longer screws
alone would therefore not complete the joint. The head seats, motor clearance,
insert installation, screw lengths and assembly sequence must be designed as
one interface.

### 4. The pelvis split is not justified by the current print geometry

As an in-memory diagnostic, unioning the existing deck and both correctly
positioned brackets creates **one 150 × 170 × 30 mm solid**. Flipped so the
robot's deck top is on the bed and both saddles grow upward, it has:

- Approximately 24,704 mm² bed contact.
- Approximately 573 mm² flagged overhang area, passing the existing heuristic.
- The same bracket build direction as the separate bracket prints.

This disproves the README's implication that separation is required to obtain
a flat print face. It does **not** prove the combined part is structurally
adequate or support-free in an actual slice.

An integrated pelvis is a reasonable redesign candidate: eliminate the eight
bracket-to-deck screws and eight inserts, replace the 6 mm mounting flanges
with continuous, filleted saddle roots, and reassess the axis height. Fusion
alone does not shorten the assembly; deleting a flange also does not remove
the servo body's required height. Any reduction needs a new clearance check.
Integration retains layer-sensitive saddle roots, so the strength question
still needs addressing. Separate brackets would need a positive reason such
as a better load-oriented print or service access.

### 5. The printability gate is a heuristic, not proof

`printability.py` accepts total down-facing overhang area up to **800 mm²** and
bed contact above 300 mm², then reports `support-free`. It does not test:

- Unsupported extrusion islands or layer-to-layer overlap.
- Bridge span, anchoring, material/profile capability or cooling.
- Local wall thickness and available extrusion paths at joint roots.
- Hole quality, fastener access or insert installation.
- Load direction relative to layers, strength, creep or fatigue.

A small unsupported feature can fail below the area threshold; a well-anchored
bridge can succeed despite being counted. The implementation also classifies
a face as bed contact when just its lowest vertex touches the bed. Requiring
all vertices to touch reduces the thigh's reported bed area by about 14.9 mm²
in this tessellation; this is a real but minor error compared with the missing
manufacturing checks.

The BOM calls the flagged area `self-supporting overhang`, although the test
explicitly selects surfaces steeper than its self-support limit. DEC-24's
claim that the build proves support-free printing is unsupported.

### 6. Layer orientation has been considered, but not structurally validated

Neutral robot axes: X fore/aft, Y lateral, Z vertical. The actual declarations
produce the following layer planes; the viewer's assembly tab is a robot pose,
not a build-plate arrangement.

| Part | Layers in robot coordinates | Engineering interpretation, not a strength result |
|------|-----------------------------|--------------------------------------------------|
| Pelvis / flipped hip brackets | XY | Saddles rise across layer interfaces; root bending and retention loads need checking |
| Hip link, `Rot()` | XY | Upright roll-fork legs carry vertical and torque-induced loads through layer interfaces; the 4 mm connecting foot deserves particular attention |
| Thigh upper, `Rot(Y=90)` | YZ | Much of the long beam lies within layers, but pitch fork plates lie in XZ and rise across layers; the beam and fork have different orientation demands |
| Motor clamp, `Rot(X=-90)` | XZ | Ring lies within layers, sensible for axle torque; axial cantilever loads and seam/rib connections remain unverified |

There are real flat printing surfaces, so the parts are not simply incapable
of sitting on an FDM bed. The missing work is a justified compromise between
manufacture, joint access and load direction. No quantified load cases,
allowable stresses, joint deflections or structural print results were found.
OQ-11 explicitly leaves even the structural perimeter profile unresolved.

FDM orientation affects mechanical integrity as well as surface finish;
Prusa's [design guidance](https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135)
describes direction-dependent strength, and its
[support guidance](https://help.prusa3d.com/article/support-material_1698)
requires support for features that start in air. Neither supports a universal
overhang-area threshold as proof of manufacturability.

DEC-23 also promises parts derived from a master model and registered seams.
The current builders construct independent solids, and registration keys are
used only in `coupon_seam`, not in the structural thigh seam. Four clearance
screws alone do not fulfil that stated interface plan.

## Proposed next design pass — pending OQ-13

1. Define the hip's required pitch/roll ranges and load cases: stance, leaning,
   wheel acceleration/braking, lateral load and handling. Establish physical
   servo/horn/retention dimensions under OQ-12.
2. Model cases, horns, moving forks, screw heads, tool approaches and cable
   exits together. Reserve swept clearances before adding structure.
3. Compare an integrated, deck-face-down pelvis with any justified service or
   strength split. Design a simpler hip carrier and driven fork together;
   compare flat cheek plates with a one-piece yoke using the actual loads.
4. Select seams and print orientations from those loads. Provide registration,
   accessible metal fasteners and filleted roots. Re-derive the motor-clamp
   connection and BOM from the actual fastening stack.
5. Check solid interference, access and hardware stacks; inspect actual sliced
   layers with supports disabled. Print a complete single-hip coupon/rig and
   establish fit, motion and stiffness before committing to full leg prints.

No replacement geometry or operating range is banked by this review. Physical
print testing remains necessary; this audit did not run the remote slicer or
start any print.

## Reproducing the principal geometric findings

From `hardware/`, using the locked environment at the reviewed revision:

```sh
uv run python - <<'PY'
from build123d import Align, Cylinder, Pos, Rot
from koala_hardware import params as P
from koala_hardware.parts import hip_link as H, thigh, pelvis, hip_bracket

link = H.build()['part']
upper = thigh.build_upper()['part']
for angle in (-30, -10, 0, 10, 30):
    posed = Pos(0, 0, -P.HIP_PITCH_DROP) * Rot(Y=angle) * upper
    common = link & posed
    print('pitch', angle, 'intersection mm3', common.volume)

for x, sign in ((P.SERVO_HORN_TOP + H.HORN_GAP, 1),
                (P.SERVO_IDLER_BOT - H.HORN_GAP, -1)):
    for y in (-P.SERVO_DRIVE_SQ / 2, P.SERVO_DRIVE_SQ / 2):
        probe = Pos(x, y, -P.SERVO_DRIVE_SQ / 2) * Rot(Y=90 * sign) * Cylinder(
            1.5, H.LEG_T, align=(Align.CENTER, Align.CENTER, Align.MIN))
        common = link & probe
        print('blocked lower screw', x, y, 'residual mm3', common.volume)

joined = pelvis.build()['part']
for side in (-1, 1):
    joined += Pos(0, side * P.HIP_ROLL_Y, -P.HIP_ROLL_DROP) * hip_bracket.build()['part']
print('joined solids', len(joined.solids()), 'size', joined.bounding_box().size)
print('clamp rib depth', thigh.FLANGE_Z[1] - thigh.FLANGE_Z[0])
PY
```
