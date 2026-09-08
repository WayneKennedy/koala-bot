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

- **DEC-34 — New six-servo lower-body prototype with explicit packaging and
  fastening** (2026-09-07). Replace every old structural builder. Use the
  shared SO-101 cradle/collar and double-horn clevis at roll, pitch and knee;
  100 mm thigh and shank, direct-drive ankle wheels, hip/knee nominal 15/30°.
  Track is 239.5 mm; nominal deck height 283.2 mm, with 150 mm reserved above
  it (433.2 mm total). Adopt ±5° roll and −10…45° hip as the prototype's
  inspection range, trading the DEC-32 wider targets for this packaging;
  knee target remains 0…90°. Pitch sits 70.115 mm forward and 34 mm outboard
  of roll to make the socket and carrier fasteners accessible. This is a
  recorded compactness tradeoff, not an optimum. Use a **flat idler seat**
  because recessing a plate onto the adopted flush idler collided with the
  case; drive recess remains 0.8 mm. Registered through-bolted crossbars and
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
  (~£17.3/servo landed), FE-URT-1 setup adapter included. **Neck:** 4x Feetech STS3032M
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
