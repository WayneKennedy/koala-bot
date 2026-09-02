# Open Questions (pending decisions)

Unresolved. Resolve -> move to [`decisions.md`](decisions.md).

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
  `hip_bracket` follows that architecture. **`hip_link` has no retention at
  all**, and cannot take any as drawn: the servo's 43.6 mm axial extent exceeds
  its 30 mm cradle, so there is no material at the screw line. Fixing it means
  widening the cradle, which moves the assembly - deliberately deferred.
  A **wrap-around bracket** appears on the base servo only, as reinforcement
  for the highest-load joint; Koala's hips are the analogue, and a ~55 mm
  through-bolt with a nut would serve the same end while cutting no thread in a
  PA+GF case (a wear item on the expensive half of the joint).
  **Blocked on measurement** - five unknowns listed in `test-log.md`, all
  answerable with calipers on the servos arriving 2026-09-04. Do not reshape
  `hip_bracket` or `hip_link` before then.
- **OQ-10 - Child-safety spec** (audience 2-5; DEC-15). Resolve during design: pinch-point
  guarding at every joint/linkage; software speed & torque limits + e-stop; graceful-fall
  behaviour; protected/enclosed LiPo; no small detachable parts; rounded edges; no hot
  exposed surfaces. Reference EN 71 (toy safety) for guidance, not as a certification target.
