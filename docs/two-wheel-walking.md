# Four walking feet and two knee-area wheels — DEC-42

**Historical study — superseded by DEC-43 (2026-09-10).** The maintainer retains
rear ankle wheels and fixed front feet to complete V1. Knee-drive relocation,
remote drives and separate folding rear feet are deferred. Calculations below
record the rejected direction; current design: [integrated CAD](cad-integrated-design.md).

2026-09-10. The maintainer clarified the mechanism: **walk on four feet with
all wheels off the ground; fold the rear lower legs clear and crouch onto the
two rear knee-area wheels for balance and drive**. The earlier interpretation
of locked ankle wheels acting as walking feet is superseded.

## Settled direction and implementation status

- Retain the bought two 37D geared/encoder motors and Ø80 wheels; cancel front
  wheels, motors, hubs and extra drive channels.
- Front forearms end at wrist/hand reach in fixed rounded printed feet.
- Rear lower legs end in separate walking feet. Existing knee servos fold them
  clear for wheeled mode. Exact rear-foot shape remains to be designed.
- Keep twelve ST3215 limb joints with hip/shoulder pitch → roll and knee/elbow
  pitch; the wheel drives remain independent of knee folding.
- Quadruped walking, four-foot standing and the contact transition are intended
  capabilities, not demonstrated performance. Power-off standing is unproven.

The CAD, viewer, drawings, generated printed BOM and prior collision checks
still describe DEC-40/41. Both forelimbs and rear drive/lower-leg structures
need revision. No new design has been exported or physically accepted here.

## Proposed mechanical arrangement

Prefer investigating a **thigh-supported drive carrier near the knee**, with
an independently articulated shank and foot. The wheel axle need not be coaxial
with the knee servo: fitting both actuators and their bearing/fastener stacks
may require an offset. Carrier ownership and offset are open, not settled CAD.

If the wheel is supported directly by the thigh structure, wheeled-mode ground
load can pass from wheel/axle into the thigh and hip without depending on the
knee servo's output geartrain to support the body. The knee then folds and
holds the relatively light lower leg. Walking still loads the knee through the
foot. This benefit must be established by the actual load path, not assumed
merely because a wheel appears beside a knee in a drawing.

Prove tyre clearance throughout walking, folded-foot clearance throughout
rolling, and the intermediate contact sequence. Feet must unload before they
are lifted; establish wheel contact and balance before relying on the wheel
pair alone. Stable four-foot standing requires the centre of mass to project
inside the supported area. A slow crawl must shift weight into each three-foot
support region before lifting the next foot. Servo workspace, traction and
terrain clearance remain unverified.

Wheel locking is not needed to make walking contacts because the wheels are
clear in that mode. A parked wheeled pose would be a separate holding problem.
Four-foot static stability avoids the two-wheel balance loop; it does not make
bent servo-driven legs support weight indefinitely without power. Mechanical
rests/stops or a demonstrated passive load path would be needed for that claim.

## Motor size and servo implications

The [DFRobot FIT0403 specification](https://wiki.dfrobot.com/fit0403) lists
205 g per motor. Retaining two gives **410 g of drive motors**, versus the old
four-drive 820 g. Removing the front motors, wheels and hubs removes about
**463 g of purchased hardware** before adding new feet and accounting for
changes in printed mounts. This is not a measured net robot-mass reduction.

**Recommendation, qualified by the [packaging screen](knee-drive-packaging.md):
retain the bought rear pair for layout studies, conditional on a sound knee
mounting arrangement.**
The strongest downsizing argument was wrist mass, which disappears. Two-wheel
propulsion and balance recovery still need torque-speed headroom, and the
manufacturer's 38 kgf·cm stall figure does not establish continuous operation.
At Ø80 mm and 122 rpm, no-load speed remains about **0.51 m/s at 12 V**.
The new geometry does not by itself prove those motors oversized or accepted.

Keep the ST3215s provisionally. Front-limb gravity and swing-inertia demands
fall substantially. For illustration, a 100 g passive distal assembly in the
old 70/75 mm arm geometry gives roughly **0.75 kgf·cm elbow / 2.49 kgf·cm
shoulder pitch**, using the same proximal allowances as the
[previous wrist-load screen](servo-wrist-loading.md). Foot mass and added hand
reach are not yet defined, so these are comparisons, not new design loads.
Moving the rear motor mass from ankle toward knee can also reduce hip swing
leverage and, with thigh support, remove that mass from the knee's moving load.

The demanding servo cases now become walking support, uneven loading, deep
crouches and contact transfer. Losing a fourth supporting foot can raise loads
on the remaining limbs even though the robot is lighter. The
[advertised 30 kg·cm at 12 V](https://www.waveshare.com/product/modules/st3215-servo.htm)
is not a demonstrated continuous holding rating. Check actual mass/CoM,
current, temperature, motion tracking and printed-joint strength under the
revised contact loads before claiming walking capability.

## Size: separate standing height from driving height

Do not enlarge the robot to consume assumed motor surplus. Longer limbs
increase servo load, while additional mass also increases wheel-drive demand.
For a uniform increase from 450 to 500 mm, lever lengths grow **11.1%**;
with unchanged supported masses, corresponding gravity moments grow 11.1%.
For a hypothetical geometrically similar robot whose mass scales with volume,
gravity moments scale with length to the fourth power and rise **52.4%**.
Neither is a prediction of this mixed printed/fixed-hardware assembly.

The wheel relocation creates a stronger reason to revisit proportions:
**wheeled mode naturally becomes shorter.** With a wheel axle exactly at the
knee, Ø80 wheels and the existing dimensions, an idealized vertical maximum is:

`40 wheel radius + 85 thigh + 150 torso + 35 neck + 75 head = 385 mm`

This is a kinematic envelope, not a solved pose. A bent thigh or tilted torso
lowers it; axle offsets change it. The 90 mm lower leg no longer contributes
to wheeled support height when folded clear. Its knee servo no longer controls
ride height if the wheel is fixed to the thigh.

Retain the ~400–500 mm overall size intention while solving four-foot standing
and a lower crouched driving pose separately. A modest increase may be justified
by knee-drive packaging, foot reach or proportions, but motor torque alone is
not the reason. Do not simply lengthen the thighs to preserve the old 450 mm
wheeled height. Feet replacing Ø80 wrist wheels also remove their former 40 mm
radius contribution: choose hand reach/foot radius and reclose the stance.

Open work is OQ-16/17/18/19; no enlargement or replacement actuator is selected.
