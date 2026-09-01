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

A **self-balancing, knee-wheeled, ground-based** companion, koala-shaped (~40-50 cm tall - a 'big toy' *smaller than a toddler*; DEC-15), printable in
**PETG** with **every part <= 200x200 mm** (designing to the commonest bed
maximises who can build it, even though the reference printer is 220 mm).

### Morphology & DOF (V1)

| Segment | DOF | Actuator | Notes |
|---------|-----|----------|-------|
| Front limbs x2 (arms *and* forelegs) | 3 each | STS3215 bus servo | shoulder pitch + roll + elbow; gesture + balance-assist; grippers optional |
| Rear leg hips x2 | 2 each | STS3215 bus servo | **active in V1** — provide *lean-into-turns* while the torso is rigid |
| Rear thigh + knee-wheel x2 | - | 12V geared DC + encoder (in thigh) | drive **wheel at the outer knee**, constant ground contact; leg ends here in V1 |
| Rear knee (expansion iface) x2 | 0 (V1) | future STS3215 | designed to accept a lower leg + foot later; **deferred, gated on need** (DEC-17) |
| Head / neck | 3 | micro servo + CF pushrod | **3-RPS parallel** (pitch/roll/heave); *yaw delegated to the base* |
| Torso | 0 (V1) | - | **rigid strut** in V1; interfaces pre-designed for a single 3-DOF platform later |

V1 actuator count: ~**10-12 STS3215** (limbs) + **3 micro** (head) + **2 DC** (drive).

### Locomotion

- **Roll / balance:** dynamic two-wheel (rear knee-wheels) inverted pendulum; mass
  carried high (koala posture) makes a forgiving pendulum. Yaw (turn to look) is
  done by the base spinning in place.
- **Lean:** 2-DOF leg hips bank into turns (V1); the torso platform adds torso lean
  once activated (V2).
- **No agile climbing in V1** — a *front-arm winch-haul* assisted clamber is possible
  if front grippers are fitted, but four-limb tree-climbing is a sibling's job (backlog).

Closest prior art: **Swiss-Mile / ANYmal-on-wheels** ([`references.md`](references.md)).

## Design principles

1. **DOF budget = cost budget.** Every DOF is one servo (~£15-25 landed). Be ruthless;
   buy spares, not speculative DOF.
2. **Actuator matched to task** (heterogeneous actuation). Spend STS3215-grade money
   only where body weight and balance flow through (limbs). Head/ears/fingers -> micro
   servos; drive -> geared DC. Exploit passive dynamics where possible.
3. **Every part <= 200x200 mm.** Segment large structures into printable modules; hide
   seams under paneling.
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
