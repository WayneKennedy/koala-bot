# Body layout — DEC-43/44

The maintainer accepted this overall layout under DEC-44 (2026-09-10).
Manufactured-part detailing is reviewed separately in [part-design-review.md](part-design-review.md).

[Supported pose PNG](design/body-quadruped.png) · [Upright PNG](design/body-upright.png).
SVGs, STEP references and joint coordinates are alongside them in
[docs/design](design/README.md), viewable independently in iPad Files.

The compact proportions adopt the maintainer's
[multi-view concept](<inspiration/Koala schematic.PNG>) and
[side view](<inspiration/Side on.PNG>) under DEC-36/37. DEC-40/41 resolved servo
and motor packaging. DEC-43 retains rear ankle wheels and replaces front
wheel drives with fixed rounded feet; knee-wheel relocation is deferred.

## Current dimensions

`hardware/src/koala_hardware/params.py` supplies the authoritative dimensions.
No servo interface is scaled to achieve body proportions.

| Feature | Dimension (mm) |
|---|---:|
| Upright head-top height | 450 |
| Head envelope, length × width × height | 85 × 110 × 75 |
| Neck, shoulder to head-envelope base | 35 |
| Torso, hip to shoulder | 150 |
| Rump allowance behind hip along torso | 70 |
| Upper arm / elbow-to-wrist forearm | 70 / 75 |
| Fixed hand extension / ball radius | 25 / 16 |
| Effective elbow-to-ball-centre length | 100 |
| Thigh / shank | 85 / 90 |
| Rear ankle wheels | 2 × Ø80, nominal width 10 |
| Rear wheel-centre track | 220 |
| Front ball-centre spacing | 149 |
| Hip / shoulder roll-centre spacing | 149 / 149 (DEC-49 common carrier) |
| Hip/shoulder pitch-servo centre spacing | 48 |
| Supported front–rear contact spacing | 260 |
| Supported hip / shoulder height | 175 / 165 |
| Supported head-top / approximate nose–rump length | 237.7 / 340 |
| Upright hip / shoulder height | 190 / 340 |

## Ground reach and poses

The former wrist wheel supplied 40 mm of ground reach below its axle. With
that wheel removed, a simple 70 + 75 mm arm cannot reach the same ground
contact from the 165 mm shoulder. A 25 mm hand extension and 16 mm ball radius
close the stance while preserving the compact torso and rear leg geometry.
DEC-48 uses a flat-section rigid forearm and separate keyed TPU contact pad,
without another joint. The nominal ball centre and contact envelope are retained.

In supported stance, rear wheel centres are (−55, ±110, 40), front ball centres
(205, ±74.5, 16), hip root X/Z (0, 175) and shoulder root X/Z (149.666, 165).
Both contact types reach Z=0. The footprint is a trapezoid, narrower at the
front. Knee flexion is 67.22° and elbow flexion 42.25°; limbs are not straight.

Upright, hip 190 + torso 150 + neck 35 + head 75 = 450 mm. Rear axles are
at X=0, Z=40; front ball centres are raised to X=100, Z=330. Knee flexion
is 62.03° and elbow flexion 110.05°. Head position and mounting remain undecided; the drawn envelope is a sizing
allocation and is omitted from the structural CAD/viewer (DEC-49).
Loaded balance and a transition between these saved poses are not established.

## Rear drive packaging and scope

Keep the bought 37D pair at the ankles. Each motor face is 23 mm inboard of
the wheel centre; each motor body extends 69 mm farther inward. At 220 mm
track the opposed motor end gap is 36 mm. DEC-40 widened the earlier 200 mm
track to clear inward roll; DEC-41 corrected pitch → roll at hips/shoulders.
The 120 mm conceptual track would overlap the motors by 64 mm.

The twelve ST3215s and two wheel-drive channels remain. Front ball feet add
no actuator, caster or wheel. Supported stance and rear-wheel balance/drive
are V1 targets; uneven-terrain stepping with wheel-feet is a later experiment.
Four separate walking feet with wheels off the ground are not required.

## Implementation and limits

`body_plan.py` solves the joint centres and creates the diagrams and kinematic
STEP references. The detailed [integrated chassis](cad-integrated-design.md)
uses those same centres, including the side-view viewer backdrop. Nominal
contact closure and finite collision samples do not establish traction,
physical fit, continuous motion, servo duty or printed strength. Battery,
neck, wiring, guards and loaded transitions remain detailed work.
