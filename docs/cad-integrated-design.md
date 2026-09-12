# Integrated chassis — DEC-43 ankle wheels and front feet

**DEC-49/50 (2026-09-11)** implements the manufacturing refinement of the accepted
DEC-44 layout. Enclosing sockets, rounded/tapered fork roots and link transitions,
independent root modules, flat-section forearms and replaceable TPU contact pads
are production CAD. Common unbevelled carriers now serve all four roots;
the shared socket has distinct drive/idler recesses. [Part review and printability tags](part-design-review.md).

Every current print is `assumed` printable, supported by a declared orientation,
reviewed support access and a successful local slice of its exported STL.
[Slice records and layer images](design/manufacturing/README.md) are in the docs
structure. Nothing in this revision is physically printed, fitted or load-tested.
The unresolved head placeholder is omitted from structural CAD and the viewer.
The head position/mount, neck, protected battery/electronics installation,
harnesses and guards remain detailed design work.

## Geometry and part boundaries

- Upper arms **70 mm**, thighs **85 mm**, rear shanks **90 mm**, between joint
  centres. Forearms retain the **100 mm** elbow-to-contact-centre reach
  (75 mm forearm + 25 mm hand). The **Ø32 mm** contact envelope is now a separate
  rounded TPU pad; no wrist articulation is added.
- Each thigh/upper arm integrates its proximal fork, rounded spine, tapered
  transition and enclosing four-ear distal socket. The accepted pocket,
  measured ear positions and horn interfaces are preserved. Side-wall returns
  support the case, and the open end admits the servo Bottom first.
- Rear shanks retain integrated 37D face/body supports and open axial motor
  insertion. Forearms use an **18 × 17.9 mm** rounded rectangular shaft with a
  flat print face. A keyed post locates each TPU pad. An M3×20 recessed screw
  and washer retain it against a captive metal nut in the rigid forearm.
- All four roots use the same unbevelled front-style carrier: print two of
  each `root_carrier_left/right` variant, common flat back on the bed.
  Rear fixed pitch cases turn 90° about their lateral axes to clear this
  carrier upright. Their socket modules have an integral right-angle return
  to the torso flange; print with the socket floor down. The rear flange
  moves 5.885 mm into the torso (Z=46 mm), preserving fastener stacks and
  bolt/pin XY positions while clearing the carrier's back and screw heads.
  Torso and tray attachments follow the revised flange datum.
  The upper link's roll fork remains perpendicular to its elbow/knee socket.
- Each pelvis/shoulder mount is now **two independent socket modules**, with a
  0.6 mm plate separation. Secure all four servo ear screws on the bench, then
  attach each module to the torso with two accessible M3 frame bolts at body
  X=−30/−20 mm and Y=±34 mm. Ø4 × 2 mm integral torso pins engage Ø4.4 mm
  module pockets; the broad flat faces carry clamping loads. Modules can be
  removed independently; the earlier installed ear-screw obstruction does not
  require opening a neighbouring socket.
- The rigid torso preserves **150 mm** root spacing. Eight M3 through-bolts
  join its flanges to the four socket modules. A rounded removable tray and
  four spacers complete the current electronics carrier.

The chassis has **24 physical prints**: eight rigid limb segments, four
carriers, four root modules, two TPU pads, torso, tray and four spacers. The
acceptance rig remains two prints; four other generic coupons are separate.
There are **17 unique designs / 24 handed export variants** including coupons.

## Engineering changes to the skeleton layout

The rear geometry, 450 mm upright head-top target and Ø80 ankle wheels are
retained. The supported pose has front ball centres at (205, ±74.5, 16) mm,
rear wheel centres at (−55, ±110, 40) mm, and ground contacts at Z=0. Front
contact spacing is 149 mm; rear track is 220 mm. The longitudinal contact
spacing remains 260 mm, producing a trapezoidal support footprint.

A 75 mm forearm alone cannot replace the former wheel's 40 mm ground reach.
The forearm and TPU contact extend 25 mm beyond the wrist to the ball centre, whose 16 mm radius closes
the supported pose with 42.25° elbow flexion. Shoulder/hip heights remain
165/175 mm. The contact is a fixed, replaceable TPU pad, with grip and wear unverified.

