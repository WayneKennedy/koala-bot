# Knee drive packaging — local feasibility screen

**Historical study — superseded by DEC-43 (2026-09-10).** The maintainer retains
rear ankle wheels and fixed front feet to complete V1. Knee-drive relocation,
remote drives and separate folding rear feet are deferred. Calculations below
record the rejected direction; current design: [integrated CAD](cad-integrated-design.md).

2026-09-10, DEC-42 / OQ-17. **The maintainer's concern is substantiated:**
retaining the 37D motor does not establish a compact knee-wheel mechanism.
A direct coaxial stack is unattractively wide with the present joint spacing.
An offset direct drive merits a complete mounting/pose study; it is not yet
an accepted mechanism. [Dimensioned PNG](design/knee-packaging.png) ·
[SVG](design/knee-packaging.svg) · [Numerical results](design/knee-packaging.json).

## Dimensions and coaxial stack

Repository datums: motor Ø37 × 69 mm from face to encoder cap; output shaft
21 mm beyond the face. Measured knee horn contact span 36.4 mm plus two
6.3 mm printed pads gives **49 mm** overall clevis width. Wheel Ø80 × 10 mm;
current hub/mount stack puts its centre 23 mm beyond the motor face.

The motor's cylinder and the servo occupy the same space if their axes and
axial envelopes coincide. The knee servo does not provide a through-hole for
an independent wheel-drive shaft. Merely sharing the centreline in a drawing
cannot make those parts coexist.

For the straightforward solution of placing the whole motor outboard of the
clevis, allow 3 mm clearance and retain the present 149.2 mm knee-centre spacing:

`track = 149.2 + 2 × (25.7 outer clevis extent + 3 gap + 69 motor + 23 wheel stack)`

Result: **390.6 mm wheel-centre track**, versus the current 220 mm. This is a
conditional layout calculation, not a universal minimum for other arrangements.
Scaling the robot modestly taller does not remove this axial-length problem.

## Offset direct-drive sample

A build123d study retains the current motor face location and wheel track,
and moves the motor/wheel axis fore/aft **in the thigh frame**, perpendicular
to the thigh. The servo reference uses the imported case with measured horns;
the actual integrated thigh is included. The lower-leg proxy is the current
clevis plus a 16 × 16 mm beam to 90 mm reach. It has no final foot or drive
carrier, and is not an exportable structural design.

| Axis offset | Motor/servo intersection | Motor/servo separation |
|---|---:|---:|
| 25 mm | 2715 mm³ | intersecting |
| 30 mm | 149 mm³ | intersecting |
| 35 mm | none | 4.14 mm |
| 40 mm | none | 9.14 mm |

At 35–45 mm offset the motor also clears the current thigh and lower-leg proxy
at sampled folds of 0°, 30°, 60°, 90° and 120°, folding away from the motor.
However, **at 120° the clevis itself intersects the servo by 16.4 mm³**,
independent of motor offset. The sampled 0–90° configurations do not have that
intersection. This does not establish a continuous safe range or include
screws, cables, mount structures, foot geometry or the opposite leg/whole body.

Use **around 40 mm offset as a starting envelope**, not an adopted dimension.
A 35 mm bare-envelope clearance is not automatically a buildable motor mount.
The wheel then lies beside the knee in side projection, on a distinct parallel
axis. Its final forward/backward direction must be selected with the folded
foot, CoM and wheel-contact pose; offset changes support geometry and moments.

## Alternatives and recommendation

1. **Offset direct drive:** fewest extra transmission parts; investigate first
   if a roughly 35–40 mm knee-to-wheel offset is acceptable in the actual body
   layout. Engineer a thigh-supported carrier and prove both contact modes.
2. **Remote motor with belt drive:** put the motor farther up the thigh and use
   an independently supported wheel axle near the knee. This separates motor
   packaging from wheel position, but adds bearings, pulleys, belt tensioning,
   guards and drive-compliance checks. The wheel must not load or be driven by
   the knee-servo horn. An axle exactly coaxial with the knee is still a bearing
   and support design problem, not a solved feature of this proposal.
3. **Different motor package:** select by axial length, diameter, torque-speed
   behavior and shaft loading. The previously compared
   [Pololu 25D](https://www.pololu.com/product/4846/specs) is lighter and narrower
   but still 69 mm long, so it does not solve the coaxial stacking problem.

Retain the bought motors as study hardware; qualify the earlier retention
recommendation on finding a sound mounting arrangement. Do not enlarge the
whole robot or commit to a belt solely to preserve those purchases. Neither
this study nor the previous DEC-40/41 audit validates a DEC-42 complete robot.

Reproduce the numerical study and SVG from `hardware/`:

```sh
uv run python -m koala_hardware.knee_packaging
```

The SVG is a dimensioned snapshot guarded against changes to its hardware
constants. PNG is a browser rasterization for the iPad Files app.
