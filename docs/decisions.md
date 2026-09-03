# Banked Decisions

Committed decisions with rationale. Unresolved items live in
[`open-questions.md`](open-questions.md). Format: `DEC-nn - decision - why`.

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
  **knee-wheels** (2x DC); **3-RPS head** (3 micro servos + CF pushrods) with **yaw
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
- **DEC-17 - Rear leg architecture** (resolves OQ-02). 2-DOF hip-to-pelvis; the 12V drive
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
  CAD pipeline *enforces* the <= 200x200 mm rule (DEC-09) with an automated bounding-box +
  assembly-interference check, so a parameter change that breaks printability fails the build.
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
