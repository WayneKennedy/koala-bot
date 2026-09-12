# Roadmap

Vertical-slice first (DEC-11): one complete, documented Koala before the family.

## Phase 0 - Design record *(done 2026-09-01)*
Repo seeded; concept, architecture, decisions captured. **Exit met:** open
questions resolved enough to start CAD (hardware ordered; OQ-03/04/09/10 remain
but don't block the lower body).

## Phase 1 - Koala V1 (the vertical slice) *(current)*
1. **CAD** - parametric body in code-CAD; parts <= 200 mm; export URDF.
   *DEC-43, 2026-09-10:* retain rear ankle drives and replace front drives with
   integrated forearms/rounded feet. The supported and upright CAD poses share
   the retained 450 mm height and 220 mm rear track. Twelve servo mounts,
   paired root crossmembers and the rigid torso remain implemented.
   Servo fit in PLA+/PETG is accepted (DEC-33), with no repeat-gauge prerequisite.
   Head/neck and complete electronics/battery packaging remain detailed work.
   Digital scope and physical gates: [cad-integrated-design.md](cad-integrated-design.md).
2. **Prototype prints** - corrected joint rig, integrated links (DEC-39), one
   rear leg, the pair, passive-foot forelimbs, torso and neck; fit/load
   evidence at each stage.
3. **Electronics bring-up** - MCU balance loop (2-wheel inverted pendulum, IMU +
   encoders); STS3215 bus + IDs; motor driver; power rail.
4. **Brain** - Pi 5 + ROS2; micro-ROS bridge; vision (camera-eyes); LLM personality.
5. **Integration** - supported stance, front-foot lift and rear-wheel balance/drive;
   validated rise/lower load transfer, leaning, gesture and look-at-you.
6. **Deliverables** - full BOM, build guide, one polished video.
**Exit:** a working, self-balancing, documented Koala anyone can reproduce.

## Phase 2 - Koala V1.x upgrades
- Activate the **3-DOF torso platform** (drop actuators into the pre-built interfaces).
- **Gait experiments** on the articulated legs — the knees themselves are V1
  (DEC-31); stepping, and any ankle DOF or articulated foot, stay gated on need.
- Optional **animatronic ears**; screen-eyes polish.

## Phase 3 - the Family
- **Climber sibling** - all-gripper limbs; winch / clutch / passive-latch hybrid
  actuation; front-arm winch-haul -> four-limb climb.
- **Swappable limb-ends** - common wrist/ankle mount: wheel <-> gripper.
- Additional bodies on the shared brain.
