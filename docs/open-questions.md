# Open Questions (pending decisions)

Unresolved. Resolve -> move to [`decisions.md`](decisions.md).

- **OQ-16 - Knee and wheel-foot leg: the choices DEC-31 leaves open.** The
  decision fixes the chain (hip roll/pitch → thigh → knee pitch → shank →
  wheel-foot) and the actuators; it does not fix: (a) **drive motor placement**
  in the shank — direct drive on the wheel axis (default) vs motor higher in the
  shank with a belt, decided by the 69 mm motor body against inner-leg
  clearance at full knee flex; (b) **thigh/shank lengths and nominal knee
  angle** against the 40–50 cm height (DEC-15); (c) **knee range**; (d) the
  **knee servo torque margin** — 30 kg.cm nominal against the mass share times
  the horizontal moment arm at the worst crouch, a number nobody has computed;
  (e) whether **no spare STS3215** (12 bought, 12 joints) is acceptable or a
  6-pack is added to the next order; (f) **track width** — an output of the
  packaging, to be recorded as a tradeoff if it widens; (g) cable routing
  through three powered joints per leg. Each resolves to a DEC entry during the
  restart ([`cad-restart-brief.md`](cad-restart-brief.md) §5).

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
  order: caliper the servos, gauge the PETG pocket, bank requirements, reserve
  swept envelopes, design with the socket primitive, then print one joint rig.
  **Closes when** a full lower body passes fit and a documented load test
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
  **Superseded 2026-09-07 by the measured SO-101 pattern**
  ([`soarm-joint-pattern.md`](soarm-joint-pattern.md)): retention is cradle +
  collar with the four M2 self-taps into the servo's own lugs through **Ø2.0
  clearance** holes, the wall **counterbored to ~2.2 mm** under the head so the
  supplied M2×5 reaches — the length problem above is solved by geometry, not
  by longer screws. The through-bolt-and-nut alternative is dropped in favour
  of the proven pattern. Upstream's printed holes put the lugs at **~2.1 mm
  from the rear face on the back face and ~5.8 mm on the horn face**, so the
  single `SERVO_TAB_X` is wrong for one face; `SERVO_TAB_HOLE = 4.0` is wrong
  for a screw hole. **Still blocked on calipers** for: both lug offsets, lug
  pilot depth, idler and horn stand-off, and the horn stack for the clevis
  span; and on **`Gauge_0` printed in PETG** for `CLEAR_POCKET` (upstream's
  zero-clearance pocket is a press fit on the reference printer in PLA+).
- **OQ-10 - Child-safety spec** (audience 2-5; DEC-15). Resolve during design: pinch-point
  guarding at every joint/linkage; software speed & torque limits + e-stop; graceful-fall
  behaviour; protected/enclosed LiPo; no small detachable parts; rounded edges; no hot
  exposed surfaces. Reference EN 71 (toy safety) for guidance, not as a certification target.
