# Roadmap

Vertical-slice first (DEC-11): one complete, documented Koala before the family.

## Phase 0 - Design record *(done 2026-09-01)*
Repo seeded; concept, architecture, decisions captured. **Exit met:** open
questions resolved enough to start CAD (hardware ordered; OQ-03/04/09/10 remain
but don't block the lower body).

## Phase 1 - Koala V1 (the vertical slice) *(current)*
1. **CAD** - parametric body in code-CAD; parts <= 200 mm; export URDF.
   *Started:* draft v0 lower body (pelvis/hips/thighs/e-tray) in `hardware/`.
2. **Prototype prints** - structural test of limbs, knee-wheels, neck.
3. **Electronics bring-up** - MCU balance loop (2-wheel inverted pendulum, IMU +
   encoders); STS3215 bus + IDs; motor driver; power rail.
4. **Brain** - Pi 5 + ROS2; micro-ROS bridge; vision (camera-eyes); LLM personality.
5. **Integration** - leaning, gesture, look-at-you; tune balance.
6. **Deliverables** - full BOM, build guide, one polished video.
**Exit:** a working, self-balancing, documented Koala anyone can reproduce.

## Phase 2 - Koala V1.x upgrades
- Activate the **3-DOF torso platform** (drop actuators into the pre-built interfaces).
- **Optional walking** (gated on need - DEC-17): add a lower leg + foot + knee servo
  *if* pure wheeled locomotion proves insufficient. Not assumed.
- Optional **animatronic ears**; screen-eyes polish.

## Phase 3 - the Family
- **Climber sibling** - all-gripper limbs; winch / clutch / passive-latch hybrid
  actuation; front-arm winch-haul -> four-limb climb.
- **Swappable limb-ends** - common wrist/ankle mount: wheel <-> gripper.
- Additional bodies on the shared brain.
