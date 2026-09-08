# koala-bot — Agent / contributor onboarding

Context for any AI agent or human working in this repository. **Most docs here
assume an AI assistant is the primary reader.** Read this, then
[`docs/concept.md`](docs/concept.md), before non-trivial work.

## The 4Cs — the standard every artefact meets

Every artefact — docs, source, CAD, commit messages — must be:

1. **Correct** — fact-based. No speculation unless labelled as such. "Unknown" and
   "unverified" are valid answers; confident guesses are not.
2. **Complete** — nothing essential missing.
3. **Coherent** — everything fits together; no contradictions.
4. **Concise** — nothing superfluous.

All four hold at once: completeness never excuses bloat; brevity never excuses
gaps; and none of the other three count if the content is wrong.

## What this project is

An open-source family of small, printable, affordable companion robots. The first
is **Koala V1** — a self-balancing, wheel-footed, knee-articulating, gesturing companion. Full intent
and morphology: [`docs/concept.md`](docs/concept.md).

## Where things live

- [`docs/concept.md`](docs/concept.md) — vision, morphology, design principles.
- [`docs/architecture.md`](docs/architecture.md) — compute tiers, actuation map, power.
- [`docs/decisions.md`](docs/decisions.md) — **banked decisions** (the durable *why*).
- [`docs/open-questions.md`](docs/open-questions.md) — **pending decisions** (unresolved).
- [`docs/roadmap.md`](docs/roadmap.md) — phases from V1 to the family.
- [`docs/backlog.md`](docs/backlog.md) — deferred features & sibling robots.
- [`docs/test-log.md`](docs/test-log.md) — what printed parts actually showed
  (coupon results, incl. "no change needed"); constants live in `params.py`.
- [`docs/bom.md`](docs/bom.md) — **the BOM**: bought parts + printed parts
  (printed table is *generated* by the CAD build; never hand-edit it).
- [`docs/sourcing.md`](docs/sourcing.md) — parts, suppliers, UK landed-cost notes.
- [`docs/references.md`](docs/references.md) — prior art & inspirations.
- [`docs/cad-restart-brief.md`](docs/cad-restart-brief.md) — **the handover for the
  lower-body redesign** (DEC-30/31): invariants, what is kept/discarded, the servo
  socket primitive, the process and its gates. Start here for any CAD work.
- [`docs/cad-restart-design.md`](docs/cad-restart-design.md) — the DEC-34
  replacement: layout tradeoffs, load calculations, fastener stacks and gates.
- [`docs/soarm-joint-pattern.md`](docs/soarm-joint-pattern.md) — what DEC-21
  "SO-ARM compatible" means in numbers: cradle + collar + clevis, measured from
  upstream CAD.
- [`docs/cad-review.md`](docs/cad-review.md) and
  [`docs/cad-redesign.md`](docs/cad-redesign.md) — post-mortems of the two
  discarded drafts (a3f265c, DEC-29). Read for failure modes, not geometry.

## The family, and what does not live here

koala-bot is one robot among several. **Facts true of more than one of them live in
[wk-robotics](https://github.com/WayneKennedy/wk-robotics), not here.** Link to them;
never copy them, because two copies of a fact drift. What is up there and load-bearing
for this repo:

- [Printing](https://github.com/WayneKennedy/wk-robotics/blob/main/docs/common.md#printing)
  — the machine, the material profiles, the press-fit and support findings, the
  ≤ 200 × 200 mm design rule.
- [Actuators](https://github.com/WayneKennedy/wk-robotics/blob/main/docs/common.md#actuators)
  — the STS3215 / STS3032M family, the 3S ceiling, and
  [how to configure a servo](https://github.com/WayneKennedy/wk-robotics/blob/main/docs/common.md#configuring-a-servo--true-for-every-sts-project):
  the FE-URT-1 adapter (bundled with the 6-packs, so already owned), one servo at a time
  because every unit ships as ID 1, the 6 V/12 V rail distinction, and the FTDI latency
  trap. **Read that before configuring the limb servos** — twelve V1 joints (DEC-31),
  twelve units bought, no spare (`docs/bom.md`), each shipped as ID 1.
- [Compute and micro-ROS](https://github.com/WayneKennedy/wk-robotics/blob/main/docs/common.md#compute-the-two-tier-split)
  — the two-tier split this project defined, and the micro-ROS mechanics.
- [Power integrity](https://github.com/WayneKennedy/wk-robotics/blob/main/docs/common.md#power-integrity).

**Sibling repos that inherit decisions made here:**
[wk-devastator](https://github.com/WayneKennedy/wk-devastator) takes this project's
two-tier architecture, its motor-driver selection and its MCU choice as starting points.
Changing DEC-16 or DEC-18 has consequences beyond this repo.

## Working conventions

- **No project fact lives only in chat.** Record durable decisions in `decisions.md`;
  put anything unresolved in `open-questions.md`. Move items between them as they resolve.
- **Distinguish decided from open.** `decisions.md` = committed; `open-questions.md` =
  still debated. Never state an open question as settled.
- **Guiding rules** (see `concept.md`): *DOF budget = cost budget* · *actuator matched
  to task* · *every part ≤ 200×200 mm* · *finish V1 end-to-end before the family*.

## Status

**Phase 1 (V1 vertical slice) — DEC-34 digital lower-body prototype, 2026-09-07.**
The two discarded drafts have been replaced with SO-101 cradle/collar/clevis
joints, articulating knees and ankle wheels. The maintainer confirms servo fit
in SO-101 parts in PLA+ and PETG; DEC-33 removes repeat-gauge/caliper prerequisites.
New parts still need **one joint rig fitted before full leg printing**, then
load/creep tests (OQ-12/13). See [`docs/cad-restart-design.md`](docs/cad-restart-design.md)
for the implemented layout and validation scope. The printer was busy during
this redesign: no new slicing or printing. V1 hardware is ordered and two
fit-test servos are on the bench; electronics bring-up follows the mechanical
gates ([`docs/roadmap.md`](docs/roadmap.md)).

**One cheap check is worth doing before firmware:** micro-ROS upstream has not tested
the Teensy 4.0 that DEC-18 bought — **[OQ-14](docs/open-questions.md)**, with the
consequence for the bridge in
[`docs/architecture.md`](docs/architecture.md#bridge--contract).
