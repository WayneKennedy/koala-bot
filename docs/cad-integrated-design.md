# Integrated chassis — DEC-43 ankle wheels and front feet

**DEC-49/50 (2026-09-11)** implements the manufacturing refinement of the accepted
DEC-44 layout. Enclosing sockets, rounded/tapered fork roots and link transitions,
independent root modules, flat-section forearms and replaceable TPU contact pads
are production CAD. DEC-53/55/56 subsequently replace the root modules and
rear carriers; the shoulders retain the DEC-49 carrier. The shared socket
has distinct drive/idler recesses. [Part review and printability tags](part-design-review.md).

**DEC-57/58, 2026-09-15:** the selected rear A/B proposal mounts the retained
pitch socket on a **45° inclined torso face** and keeps the DEC-56 carrier.
The [rear-leg review](design/rear-leg/README.md) uses that proposal; the main
assembly still uses the previous torso flange. The production thigh now has
a stepped, filleted roll yoke with unobstructed horn fixings and a knee case
clocked 90° about its shaft. The shank has an extended open knee fork and
filleted motor supports. The 85/90 mm centres, saved feet and 220 mm neutral
track remain unchanged. Local 1° solid-CAD samples clear ±30° thigh roll and
0–120° knee flexion. Full rear hardware checks and their scope are recorded in
the review; a locomotion trajectory has not been accepted.

The revised root modules, hip carriers, thighs and shanks are `unknown` printable;
the other parts retain their recorded `assumed` tags. Earlier revisions have
declared orientations, reviewed support access and local slices; those slices
apply only to the matching STL hashes.
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
- Each thigh/upper arm integrates its proximal fork and distal socket. The
  DEC-58 thigh uses the stepped roll yoke and sideways knee case described
  above; the upper arm retains its rounded spine and tapered
  transition and enclosing four-ear distal socket. The accepted pocket,
  measured ear positions and horn interfaces are preserved. Side-wall returns
  support the case, and the open end admits the servo Bottom first.
- Rear shanks retain integrated 37D face/body supports and open axial motor
  insertion. Forearms use an **18 × 17.9 mm** rounded rectangular shaft with a
  flat print face. A keyed post locates each TPU pad. An M3×20 recessed screw
  and washer retain it against a captive metal nut in the rigid forearm.
- **DEC-53 root module (2026-09-14) — one `root_socket` design at all four
  roots, handed, two per hand.** Plate faces the torso: 46.9 × 36.7 × 6 mm
  under the shoulder-style enclosing socket, the pelvis pair being the
  shoulder pair turned 180° about the pitch axis, so the pitch case stands
  into the torso at both roots. Four M3 nuts sit captive in the socket shelf
  under the servo Bottom (±10 mm along the axis, ±6 mm across; 5.7 AF × 2.6 mm
  pockets, 8.4 mm plastic under each) and the fitted servo traps them;
  M3×16 screws drive from the torso side through the flange, plate and
  shelf. All four ear screws are fitted on the bench (DEC-45 retained).
  No locating pins; the torso is expected to locate the plate outline
  (deferred, OQ-23). The rear flange returns to Z = 40.115 mm and the frame
  spans 46.1 to 103.9 mm. **The DEC-49 carrier no longer clears this
  module at the rear**: its back sits at the module's plate plane and its
  corners sweep 46 mm, so the saved upright pose intersects and quadruped
  pitch is capped near 42° until the carrier is re-derived (DEC-52, OQ-22).
  The carrier bullets below describe the export that still exists.
- **DEC-55 hip carrier** replaces the rear pair: body below the pitch axis,
  roll servo Bottom-down beside the pitch servo, roll centres 128.1 mm apart,
  flat back on the bed; the thigh's forks pass the roll socket (see DEC-55).
  **DEC-56** narrows the block to the 16 mm fork neck, adds tapered 2 mm
  inner-edge bevels, R6.3 fork-root and R5 socket-root fillets, plus R1.5 at
  the narrow socket lip. The horn pads and servo datums are unchanged.
  [Current carrier and validation](design/hip-carrier-refinement.json).
  The [45° socket-mount proposal](design/carrier-orientation/README.md) is
  held under DEC-57 and implemented in the separate rear-leg review. The old
  torso mount still limits the main assembly. Root clearance alone does not
  establish a gait.
  The shoulder pair is still the DEC-49 carrier (`shoulder_carrier_left/right`),
  common flat back on the bed, until DEC-54's chain replaces it. *(DEC-49
  text follows.)* The rear flange previously moved 5.885 mm into the torso
  (Z=46 mm) with rear cases turned 90° and right-angle socket modules;
  that arrangement is gone.
  The upper link's roll shaft remains perpendicular to its elbow/knee shaft;
  DEC-58 clocks the rear case around that unchanged knee shaft.
