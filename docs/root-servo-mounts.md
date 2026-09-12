# Paired pitch-servo mounting access — DEC-45

The maintainer identified a real assembly defect: **each fixed pitch servo
blocks the retaining screws of its sibling**. This affects both the pelvis
and shoulder crossmember. Installing the servos before the carriers, as the
previous assembly notes suggested, does not resolve the mutual obstruction.

## What the DEC-43 CAD showed

The pitch-servo centres are 48 mm apart. The DEC-43 printed saddles left
only **3.1 mm** between their closest exterior walls. A straight driver probe,
using the current M2 head-clearance diameter and extending 40 mm outward from
each inboard screw seat, intersects the opposite servo and crossmember at
**all eight inboard ear screws** (two per servo, four servos).

[Measured results](design/so101/root-access-study.json) record each case. The
sibling-servo intersection is approximately 308 mm³ per probe. This tests
ordinary straight access; it is not a search for special right-angle tooling.
Removing the first servo to reach the second simply exchanges the problem.
The existing assembly collision pass did not test these installed driver paths.

## The SO-101 reference

`Under_arm_SO101.step` and `Motor_holder_SO101_Wrist.step` supply a useful
**cradle plus removable holder** pattern. The two source files share native
assembly coordinates. The [comparison image](design/so101/split-socket-reference.png)
and [STEP references](design/so101/README.md) preserve their original surfaces.
This is a justified installation/service seam, consistent with DEC-39.

The important property is that part of the socket can be installed separately.
A literal copy of the wrist sleeve is not yet a solution: if the final assembly
still requires tightening screws towards the centre gap, those screws remain
blocked. Split placement and assembly order must address the actual access.

## Adaptation to the four fixed pitch servos

**Selected direction:** split each paired crossmember into **separate left and
right servo-socket modules**. There are two modules at the pelvis and two at
the shoulders. Each module can enclose its servo using the SO-101 upper-arm
construction, since all its ear screws are accessible on the bench. A two-piece
socket remains an option where insertion requires it; separate inboard retainers
are no longer the primary proposal.

The intended sequence is:

1. Fit each servo into its own socket module on the bench and secure all four
   ear screws while every side is accessible.
2. Locate the module on the rigid torso frame using positive alignment features
   that preserve the accepted joint centres and pitch → roll arrangement.
3. Secure it with structural fasteners accessible outside the servo footprint.
4. Fit the neighbouring module independently, then the pitch carriers. The
   removal sequence must not require access through the neighbouring servo.

The frame remains the common structural connection between left and right.
Locating/bearing surfaces transfer module loads into it; the structural bolts
retain that engagement. Use real metal nuts/threads for new structural fixings.
Do not assume the existing frame-hole locations give tool or screw-head access
with a servo installed: that must be designed into the new interface.

## Implemented — DEC-48/49/50

Production CAD now has four independent enclosing socket modules. Each pair
has a 0.6 mm plate gap. Two M3 frame bolts per module sit outside the case at
body X=−30/−20 mm and Y=±34 mm. Ø4 × 2 mm pins on the torso engage Ø4.4 mm
blind module pockets; broad flat faces carry the clamping load.

All four ear-driver approaches are checked on an isolated module; the
conservative case can enter along the open socket axis. The installed frame
bolt-head approaches clear both sockets and the servo bodies. Root bolts/nuts
are included in the assembly's hardware envelopes. The inboard ear screws
remain intentionally serviced on the bench, after removing that module.

DEC-49 turns the rear cases 90° about their pitch axes to clear the common
front-style carrier upright. Each pelvis socket has an integral right-angle
return to the frame flange, raised 5.885 mm to Z=46 mm to clear the carrier
and frame screw heads. Bolt/pin XY positions and clamping stacks are retained.
Its socket-floor face goes on the bed;
the shoulder module retains its flat-frame-face-down orientation. Both pockets
open upward when printed. DEC-50 makes the drive/idler recesses unequal.
The modules remain `assumed` printable, with local slice evidence. Physical support removal, tool use,
fit and loads remain to be checked. [Current assembly and fastening details](cad-integrated-design.md).
