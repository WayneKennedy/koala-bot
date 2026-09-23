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
- **A DEC survives discarding the CAD, or has physical evidence** (DEC-59). Feedback on a
  render, a marked-up screenshot, a choice between assistant-generated options, approval to
  continue, or the assistant's own geometry is a **revision note** in
  [`docs/cad-integrated-design.md#revision-log`](docs/cad-integrated-design.md#revision-log),
  status `unprinted`. Never bank it as a decision. Corrections of assistant errors go to
  `docs/test-log.md` or the pattern doc.
- **Check what is owned before suggesting a purchase.** Read the private
  [wk-inventory `docs/stock.md`](https://github.com/WayneKennedy/wk-inventory/blob/main/docs/stock.md)
  and search the owner's invoices, and say what was found. Full rule and the owner's goal
  (fewer unused parts, more finished projects):
  [wk-inventory `AGENTS.md`](https://github.com/WayneKennedy/wk-inventory/blob/main/AGENTS.md#before-anything-is-bought).
- **Every printed part has a version** (owner, 2026-09-19). `version` in the part's spec,
  ledgered with a geometric fingerprint in [`hardware/part-versions.json`](hardware/part-versions.json)
  (`uv run python -m koala_hardware.part_versions`, `--update "<what changed and why>"` after a
  bump). A geometry change without a bump fails `tests/test_part_versions.py`. `proven` and every
  `test-log.md` entry name the version printed; a bump resets the part to `unknown` unless the
  entry says the change is cosmetic. Versions never go down. The generated BOM shows them.
- **Before building on any redesign, render it from several angles and ask: does this
  design look stupid?** (owner, 2026-09-19, after a rotated-flange torso that cut the rails,
  broke the battery space and looked dumb reached the viewer.) `uv run python -m
  koala_hardware.render_views <part>` writes `docs/design/parts/<part>-views.png` (iso, front,
  side, top). Look at it, answer the question honestly in the revision log, and only then run
  the export/audit/viewer chain. A render that would embarrass the project is a stop, not a note.
- **Per-part printability:** maintain `unknown`, `assumed` or `proven` in
  [`docs/part-design-review.md`](docs/part-design-review.md) (DEC-47). New parts
  default to unknown; reassess after changes; proven needs a recorded print.
- **Guiding rules** (see `concept.md`): *DOF budget = cost budget* · *actuator matched
  to task* · *every part ≤ 200×200 mm* · *finish V1 end-to-end before the family*.

## Status

**2026-09-21 — walking first (DEC-62):** build with four identical
`front_contact_pad` v1 TPU feet and new handed `foot_shank` v1 rear links,
without rear drive hardware. Swap complete rear shanks at the retained knees
for the wheeled V1 end goal; `shank` v2 geometry is unchanged. The walking
reference uses 90 mm knee-to-pad centres and 132.6 mm rear foot spacing at
neutral roll; 220 mm remains the wheel track. The viewer opens in `walking`
and retains both wheeled poses. New shanks are `unknown`/unprinted.
[Files, assembly and evidence](docs/design/walking/README.md).

**Phase 1 (V1 vertical slice), current CAD 2026-09-19:** recessed **roll → pitch**
front shoulders now complement the retained **pitch → roll** rear legs. This is
an **unprinted revision**, recorded in
[`cad-integrated-design.md`](docs/cad-integrated-design.md#revision-log), not a new
banked decision. Historical DEC-37/40/42/44/45/46/48/49/55/56/57/58 references
name revision notes following DEC-59. DEC-60 retains 220 mm rear track with
52.5 mm rear pitch centres; DEC-61's 45° rear sockets and bracket are implemented
in the main assembly.

Torso v5 extends to shoulder cap Z183.5 while retaining **150 mm hip-to-shoulder
spacing**. Its ±47 mm side envelope wraps sockets whose lips are at ±37 mm:
**10 mm recess**, not a claim that horns or moving carriers are flush. Front
A roll centres are 110.23 mm apart; B pitch centres are 190.23 mm apart. Each
front A module mounts to a removable `shoulder_mount` v1 cassette on the bench;
load all four cassette frame nuts **before** attaching the A root. Four
front-access M3×20 secure each cassette to the torso; service removal is
laterally outward. The unchanged
`root_socket` v1 remains the same print at all four limbs. Rear driver corridors
now pass through the complete torso.

Front `shoulder_carrier` is **v3**; `upper_arm` and `forearm` remain **v2**;
all are **`unknown`**. B sits 40 mm outboard of A, with extra separation because
the B35 trial's full upper-arm/A-case sweep stopped at +6° roll. Their
broad common print planes, open forks, enclosing pockets and filleted roots
apply the rear redesign lessons. Front B/C shafts are parallel: the sideways
"hug" elbow remains OQ-25. Torso v5, shoulder mount v1 and corrected-rounding
thigh v3 are also `unknown`; shank v2 and hip carrier v1 retain `assumed`.
Root socket v1 is **`proven`** (plate 1, 2026-09-19: fit passes; ear holes need
clearing because the old profile lacked bed-only support, now fixed).
Hip-carrier v1 has plate 2 slices; no physical result is recorded. Existing
thigh v2 slices do not validate v3; unchanged shank v2 retains its slice record.
All 11 changed handed exports have current-version/hash-matched local organic
bed-only slices and selected layer plots in the
[front record](docs/design/front-redesign/README.md), including carrier v3.
Those support the proposed print approach without proving physical removal or
strength; changed parts remain `unknown`.

There are **19 designs / 28 handed exports** including six coupons and both
rear-shank alternatives; the robot uses **28 physical prints walking / 26 wheeled**. The [front record](docs/design/front-redesign/README.md)
contains views and full front moving-package roll checks at ±30°/2° in both
saved configurations, plus installed two-front checks at five roll settings.
The 1° adjacent-joint report has narrower carrier-only roll scope; it does not
define whole-limb travel. None proves continuous or loaded movement.
The viewer/assembly use the distinct front and rear transform orders; hidden
parts still constrain the sampled clearance search. Node.js is required to
build its geometry/engine-hashed caches. Calibration, complete cables and
loaded acceptance remain OQ-21/22.

Retain twelve STS3215 limb joints, the bought 37D rear drives, 85/90 mm rear
links, 70 mm upper arms, 100 mm elbow-to-front-contact reach, 220 mm rear track
and the 450 mm upright head-top sizing target. A dorsal shoulder slot and four
M3 points reserve a removable cartridge for **three small bought STS3032M** neck
servos. [Neck provision](docs/design/neck-provision.md) distinguishes published
case envelopes from the unmeasured M variant; servo retention, fixed-lead
boards, 3-RPS linkage and head position remain open. No neck print is added.
Battery/electronics packaging, guards and loaded transitions remain OQ-17/18/26.
Shared SO-101 fit remains accepted; no repeat gauge is required (DEC-33).

Start with [`cad-integrated-design.md`](docs/cad-integrated-design.md) and
[`part-design-review.md`](docs/part-design-review.md). Record physical support
removal, fit, stiffness and creep by exact print version; TPU traction and wear
remain OQ-19. Independent CAD and images live in [`docs/design/`](docs/design/README.md).

**One cheap check is worth doing before firmware:** micro-ROS upstream has not tested
the Teensy 4.0 that DEC-18 bought — **[OQ-14](docs/open-questions.md)**, with the
consequence for the bridge in
[`docs/architecture.md`](docs/architecture.md#bridge--contract).