- The rigid torso preserves **150 mm** root spacing, shape deferred (DEC-53).
  Sixteen M3×16 root screws pass its flanges into the four socket modules;
  the front rails sit at X = 10–20 mm to clear them. A rounded removable tray and
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
roll in DEC-49; DEC-55 places rear roll at ±64.05 mm, while the front stays
at ±74.5 mm. There is no added link length between the intersecting axes.
Motor-face offsets absorb the rear spacing change so wheel track stays
220 mm. The measured servo
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
| Root modules to torso | M3×16 from the torso side through the 5 mm flange, 6 mm plate and shelf into a captive M3 nut under the servo (DEC-53); length to verify |
| Motor faces | Six M3×8 through 5 mm face plate; 3 mm nominal engagement, bore depth unverified |
| Hub | 5 mm plate + 3 mm cap head + 0.5 mm clearance + 9.5 mm hub = 18 mm nominal stack |
| Front TPU pads | Recessed M3×20 and washer into a side-loaded captive M3 nut; key locates the pad; no printed thread |
| Tray | M3×25 through 4 mm tray, 4 mm spacer and 10 mm frame boss; washers and nut |

Drop four M3 nuts into each root module's shelf pockets, fit the servo and
all four ear screws on the bench, then offer the module to the torso and
drive its four M3×16 from the torso side (DEC-53). Fit all
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
from the current configuration in **0.25° increments**, with **2° additional
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
slider bounds. [travel-endpoints.json](design/manufacturing/travel-endpoints.json)
records an earlier revision and does not validate the current root/carrier.
The earlier [DEC-56 checks](design/hip-carrier-refinement.json) found small
imported-STEP intersections at the then-displayed forward pitch minima.
DEC-58 increases the reserve to 2° and records separate
[rear-proposal endpoint checks](design/rear-leg/viewer-endpoints.json).
The old manufacturing endpoint report does not validate today's full chassis
or arbitrary slider combinations; continuous travel remains OQ-21/22.

The static build includes geometry- and engine-hashed clearance caches so it
opens without repeating the full initial search. The browser recomputes changed
configurations in a worker; stale caches are rejected. This requires Node.js
when building, not when viewing the static site.

Continue physical acceptance with the new joint rig, a rear leg, the pair,
front limbs and loaded support/transition checks (OQ-12/13/17/18). Use actual
hardware masses and the material-specific slice estimates before revising servo
load or thermal claims.

## Revision log

Dated notes on **unprinted** geometry, reclassified out of `decisions.md` by
DEC-59 (2026-09-18). Entries keep their original DEC numbers so existing
cross-references resolve; the full original text is in git
(`git show 82e4995:docs/decisions.md`). A note here is not accepted geometry:
it records what was tried, what triggered it, and what replaced it. An entry
leaves `unprinted` only when [`test-log.md`](test-log.md) records a print of
that revision. New CAD iterations go here, one entry each, never to
`decisions.md`.

- **DEC-37** (2026-09-08, engineering judgement authorised by the maintainer).
  Closed DEC-36's segment lengths into two poses: quadruped hip/shoulder axes
  175/165 mm, 260 mm wheelbase, 200 mm track, upright hip/shoulder 190/340 mm,
  head top 450 mm, passive wrist wheels. Track went to 220 mm in DEC-40; wrists
  were driven by DEC-38 and removed by DEC-43. Link lengths and the 450 mm
  target persist through DEC-43. Numbers: `params.py` `BODY_*`; masters in
  [`design/README.md`](design/README.md). Unprinted.
- **DEC-40** (2026-09-08, no maintainer trigger recorded). First integrated
  4×4 chassis replacing DEC-34: one print per segment, SO-101 four-ear saddles
  at all twelve servos, 150 mm torso, track 200 → 220 mm because the paired
  37D bodies collided upright, raised wrists moved to 100 mm forward / 330 mm
  high, 0.5 mm washers on the Back M3×6 fixings. Axis order corrected by
  DEC-41 the same day; front drives removed by DEC-43. Unprinted.
- **DEC-42** (2026-09-10, maintainer instruction; superseded by DEC-43 the
  same day). Wheels moved from the ankles to the rear knee area with separate
  folding rear feet; all front drives cancelled. The cancellation and the
  integrated forearms with fixed ball feet survive in DEC-43; the knee wheels
  do not. [Assessment](two-wheel-walking.md). Unprinted.
- **DEC-44** (2026-09-10, maintainer visual review of a render). "Layout
  accepted" at the DEC-43 numbers; the SO-ARM101 upper arm adopted as the
  construction reference (`IMG_7004`, [templates](design/so101/README.md)).
  Re-opened by DEC-52: joint centres are targets, not datums. Pitch → roll
  retained (DEC-41). Unprinted.
