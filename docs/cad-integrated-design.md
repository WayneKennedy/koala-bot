# Integrated chassis — current CAD and acceptance scope

**2026-09-21: interchangeable footed rear shanks for the first walking build
(DEC-62).** `foot_shank` v1 fits the existing knees and accepts the unchanged
front TPU pad. The wheeled `shank` v2 remains available. See the
[walking build, files and checks](design/walking/README.md).

**2026-09-19: recessed roll-first shoulders and front limbs derived from the rear
printability work.** This is an **unprinted revision**, recorded below rather
than banked as a decision. The torso extends around the shoulder A servos;
removable cassettes preserve bench access to the unchanged, physically proven
`root_socket` v1. Front shoulders now implement **roll → pitch → elbow**;
rear hips retain **pitch → roll → knee** and the DEC-61 inclined rear mount.

The chassis uses **28 physical prints walking / 26 wheeled**, from
**19 designs / 28 handed export variants** including six coupons and both
rear-shank alternatives. Changed torso, shoulder cassettes,
front links and corrected thigh are `unknown` printable. Root socket v1 is
`proven` with its recorded ear-hole support caveat; unchanged hip carrier v1
and shank v2 retain their recorded `assumed` status.
[Per-part versions and print approaches](part-design-review.md) ·
[Front revision, images and local clearance evidence](design/front-redesign/README.md).

## Geometry and part boundaries

- **Torso v5:** the hip-to-shoulder axis separation stays **150 mm**. Its cage
  now reaches body Z = **183.5 mm** around shoulder A; the side envelope is
  Y = ±47 mm. Dorsal rails remain at X = −46…−36 mm and taper laterally
  from Y = ±43 to ±29 mm over Z = 106…122 mm, opening the shoulder roll
  sweep. Ventral rails step from X = 10…20 to 26…36 mm below the shoulders. The body frame uses X dorsal
  negative, Y lateral and Z along the spine.
- **Recessed shoulders:** A roll centres are **110.23 mm apart**. The enclosing
  socket lips sit at Y = ±37 mm, **10 mm inside** the torso's ±47 mm side
  envelope. This measurement describes the socket lip: the servo's output
  region, horns and moving carrier still project outside it. It is an open
  structural cage, not a flush cosmetic shoulder skin.
- **Independent `shoulder_mount` v1 cassettes:** each carries one root socket
  on its original four M3×16 screws. Fit those on the bench, then mount the
  cassette through the front of the torso with four M3×20 screws into captive
  nuts. Broad flange contact and an R1.5 internal root connect the recessed
  module to the ventral frame. Either side removes independently.
- **`shoulder_carrier` v3:** the A fork and enclosing B socket share one broad
  print plane. B is **40 mm outboard of A**, placing the pitch centres
  **190.23 mm apart**. R6.3 fork roots and straight inner-ear driver tunnels
  preserve access without a hidden support chamber.
- **`upper_arm` v2:** **70 mm** pitch-to-elbow centres, with parallel B/C shafts,
  an enclosing elbow pocket and thickened cup wall coplanar with the outer
  drive fork face. R6.3 fork roots and R2 outer rounding follow the rear
  lessons. Seven short/narrow junction edges reject R2 and are explicitly
  reported as sharp; fitting faces and the accepted servo interface remain.
- **`forearm` v2:** **100 mm** elbow-to-contact reach (75 + 25 mm), a longer open
  elbow fork, R6.3 roots, an R3-rounded taper and a broad flat native −Y print
  face. The existing keyed **Ø32 mm TPU pad**, captive nut and recessed
  M3×20 screw/washer interface remain; no wrist joint is added.
- **Rear:** 85 mm thighs, 90 mm shanks, two bought 37D ankle drives and
  **220 mm track** remain. Hip pitch centres stay **52.5 mm apart** (DEC-60).
  Thigh v3 fixes the rounding implementation without changing joint datums;
  shank v2 retains its flush motor/fork print face. The rear pitch sockets
  mount on the retained **45° plate** (DEC-61). Torso v5 adds Ø6.6 clearance
  corridors through the retained flange for straight Ø6 rear screw drivers.
- **Walking rear alternative:** `foot_shank` v1 retains 90 mm from knee to
  contact centre and uses `front_contact_pad` v1, with no drive motor, shaft,
  hub or wheel. The pads sit on the shanks' centreline: **132.6 mm rear contact
  spacing** at neutral roll. The 220 mm track applies to wheels. Both
  configurations use the same knee horns and upper chassis; exchange the
  complete shanks, then select/calibrate the matching kinematics and mass model.
