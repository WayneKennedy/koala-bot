# Open Questions (pending decisions)

Unresolved. Resolve -> move to [`decisions.md`](decisions.md).

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

- **OQ-13 - Lower-body mechanical redesign and FDM validation.** The
  [review of revision a3f265c](cad-review.md) confirms printed hip/thigh
  interference at neutral, blind roll-horn holes and an unassemblable
  motor-clamp fastener arrangement. The existing gates do not establish
  support-free manufacture or layer strength. Reassess the pelvis split
  (the joined geometry fits flat on the bed), design the hip carrier and
  driven fork together, then validate access, motion, load paths and sliced
  layers before structural printing. Replacement geometry is implemented in
  DEC-29; [its validation record](cad-redesign.md) distinguishes passed sampled
  checks from open physical acceptance. Retention dimensions and structural
  profile remain OQ-12 and OQ-11.

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
- **OQ-12 - Servo body retention.** The STS3215 is held by a **snug printed
  pocket plus 4 self-tapping screws** - 2 into the front face, 2 into the back
  - per the SO-ARM101 assembly video. Its body mount and its horn drive are
  **separate feature families on separate datums**; see
  [`test-log.md`](test-log.md) for why that distinction matters.
  The integral pelvis roots retain a provisional version of that architecture.
  **Historical a3f265c state:** `hip_link` had no body retention.
  DEC-26 widened its cradle around the full pitch-servo envelope, so material
  now exists for a through-bolt pattern, but the physical bore locations and
  idler stand-off remain unverified. A later attempt put four cutters along X;
  that was geometrically incapable of retention because the case bores run
  along the output axis (+Y in the compact-hip frame), so it was removed.
  A **wrap-around bracket** appears on the base servo only, as reinforcement
  for the highest-load joint; Koala's hips are the analogue, and a ~55 mm
  through-bolt with a nut would serve the same end while cutting no thread in a
  PA+GF case (a wear item on the expensive half of the joint).
  **Blocked on measurement** - seven checks are listed in `test-log.md`, all
  answerable with calipers on the physical servos; two 12 V ST3215 units are in
  hand since 2026-09-07, so the checks are now doable, not merely listed.
  **The screw is settled: M2 self-tapping**, supplied as M2x5 in that box
  (`SELFTAP_DIA` = 2.0, clearance 2.4). **Its length is not**, and neither are
  the hole locations. Length = printed wall + engagement, and the current CAD
  offers two different walls at the four holes - 3.95 mm and 6.35 mm in
  `hip_bracket.build_root()` - so either those walls are equalised to one
  flange thickness (~4 mm, giving M2x8 throughout) or the thick side is
  counterbored; and the case bore depth that bounds engagement is unmeasured.
  **DEC-29 authorization supersedes the former geometry freeze:**
  the pitch servo now has a removable external case clamp, not invented case
  screw locations. Its preload, creep, cable exit and real-case fit remain
  unverified. Roll retention geometry and idler spacing still require
  measurement.
- **OQ-10 - Child-safety spec** (audience 2-5; DEC-15). Resolve during design: pinch-point
  guarding at every joint/linkage; software speed & torque limits + e-stop; graceful-fall
  behaviour; protected/enclosed LiPo; no small detachable parts; rounded edges; no hot
  exposed surfaces. Reference EN 71 (toy safety) for guidance, not as a certification target.
