# koala-bot — Agent / contributor onboarding

> **The project record moved to Basic Memory on 2026-11-10** (project `main`, folder `robotics/koala-bot/`; start at
> the *Koala Bot* note). The README's project description, `docs/concept.md`, `architecture.md`, `roadmap.md`,
> `backlog.md`, `decisions.md`, `open-questions.md`, `bom.md`, `sourcing.md`, `references.md`, `test-log.md`,
> `inspiration/README.md`, every design study and review under `docs/` (`body-layout`, `cad-*`, `drive-motor-sizing`,
> `integrated-links`, `knee-drive-packaging`, `part-design-review`, `root-servo-mounts`, `servo-wrist-loading`,
> `soarm-joint-pattern`, `two-wheel-walking`) and every `docs/design/*` README are canonical there; the copies here were deleted on 2026-11-10 (git history keeps them).
> This repo keeps what is about the code and artefacts: `AGENTS.md`, `CONTRIBUTING.md`, `LICENSING.md`,
> `docs/freecad.md`, `hardware/` (CAD sources, FreeCAD revision archive, migration evidence, sim meshes),
> `firmware/`, `software/`, and the images, STL/FCStd exports and JSON study data under `docs/design/` and
> `docs/inspiration/`.

Context for any AI agent or human working in this repository. **Most docs here
assume an AI assistant is the primary reader.** Read this, then
[*Koala Bot Concept*](memory://main/robotics/koala-bot/koala-bot-concept), before non-trivial work.

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
and morphology: [*Koala Bot Concept*](memory://main/robotics/koala-bot/koala-bot-concept).

## Where things live

- [*Koala Bot Concept*](memory://main/robotics/koala-bot/koala-bot-concept) — vision, morphology, design principles.
- [*Koala Bot Body Layout*](memory://main/robotics/koala-bot/koala-bot-body-layout) — DEC-43/44 accepted device layout,
  resolved dimensions and engineering choices; viewable PNG/SVG/FreeCAD masters
  live in [`docs/design/`](docs/design/README.md).
- [*Koala Bot CAD Integrated Design*](memory://main/robotics/koala-bot/koala-bot-cad-integrated-design) — current
  implemented chassis, assembly sequence and validation scope.
- [*Koala Bot Integrated Links*](memory://main/robotics/koala-bot/koala-bot-integrated-links) — DEC-39: integrated
  SO-101-style structural links, with seams only where justified.
- [*Koala Bot Architecture*](memory://main/robotics/koala-bot/koala-bot-architecture) — compute tiers, actuation map, power.
- [*Koala Bot Decisions*](memory://main/robotics/koala-bot/koala-bot-decisions) — **banked decisions** (the durable *why*).
- [*Koala Bot Open Questions*](memory://main/robotics/koala-bot/koala-bot-open-questions) — **pending decisions** (unresolved).
- [*Koala Bot Roadmap*](memory://main/robotics/koala-bot/koala-bot-roadmap) — phases from V1 to the family.
- [*Koala Bot Backlog*](memory://main/robotics/koala-bot/koala-bot-backlog) — deferred features & sibling robots.
- [*Koala Bot Test Log*](memory://main/robotics/koala-bot/koala-bot-test-log) — what printed parts actually showed
  (coupon results, incl. "no change needed"); constants live in `params.py`.
- [*Koala Bot BOM*](memory://main/robotics/koala-bot/koala-bot-bom) — **the BOM**: bought parts + printed parts
  (printed table is *generated* by the CAD build; never hand-edit it).
- [*Koala Bot Sourcing*](memory://main/robotics/koala-bot/koala-bot-sourcing) — parts, suppliers, UK landed-cost notes.
- [*Koala Bot References*](memory://main/robotics/koala-bot/koala-bot-references) — prior art & inspirations.
- [*Koala Bot CAD Restart Brief*](memory://main/robotics/koala-bot/koala-bot-cad-restart-brief) — **the handover for the
  lower-body redesign** (DEC-30/31): invariants, what is kept/discarded, the servo
  socket primitive, the process and its gates. Historical requirements;
  start current CAD with [*Koala Bot CAD Integrated Design*](memory://main/robotics/koala-bot/koala-bot-cad-integrated-design).
- [*Koala Bot CAD Restart Design*](memory://main/robotics/koala-bot/koala-bot-cad-restart-design) — the DEC-34
  replacement: layout tradeoffs, load calculations, fastener stacks and gates.
- [*Koala Bot SO-ARM Joint Pattern*](memory://main/robotics/koala-bot/koala-bot-so-arm-joint-pattern) — what DEC-21
  "SO-ARM compatible" means in numbers: cradle + collar + clevis, measured from
  upstream CAD.
- [*Koala Bot CAD Review*](memory://main/robotics/koala-bot/koala-bot-cad-review) and
  [*Koala Bot CAD Redesign*](memory://main/robotics/koala-bot/koala-bot-cad-redesign) — post-mortems of the two
  discarded drafts (a3f265c, DEC-29). Read for failure modes, not geometry.

## The family, and what does not live here

koala-bot is one robot among several. **Facts true of more than one of them live in
[wk-robotics](https://github.com/WayneKennedy/wk-robotics), not here.** Link to them;
never copy them, because two copies of a fact drift. What is up there and load-bearing
for this repo:

- [Printing](memory://main/robotics/robotics-common)
  — the machine, the material profiles, the press-fit and support findings, the
  ≤ 200 × 200 mm design rule.
- [Actuators](memory://main/robotics/robotics-common)
  — the STS3215 / STS3032M family, the 3S ceiling, and
  [how to configure a servo](memory://main/robotics/robotics-common):
  the bus adapter (the 6-packs shipped **without** the listed FE-URT-1 — use the family's Waveshare Bus Servo Adapter (A) or FE-URT-2), one servo at a time
  because every unit ships as ID 1, the 6 V/12 V rail distinction, and the FTDI latency
  trap. **Read that before configuring the limb servos** — twelve V1 joints (DEC-31),
  eight units in hand (four of the twelve bought went to SO-ARM101 on 2026-09-12; [*Koala Bot BOM*](memory://main/robotics/koala-bot/koala-bot-bom)), each shipped as ID 1.
- [Compute and micro-ROS](memory://main/robotics/robotics-common)
  — the two-tier split this project defined, and the micro-ROS mechanics.
- [Power integrity](memory://main/robotics/robotics-common).

**Sibling repos that inherit decisions made here:**
[wk-devastator](https://github.com/WayneKennedy/wk-devastator) takes this project's
two-tier architecture, its motor-driver selection and its MCU choice as starting points.
Changing DEC-16 or DEC-18 has consequences beyond this repo.

## Working conventions

- **No project fact lives only in chat.** Record durable decisions in [*Koala Bot Decisions*](memory://main/robotics/koala-bot/koala-bot-decisions);
  put anything unresolved in [*Koala Bot Open Questions*](memory://main/robotics/koala-bot/koala-bot-open-questions). Move items between them as they resolve.
- **Distinguish decided from open.** [*Koala Bot Decisions*](memory://main/robotics/koala-bot/koala-bot-decisions) = committed; [*Koala Bot Open Questions*](memory://main/robotics/koala-bot/koala-bot-open-questions) =
  still debated. Never state an open question as settled.
- **A DEC survives discarding the CAD, or has physical evidence** (DEC-59). Feedback on a
  render, a marked-up screenshot, a choice between assistant-generated options, approval to
  continue, or the assistant's own geometry is a **revision note** in
  [`docs/cad-integrated-design.md#revision-log`](memory://main/robotics/koala-bot/koala-bot-cad-integrated-design),
  status `unprinted`. Never bank it as a decision. Corrections of assistant errors go to
  [*Koala Bot Test Log*](memory://main/robotics/koala-bot/koala-bot-test-log) or the pattern doc.
- **Check what is owned before suggesting a purchase.** Read the private
  [*Stock*](memory://main/inventory/stock)
  and search the owner's invoices, and say what was found. Full rule and the owner's goal
  (fewer unused parts, more finished projects):
  [*Inventory Guide*](memory://main/inventory/inventory-guide).
- **Every printed part has a version** (owner, 2026-09-19). `version` in the part's spec,
  ledgered with a geometric fingerprint in [`hardware/part-versions.json`](hardware/part-versions.json)
  (`./freecad-run -m koala_hardware.part_versions`, `--update "<what changed and why>"` after a
  bump). A geometry change without a bump fails `tests/test_part_versions.py`. `proven` and every
  [*Koala Bot Test Log*](memory://main/robotics/koala-bot/koala-bot-test-log) entry name the version printed; a bump resets the part to `unknown` unless the
  entry says the change is cosmetic. Versions never go down. The generated BOM shows them.
- **Before building on any redesign, render it from several angles and ask: does this
  design look stupid?** (owner, 2026-09-19, after a rotated-flange torso that cut the rails,
  broke the battery space and looked dumb reached the viewer.) `./freecad-run -m
  koala_hardware.render_views <part>` writes `docs/design/parts/<part>-views.png` (iso, front,
  side, top). Look at it, answer the question honestly in the revision log, and only then run
  the export/audit/viewer chain. A render that would embarrass the project is a stop, not a note.
- **Per-part printability:** maintain `unknown`, `assumed` or `proven` in
  [*Koala Bot Part Design Review*](memory://main/robotics/koala-bot/koala-bot-part-design-review) (DEC-47). New parts
  default to unknown; reassess after changes; proven needs a recorded print.
- **Guiding rules** (see [*Koala Bot Concept*](memory://main/robotics/koala-bot/koala-bot-concept)): *DOF budget = cost budget* · *actuator matched
  to task* · *every part ≤ 200×200 mm* · *finish V1 end-to-end before the family*.

## Status

**2026-10-01 — thigh v7 thick horn lead-ins:** both transitions extend across
the screw pattern with deeper counterbores at unchanged bearing-seat depths.
Removal-only thin-neck prototypes are rejected. Unknown/unprinted;
[current geometry and validation](docs/design/thigh-leadin/README.md).

**2026-10-01 — R3 family exterior:** owner corrected the R4 review to include
curved outer horn rims and consistent inner/outer edge fillets. Current scope,
versions, exceptions and validation are in [R3 rounding](docs/design/rounded-family-r3/README.md).
Use `FAMILY_EDGE_RADIUS`; preserve bearing contacts, thin interfaces and accepted
bend caps. Eleven changed production designs remain unknown/unprinted. Root
socket v1's physical evidence is historical; the revised root socket is v2.

**2026-10-01 — full-depth footed links:** owner selected forearm v3 and foot
shank v2 at 20.8 mm depth with matching TPU pad v2; all unknown/unprinted.
Respect the servo-pocket travel boundary. `bend_limits.py` defines the CAD
inspection bounds; native whole-robot endpoint poses and evidence are in
[flat-links](docs/design/flat-links/README.md). These suspended review poses
are not grounded stances or calibrated/loaded motion limits. The 90/100 mm
rear/front lengths remain distinct; common length is still OQ-27.

**2026-09-29 — FreeCAD migration (DEC-63):** Python is canonical; native FCStd
feature histories and matching replay scripts are archived per revision in
`hardware/freecad/`. Read [the FreeCAD workflow](docs/freecad.md) before CAD work.
Use `hardware/freecad-run`, not the uv interpreter, for geometry commands.
Thigh and shoulder carrier are now **v4**, `unknown`/unprinted, recording local
kernel-dependent corner-blend differences. Current dimensions/interfaces are
retained. Earlier v3 slices below are historical. Native Part trees include
Sketcher profiles; they are not PartDesign Bodies. Preserve GUI edits before
regeneration; never edit archived source snapshots. The dated status below
records the pre-migration manufacturing evidence.

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
[*Koala Bot CAD Integrated Design*](memory://main/robotics/koala-bot/koala-bot-cad-integrated-design), not a new
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
servos. [Neck provision](memory://main/robotics/koala-bot/design/koala-bot-design-neck-provision) distinguishes published
case envelopes from the unmeasured M variant; servo retention, fixed-lead
boards, 3-RPS linkage and head position remain open. No neck print is added.
Battery/electronics packaging, guards and loaded transitions remain OQ-17/18/26.
Shared SO-101 fit remains accepted; no repeat gauge is required (DEC-33).

Start with [*Koala Bot CAD Integrated Design*](memory://main/robotics/koala-bot/koala-bot-cad-integrated-design) and
[*Koala Bot Part Design Review*](memory://main/robotics/koala-bot/koala-bot-part-design-review). Record physical support
removal, fit, stiffness and creep by exact print version; TPU traction and wear
remain OQ-19. Independent CAD and images live in [`docs/design/`](docs/design/README.md).

**One cheap check is worth doing before firmware:** micro-ROS upstream has not tested
the Teensy 4.0 that DEC-18 bought — **[OQ-14](memory://main/robotics/koala-bot/koala-bot-open-questions)**, with the
consequence for the bridge in
[*Koala Bot Architecture*](memory://main/robotics/koala-bot/koala-bot-architecture).