- **DEC-45** (2026-09-10, maintainer feedback). Paired pitch mounts split into
  independently removable socket modules so all four ear screws are reachable
  on the bench. Carried into DEC-53 (one module per servo, captive nuts).
  [Access evidence](root-servo-mounts.md). Unprinted.
- **DEC-46** (2026-09-10, maintainer instruction for the next viewer update).
  Viewer sliders show sampled mechanical-clearance ranges instead of ±5°;
  implemented in `mechanical_limits.js` with caches keyed by geometry and
  engine hashes. Ranges are CAD clearances, not loaded limits (OQ-21).
  Tooling, not geometry.
- **DEC-48** (2026-09-10, maintainer instruction). DEC-44 construction applied
  throughout: enclosing sockets, rounded links, flatter forearms, separate
  keyed TPU front pads with recessed fixings; DEC-47 tags assigned; local
  slices and layer images in [`design/manufacturing/`](design/manufacturing/README.md).
  Root parts replaced by DEC-53/55. Unprinted.
- **DEC-49** (2026-09-11, maintainer trial instruction). Front carrier tried
  at all four roots: rear cases rotated 90°, right-angle pelvis socket module,
  rear flange moved to Z = 46 mm, head placeholder removed from CAD. The trial
  produced the weak, unprintable pelvis socket (OQ-22, 2026-09-14) and the
  carrier that DEC-52 names as the wrongly fixed constraint. Replaced by
  DEC-53/55. Head removal stands (OQ-18). Unprinted.
- **DEC-55** (2026-09-14, maintainer choice between two rendered options,
  "option 2"). Hip carrier body below the pitch axis, roll servo Bottom-down
  beside the pitch servo, thigh forks as pads passing the roll socket, roll
  centres 128.1 mm. Viewer travel as committed: roll −3.5° to 9.75°,
  quadruped pitch −2.75° to 96°. Revised by DEC-56/58. Unprinted; strength
  unverified.
