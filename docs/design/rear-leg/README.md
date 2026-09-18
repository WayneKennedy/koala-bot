# Rear leg — DEC-57/58, 2026-09-15

The maintainer selected the **45° pitch-socket mount as the proposed A/B
arrangement**, retaining the DEC-56 carrier and servo B placement. This review
progresses to the thigh and the lower leg's 37D motor mount. The full torso
remains deferred; the green surface is a patch of its proposed mounting face.

[Live review over Tailscale](https://blake.tail13a0c0.ts.net:8443/rear-leg/) ·
[Quadruped view](rear-leg-quadruped.png) · [Upright view](rear-leg-upright.png) ·
[30° outward roll](rear-leg-roll-30.png) · [Structural sections](sections.png) ·
[Thigh views](../parts/thigh_right.png) · [Shank views](../parts/shank_right.png).

## Geometry

The **85 mm thigh**, **90 mm shank**, joint centres, saved foot positions and
**220 mm neutral rear track** are retained. No bought actuator is added.

- **Thigh:** stepped yoke with cheeks 4 mm outside the roll socket. New joins
  start beyond the complete horn pads; the short tails stop at 13.5 mm so
  their corners clear the measured idler-side case pad during rotation.
  R6.3 inner roots connect the yoke to its lower bridge. Servo C's case is
  clocked **90° about its unchanged knee shaft**, putting its Bottom toward
  native +Y. This clears the knee socket from the carrier's inward-roll path.
  Knee-socket roots are R5; the 2 mm socket lip uses R1.5, with 0.5 mm left
  to the accepted pocket. R1.5 outer pad returns keep the straight horn
  drivers clear.
- **Shank:** the open fork extends to a bridge 46 mm from the knee axis,
  leaving space for the folded thigh. R6.3 fork roots and R5 spine/motor
  face/body-ring roots are made after the structural union. The motor bore,
  central boss clearance and six screw paths are cut afterward. The 37D
  still slides axially in from inboard; install face screws before the hub
  and wheel. The six M3×8 face screws retain 3 mm nominal engagement; the
  actual available thread depth and face boss remain physical checks.
  The small 2.25 mm step outside the drive fork has an R2 return.

[Thigh right STEP](thigh-right.step) · [Thigh left STEP](thigh-left.step) ·
[Shank right STEP](shank-right.step) · [Shank left STEP](shank-left.step).
These part exports use the declared print orientation, already on the bed.
[Quadruped assembly STEP](rear-leg-quadruped.step) ·
[Upright assembly STEP](rear-leg-upright.step) contain only project geometry.
The distributable viewer uses measured case/horn envelopes; the locally
imported vendor servo STEP is used for checks and is not redistributed.

## Clearance evidence

[Solid-CAD checks and source hashes](clearance.json) record:

- **Local thigh roll −30° to +30°, every 1°:** thigh against carrier and both
  imported and conservative measured B case references; no intersection
  above 0.01 mm³.
- **Local knee flexion 0° to 120°, every 1°:** shank against thigh and both
  C case references, with the same criterion. These are provisional design
  targets, not calibrated servo settings or accepted walking limits.
- All eight horn fixing bores, head/washer pockets and straight driver
  approaches on each link are clear after the final structural unions.
  C's ear-head/driver and nominal cable corridors clear, as do sampled
  open-end case insertion positions. All six motor screw bores/drivers and
  the axial motor insertion checks pass.
- Both rear legs, motors, wheels and nominal hardware clear at the recorded
  baseline and independent pitch/roll/knee samples in both saved body poses.
  Full nominal assembly checks also pass with the previous torso mount.
  The audit now checks hardware component solids individually and uses
  hexagonal captive-nut references, fixing earlier false/missed clashes.

The [viewer limits](viewer-limits.json) are a separate 0.25° mesh search with
2° reserve. The previous 1° reserve left 0.013/0.020 mm³ imported-case contact
at the quadruped/upright forward pitch endpoints, so it was increased after
independent checks. The search stops at the first obstruction and includes hidden parts and
the opposite leg. The motors constrain simultaneous inward roll; the local
±30° thigh clearance must not be read as permission for both legs to move
inward by 30°. [Independent endpoint checks](viewer-endpoints.json) compare
its initial bounds against the solid CAD and include combined motion samples.
All twelve initial endpoints and four combined samples pass. Simultaneous
inward roll is limited to −5.5° in quadruped and −5° upright with the reserve;
the **180° outward value is the search ceiling**, not a confirmed physical
stop. [Browser checks](browser.json) cover both cached poses, controls and
part selection.

The rear review omits the complete torso, front limbs, harnesses and guards.
Floor contact does not constrain these inspection sliders. Real indexing,
tolerances, motor dimensions marked for verification, loaded transitions,
walking and strength remain unverified.

## Manufacture and reproduction

Both revised parts are **unknown printable**. Valid connected solids and
watertight handed STL exports fit the 200 × 200 mm bed.
[Export hashes and surface metrics](manufacturing.json). The thigh is
44.9 × 109.8 × 72.9 mm in its declared orientation, with 962 mm² bed contact;
the shank is 123.4 × 46 × 51.3 mm, with 1821 mm². Both need accessible local
support and a layer/removal review. The surface screen flags 2742/2241 mm²
respectively; it does not prove printing or structural performance. No slice
or physical print of this revision has been made.

From `hardware/`:

```sh
.venv/bin/python -m unittest discover -s tests
.venv/bin/python -m koala_hardware.export
.venv/bin/python -m koala_hardware.rear_leg_review
```

The last command builds `hardware/build/viewer/rear-leg/` on the existing
viewer server. The separate main viewer retains its earlier torso mounting
geometry while incorporating the revised thigh and shank. The archived
[earlier socket-angle comparison](../carrier-orientation/README.md) remains
available for the A/B proposal's history.
