# Roadmap

Vertical-slice first (DEC-11): one complete, documented Koala before the family.

## Phase 0 - Design record *(done 2026-09-01)*
Repo seeded; concept, architecture, decisions captured. **Exit met:** open
questions resolved enough to start CAD (hardware ordered; OQ-03/04/09/10 remain
but don't block the lower body).

## Phase 1 - Koala V1 (the vertical slice) *(current)*
**DEC-62, 2026-09-21:** build and train quadruped walking on four TPU feet first.
Swap complete rear shanks at the existing knees for the retained wheeled V1
endpoint; twelve limb joints and the upper chassis serve both builds.

1. **CAD** - parametric body in code-CAD; parts <= 200 mm; export URDF.
   *DEC-43, 2026-09-10:* retain rear ankle drives and replace front drives with
   integrated forearms/rounded feet. The supported and upright CAD poses share
   the retained 450 mm height and 220 mm rear track. Twelve servo mounts,
   paired root crossmembers and the rigid torso remain implemented.
   Servo fit in PLA+/PETG is accepted (DEC-33), with no repeat-gauge prerequisite.
   Head/neck and complete electronics/battery packaging remain detailed work.
   Digital scope and physical gates: [cad-integrated-design.md](cad-integrated-design.md).
   *DEC-52, 2026-09-14:* structural redesign proceeds torso-first, outward:
   torso frame → root modules → carriers → upper links → lower links → feet and
   wheels, each stage reviewed visually before the next; downstream parts are
   re-derived, not preserved. *DEC-53:* the design vehicle is one rear leg in
   isolation; torso shape deferred. Current step: the root module with captive nuts.
2. **Prototype prints** - corrected joint rig, integrated links (DEC-39), one
   rear leg, the pair, passive-foot forelimbs, torso and neck; fit/load
   evidence at each stage.
3. **Electronics bring-up** - STS3215 bus + IDs, power rail and IMU; four-foot
   support and walking training. Bring up the motor driver, encoders and MCU
   balance loop with the wheeled shanks later.
4. **Brain** - Pi 5 + ROS2; micro-ROS bridge; vision (camera-eyes); LLM personality.
5. **Integration** - loaded four-foot walking first; then exchange rear shanks,
   supported stance, front-foot lift and rear-wheel balance/drive;
   validated rise/lower load transfer, leaning, gesture and look-at-you.
6. **Deliverables** - full BOM, build guide, one polished video.
**Exit:** a working, self-balancing, documented Koala anyone can reproduce.

## Phase 2 - Koala V1.x upgrades
- Activate the **3-DOF torso platform** (drop actuators into the pre-built interfaces).
- **Wheel-foot gait experiments** on the articulated legs — four-TPU-foot
  walking moves into Phase 1 (DEC-62); any ankle DOF stays gated on need.
- Optional **animatronic ears**; screen-eyes polish.

## Phase 3 - the Family
- **Climber sibling** - all-gripper limbs; winch / clutch / passive-latch hybrid
  actuation; front-arm winch-haul -> four-limb climb.
- **Swappable limb-ends** - common wrist/ankle mount: wheel <-> gripper.
- Additional bodies on the shared brain.
