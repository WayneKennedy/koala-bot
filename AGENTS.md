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
- [`docs/body-layout.md`](docs/body-layout.md) — DEC-43/44 accepted device layout,
  resolved dimensions and engineering choices; viewable PNG/SVG/STEP masters
  live in [`docs/design/`](docs/design/README.md).
- [`docs/cad-integrated-design.md`](docs/cad-integrated-design.md) — current
  implemented chassis, assembly sequence and validation scope.
- [`docs/integrated-links.md`](docs/integrated-links.md) — DEC-39: integrated
  SO-101-style structural links, with seams only where justified.
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
  socket primitive, the process and its gates. Historical requirements;
  start current CAD with `cad-integrated-design.md`.
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
  the bus adapter (the 6-packs shipped **without** the listed FE-URT-1 — use the family's Waveshare Bus Servo Adapter (A) or FE-URT-2), one servo at a time
  because every unit ships as ID 1, the 6 V/12 V rail distinction, and the FTDI latency
  trap. **Read that before configuring the limb servos** — twelve V1 joints (DEC-31),
  eight units in hand (four of the twelve bought went to SO-ARM101 on 2026-09-12; `docs/bom.md`), each shipped as ID 1.
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
- **Per-part printability:** maintain `unknown`, `assumed` or `proven` in
  [`docs/part-design-review.md`](docs/part-design-review.md) (DEC-47). New parts
  default to unknown; reassess after changes; proven needs a recorded print.
- **Guiding rules** (see `concept.md`): *DOF budget = cost budget* · *actuator matched
  to task* · *every part ≤ 200×200 mm* · *finish V1 end-to-end before the family*.

## Status

**Phase 1 (V1 vertical slice) — DEC-49/50 common carriers and asymmetric sockets, 2026-09-11.**
The accepted DEC-44 overall layout is retained. Production CAD now implements
rounded links/fork roots, enclosing servo sockets, independently removable
left/right root socket modules, flatter forearms and separate keyed TPU contact
pads with recessed metal fixings. There are 17 designs / 24 handed exports
including six coupons; the chassis uses 24 physical prints. Every current print
is tagged `assumed`, with local slices and layer images in
[`docs/design/manufacturing/`](docs/design/manufacturing/README.md). None is proven
by a physical print of this revision. Shared SO-101 fit remains accepted; no
repeat gauge is required (DEC-33).

Retain pitch → roll, twelve ST3215s, two bought 37D rear ankle drives,
70 mm upper arms, 100 mm elbow-to-contact centres, 85/90 mm rear links,
150 mm torso, 220 mm rear track and 450 mm upright head-top sizing target.
Common carriers are printed twice per hand, at 149 mm front/rear roll spacing.
Rear pitch cases point forward in the torso frame; their integral socket
returns meet a rear flange raised to Z=46 mm; bolt/pin XY positions and
fastener stacks are retained. Drive/idler socket slots
are 14/18.5 mm wide. Head placement is undecided and omitted from structural CAD.
The viewer uses sampled pose-dependent mechanical-clearance ranges (DEC-46),
with initial caches tied to geometry/engine hashes. Hidden parts still constrain
travel. Node.js is needed when building the static viewer. Calibration, cables,
loads and continuous travel acceptance remain open (OQ-21).

Start with [`docs/cad-integrated-design.md`](docs/cad-integrated-design.md) and
[`docs/part-design-review.md`](docs/part-design-review.md). The new joint rig,
physical support removal, fitting and load/creep checks remain OQ-12/13/20;
TPU grade/traction and wear are OQ-19. Head/neck, complete electronics/battery
packaging and loaded transitions remain OQ-17/18. No extra front drive hardware
is required. Independent images and CAD live in [`docs/design/`](docs/design/README.md).

**One cheap check is worth doing before firmware:** micro-ROS upstream has not tested
the Teensy 4.0 that DEC-18 bought — **[OQ-14](docs/open-questions.md)**, with the
consequence for the bridge in
[`docs/architecture.md`](docs/architecture.md#bridge--contract).
