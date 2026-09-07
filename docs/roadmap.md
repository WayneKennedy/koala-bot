# Roadmap

Vertical-slice first (DEC-11): one complete, documented Koala before the family.

## Phase 0 - Design record *(done 2026-09-01)*
Repo seeded; concept, architecture, decisions captured. **Exit met:** open
questions resolved enough to start CAD (hardware ordered; OQ-03/04/09/10 remain
but don't block the lower body).

## Phase 1 - Koala V1 (the vertical slice) *(current)*
1. **CAD** - parametric body in code-CAD; parts <= 200 mm; export URDF.
   *Restarted 2026-09-07 (DEC-30):* two lower-body drafts discarded; the
   redesign follows [`cad-restart-brief.md`](cad-restart-brief.md) — calipers
   and a PETG gauge first, then a servo socket primitive, then legs with knees
   and wheel-feet (DEC-31).
2. **Prototype prints** - one joint rig, then one leg, then the pair; neck.
3. **Electronics bring-up** - MCU balance loop (2-wheel inverted pendulum, IMU +
   encoders); STS3215 bus + IDs; motor driver; power rail.
4. **Brain** - Pi 5 + ROS2; micro-ROS bridge; vision (camera-eyes); LLM personality.
5. **Integration** - leaning, gesture, look-at-you; tune balance.
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