The raised front ball centres remain 100 mm forward of the shoulder and
330 mm high in the upright review pose. Elbow flexion becomes 110.05° with the
100 mm effective lower limb. These are inspection poses, not a balance
trajectory. DEC-49 aligns both hip/shoulder roll-centre spacings at 149 mm;
pitch-servo centres remain 48 mm apart. Rear motor end gap remains 36 mm.

## Hip and shoulder axes — DEC-41 correction

DEC-40 attached its roll servos to the rigid torso. Pitching that torso into
quadruped turned their axes almost vertical: the resulting motion was yaw.
The earlier collision checks did not test the intended degree of freedom.

The physical chain is now **fixed lateral pitch → carried roll → knee/elbow
pitch**. The roll servo travels with the pitch carrier; its axis lies in the
sagittal plane perpendicular to the upper limb. A roll command therefore moves
the knee/elbow sideways in both saved poses. The axis tilts with upstream pitch;
it is not held world-horizontal through arbitrary motion. There is no yaw joint.

Both root axes intersect as geometric lines. The servo bodies sit at different
lateral positions: ±24 mm for pitch and ±74.5 mm for both hip and shoulder
roll. There is no added link length between their axes. The rear roll centres
move inward 0.1 mm per side to match the front print; motor-face offsets absorb
the change so wheel track stays 220 mm. The measured servo
interfaces and twelve-actuator budget are retained.

## Corrected servo interface

`servo_iface.py` uses the confirmed Gauge_0 **34.9 × 24.7 mm** pocket. The
four-ear saddle bosses reach the **31.8 mm** ear planes (+16.4/−15.4 in the
pocket frame), outside the centred widest case pads. M2 hole positions are
±10.25 mm laterally, 2.25 mm Back and 5.8 mm Front above the Bottom.
DEC-50 follows the pinned SO-101 socket: the drive slot is 14 mm wide from
the floor; the idler slot is 18.5 mm wide from 5 mm above the floor. Its
continuous lower seat separates the low M2 bores from the slot boundary,
removing the earlier tangency and the need for a widened relief. Ear planes,
hole centres and the Gauge_0 gap stay unchanged.
[Dimensioned slot views](design/so101/socket-slot-comparison.png).
Each M2×5 screw bears on a **2.2 mm** plastic seat, giving **2.8 mm nominal
penetration** into the servo ear. All four screws retain the servo itself.

Both horn contact faces are flat, **36.4 mm** apart; the old Ø20.5 recess is
removed. Each horn pad has a **3.5 mm web** and **Ø6.4 × 2.8 mm** head pockets,
for 6.3 mm total thickness. The Front centre clears the supplied pan head with
a cylindrical pocket and Ø3.2 access hole; the Back has a blind boss relief.
Neither centre is a conical screw-bearing seat.

The Back M3×6 square fixings use **OD6 × 0.5 mm narrow washers**, leaving
2.0 mm nominal engagement against the measured 2.1 mm tapped idler body.
Front square fixings retain 2.5 mm engagement. Procure those washers and check
actual clamping/bottoming on the rig; the nominal arithmetic does not establish
thread strength. Heads and washers are included in the assembled CAD envelopes.

The circular fork nose is Ø20.8; the tapered roots broaden farther from the pivot. Its web ligament outside each M3 bore is
about 1.7 mm at the narrowest radial point; the outer head-pocket rim is thin.
The compact shape clears the measured Back bay nominally, but connector plug
size, tolerances, wear and fork strength need the real rig. A plugged-in loom
and its flexing service loop are not modelled as accepted hardware.

The optional imported case's stale Back centre projection is removed locally
before composing the measured boss/horn stack. The retained ≤50 mm³ reference
fit screen applies **only** to a servo and its owning saddle, and only inside
its intended pocket contact region. It does not allow moving-part interference.
The fallback stepped case is checked separately; neither reference overrides
physical measurements or the confirmed SO-101 fit.

## Fasteners and assembly