- **Neck provision:** a dorsal shoulder-cap slot and four generic M3 mounting
  points reserve a removable cartridge for the **three small bought STS3032M**
  servos. Published small-case envelopes are shown; purchased M dimensions,
  fixed-lead boards, retention and 3-RPS linkage geometry remain unverified.
  [Source dimensions, interface and limits](design/neck-provision.md).

The unchanged electronics tray and four spacers remain. The two new shoulder
cassettes account for the increase from 24 to 26 chassis prints. The neck
reference envelopes are neither printed parts nor an accepted head installation.

## Poses, axes and silhouette

The separate **walking** reference keeps the supported torso/front limb pose
and rear contact X = −55 mm, but lowers the rear ball centres to Z = 16 mm
and re-solves the knees for 85/90 mm links. All four TPU contacts meet Z = 0.
This is a standing CAD reference for training, not a demonstrated walking gait.
The two wheeled poses below remain unchanged.

The supported reference retains front contact centres at X/Z = **205/16 mm**
and rear wheels at **−55/40 mm**. With unrolled shoulders, front contact spacing
now follows the **190.23 mm** pitch spacing; rear track remains 220 mm and
longitudinal contact spacing 260 mm. Upright, the front contacts retain the
100 mm forward / 330 mm high reference. These are inspection poses, not a
loaded transition or controller targets. The **450 mm upright head-top** figure
remains a sizing allocation.

Front A rotates about the torso's longitudinal axis. Its downstream B pitch
joint and elbow follow that rotation; pitch and elbow axes remain parallel.
Rear A instead rotates about the lateral pitch axis and carries B roll.
The assembly and viewer therefore use different transform orders for the two
limb pairs. Their left/right halves remain mirrored. The optional sideways
"hug elbow" is not implemented; the current sagittal elbow preserves supported
foreleg shortening, with the alternative still tracked in OQ-25.

The torso and cassette multi-view review finds a compact cage, broad rails,
a shallow chest step and inward socket flanges, with no outriggers or disconnected
features: **an acceptable structural prototype**. V5's inward dorsal taper
narrows the upper back without adding depth or a backpack. Front parts pass their
individual visual review. [Assembled views](design/front-redesign/body-views.png)
also retain compact depth, with front shoulder span near the rear wheel span
and deliberate front/rear differences. The head is still a sizing allocation;
this is structural-prototype review, not a finished shell or gesture acceptance.

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

The generated [BOM fastening schedule](bom.md) is authoritative for quantities.
Candidate stacks still require real clamping, engagement and tool checks.

| Connection | Stack / access |
|---|---|
| Case ears | M2×5 through 2.2 mm seat; 2.8 mm nominal penetration |
| Drive horn square | M3×6 through 3.5 mm web; 2.5 mm engagement |
| Idler horn square | M3×6, 0.5 mm narrow washer, 3.5 mm web; 2.0 mm engagement |
| Root socket to rear torso / front cassette | Four M3×16 through 5 mm flange and the unchanged socket plate/shelf into captive nuts |
| Front cassette to torso | Four M3×20 per side, driven from the front into cassette captive nuts; Ø6 straight driver paths |
| Motor faces | Six M3×8 through 5 mm face plate; 3 mm nominal engagement, bore depth unverified |
| Hub | 5 mm plate + 3 mm cap head + 0.5 mm clearance + 9.5 mm hub = 18 mm nominal stack |
| Front TPU pads | Recessed M3×20 and washer into side-loaded captive nut; keyed location |
| Tray | M3×25 through 4 mm tray, 4 mm spacer and 10 mm frame boss; washers and nut |

1. **Preload all four M3 frame nuts into each bare front cassette before
   attaching its A root.** The fitted root blocks the straight loading path
   of the two inner nuts. Hold the nuts in place during bench assembly.
2. Drop four M3 nuts into each root socket, then install A and all four ear
   screws on the bench. For a front limb, bolt that complete root to the
   preloaded cassette with four M3×16, offer the cassette to the ventral
   crossmembers and install four front-access M3×20. For a rear limb, mount the root directly
   to the inclined flange; its driver corridors pass through the complete torso.
