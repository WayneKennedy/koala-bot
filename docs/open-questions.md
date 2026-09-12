# Open Questions (pending decisions)

Unresolved. Resolve -> move to [`decisions.md`](decisions.md).

- **OQ-21 — Physical joint travel and control limits.** DEC-48 implements
  DEC-46's pose-dependent viewer search using the printed geometry and nominal
  hardware envelopes. The search uses 0.25° steps and a 1° reserve before the
  first intersection, within a ±180° search ceiling. Servo indexing, actual
  electrical limits, tolerances, complete cables/guards and loaded operation
  remain unverified. This is a finite-resolution clearance aid, not continuous
  swept-volume certification or a gait controller limit.

- **OQ-20 — Physical acceptance of the SO-101 construction adaptation.**
  DEC-48/49/50 implement enclosing asymmetric sockets, rounded links/forks,
  common carriers at all four roots and independent root modules. Bench driver approaches, nominal
  insertion and CAD clearances are checked; local slices support `assumed`
  printability. Check real support removal, mounting fit, assembly/service
  access and load/creep on the revised parts. No repeat Gauge_0 is required.
  [Part review](part-design-review.md).

- **OQ-19 — Front-foot contact acceptance.** DEC-43 fixes the rear ankle-wheel
  location and retains current size. The CAD uses a 75 mm forearm plus 25 mm
  hand to a fixed Ø32 mm ball centre, with both front feet on the floor in the
  supported pose. DEC-48 selects separate TPU pads with keyed seats and recessed
  fixings. Establish TPU grade/settings, grip, wear and contact behaviour under
  load; the geometry and local slice do not establish traction.
- **OQ-18 — Detailed packaging and contact transition.** Check the transition
  from front feet plus rear wheel contacts to rear-wheel balance: CoM/support
  polygons, clearances, body-weight shifts and servo forces throughout. Define
  physical haunch/rest supports if needed. Head position and mounting are
  undecided; DEC-49 removes the unsupported placeholder from structural CAD
  and clearance searches. Complete neck, battery/electronics,
  harnesses and guards. Power-off standing needs a demonstrated support path.
- **OQ-17 — Two-wheel drive acceptance and later gait.** Wheel location and
  bought 37D retention are settled by DEC-43; no knee-drive or belt study is
  required for V1. Establish actual drive current/thermal duty, axle/hub loads
  and rear-pair balance recovery on the assembled robot. Uneven-terrain stepping
  with wheel-feet, including wheel holding and traction, remains a later
  experiment. [Historical motor comparison](drive-motor-sizing.md).
- **OQ-16 — Limb physical acceptance.** Retain twelve ST3215s — **eight in hand**
  since four went to SO-ARM101 on 2026-09-12 (`bom.md`); re-order before all four limbs
  can be fitted. Removing front
  drives reduces arm swing loads; rear wheel mass remains at the ankles.
  Establish actual mass/CoM, continuous torque/temperature, ground reactions
  and printed joint strength for support and transition. Digital collision
  checks do not validate loaded motion. Fit one joint, then complete limbs
  and loaded support.

- **OQ-13 - Lower-body mechanical redesign and FDM validation.** Two drafts
  have been discarded (DEC-30): a3f265c for interference, blind holes and an
  unassemblable motor clamp ([review](cad-review.md)); DEC-29 for breaching
  DEC-21's mounting pattern and widening the track to 258.8 mm as a packaging
  escape ([record](cad-redesign.md)). Neither reached a structural print. The
  redesign now follows [`cad-restart-brief.md`](cad-restart-brief.md) in
  order: use the confirmed SO-101 fit (DEC-33), bank requirements, reserve
  swept envelopes, design with the socket primitive, then print one joint rig.
  DEC-40 replaces DEC-34 with integrated four-limb geometry and the corrected
  interface ([design record](cad-integrated-design.md)). No new part
  has yet been sliced or printed. **Closes when** a full lower body passes fit and a documented load test
  (OQ-11). Retention dimensions remain OQ-12; the leg's open choices are OQ-16.