The generated schedule in [bom.md](bom.md) covers all twelve joints and two
motor mounts. Candidate hardware stacks, before physical checks:

| Connection | Stack / access |
|---|---|
| Case ears | M2×5 through 2.2 mm seat; 2.8 mm nominal penetration |
| Front horn square | M3×6 through 3.5 mm web; 2.5 mm engagement |
| Back horn square | M3×6, 0.5 mm narrow washer, 3.5 mm web; 2.0 mm engagement |
| Torso flanges | M3×14, two 5 mm flanges, two 0.5 mm washers and 2.4 mm nut; about 0.6 mm protrusion |
| Motor faces | Six M3×8 through 5 mm face plate; 3 mm nominal engagement, bore depth unverified |
| Hub | 5 mm plate + 3 mm cap head + 0.5 mm clearance + 9.5 mm hub = 18 mm nominal stack |
| Front TPU pads | Recessed M3×20 and washer into a side-loaded captive M3 nut; key locates the pad; no printed thread |
| Tray | M3×25 through 4 mm tray, 4 mm spacer and 10 mm frame boss; washers and nut |

Fully secure each root servo into its separate socket module on the bench;
then locate and bolt the modules onto the torso. Fit all
four roll-servo ear screws in each carrier before fitting the upper link.
Fit each elbow/knee servo into its upper link before installing the lower
link. With its horns removed, the open end of the enclosing socket admits the servo without passing
a fitted horn through a closed collar. Fit the horns and centre fixing, then
seat the integral clevis and install its eight square fixings without pulling
the forks inward. Remove the driven link again for servo replacement.

Install motor bodies axially from inboard, followed by face screws, hubs and
wheels. The removable tray gives wiring access. Full harness routing, every
tool operation with real plugs, wheel/hub retention and child-safe covers
remain physical/detailed checks; nothing is attached with printed threads.

## Manufacturing and validation

Every exported variant is a valid STEP and a watertight positive-volume STL
within the 200 × 200 mm bed rule. The declared orientation is already applied
in the STL. The [part review](part-design-review.md) records support removal
for every design. All four carriers and the forearms have useful flat backs; the
orthogonal upper links and motor shanks use accessible local supports. The TPU
pad uses no support. Slice success establishes toolpaths, not physical quality.

The audit covers the measured interface, 19 rig angles, motor insertion,
frame contact and 62 complete assembly samples around the saved poses. A
separate fallback check uses the conservative caliper case. Root-module bench
screw access and insertion are checked separately from installed frame-bolt
access. Unit tests check the joint axes, solid/mesh integrity, fastening
schedule and TPU/rear-wheel ground contacts.

The viewer uses those same joint transforms. It searches the reachable interval
from the current configuration in **0.25° increments**, with **1° additional
reserve** before the first detected intersection. Changing a slider or body
pose recomputes the grouped bounds; all four limbs must clear. Geometry/hardware
and hidden parts still participate in the search. Servo cases use the
conservative caliper profile. For a servo's own coaxial fork, its circular
horns/centre reliefs are treated as the rotationally invariant interfaces
checked by the rig audit; the case remains an obstacle. Full nominal hardware
participates against other parts. The head placeholder is omitted; its unresolved placement does not constrain
carrier geometry or travel. Body-master head outlines show sizing intent only.

This is a finite-resolution mesh search, not continuous swept-volume proof.
The ±180° search ceiling is not a calibrated servo setting. Floor contact,
complete cables/guards, tolerances and loaded motion are not established by the
slider bounds. Initial limits have independent BREP endpoint checks recorded
in [travel-endpoints.json](design/manufacturing/travel-endpoints.json).

The static build includes geometry- and engine-hashed clearance caches so it
opens without repeating the full initial search. The browser recomputes changed
configurations in a worker; stale caches are rejected. This requires Node.js
when building, not when viewing the static site.

Continue physical acceptance with the new joint rig, a rear leg, the pair,
front limbs and loaded support/transition checks (OQ-12/13/17/18). Use actual
hardware masses and the material-specific slice estimates before revising servo
load or thermal claims.
