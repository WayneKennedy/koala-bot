# Banked Decisions

Committed decisions with rationale. Unresolved items live in
[`open-questions.md`](open-questions.md). Format: `DEC-nn - decision - why`.

**CAD implementation caveat:** both lower-body drafts are discarded (DEC-30).
The [review of revision a3f265c](cad-review.md) found assembly defects and
insufficient manufacturing/strength validation; DEC-29 replaced that geometry
but breached DEC-21 in a different way. DEC-24's historical claim that the
build proves support-free printing is not established by its area heuristic.
DEC-23/26/27/28/29 describe intent and lessons, not accepted geometry. The
redesign is governed by [`cad-restart-brief.md`](cad-restart-brief.md);
acceptance remains open as OQ-13.

**2026-09-08 measurement update:** DEC-34's implemented socket and digital pass
are superseded by the [impact assessment](cad-measurement-impact.md). DEC-40 implements the corrected interface and replaces its geometry;
physical acceptance remains open.

- **DEC-51 — koala-bot keeps one TB9051FTG and its rear 37D pair; the four-wheel
  hardware is surplus to the family** (2026-09-11, maintainer report). The second 37D
  pair and two more Dual TB9051FTGs, ordered for DEC-38's four driven wheels, arrived
  2026-09-11 — after DEC-43 had cancelled the front drives. koala-bot's allocation is
  unchanged: two 37D 12 V 122 rpm motors + encoders at the rear ankles and **one**
  driver (DEC-16). Of the rest, one driver is wk-devastator's outright — the loan of
  2026-09-07 is dissolved, nothing is returned, and the two robots can now be in drive
  bring-up at once (its DEC-13, amended) — and one driver plus the two motors are an
  unallocated pool, tabulated in
  [wk-robotics `common.md`](https://github.com/WayneKennedy/wk-robotics/blob/main/docs/common.md#drive-motors-drivers-and-mcus-in-hand) with a candidate use on its idea bench. An
  unallocated **Teensy 4.1 NE** arrived the same day and sits in the same pool; it is
  the no-cost fallback for OQ-14 but not reserved for koala. **Resolves OQ-15**: no
  second driver needs buying. Order date, supplier and price of the extra parts are not
  recorded; the motor and driver part numbers match the 2026-09-01 Pi Hut order.

- **DEC-50 — Preserve unequal drive/idler socket slots** (2026-09-11,
  maintainer correction). The raised drive-side case plane is narrower than
  the idler-side plane. The pinned SO-101 Upper arm socket has a **14 mm drive
  slot from the floor**, and an **18.5 mm idler slot starting 5 mm above it**.
  Apply those distinct profiles in the shared socket primitive. Retain the
  accepted 34.9 × 24.7 mm pocket, measured ear planes and four screw datums.
  Remove the earlier assumption that both faces use the Back pad width. The
  continuous lower idler seat also removes the old bore/strip tangency without
  widening its slot. Fallback collision geometry must preserve this asymmetry.
  [Interface evidence](design/so101/socket-slot-comparison.png).

- **DEC-49 — Use the front carrier at all four limb roots, without its bevel**
  (2026-09-11, maintainer trial instruction). Export one common carrier design,
  two prints per hand: `root_carrier_left/right`, four installed carriers.
  Both roll-centre spacings become 149 mm; each rear centre moves inward 0.1 mm
  and its motor-face offset grows 0.1 mm, retaining 220 mm wheel track.
  A direct substitution clears quadruped but intersects the old pelvis socket
  and pitch case upright. Rotate each fixed rear case 90° about its existing
  lateral pitch axis, pointing the case forward in the torso frame; use an
  integral right-angle socket module. Move the rear mounting flange from
  Z=40.115 to 46 mm in the torso frame, retaining bolt/pin XY positions and
  fastener stacks. This leaves over 2 mm between the common back's radial
  envelope and the frame screw heads; the earlier flange obstructed pitch
  travel near upright. Update torso/tray datums together. The socket floor
  is the print bed face. Pitch → roll, limb
  lengths and the saved sagittal poses remain intact. Validate the resulting
  assembly and print approach; physical acceptance remains open.
  Remove the head placeholder from structural CAD/viewer and collision checks.
  Head position and mounting are undecided; the 450 mm overall sizing target
  remains an allocation, not a solved head installation.

- **DEC-48 — Manufacture the accepted layout with enclosing sockets and rounded
  links; separate TPU front contacts** (2026-09-10, maintainer instruction).
  Apply the DEC-44 construction principles throughout the CAD, implementing
  DEC-45's independent root modules and DEC-47's per-part printability tags.
  Preserve joint centres, axis order, rear ankle drives and saved poses. The
  forearms may be flatter in section; use a separate, replaceable TPU ground
  contact on a keyed seat with a recessed fixing and captive metal nut.
  Preserve the agreed hand reach and rounded ground envelope. Every current
  print requires a credible orientation/support approach before being labelled
  assumed; successful physical prints alone can establish proven. Local
  slicing and manufacturing records accompany the revised exports. Refresh
  the viewer with printability tags and DEC-46 mechanical travel searches.
  [Current part review](part-design-review.md) and
  [manufacturing evidence](design/manufacturing/README.md).

- **DEC-47 — Track printability for every printed part** (2026-09-10,
  maintainer instruction). Each part has `printable = unknown | assumed | proven`.
  Default to unknown; assumed requires a reviewed print approach, proven a
  recorded successful print of the relevant revision. Reassess after changes;
  shared socket fit or an earlier revision does not prove a new whole part.
  The [part review](part-design-review.md#printability-tags--dec-47) holds the
  per-part tags and definitions, including coupons and separate candidates.
  These tags do not assert assembly access, fit, strength or loaded operation.

- **DEC-46 — Viewer sliders expose the CAD mechanical travel** (2026-09-10,
  maintainer instruction for the **next visualizer update**). Replace the
  arbitrary ±5° inspection ranges with conservative clearance bounds derived
  from the current printed parts and modelled servo/hardware envelopes.
  Bounds depend on body pose and the other joint positions; update them when
  those change. Use the reachable interval from the current configuration,
  stopping before interference rather than jumping across a blocked interval.
  Any grouped control must respect the limits of every joint it moves.
  Label these as CAD mechanical-clearance ranges, not validated loaded servo
  limits. Regenerate bounds when geometry changes. Current viewer remains
  unchanged until that update; determination/validation of bounds is OQ-21.

- **DEC-45 — Separate left/right pitch-servo socket modules** (2026-09-10,
  maintainer feedback and refinement). Each fixed pitch servo blocks its
  sibling's inboard ear screws in the current pelvis and shoulder crossmembers.
  Split each paired mount into **two independently removable socket modules**:
  two at the pelvis and two at the shoulders. Fully fasten each servo into its
  own socket on the bench, then attach the modules to the common rigid torso
  frame using accessible structural fasteners and positive locating surfaces.
  Preserve joint centres, pitch → roll order and all four ear screws per servo.
  This is an installation/service seam justified by DEC-39. Exact module/frame
  interfaces and fastener access remain OQ-20; existing hole positions are not
  automatically accepted. The SO-101 under-arm/wrist-holder pair remains a
  useful optional socket-level construction pattern, not a requirement for
  another removable wall within every module. Current production mounts are
  not yet revised. [Access evidence and assembly intent](root-servo-mounts.md).

- **DEC-44 — Overall layout accepted; refine the manufactured parts** (2026-09-10,
  maintainer visual review). Bank DEC-43's overall geometry as the device
  layout: 450 mm upright head-top height, 150 mm torso, 220 mm rear track,
  70 mm upper arms, 75 + 25 mm forearm/hand reach to Ø32 mm fixed front feet,
  85/90 mm rear legs and the bought rear ankle-drive pair. Preserve joint
  centres and both saved poses while reviewing construction; this accepts the
  layout, not present part detailing or physical strength/printability.
  Replace the boxy treatment with the SO-ARM101 upper arm's construction
  principles: enclosing servo-base sockets, broad connected fork roots,
  rounded exposed edges and a deliberate build face. The maintainer's
  `IMG_7004.HEIC` is the reference; exact upstream STEP sections are retained
  as [templates](design/so101/README.md). Review every structural part and the
  associated coupons before propagating a revised interface. Friction fit
  locates/supports the case; retain the four ear screws for positive retention.
  No repeat SO-101 fit gauge is required (DEC-33). Following the roll-first
  discussion, the maintainer accepts retaining **pitch → roll** (DEC-41):
  upstream pitch can reorient the roll assembly as the torso changes pose.
  Roll remains relative to the upper limb; ground alignment requires coordinated
  pitch control, not passive stabilization. Orthogonal link construction
  remains the manufacturing task (OQ-20). [Part critique](part-design-review.md).

- **DEC-43 — Keep rear ankle wheels; build V1 with fixed front feet** (2026-09-10,
  maintainer instruction). Retain the bought pair of 37D drives and Ø80 wheels
  at the rear ankles, with the existing integrated shanks. Supersede DEC-42's
  knee-wheel relocation and separate folding rear feet: the packaging detour
  is deferred to keep progress towards a working robot. Retain its cancellation
  of front drives and its integrated forearms with fixed rounded feet.
  Keep twelve ST3215s, hip/shoulder pitch → roll, knee/elbow pitch, 85/90 mm rear
  links, 150 mm torso, 220 mm rear track and 450 mm upright head-top baseline.
  Front geometry retains 70 mm upper arms and 75 mm elbow-to-wrist length;
  add 25 mm hand reach to the centre of a fixed Ø32 mm ball, all one print
  with the elbow forks. Front contact centres remain 260 mm ahead of the rear
  wheels in supported stance, and 149 mm apart. No replacement motors,
  enlargement or additional drive hardware is required.
  V1 focuses on supported stance using front feet and rear wheels, then
  foreleg lift and rear-wheel balance/drive. Walking on uneven ground with
  wheel-feet remains experimental; four walking feet with wheels clear are
  no longer a V1 requirement. Contact transitions, traction and loaded duty
  remain to be demonstrated. [Implemented design](cad-integrated-design.md).

- **DEC-42 — Four walking feet, two knee-area wheels (knee provisions superseded by DEC-43)** (2026-09-10,
  maintainer instruction and clarification). Retain the bought pair of 37D
  geared/encoder motors and Ø80 wheels as the **only wheels**, relocating
  them from the ankles to the rear knee area. Each rear lower leg ends in a
  separate foot: lower the legs for quadruped standing/walking with all wheels
  clear of the ground; fold the lower legs up to permit wheel contact in the
  crouched balancing/drive pose. Abort all wheeled forelimbs. Each forearm is
  one integrated limb ending at wrist/hand reach in a fixed rounded ball foot;
  no caster or active wrist joint is requested. Preserve hip/shoulder
  pitch → roll, knee/elbow pitch and the twelve ST3215 limb actuators.
  Supersedes DEC-31's ankle wheel location and DEC-36/37/38/40's front wheels.
  Intended transition: establish rear-wheel contact, unload/fold the rear feet,
  unload/lift front feet and establish balance on the rear pair; the exact
  contact sequence and trajectory need design. Four-foot walking does not
  require locked wheels as ground contacts. Power-off standing remains unproven.
  Wheel axle offset, thigh-versus-shank carrier ownership, folded-foot clearance,
  ground-contact geometry and gait/transition loads remain OQ-17/18/19.
  Two wheel-drive channels/encoders suffice; cancel additional front motors,
  wheels/hubs and drive-channel procurement. Existing CAD/viewer and generated
  printed BOM still depict DEC-40/41 until revised. The ~400–500 mm overall
  size goal remains; walking/standing and crouched driving heights must be
  distinguished. No enlargement or replacement motors/servos are banked.
  [Motor, servo and scaling assessment](two-wheel-walking.md).

- **DEC-41 — Hip and shoulder pitch precede roll** (2026-09-08,
  maintainer correction). DEC-40 fixed its first roll servo to the pitching
  torso: its axis became nearly vertical in quadruped, producing yaw instead
  of limb abduction. Correct the physical chain to **torso → lateral pitch →
  roll → knee/elbow pitch → wheel**. The pitch servo is retained by the
  crossmember; its integral carrier holds the roll servo. Roll is perpendicular
  to the upper limb in its sagittal plane, so it moves the knee/elbow sideways;
  its orientation follows the upstream pitch joint. It is not a separately
  stabilized world-horizontal axis. The upper limb has perpendicular proximal
  roll forks and distal knee/elbow saddles, still one print per segment.
  Pitch-servo centres are 48 mm apart. Move roll centres 7 mm farther out on
  each side (hip 149.2 mm, shoulder 149 mm) to clear the fixed root saddles;
  adjust the integrated motor mounts to preserve the 220 mm wheel track.
  Hip and shoulder carriers have different pitch-fork/bridge arrangements to
  clear the fixed cases and head in both poses. Keep all link lengths, 450 mm
  height, four drives and twelve limb servos. This supersedes DEC-40's axis
  order, carrier geometry and root-axis spacing. Validate physical servo-axis
  alignment and lateral motion explicitly, as well as collision clearance.

- **DEC-40 — Implement the integrated 4×4 chassis** (2026-09-08).
  Replaces DEC-34's structural builders and frozen viewer with the compact
  four-limb CAD under DEC-36/38/39. Each segment and orthogonal carrier is one
  print; all twelve servos use the SO-101 four-ear saddle. A rigid 150 mm torso
  joins integrated pelvis/shoulder crossmembers with real service seams.
  Keep 70/75 mm front and 85/90 mm rear links, Ø80 wheels and 450 mm upright
  height. **Revise track from 200 to 220 mm**: inward roll caused the paired
  37D motor bodies to collide in the narrower upright assembly. Neutral motor
  end gap becomes 36 mm; rear pitch-axis spacing becomes 135.2 mm, shoulders
  remain 135 mm. **Move raised wrists from 60 to 100 mm forward and from 350 to 330 mm
  high**, to clear the folded elbow and retain motor/head clearance during
  combined joint adjustments. These are
  explicit engineering revisions to DEC-37/38, not changes to servo fit.
  Correct the measured flat horn/ear datums, supplied head pockets and Back
  centre/bay clearance. Add 0.5 mm OD6 narrow washers to the Back M3×6 square
  fixings for 2.0 mm nominal engagement; verify the stack on the rig.
  Local supports and a two-print saddle/clevis rig replace the old flat-piece
  export strategy. The user authorizes replacing the static review scene with
  this CAD. Implementation, assembly and validation scope:
  [cad-integrated-design.md](cad-integrated-design.md). Head/neck, complete
  electronics/battery packaging, continuous loaded motion and physical
  acceptance remain open; a digital export does not settle them.

- **DEC-39 — Integrated SO-101-style limb structures** (2026-09-08,
  maintainer feedback). Default to **one structural print per link**, taking
  `Upper_arm_SO101` and `Under_arm_SO101` as the construction reference:
  both proximal horn forks, their bridge/spine and the distal mounting
  structure form one part. For upper arms/thighs the distal feature is the
  next servo's cradle or SO-101 elbow-style saddle; for forearms/shanks it
  is the wheel motor mount/support. A separate collar or service retainer
  is allowed where installation requires it. Do not split forks, crossbars
  and motor plates merely to print every face flat. Choose orientation
  against the load path and accessible support removal; local removable
  support is acceptable. Keep the ≤200 × 200 mm bed rule, PETG, real
  fastening hardware and measured servo fit. All actual seams need a
  specific assembly, service, strength or bed-size justification.
  This supersedes DEC-23/25/29/34's blanket decomposition, one-feature-face
  and flat-cheek prescriptions, and the mandatory separate collar at every
  joint. The four-ear retention and double-horn support requirements remain;
  this does not waive insertion, screw access, slicing or physical load checks.
  Why: the earlier response to printing defects created unnecessary seams,
  fasteners and assembly work. [Part strategy and upstream evidence](integrated-links.md).

- **DEC-38 — Powered wrist wheels: V1 is 4×4** (2026-09-08, maintainer
  instruction). Drive all four Ø80 wheels, including both wrists; reverses
  DEC-37's passive front wheels. Keep twelve limb servos and add two wheel
  motors and two independently controlled drive channels: four of each in
  the complete robot. Use the same 37D 12 V geared/encoder envelope as the
  rear drive for the front design baseline; the extra hardware is not yet
  bought. Reassess distal arm load, current, wiring, driver placement and
  mass/CoM with all four drives. Dimensions and standing-height targets stay
  as DEC-37. Lower the raised-wrist review position from 360 to **350 mm**
  above the floor: front motor envelopes then clear the head underside by
  **6.5 mm**, rather than intersecting it by 3.5 mm. The master now includes
  all four motor envelopes; this is nominal clearance, not a swept check.
  Upright balancing still uses rear ground contact; front motors must be
  controlled appropriately when those wheels are airborne. OQ-17 tracks
  the remaining drive implementation and acceptance.

- **DEC-37 — Resolve the conceptual dimensions into two closed poses**
  (2026-09-08, engineering judgement authorized by the maintainer). Preserve
  DEC-36's 70/75 mm front and 85/90 mm rear links, 150 mm torso, 35 mm neck
  and Ø80 wheels. Use quadruped hip/shoulder axes at **175/165 mm**, a
  **260 mm wheelbase**, and **200 mm track**. Upright hip/shoulder heights
  become **190/340 mm**, with the head envelope ending at **450 mm**.
  Head packaging envelope: **85 × 110 × 75 mm**, including ears in its height.
  The conceptual 240 mm shoulder height exceeds the front leg's 185 mm
  straight reach; 165 mm retains elbow bend. A 120 mm track makes the two
  bought 69 mm motor bodies overlap by 64 mm; 200 mm gives **16 mm end gap**
  with the existing direct-drive hub stack. Adopt approximately **340 mm**
  nose–rump length rather than forcing the 340 mm dimension chain into 330.
  Wrist wheels are **passive**, on 6 mm steel axles, two radial bearings per
  wrist and metal axial retention; rear wheels retain the two purchased
  drive motors. No extra motor channel or active wrist joint is added.
  These choices resolve the drive-split and contradictory-dimension questions
  raised in DEC-36; detailed housings, servo placement, load transfer and
  the rise trajectory remain design work under OQ-17/18.
  **Drive update:** DEC-38 supersedes the passive wrists and raised-wrist
  position; DEC-39 governs part integration. The retained geometric choices
  and [schematics and STEP masters](design/README.md) derive from one joint
  model, with checked link closure, floor contacts and motor separation.
  They do not establish a printable mechanism, swept clearance or physical
  acceptance. The detailed redesign proceeds pelvis first against this master.

- **DEC-36 — Four wheel-ended limbs and compact koala proportions**
  (2026-09-08, maintainer instruction). Put **Ø80 mm wheels at both wrists
  and both ankles** in V1: four wheels, with no hands or feet in this baseline.
  Adopt the general shape and approximate dimensions of the maintainer's
  GPT-prepared [multi-view](<inspiration/Koala schematic.PNG>) and
  [side-view](<inspiration/Side on.PNG>) drawings: large head, compact torso,
  short folded rear legs, front limbs usable as forelegs and arms; quadrupedal
  and upright configurations, with **~450 mm upright standing height**.
  Nominal segments: upper arm/forearm **70/75 mm**, thigh/shank **85/90 mm**,
  shoulder-to-hip torso **150 mm**, neck **35 mm**, head length/height
  **85/75 mm**, hip-to-rump envelope **70 mm**. Other envelope targets and
  conflicting annotations are in [`body-layout.md`](body-layout.md);
  `params.py`'s `BODY_*` constants are the dimensional source.
  Why: the 100/100 mm links and compressed upper-body allowance of the earlier
  schematic produced a long-legged silhouette unlike the intended koala.
  Supersedes DEC-32/34's body proportions, deck/track packaging targets and
  the 433/483 mm backdrop proposals; extends DEC-31's ankle wheels to the
  front limbs. Keep the proven SO-101 interface basis and the existing
  twelve limb-servo allocation. The drawing legends do **not** add wrist/ankle
  articulation, neck yaw or a jaw actuator to the DOF budget.
  Wrist drive and conflicting envelope annotations were initially open;
  **DEC-37 resolves them** using the maintainer's delegated engineering judgement.
  Detailed wrist mounting and body mechanisms remain OQ-17/18. Segment lengths
  govern the next layout, rather than silently becoming longer limbs.
  The current CAD/viewer remains a frozen DEC-34 review specimen until revised
  joint by joint, beginning at the pelvis; this decision is not a CAD acceptance.

- **DEC-35 — `blake` is the reference workstation; the CAD viewer is always
  on there** (2026-09-08). The viewer runs as a user systemd service on blake
  (`hardware/systemd/koala-viewer.service`, linger enabled) behind Tailscale
  Serve at `https://blake.tail13a0c0.ts.net:8443/`. The ad-hoc instance and
  serve config on `ivory` are removed. Why: one canonical, always-reachable
  view of the working tree for the maintainer and every harness, instead of
  stale ad-hoc servers on two machines — two were found on 2026-09-08 serving
  discarded geometry. The scene is rebuilt only on service (re)start; it does
  not track edits live.

- **DEC-34 — New six-servo lower-body prototype with explicit packaging and
  fastening** (2026-09-07). Replace every old structural builder. Use the
  shared SO-101 cradle/collar and double-horn clevis at roll, pitch and knee;
  100 mm thigh and shank, direct-drive ankle wheels, hip/knee nominal 15/30°.
  Track was designed as 239.5 mm on the incorrect 37.5 mm span; current code
  derives 238.2 after the measured 36.4 span and asymmetric face shift. Final
  track awaits interface correction; nominal deck height is 283.2 mm, with 150 mm reserved above
  it (433.2 mm total). Adopt ±5° roll and −10…45° hip as the prototype's
  inspection range, trading the DEC-32 wider targets for this packaging;
  knee target remains 0…90°. Pitch sits 70.115 mm forward and 34 mm outboard
  of roll to make the socket and carrier fasteners accessible. This is a
  recorded compactness tradeoff, not an optimum. The initial implementation
  used a **flat idler seat** because a recess collided with its then-current
  case reference, retaining a 0.8 mm drive recess. That rationale and drive
  recess are superseded by the measured flat horn faces and proud centre
  features in `soarm-joint-pattern.md`. Registered through-bolted crossbars and
  separate motor plates replace the old friction cap and thigh/motor seams;
  threaded structural connections use metal nuts. No new physical fit or
  strength is claimed. Requirements, load calculations, assembly sequence,
  tests and outstanding gates: [`cad-restart-design.md`](cad-restart-design.md).

- **DEC-33 — Reuse the confirmed SO-101 servo fit; remove the caliper/PETG
  gauge prerequisite** (2026-09-07, maintainer instruction). The standard
  ST3215 servos fit the SO-101 parts in **both PLA+ and PETG**, confirmed by
  the maintainer during this restart. Proceed with the Gauge_0 pocket and
  upstream printed-part interface dimensions without another gauge print or
  caliper gate. `SOCKET_CLEAR = 0` applies to that nominal pocket only;
  generic `CLEAR_POCKET` remains separate. Lug offsets and the 37.5 mm horn
  span retain **upstream CAD** provenance, not invented caliper readings.
  New cradle/collar/clevis geometry still needs the single-joint rig fit,
  layer inspection and load tests before acceptance. Supersedes restart
  brief §6 steps 0–1 and the equivalent prerequisites in OQ-12/13.
  **Partly reversed 2026-09-08:** the first caliper reading taken anyway found
  the adopted 37.5 mm horn span wrong by 1.1 mm (measured 36.4, test-log). The
  37.5 was a probing error in `soarm-joint-pattern.md`, which the part STEP
  itself contradicts; upstream's CAD stands. The lesson holds either way: a
  number nobody has put a caliper on is a candidate, and the remaining
  horn-stack figures are being measured one by one.

- **DEC-32 — Establish quantitative restart design targets before structure**
  (2026-09-07). Size against the DEC-15 upper mass of **3 kg**. Evaluate
  two-wheel stance (half the weight per leg), fore/aft acceleration and
  braking at **0.5g**, a **2g total-weight load on one wheel** for structural
  testing, a **10 N lateral shove at the head-top allocation**, and lifting
  the full robot by the torso (legs hanging; powered holding is not assumed).
  These are chosen engineering test targets, not measured service loads or
  safety ratings. Clearance-study targets: hip pitch −30…+45°, knee 0…90°,
  roll ±10°; supported crouching follows hip = knee/2 with equal links.
  Desired nominal deck height **~300 mm**, upper-body height allocation
  **150 mm**, preferred wheel track **≤240 mm**. Link lengths, socket/hip
  offsets and achievable track remain OQ-16 until packaging checks; initial
  100 mm equal links are a study candidate. Why: both discarded drafts
  omitted this step. Reproducible analysis and exclusions:
  [`cad-restart-design.md`](cad-restart-design.md). An advertised servo
  torque comparison does not establish continuous duty or structural strength.

- **DEC-31 — Rear legs: articulating knees, wheels as feet** (2026-09-07;
  supersedes DEC-17 and the knee-wheel clause of DEC-07). Each rear leg is
  hip roll + hip pitch (STS3215) → thigh → **knee pitch (STS3215, active in
  V1)** → shank → **drive wheel at the ankle position, acting as the foot**
  (37D motor + hub + Ø80 wheel, DEC-19). No ankle DOF in V1. Overall size
  (DEC-15) and the rest of the skeleton (DEC-07/08) are unchanged. Why: the
  knee was deferred "gated on need"; the maintainer has decided the need is
  now — a leg that ends at the knee cannot crouch, stand or step, and a wheel
  at a knee reads as a wheel, not a foot. Cost: two more STS3215 joints, so
  the **twelve bought units cover twelve joints with no spare** (6 arm, 4 hip,
  2 knee); the knee servo's torque margin and the motor's placement in the
  shank are OQ-16. Concept, roadmap and BOM updated to match.
- **DEC-30 — CAD restart: discard both lower-body geometries, keep the
  tooling, hand over with a brief** (2026-09-07). The a3f265c and DEC-29 part
  builders are deleted rather than patched; `params.py`, `servo_iface`,
  `fasteners`, the export/audit/printability/viewer/slice tooling, tests,
  coupons and docs are kept. Why: both drafts were designed around unmeasured
  hardware and around a servo model rather than the proven SO-101 printed
  parts, and each pass patched the previous one; a third patch would inherit
  the same inputs. The restart is sequenced measure → requirements →
  envelopes → structure → single-joint rig, per
  [`cad-restart-brief.md`](cad-restart-brief.md), which is the handover to
  the harness doing the design (the maintainer has assigned GPT Astra). The
  first artefact is a servo socket primitive built from
  [`soarm-joint-pattern.md`](soarm-joint-pattern.md) and used at every joint.
  Old geometry stays recoverable at `a3f265c` and `4fc188a`.

- **DEC-29 — FDM-oriented lower-body prototype** *(geometry discarded by DEC-30; lessons stand)* (2026-09-06, authorized after
  the CAD review). Integrate pelvis and roll roots; remove bracket mounting
  flanges. Replace enclosing hip links with flat roll cheeks, an open pitch
  saddle and removable case cap. Replace thigh/motor-clamp seams with flat
  twin cheeks and through-bolted compression spacers; the outer cheek mounts
  the motor face directly. Keep rounded, tapered profiles without sacrificing
  flat bed faces. Supersedes DEC-23's universal insert/key prescription for
  these joints, DEC-24's proof claim, DEC-25's upright-fork print prescription,
  and DEC-26/27's old packaging numbers. Track increases to 258.8 mm, stance
  becomes 268 mm; this width/motion tradeoff remains prototype evidence, not an
  optimum. [Design, assembly and validation record](cad-redesign.md).
  Physical fit, clamp friction, fastener engagement, sliced layers and strength
  remain unverified; sampled nominal collision tests are not motion limits.

- **DEC-01 - Koala-inspired family; V1 = self-balancing wheeled companion.** The
  koala/primate body plan serves both "companion with personality" and "locomotion
  showpiece"; a lovable mascot suits an open-source / video audience.
- **DEC-02 - V1 is ground-based; climbing is a later sibling.** Wheel-vs-gripper at a
  limb-end is a hard fork; splitting it across family members beats compromising one
  body. A front-arm winch-haul clamber stays possible if grippers are fitted.
- **DEC-03 - Two-tier compute: real-time MCU + Pi 5 (ROS2/LLM).** The balance loop MUST
  run on the MCU (Linux is not real-time). See [`architecture.md`](architecture.md).
- **DEC-04 - micro-ROS bridge; the topic contract is the shared-brain backbone.** Define
  the topics once; every family member inherits the nervous system.
- **DEC-05 - Heterogeneous actuation; DOF budget = cost budget.** STS3215 bus servos for
  limbs, micro servos for the head, geared DC for drive. Spend STS3215-grade money only
  where weight/balance flow through.
- **DEC-06 - Single ~12 V (3S) rail for motors + servos; 5 V buck for the Pi.** Drives the
  servo-voltage choice -> **12 V STS3215** (unified rail, more torque, less bus current).
  Power integrity is treated as first-class.
- **DEC-07 - V1 morphology:** front limbs 3-DOF x2 (dual-purpose arms/forelegs); rear leg
  **hips 2-DOF x2, active in V1** (lean-into-turns while the torso is rigid); rear
  **knee-wheels** (2x DC) *— superseded by DEC-31: 1-DOF knees, wheels at the ankles*; **3-RPS head** (3 micro servos + CF pushrods) with **yaw
  delegated to the mobile base**.
- **DEC-08 - Torso: a single 3-DOF parallel platform** (not two stacked, not 6-DOF). Cuts
  actuators 6->3 (cost + mass, and mass sits high on the pendulum). **Rigid struts in V1**;
  pelvis & shoulder-girdle interfaces pre-designed to accept the 3 actuators later.
- **DEC-09 - PETG; every part <= 200x200 mm; parametric code-CAD.** Design to the commonest
  bed for reproducibility; `build123d`/`CadQuery` so body-is-source-code.
- **DEC-10 - Tri-licence:** CERN-OHL-S-2.0 (hardware), MIT (software), CC-BY-SA-4.0
  (docs/models). See [`../LICENSING.md`](../LICENSING.md).
- **DEC-11 - Vertical-slice discipline:** finish V1 end-to-end (design->print->BOM->
  firmware->app->docs->video) before starting the family.
- **DEC-12 - Mechanical honesty (banked from an InMoov build):** no plastic-on-plastic
  sliding threads; real bearings / rotary-servo+pushrod / metal leadscrews; low-friction
  spherical bearings. A 3-RPS neck *can* be strut-less (virtual pivot) but pays in coupled
  motion (3 actuators) or actuator count (6).
- **DEC-13 - Modelling split:** URDF+RViz for serial chains; CAD motion study for the
  parallel torso/neck (URDF can't hold closed loops); Gazebo/PyBullet for physics.
- **DEC-14 - Prototyping fab:** the maintainer's calibrated Creality Ender-5 S1 running
  Klipper is the reference printer, driven headlessly - PrusaSlicer CLI on the printer's
  Pi over Tailscale (OrcaSlicer on the desktop only when a print needs tuning). The BOM's
  filament and time figures are measured through that pipeline, not estimated.
- **DEC-15 - Size: ~40-50 cm tall; audience is young children (grandkids, 2-5).** A "big
  toy" *smaller than the child* - approachable, non-intimidating. Cascades: lighter robot
  (~1.5-3 kg) so limb/drive torque headroom is generous; a shorter inverted pendulum is
  slightly twitchier to balance, mitigated by the koala's high CoM. Makes **child-safety a
  hard requirement** (concept.md principle 7; OQ-10). Resolves OQ-01.
- **DEC-16 - Motor driver: Pololu Dual TB9051FTG** (resolves OQ-07). At the ~1.5-3 kg mass
  from DEC-15, its 2.6 A cont / 5 A peak per channel is comfortable and the current-sense
  output is a bonus. Wired to the Teensy as a breakout (form factor moot; soldering fine).
- **DEC-17 - Rear leg architecture** *(superseded by DEC-31: knees are active in V1 and the wheel moves to the ankle position)* (resolves OQ-02). 2-DOF hip-to-pelvis; the 12V drive
  motor sits **in the thigh** with the **wheel at the outer knee**, in constant ground
  contact. The V1 leg **ends at the knee** (no shin/foot). The knee is designed as an
  **expansion interface** to later accept a lower leg + foot + servo - but this is
  **deferred and gated on need**: pure wheeled locomotion may prove sufficient, weighed
  against the complexity of an articulated foot. So V2 walking is *conditional, not assumed*.
- **DEC-18 - MCU: Teensy 4.0** (resolves OQ-05). Ordered; a 600 MHz Cortex-M7 gives ample
  headroom for the balance loop. ESP32 / RP2040 remain valid cheaper/wireless variants.
- **DEC-19 - Drive/balance base parts confirmed; wheel diameter locked.** Pololu 80x10 mm
  wheels + Pololu 6 mm universal hubs (matched set for the 37D 6 mm D-shaft), Adafruit BNO085
  IMU (fusion, I2C), TB9051FTG driver, 2x 37D motors, Teensy 4.0. **Wheel diameter = 80 mm is
  a fixed control constant** (odometry + balance). Full BOM in [`sourcing.md`](sourcing.md).
- **DEC-20 - Power integrity is first-class (banked from InMoov).** Prototype from a stiff
  LiPo (not a bench PSU); isolate the logic rail from the servo/motor rail; bulk caps on the
  servo bus; **3S only** (4S would exceed the 12V servo rating); fuse the pack. Detail in
  [`architecture.md`](architecture.md) "Power integrity".
- **DEC-21 - Keep servo mounting SO-ARM compatible** (resolves OQ-08). The STS3215 limb
  joints adopt the Standard Open Arm servo + bracket mounting standard, so off-the-shelf
  kits (servos + metal brackets + FE-URT-1) drop straight in and we inherit the LeRobot
  software / community ecosystem. Body and personality stay custom; the joint skeleton
  borrows a proven, cheap, supported standard - and it makes the AliExpress kit brackets
  useful rather than spare (see [`sourcing.md`](sourcing.md)). **Brackets are printed** - the servo/horn geometry is built into each printed limb part (from the open SO-ARM CAD); one metal bracket set is kept only as a dimensional reference. Go metal on a joint only if it flexes in testing (unlikely at ~2 kg).
  **Track SO-101, not SO-100** (checked 2026-09-02): upstream deprecates SO-100 and directs
  new builds to SO-101. Both live in the [SO-ARM100 repo](https://github.com/TheRobotStudio/SO-ARM100),
  which kept its original name - so the repo name is not the revision. The 100->101 changes
  (wiring routing, assembly, *leader*-arm motors) do not touch the servo itself, so every
  `[STEP]` constant taken from `STS3215_03a.step` stands - upstream ships no SO-101 servo
  model precisely because the servo is unchanged. The *bracket* did change (SO-101 renames it
  and trims 1.7 mm in Y), but nothing in `params.py` derives from it, so V1 geometry is
  unaffected. Verified against upstream `7629d2a`; measurements in
  [`../hardware/vendor/so-arm100/README.md`](../hardware/vendor/so-arm100/README.md).
  **Amended 2026-09-07 — what "compatible" means.** Not the servo's case
  dimensions: the SO-101 **mounting architecture**, measured in
  [`soarm-joint-pattern.md`](soarm-joint-pattern.md): a **cradle** in the
  structural part holding the rear ~17 mm of the case, a separate 3 mm **collar**
  that slides over servo and cradle and closes the pocket, four M2 self-taps into
  the servo's own lugs through Ø2.0 clearance holes, and a **clevis** on the driven
  link bolted to both the drive and idler horns. **Both drafts breached this
  decision:** a3f265c's `hip_link` had no body retention at all, and DEC-29 used a
  friction cap and screws driven into an unmeasured case wall. Neither breach was
  flagged against DEC-21 at the time, although `cad-review.md` and the vendor
  README both noted that nothing had been taken from the SO-ARM bracket. From
  DEC-30 on, every STS3215 joint instantiates one socket primitive that implements
  this pattern; a joint that does not is a DEC-21 breach by definition.
- **DEC-26 - Compact hip: pitch servo aft and outboard** (supersedes the stacked
  layout inside DEC-07, not DEC-07 itself). The roll and pitch axes sat **60 mm**
  apart, which read as a hip *plus a knee halfway down the thigh* rather than as a
  hip. That gap was never chosen: `BRACKET_CLEAR_R` (24) + `SERVO_ABOVE` (35.2) =
  59.2 - the pitch servo was standing on the roll servo's head, pointing up.
  **The fix uses a free degree of freedom.** A servo's output axis runs through
  its body, so *sliding it along that axis does not move the axis at all*. Point
  the pitch servo **aft** and slide it **outboard**, and the binding clearance
  becomes the roll servo's half-body below its axis (10.2) against the pitch
  servo's half-**width** (12.4) rather than its half-length: **26 mm**.
  Pattern borrowed from hexapod coxa/femur hips, which sit servos side by side
  rotated 90 deg rather than stacking them.
  `THIGH_DROP` absorbs the 34 mm (120 -> 154) so the stance stays 270 mm - the
  leg now reads as one long thigh. Outboard rather than inboard was chosen so the
  thigh fork straddles the wheel plane instead of reaching out to it; the cost is
  ~30 mm more roll moment, small against 30 kg.cm. **Verified by a collision
  sweep** (`hip_link` + pitch servo against `hip_bracket` + roll servo): clear
  through +/-30 deg, with the only residual being the fork plates sitting inside
  the keep-out's padded horn discs, which is where they bolt.
- **DEC-27 - Real motor envelopes set the stance width.** The first lower-body
  render omitted the bought 37D motors, hiding a 44 mm centreline overlap; the
  100 mm pelvis also left each bracket's outer bolt pair beyond the plate. The
  DFRobot FIT0403 drawing gives 69 mm from mounting face to encoder cap (90 mm
  overall including the 21 mm shaft). Moving each hip axis from +/-33 to +/-57
  mm leaves 4 mm between encoder caps; wheel centres become +/-90 mm and a
  150 x 170 mm pelvis contains every bracket hole with a 5.3 mm edge. These
  packaging datums are now checked by the CAD build. The same check binds the
  motor-clamp flange to the thigh's shared seam datum; DEC-26 had lengthened the
  thigh without moving that flange, leaving an otherwise silent 34 mm gap.
- **DEC-28 - Soft form follows the structure, not a cosmetic shell.** The V1
  lower body uses rounded deck corners and a tapered, radiused thigh beam while
  preserving flat joint/seam datums, constant-thickness support-free prints,
  and purchased-part clearances. This establishes an organic visual language
  without adding non-functional panels before the structural prototype works.
- **DEC-22 - Servo sourcing & neck actuator confirmed** (resolves OQ-06). Both orders placed
  2026-09-01. **Limbs:** 12x Feetech STS3215 12V 30 kg from RCmall (AliExpress), 2x 6-pack
  (~£17.3/servo landed), FE-URT-1 setup adapter listed as included *(2026-09-12: none shipped — see `sourcing.md`; the family's adapters cover setup)*. **Neck:** 4x Feetech STS3032M
  (metal case, 4.5 kg.cm, magnetic feedback, STS protocol - one software stack with the limbs,
  but 6V, so on its own 6V bus segment via a second Teensy UART). SCS0009 was the cheaper,
  different-protocol alternative. Drive/balance base (DEC-19) ordered from Pi Hut the same day.
- **DEC-23 - Part decomposition: one master model, screw-joined designed seams.** The body
  is modelled as a single parametric assembly; printable parts are *derived* by explicit
  split operations. Every seam is a designed joint: registration features (pins/keys) for
  alignment + **M3 screws into brass heat-set inserts** (captive nuts on thin parts; no
  printed threads, per DEC-12). Screws loaded in shear, never across layers; seams placed
  off load paths and hidden under paneling; each part declares its print orientation. The
  CAD pipeline *enforces* the <= 200x200 mm rule (DEC-09) with automated bounding-box,
  connected-solid, and critical assembly-datum checks, so a parameter change that breaks
  printability or known packaging constraints fails the build. General collision sweeps
  remain explicit motion-study work rather than a claim made by the export pipeline.
- **DEC-24 - Every part prints support-free, and the build proves it.** Bed *fit* is not
  printability: a part is only done when it has a declared orientation needing no support.
  Enforced by `hardware/.../printability.py`, which measures, per part, bed-contact area and
  the area of down-facing surfaces steeper than the 45 deg self-support limit, and **fails the
  build** on either (bed < 300 mm2 = standing on pinpoints; overhang > 800 mm2 = real support).
  It also ranks the principal orientations, so orientation is measured rather than guessed.
- **DEC-25 - Socket cap heads, standing proud by default; no countersinks in plastic.**
  Three reasons. **Countersunk heads are a wedge**: the cone bears against the layer
  lines and, under load or over-tightening, splits or creeps the print apart - a flat
  seat spreads the same load across a face. **Cap heads take more torque** (full hex
  engagement, no cam-out) which matters when a joint is opened repeatedly during
  bring-up. **A proud head costs nothing** on an internal joint: 3 mm of clearance is
  free where nothing mates or sweeps. Counterbore (`fasteners.m3_counterbore`, flat
  pocket - never a cone) **only** where a proud head would foul a mating face or a
  moving part, and orient that face upward so the pocket prints as open air rather
  than a bridge. Heads on **exposed outer surfaces** must be recessed or covered by
  paneling, per the child-safety principle (concept.md 7; OQ-10) - proud fasteners on
  a surface a child touches are a snag point, and that is where the exception bites.
  Design consequences, learned by failing them: **features on one face only** (a plate with
  bosses up *and* structure down cannot print - split it, DEC-23); **no closed cavity floors**
  (they become bridged ceilings when flipped); **a fork prints axis-horizontal** so both tines
  stand, never axis-vertical with the far tine bridging air; and where two features disagree
  (fork + cross-axis motor tube) **split at a seam** rather than accepting support.
