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
  Klipper + a headless PrusaSlicer pipeline is the reference printer.
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