- **DEC-56** (2026-09-14, maintainer's marked-up viewer screenshot). Carrier
  block 24 → 16 mm, R6.3/R5 fillets after union, tapered 2 mm bevels. Did not
  resolve the forward-pitch shortage the maintainer raised; the imported STEP
  still intersects by 0.013–0.020 mm³ at the forward endpoints.
  [Image](design/hip-carrier-refinement.png). Unprinted.
- **DEC-57** (2026-09-15, maintainer approval of the socket-tilt viewer).
  Rear servo A socket on a torso face inclined 45° (body Y −45°), carrier as
  DEC-56, angled-fork carrier parked. Used only by the separate
  [rear-leg review](design/rear-leg/README.md); the main assembly keeps the
  earlier mount, so **two mounts coexist in CAD**. Inclined torso walls,
  indexing and loaded travel open (OQ-22). Unprinted.
- **DEC-58** (2026-09-15, assistant geometry following the instruction to
  progress outward from DEC-57). Thigh: stepped roll yoke because the knee
  shelf swept into the carrier; servo C clocked 90° about the knee shaft.
  Shank: open fork bridging 46 mm from the knee axis, filleted motor supports.
  Viewer reserve 1° → 2°. Radii and offsets live in `parts/links.py`. Local
  checks: ±30° roll, 0–120° knee. [Review](design/rear-leg/README.md).
  Unprinted; printability `unknown`.
- **2026-09-18 review** (owner, from the [rear-leg viewer](design/rear-leg/README.md)).
  Root socket module and hip carrier look right: tagged `assumed`. Thigh and
  shank: general geometry good, but as drawn they would need a lot of support,
  which would probably ruin the parts. Both stay `unknown`; the next revision
  of either must fix orientation or form before any slice. The owner expects
  the shank to be the easier fix. Basis: the owner's aesthetic judgement and
  printability instinct from the render, not a slice. Nothing printed.
- **2026-09-18 thigh orientation study** (assistant, geometry screen on the
  DEC-58 STL; [image and figures](design/rear-leg/README.md)). No lying or
  standing orientation gets below ≈48 cm³ of support because the C-yoke's
  cheeks are parallel cantilevers and the knee socket is offset to one cheek.
  **Proposals, unmodelled:** (1) stand the part on the knee socket and centre
  the socket under the bridge so socket wall and bridge face form one flat
  foot, which needs the DEC-58 carrier-clearance check re-run because C's case
  moves toward −Y; (2) if the socket must stay offset, fill under the bridge
  from the socket wall to the thin cheek with a 45° wedge (≈12 cm³ solid at
  16 mm yoke width) so the bridge is self-supporting standing up; (3) chamfer
  the fork steps to 45° so the forks print support-free on top. Interim with
  no CAD change: print flipped (thick cheek and socket wall down), which halves
  support and keeps it out of the pocket. Standing orientations put layers
  across the cheeks' bending load; strength unverified either way. Unprinted.
- **2026-09-19 thigh options modelled** (assistant, owner's instruction to model
  both and show them in the rear-leg viewer, left = option 1, right = option 2).
  Neither original proposal survived contact with the geometry: the knee socket
  is fixed by C's shaft so it cannot be centred, and a wedge under the bridge
  would sit where the case is. Modelled instead: **option 1** a one-print frame
  thigh standing on the knee socket (foot + bar close the knee end; C enters
  sideways); **option 2** a two-print thigh with a bolted drive-side cheek
  (lip over the bridge end, two M3 into captive nuts; body lies on the
  cup-floor plane). An outer lap plate on the cheek failed the 0–120° knee
  check at 117° and was removed. Record, screen and checks:
  [thigh-options](design/rear-leg/thigh-options/README.md). Main assembly and
  BOM unchanged. Unprinted; strength unverified.
- **2026-09-19 option 3 chosen direction** (owner, from the viewer). One print:
  option 2's body form with the drive-side cheek kept in the same part, and the
  step from the thickened cheek to the idler pad replaced by one flat taper
  along the owner's red line (`THIGH_CHAMFER_Z`). To be printed on the
  cup-floor plane with tree support, which the owner trusts from SO-ARM101.
  Modelled on both legs of the rear-leg viewer; record and checks in
  [thigh-flat](design/rear-leg/thigh-flat/README.md). Slice pending the
  printer (plate 1 running). Unprinted; strength unverified.
- **2026-09-19 shank motor inset** (owner, from the viewer). The DEC-58 shank's
  outer print face has a 2.25 mm step between the motor-mount face and the
  drive fork; the owner asked for the motor to move inboard by that step so
  the face is one plane (`SHANK_MOTOR_INSET`, `option_shank_flush`). Track
  220 → 215.5 mm and motor gap 36 → 31.5 mm follow if adopted; carried in the
  rear-leg viewer's option 3 mode with the moved motor stack, not yet in the
  main assembly. [Record](design/rear-leg/thigh-flat/README.md). Unprinted.
- **2026-09-19 thigh v2, shank v2, rounding pass** (owner: "final pass for
  these legs"). The tapered one-piece thigh and the flush-faced shank become the
  production `thigh` and `shank` (v2 in `part-versions.json`), with DEC-60
  making the flush face fall out of the spacing rather than a motor inset.
  Every straight convex square edge of at least 8 mm outside the fork pads,
  joins, knee cup pocket, motor face and ring is filleted R2 (cup outer edges
  R1.5) by `links.round_convex_edges`; edges the kernel refuses stay sharp and
  are counted in the build log. Both print faces are the flat planes chosen
  above: thigh on the cup-floor plane with tree support, shank on its outer
  face. Tagged `assumed` on the owner's judgement of the forms; the rounding
  itself is unreviewed. Unprinted; sliced when the printer is free.
- **2026-09-19 45° rear mount into the main assembly** (owner). DEC-61 banks
  DEC-57's proposal: the tilt moves into the rear pitch-socket placement and
  the torso's rear flange becomes the inclined face. Torso v2 also carries
  DEC-60's spacing. The rear-leg review's own tilt and face patch are removed.
- **2026-09-19 torso rebuilt as box + bracket** (owner rejected the first
  DEC-61 torso in the viewer: the rotated flange cut head pockets through the top
  rails, ran the 45° plate far too high into the planned battery space, and
  looked dumb; "revert to a cube, with an additional 45° block on the rear face,
  lower, more or less where the sockets mounted before"). Torso v3: the DEC-60
  box unchanged, plus a bracket under the rear face carrying the inclined 5 mm
  pelvis plate (the flange plane rotated about the pitch axis with the modules,
  clipped to the torso footprint) on two 3 mm side gussets, open at the back so
  the module screws and their driver reach the plate. Multi-view render
  ([image](design/parts/torso_frame-views.png)), judged before the rebuild:
  **does it look stupid? No.** Frame contact and screw-path audit pass.
  Unprinted.
- **2026-09-19 pad-completeness test narrowed** (assistant). The v2 rounding
  pass takes R2 off the fork arms' outer corners (22 mm³ on the shank between
  6.6 and 10.4 mm from the horn axis); `test_rear_links_keep_complete_horn_pads_and_driver_paths`
  now protects the arms' inner 12 mm core, every seat and web, and still runs
  the head and driver checks. Part versions are ledgered in
  `hardware/part-versions.json` with a placement-invariant fingerprint compared
  within tolerance (0.5 mm³, 0.1 mm), so rigid shifts such as DEC-60's do not
  count as changes.
