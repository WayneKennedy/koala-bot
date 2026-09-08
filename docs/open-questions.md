# Open Questions (pending decisions)

Unresolved. Resolve -> move to [`decisions.md`](decisions.md).

- **OQ-16 - Knee/wheel-foot acceptance and remaining choices.** DEC-34
  banks the prototype's direct-drive motor placement, 100/100 mm links,
  15/30° nominal hip/knee angles, 239.5 mm track and sampled motion ranges.
  [`cad-restart-design.md`](cad-restart-design.md) records the tradeoffs and
  first torque calculations. Still open: continuous servo torque/temperature,
  actual mass and CoM, powered load sharing at crouch, whether twelve bought
  STS3215s with no spare is acceptable, complete cable routing/guarding, and
  any further hip compaction. Sampled geometric clearance does not settle
  balance limits or loaded motion. Future torso-platform and shoulder-girdle
  mounting details remain to be designed; the pelvis reserves a rigid-strut
  interface only.

- **OQ-15 - Whether to buy a second TB9051FTG.** The driver bought under DEC-16
  (qty 1, purchased 2026-09-01) has been **lent to wk-devastator**, which settled its
  own driver question by borrowing rather than buying
  ([its DEC-13](https://github.com/WayneKennedy/wk-devastator/blob/main/docs/decisions.md)).
  One board cannot be in two robots, so **koala-bot and the tank cannot both be in drive
  bring-up at the same time.**
  **Not urgent, and the trigger is knowable.** koala-bot is in CAD and printing with no
  structural part printed yet; the tank's motors arrive around 26 September. This becomes
  live the moment koala-bot's drive bring-up is scheduled - either buy a second (~£30.70)
  or agree the tank returns it. **Until then, do not plan koala-bot's drive bring-up
  against a board that is in another robot.**

- **OQ-13 - Lower-body mechanical redesign and FDM validation.** Two drafts
  have been discarded (DEC-30): a3f265c for interference, blind holes and an
  unassemblable motor clamp ([review](cad-review.md)); DEC-29 for breaching
  DEC-21's mounting pattern and widening the track to 258.8 mm as a packaging
  escape ([record](cad-redesign.md)). Neither reached a structural print. The
  redesign now follows [`cad-restart-brief.md`](cad-restart-brief.md) in
  order: use the confirmed SO-101 fit (DEC-33), bank requirements, reserve
  swept envelopes, design with the socket primitive, then print one joint rig.
  DEC-34 now provides replacement geometry and digital checks; no new part
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
  [`architecture.md`](architecture.md#bridge--contract) - not a redesign.
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
  asymmetric lug positions and nominal horn span; no value is presented as
  a new caliper measurement. Still demonstrate the **new** cradle/collar/
  double-horn clevis on a real servo: insertion and removal, M2x5 engagement
  without bottoming, both horn patterns, M3 engagement and centre-screw
  access, free rotation without axial preload, and cable clearance. Log
  the rig fit before printing a full leg. Full-body strength remains OQ-13.

- **OQ-10 - Child-safety spec** (audience 2-5; DEC-15). Resolve during design: pinch-point
  guarding at every joint/linkage; software speed & torque limits + e-stop; graceful-fall
  behaviour; protected/enclosed LiPo; no small detachable parts; rounded edges; no hot
  exposed surfaces. Reference EN 71 (toy safety) for guidance, not as a certification target.
