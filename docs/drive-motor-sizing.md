# Compact chassis drive-motor sanity check

**Superseded scope:** DEC-42/43 removed front wheel drives. Keep this
four-wheel assessment as comparison evidence; the current recommendation is
[rear ankle wheels and fixed front feet](cad-integrated-design.md). The second
37D pair this page advised against was already on order; it arrived 2026-09-11
and is surplus (DEC-51), not a front-drive purchase.

2026-09-10 — assessment for OQ-17, **not a replacement decision**. DEC-38's
four driven wheels remain settled; the current CAD still uses FIT0403 motors.

**Assessment:** four 37D units are a conservative, heavy baseline for the compact
robot. Smaller encoder gearmotors merit evaluation, especially at the wrists.
The reduction in standing size does not establish a reduction in finished mass:
use the existing **3 kg design ceiling**, not a measured weight. Rear motors must
also recover upright balance using only two ground contacts.

## Verified motor data

Manufacturer specifications checked 2026-09-10:

| At 12 V | Current DFRobot FIT0403 | Example candidate: Pololu 4846 |
|---|---:|---:|
| Gear ratio | 90:1 | 74.83:1 |
| Diameter | 37 mm | 25 mm |
| Face-to-encoder-cap length | 69 mm | 69 mm |
| Output shaft diameter | 6 mm | 4 mm |
| Mass per motor | 205 g | 104 g |
| No-load output speed | 122 rpm | 130 rpm |
| Advertised/extrapolated stall torque | 38 kgf·cm | 22 kgf·cm |
| Stall current | 7 A | 5 A |
| Four-motor mass | 820 g | 416 g |

Sources: [DFRobot specification](https://wiki.dfrobot.com/fit0403),
[DFRobot dimension drawing](https://dfimg.dfrobot.com/wiki/17480/FIT0403_gb37y3530-12v-90en_dimension_1.0.jpg)
(the retained CAD envelope), [Pololu 4846 specification](https://www.pololu.com/product/4846/specs).

Stall torque is not continuous torque. The reviewed FIT0403 specification does
not establish a continuous operating point. Pololu gives 3.3 kgf·cm at 110 rpm
and 0.87 A at maximum efficiency for its candidate; that is a performance point,
not an unconditional thermal rating. Its
[25D HP family guidance](https://www.pololu.com/category/186/12v-high-power-hp-25d-mm-gearmotors)
limits continuously applied gearbox load to 4 kgf·cm and intermittent torque to
8 kgf·cm, and recommends generally staying at or below 25% of stall current.
All constraints apply together; compare operating curves and duty cycle.

## First-order load calculation

Assumptions for a screening calculation, **not banked operating requirements**:
3 kg total mass, 40 mm wheel radius, 1 m/s² acceleration, rolling-resistance
coefficient 0.03, equal drive-force sharing and adequate tyre traction.

`F = m × (a + g sin(slope) + Crr × g cos(slope))`

`wheel torque = F × wheel radius / number of driving wheels`

| Accelerating case | Per wheel, four drives | Per wheel, two drives |
|---|---:|---:|
| Level surface | 0.039 N·m | 0.078 N·m |
| 10° incline | 0.090 N·m | 0.180 N·m |

These are wheel-output translation loads. They exclude rotating inertia,
gearbox losses when converting output load to current, steering scrub, carpet,
threshold impacts, unequal wheel loading and balance-recovery dynamics. The
incline/two-drive row is not a validation of upright balancing on an incline.
Requirements scale with actual mass and acceleration. Body height alone is not
in this rolling-load equation; it enters balance dynamics and mass distribution.

At Ø80 mm, the current motor's no-load speed corresponds to **0.51 m/s** at 12 V;
the example candidate gives **0.54 m/s**. Loaded speed and battery voltage reduce
that headroom. The existing gearing is not obviously excessive in speed.

## Packaging and limb consequences

Four current motors consume **27% of the 3 kg mass ceiling** before wheels,
hubs, mounts, twelve limb servos, battery and electronics. Changing only the
front pair to the example candidate saves **202 g**; changing all four saves
**404 g**, excluding changes in mounts/hubs/wiring.

Approximating motor mass at the wrist axis, a horizontal 75 mm forearm sees
**0.151 N·m** of elbow gravity torque from a 205 g motor alone; a 104 g motor
contributes **0.077 N·m**. With the whole 145 mm arm horizontal, corresponding
shoulder contributions are **0.292 / 0.148 N·m**. These are illustrative static
poses, not current-pose total loads or complete servo sizing. Wheels, printed
parts and dynamic acceleration add to them. Distal mass reduction also reduces
arm inertia for the same motion.

Smaller diameter does **not** necessarily fix track width: this particular 25D
candidate has the same 69 mm axial body length. A narrower chassis needs a
shorter motor or changed mounting arrangement and a new clearance assessment.
A swap also requires new motor plates/support rings, 4 mm hubs, shaft-stack
checks, encoder scaling and controller/current-limit tuning. It is not a
parameter-only diameter substitution.

## Recommendation and remaining selection work

Evaluate a roughly 100 g, 12 V encoder gearmotor in the 25D class before
ordering another pair of 37D motors. Pololu 4846 is a quantified comparator,
not a selected supplier or proof that this exact unit is optimal. Keep the
already bought rear pair available for initial balance experiments; lighter
front motors offer an incremental route, while four matching lighter units
would give the largest mass reduction.

Before committing: close the mass/CoM estimate; set speed, acceleration,
terrain and recovery requirements; assess torque-speed/current behavior at
battery operating voltage; check gearbox backlash, wheel-shaft radial/impact
loads and thermal duty. Demonstrate rear-pair balance recovery and four-wheel
steering/threshold performance. Revisit the chassis and BOM only after motor
selection. The present sanity check justifies reopening motor sizing, not
claiming acceptance of a smaller drive.
