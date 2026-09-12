# Koala — Concept & Design Principles

## Vision

An open-source **family** of small, printable, affordable, fully-documented
companion robots. The differentiator is not novelty but **completeness**: a
coherent family sharing one "brain", each member shipped with a build video, full
BOM, and working software — the opposite of the half-finished robots that litter
model repositories.

The family is unified by a **shared brain** (common electronics + firmware + a
ROS2/topic contract, see [`architecture.md`](architecture.md)) with **swappable
bodies**. The defining split between members is **wheel-vs-gripper limb-ends**
(see [`backlog.md`](backlog.md)).

## Koala V1 — the first member

A ground-based companion with **two rear ankle wheels and two replaceable rounded TPU
front contacts**, articulating knees and a two-wheel balancing/drive mode
(DEC-31/41/43). The compact koala baseline is **450 mm upright head-top height**,
within the ~400–500 mm overall size goal (DEC-15). Head mounting and position
are unresolved; this height is a sizing allocation, not a solved installation. The supported quadruped pose
is lower. These poses are CAD references; loaded transitions and locomotion
remain to be demonstrated. Dimensions: [body-layout.md](body-layout.md).
Printable in
**PETG** with **every part <= 200x200 mm** (designing to the commonest bed
maximises who can build it, even though the reference printer is 220 mm).

### Morphology & DOF (V1)

| Segment | DOF | Actuator | Notes |
|---------|-----|----------|-------|
| Front limbs x2 (arms *and* forelegs) | 3 each | STS3215 bus servo | shoulder pitch → roll → elbow; flatter integrated forearm ending in a replaceable TPU contact at wrist/hand reach; support and gesture; 75 mm forearm + 25 mm hand to Ø32 mm ball centre (DEC-43) |
| Rear leg hips x2 | 2 each | STS3215 bus servo | **pitch + roll**, in that serial order (DEC-41); active lean and leg placement with a rigid torso |
| Rear knees x2 | 1 each | STS3215 bus servo | **active in V1** (DEC-31) — articulating knee between thigh and shank; with the hips it sets ride height, crouch and stand |
| Rear ankle wheels x2 | continuous spin | Bought 37D 12V geared DC + encoder | integrated 90 mm shanks retain ankle drives; no separate rear walking feet |
| Head / neck | 3 | micro servo + CF pushrod | **3-RPS parallel** (pitch/roll/heave); *yaw delegated to the base* |
| Torso | 0 (V1) | - | **rigid strut** in V1; interfaces pre-designed for a single 3-DOF platform later |

V1 actuator count: **12 STS3215** (6 arm + 4 hip + 2 knee; twelve bought, no spare — OQ-16) + **3 micro** (head) + **2 DC** (rear drive; bought pair retained).

### Locomotion

- **Supported stance:** front ball feet and rear wheel-feet provide four
  contacts. Standing without active balancing is intended; power-off standing
  is not established. Uneven-terrain stepping with wheel-feet is a later gait
  experiment, not a prerequisite for completing V1.
- **Wheeled balance/drive:** raise the forelegs and balance on the rear ankle
  wheel pair. Differential drive turns the robot; hip and knee angles set
  posture and ride height.
- **Lean:** 2-DOF leg hips bank into turns (V1); the torso platform adds torso lean
  once activated (V2).
- **Mode transition:** transfer load from supported stance to rear wheels while
  lifting front feet and establishing balance. CoM, support and servo loads
  throughout the motion remain open; there is no knee-wheel deployment mechanism.
- **No agile climbing in V1.** Rounded front feet add no grasping DOF;
  grippers and winch-assisted clambering remain later options in the backlog.

Closest prior art: **Swiss-Mile / ANYmal-on-wheels** ([`references.md`](references.md)).

## Design principles

1. **DOF budget = cost budget.** Every DOF is one servo (~£15-25 landed). Be ruthless;
   buy spares, not speculative DOF.
2. **Actuator matched to task** (heterogeneous actuation). Spend STS3215-grade money
   only where body weight and balance flow through (limbs). Head/ears/fingers -> micro
   servos; drive -> geared DC. Exploit passive dynamics where possible.
3. **Every part <= 200x200 mm.** Prefer one integrated structural print per link
   (DEC-39), with an explicit print orientation. Add a seam only for a specific
   assembly, service, strength or bed-size reason; any seam remains a designed
   joint derived from the master model.
   Bed fit is enforced by the CAD build. Support-free manufacture remains a
   preference, with accessible local supports allowed. Sliced-layer and physical
   validation remain necessary; the surface-area
   screen alone does not prove it (DEC-29).
4. **Body-as-source-code.** Parametric code-CAD (`build123d` / `CadQuery`) so `bed_size`
   and `scale` are parameters, geometry lives in-repo, and it can export URDF.
5. **Finish V1 end-to-end before the family** — design -> print -> BOM -> firmware ->
   app -> docs -> one video.
6. **Mechanical honesty** (banked from an InMoov build): no plastic-on-plastic sliding
   threads; real bearings, rotary-servo + pushrod linkages, or metal leadscrews;
   low-friction spherical bearings; a *virtual* pivot via a parallel mechanism where
   it earns its keep.
7. **Child-safe by design.** The audience is young children (2-5). No pinch points at
   joints/linkages; software speed & torque caps + e-stop; graceful (gentle) falls; a
   protected/enclosed LiPo; no small detachable / choke-hazard parts; rounded edges; no
   hot exposed surfaces. Specifics tracked in [`open-questions.md`](open-questions.md) (OQ-10).