- **OQ-14 - micro-ROS on the bought Teensy 4.0.** Upstream lists the 4.0 as
  "Not tested" where the 4.1 is Supported. DEC-18 bought the 4.0, and DEC-04 makes
  the bridge load-bearing, so the untested board sits on a load-bearing path
  rather than a peripheral one. The board table and the shared reasoning
  live in
  [wk-robotics](https://github.com/WayneKennedy/wk-robotics/blob/main/docs/common.md#micro-ros-how-the-mcu-joins-the-graph),
  not here.
  **Cheap to close, and worth closing before firmware:** flash a micro-ROS example
  to the 4.0, then log the result in [`test-log.md`](test-log.md). If it fails the
  fallback is a Teensy 4.1 or the ESP32 named in
  [`architecture.md`](architecture.md#bridge--contract) - not a redesign. Since
  2026-09-11 the family holds an **unallocated Teensy 4.1 NE**
  ([wk-robotics `common.md`](https://github.com/WayneKennedy/wk-robotics/blob/main/docs/common.md#drive-motors-drivers-and-mcus-in-hand)),
  so the fallback costs nothing to buy - but it is first-come, not reserved for koala.
  **This is now koala's risk alone:** wk-devastator closed its half as DEC-10 - it
  buys a 4.1 rather than prove a 4.0 - and confirmed koala's 4.0 is committed to
  this build, not a family spare. Whether an untested board already bought is worth
  proving or writing off is a koala decision nobody else shares.

- **OQ-03 - Torso platform's 3 DOF.** pitch + roll + **yaw** (twist, very lifelike) vs
  pitch + roll + **heave** (breathing bob). Can't have all four from 3 actuators.
- **OQ-04 - Head eyes & mass.** Screen/OLED eyes (light, expressive) vs mechanical eye
  servos (mass). Confirm the < ~250-300 g head budget that keeps micro servos viable.
- **OQ-09 - Swappable limb-ends in V1.** Design the quick-swap wrist/ankle mount into V1,
  or defer to the climber sibling?
- **OQ-11 - Structural print profile.** The BOM's measured filament and time come
  from the reference printer's **general-purpose** PETG profile (3 perimeters, 15 %
  grid) — that profile was measured *with*, not chosen *for*, koala-bot. Load-bearing
  parts (hip link, thigh, hip bracket) may want 4-5 perimeters, since perimeters buy
  more strength per gram than infill; the cost is time and filament, and the BOM
  totals move with it. **Resolve on evidence:** print one structural part, load it to
  failure or to visible flex, and compare. Until then the profile table in
  [`bom.md`](bom.md) is a record of how the numbers were produced, not a decision.
- **OQ-12 - New socket rig acceptance.** DEC-33 removes the caliper and
  repeat-gauge prerequisite: the maintainer confirms ST3215 fit in the
  SO-101 parts in PLA+ and PETG. Adopt the upstream printed-part pocket,
  asymmetric lug positions and the corrected measured horn stack in
  [`soarm-joint-pattern.md`](soarm-joint-pattern.md); the 2026-09-08 caliper
  evidence is recorded in `test-log.md`. The [DEC-40 implementation](cad-integrated-design.md) addresses the earlier
  interface failures; demonstrate its **new four-ear saddle and integrated
  double-horn clevis** on a real servo: insertion and removal, M2x5 engagement
  without bottoming, both horn patterns, M3 engagement and centre-screw
  access, free rotation without axial preload, and cable clearance. Log
  the rig fit before printing a full leg. Full-body strength remains OQ-13.

- **OQ-10 - Child-safety spec** (audience 2-5; DEC-15). Resolve during design: pinch-point
  guarding at every joint/linkage; software speed & torque limits + e-stop; graceful-fall
  behaviour; protected/enclosed LiPo; no small detachable parts; rounded edges; no hot
  exposed surfaces. Reference EN 71 (toy safety) for guidance, not as a certification target.
