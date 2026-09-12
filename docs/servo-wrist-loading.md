# ST3215 loading with driven wrists

**Superseded scope:** DEC-42/43 removed front wheel drives. Keep this
four-wheel assessment as comparison evidence; the current recommendation is
[rear ankle wheels and fixed front feet](cad-integrated-design.md).

2026-09-10 — preliminary load screen for OQ-16/17. **Assessment:** retain the
12 V ST3215 limb servos. The present short arms appear compatible with lifting
and gentle gestures even with the 205 g wrist motors. Sustained holding,
dynamic motion and body-support loads remain unverified; this is not physical
acceptance or a reason to increase servo size now.

## Inputs and conservative airborne load estimate

Upper arm 70 mm, forearm 75 mm, from the current body master. Per arm:

| Item | Screening mass | Basis |
|---|---:|---|
| FIT0403 motor | 205 g | Manufacturer; [drive assessment](drive-motor-sizing.md) |
| Ø80 wheel including tyre | ~20 g | [Pololu 1430](https://www.pololu.com/product/1430/specs): 0.7 oz per wheel |
| 6 mm hub | 6.8 g | [Pololu 1999](https://www.pololu.com/product/1999/specs): single hub, excluding screws |
| Integrated forearm/motor mount | 49 g | Current generated BOM, solid-PETG maximum; no slice/weighing |
| Distal horns, fasteners and wiring | 20 g | Unweighed allowance |
| **Distal assembly used in calculation** | **320 g** | ~301 g subtotal rounded upward |

For an intentionally conservative gravity screen, lump the entire 320 g at the
wrist axis. The real forearm print and proximal hardware are closer to the
elbow, so this overstates their moment. It is an estimate, not a guaranteed
upper bound on an eventual assembly with guards and a completed harness.

Using `torque (kgf·cm) = mass (kg) × horizontal lever (cm)`:

- **Elbow, horizontal forearm:** `0.320 × 7.5 = 2.40 kgf·cm` (0.235 N·m).
- **Shoulder pitch, horizontal extended arm:** distal contribution
  `0.320 × 14.5 = 4.64 kgf·cm`. Add an elbow servo (55 g at 7 cm), upper-arm
  print (34 g at assumed 3.5 cm), 15 g upper-link hardware at 7 cm, and a
  root allowance of roll servo + carrier + hardware (55 + 37 + 15 g at an
  assumed 4 cm gravity lever): **5.68 kgf·cm** total (0.557 N·m).

Print masses are current BOM solid maxima. Servo mass uses the repository's
55 g nominal value; hardware masses and their centres require weighing. These
are lever-arm screening configurations, not claims of collision-validated
full extension. Shoulder roll also needs checking when the arm is abducted:
its carried parts differ from pitch, and its gravity moment changes with both
pitch and roll. The distal extended-arm contribution can be of the same order;
roll cannot be declared unloaded from the sagittal drawing.

Replacing only the 205 g motor with the previously compared 104 g motor, while
holding every other allowance fixed, reduces this screen to **1.64 kgf·cm at
the elbow and 4.21 kgf·cm at shoulder pitch**. New mounts/hubs could change those
figures. Motor gravity torque roughly halves; total joint load does not.

## Servo capability and operating limits

[Waveshare's 12 V ST3215 specification](https://www.waveshare.com/product/modules/st3215-servo.htm)
advertises up to 30 kg·cm at 12 V. The reviewed source does not establish a
continuous holding rating. Our 2.4 / 5.7 kgf·cm static estimates are about
8% / 19% of that advertised maximum; these ratios are **not thermal margins or
safety factors**. Do not treat 30 kg·cm as permission to hold that load.

Moving adds inertia torque (`I × angular acceleration`), particularly on abrupt
starts, reversals or stops. Battery sag, friction and gearing affect available
performance; sustained holding produces heat even without visible movement.
The printed fork ligaments and screw interfaces require their own acceptance.
A stronger motor alone would not prove those structures adequate.

## Ground contact is a different load case

At the saved quadruped pose, a 3 kg robot with equal vertical wheel reactions
has 0.75 kgf at each contact. The front contact is 55.33 mm ahead of its shoulder
and 50.83 mm ahead of its elbow. **Ground-reaction contributions alone** are
therefore 4.15 kgf·cm at shoulder pitch and 3.81 kgf·cm at the elbow. If one front
contact carries half the robot's weight instead, these become 8.30 / 7.63.
These are illustrative load shares, not a measured distribution or complete
inverse statics: link gravity must be combined with its correct sign, and
horizontal tyre forces, inertia, roll-axis moments and impacts remain absent.

Thus lifting the wrist is not presently the main reason to question the
ST3215 choice. Validate one complete arm's gravity holds and slow gestures
with current, temperature and position tracking at the intended supply voltage;
then validate body-support and transition cases. Lighter wrist motors improve
inertia, heat demand and impact loads even if the present servos can lift them.