3. Fit B and all four ear screws to its carrier before installing the upper
   link. Fit C and all four ear screws to the upper link before the lower link.
   Insert cases Bottom-first with horns removed. Install horns/centre fixings,
   then clevis square fixings without pulling the forks inward.
4. Insert each footed lower link's captive nut before fitting the keyed TPU pad.
   For walking, fit a handed `foot_shank` at each rear knee using the same
   drive/idler horns, square screws, centre retention and idler washers as
   `shank`. For the wheeled build, install rear motors axially from inboard,
   then their face screws, hubs and wheels. Exchange whole shanks with the
   robot supported and power isolated; the knee servos stay in the thighs.

Servo replacement requires removal of its driven link. Front root service
removes the four frame screws and slides the cassette **laterally outward**
to expose its bench screws; pulling rearward eventually hits the dorsal rails.
No driver is expected to pass through the opposite A servo. Harness routing, actual plugs, retention and
child-safe guards remain detailed/physical checks.

## Manufacturing and validation

The [current validation record](design/cad-validation.json) links the final
versions, exports, slices and scoped checks.

Each changed print has a deliberate broad bed plane and externally accessible
support removal; [part review](part-design-review.md) records the details.
[Current local slices and selected layers](design/front-redesign/README.md#local-slicing-and-support-review)
cover all 11 changed handed exports, including torso v5. Inspected layers show
broad bases and trees in open forks/cups and through the torso cage. They do
not prove every layer start or physical support removal. These parts remain
`unknown` and are **not physically proven**. Existing slices apply only to
their recorded STL hashes: the sliced thigh v2 does not validate corrected
thigh v3. OQ-22 records earlier shank v2 organic slices with hashes matching
the current exports; their G-code and layers were not re-reviewed in this
session's 11-slice batch. Older manufacturing-report shank slices predate v2.

The [complete front moving-package report](design/front-redesign/driven-package-clearance.json)
checks outward-positive shoulder roll **±30° at 2° intervals**, in both saved
pitch/elbow configurations, including all moving front prints/cases/fixings
against fixed A/module/cassette hardware: 2,604 solid pairs per pose, no overlap.
The [installed-front report](design/front-redesign/installed-front-clearance.json)
checks both fronts at five roll settings against the torso, neck envelopes,
opposite front and nominal rear hardware with both case models: 20 configurations,
1,236 candidate pairs, no hits. Narrower adjacent-joint/rail checks and their
limits remain in the [front record](design/front-redesign/README.md).

For the **2026-09-19 wheeled revision**, the 65-test Python suite, 26 handed exports, two assembly STEP exports and
11 current-version review slices pass. Both complete nominal poses pass
180 checked pairs each. The [62-sample primary audit](design/front-redesign/assembly-audit.json)
and [two-pose fallback audit](design/front-redesign/assembly-audit-fallback.json)
pass. The main browser smoke test and
[all initial grouped-slider endpoints](design/front-redesign/viewer-endpoints.json)
pass (24 configurations / 1,452 pairs across both case models). The
[rear production review](design/rear-leg/README.md) also passes both browser
poses, all 12 initial bounds and four combined configurations; its exploratory
−45° quadruped pitch collision is outside the current viewer bound. The frame audit includes the actual torso in rear
driver checks and distinguishes front bench root fixings from installed
cassette fixings; service tests enforce loading cassette nuts before A.

The **2026-09-21 walking addition** brings the suite to 71 passing tests,
28 handed exports and three assembly STEP configurations. Both new shanks
have version/hash-matched local slices; nominal primary/fallback audits,
31 nearby walking samples and 12 walking viewer-endpoint checks pass.
[Walking evidence and its limits](design/walking/README.md).

The viewer uses the same serial joint orders as the assembly, samples
pose-dependent clearance in **0.25° increments**, and reserves **2°** before the
first detected collision. Hidden structure and hardware still constrain travel.
Caches are keyed by geometry and engine hashes; Node.js is needed to build them,
not to view the site. The unresolved head geometry is omitted. This finite
mesh search does not prove continuous motion, calibrated servo travel, cable
clearance, ground contact or loaded balance. Historical manufacturing/viewer
endpoint reports apply only to their own revision. Current validation outcomes
are recorded with the [front revision evidence](design/front-redesign/README.md).

Continue with support removal, fitting and load/creep on the actual parts;
head/neck, battery/electronics and loaded transitions remain OQ-17/18/21/22.
No new repeat SO-101 fit gauge is required.

## Revision log

- **2026-09-21 footed rear shank v1 — unprinted.** Implements DEC-62 with a
  separate `foot_shank`, 90 mm from knee axis to TPU ball centre. The long
  open fork retains the knee's horn span, bores, head recesses and driver
  access. The shared front lower-link construction is shortened at its taper
  and terminal seat; `forearm` v2 and `front_contact_pad` v1 geometry stay
  unchanged. No motor ring or drive hardware is included. The same pad key,
  captive nut and recessed M3×20/washer fasten the rear TPU pad.
  **Visual gate:** inspected iso, side, end and top in
  [four views](design/parts/foot_shank-views.png) before export/audit/viewer.
  Does it look stupid? **No:** it reads as the front foot's shorter counterpart,
  with a continuous tapered shaft, open knee fork and useful broad print face;
  no redundant motor bracket remains. This is assistant shape review, not
  physical acceptance. Printability starts `unknown`.

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

- **2026-09-19 recessed roll-first front revision and review corrections**
  (owner instruction, autonomous CAD development; **unprinted**). Front A now
  rolls about the spine; B and C have parallel pitch shafts. Torso v5 extends
  around A to Z183.5 with 10 mm socket-lip recess, retaining 150 mm root spacing.
  New removable shoulder cassettes v1 keep unchanged root sockets v1 bench
  serviceable; front carrier/upper arm/forearm become v2 with broad print planes,
  open support access and rounded load paths. Thigh v3 corrects the rounding
  bug; rear root driver corridors now include the torso. Geometry fingerprints
  gain internal-feature locations and updates reject version decreases;
  [four defect corrections](test-log.md#2026-09-19--four-cad-review-defects-corrected-digital-only).
  A dorsal cartridge interface reserves three **small STS3032M** neck servos;
  actual mounting/linkage remains open. **Does it look stupid? No at individual
  part review:** torso/cassettes form a compact cage with broad rails, a shallow
  chest step and inward flanges; front links have continuous printable forms.
  Assembled views also retain compact depth and deliberate front/rear forms;
  the head and loaded gesture acceptance remain unresolved.
  Changed parts are `unknown`, not physically proven. Current dimensions,
  views and the scoped 1° local checks: [front record](design/front-redesign/README.md).
- **2026-09-19 torso v5 clearance correction within the front revision**
  (assistant audit finding; **unprinted**). Torso v4 cleared the nominal pose
  but its upper dorsal rails clipped the moving front carrier at **+1° roll**.
  Nominal/static clearance was insufficient. V5 tapers those rails from
  Y±43 to Y±29 over Z106…122 while preserving X−46…−36, the 94 mm outer width,
  82 mm maximum depth and 10 mm socket-lip recess. Neck-cartridge mounts move
  +10 mm in X to (−28, +2) × Y±30 so the screws exit into open space rather
  than the upper rails. V4's local slice is superseded by a hash-matched v5
  slice; inspected layers show trees through the open cage. The scoped ±30°
  roll rail sweep clears all 12 moving front-chain solids at 2° samples in both
  poses. The final 62-sample primary and two-pose fallback audits pass;
  the main browser smoke test and all initial grouped-slider endpoint checks
  pass. The rear production viewer and its endpoint checks are refreshed and pass.
- **2026-09-19 shoulder carrier v3, B offset 35 → 40 mm** (assistant viewer
  finding; **unprinted**). The B35/v2 carrier's local joint tests and small
  full-assembly samples passed, but the full upper-arm/A-case sweep stopped
  at about **+6° roll**. B40 moves the pitch centres and unrolled front contacts
  to **190.23 mm** spacing, leaving A spacing 110.23 mm, recess 10 mm and torso
  v5 unchanged. At the examined ±28/29/30° roll samples in both saved poses,
  the conservative A-case separation improves from 0.765 mm (B39 upper fork)
  / 1.065 mm (B39 horn head) to **1.765 / 2.065 mm** with B40. These are sampled
  component clearances, not loaded or continuous travel limits. The upper arm
  and forearm remain v2; carrier geometry becomes v3. Final exports, matched
  slices and views are regenerated; the complete-package and installed-front
  reports pass within their stated sampled scope, as do the final 62-sample
  primary and two-pose fallback audits. Browser/rear-viewer refresh remain
  separate from those checks.
