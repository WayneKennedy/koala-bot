# koala-bot 🐨🤖

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

An open-source, 3D-printable family of small companion robots — nature-inspired,
affordable, and fully documented (build video + full BOM + software).

**Status:** pre-alpha — *design phase*. Mechanics, electronics, and software are
still converging; nothing is built yet. This repo currently holds the **design
record**. See [`docs/roadmap.md`](docs/roadmap.md) for direction and
[`docs/open-questions.md`](docs/open-questions.md) for what's undecided.

## What it is

**Build order (DEC-62):** first train quadruped walking with four TPU feet.
[Footed rear shanks](docs/design/walking/README.md) interchange at the existing
knees with the wheeled shanks; wheels remain the V1 end goal.

The first family member, **Koala (V1)**, is a **self-balancing, wheel-footed
companion** roughly the size and shape of a koala, printable in **PETG on a
200×200 mm bed**. It sits between *locomotion showpiece* and *desk companion*:
- rolls and balances on two wheel-feet (rear legs, wheels at the ankles);
- crouches and stands on articulating knees, leans into turns via 2-DOF hips;
- gestures with 3-DOF dual-purpose front limbs (arms *and* forelegs);
- looks at you with a 3-RPS parallel neck (yaw delegated to the mobile base).

Locomotion is ground-based; a **climbing sibling** is a planned later family
member. Full intent, morphology, and principles: [`docs/concept.md`](docs/concept.md).

## Repo map

| Path | Contents |
|------|----------|
| [`docs/`](docs/) | The design record — concept, architecture, decisions, roadmap, BOM, sourcing (**start here**) |
| [`hardware/`](hardware/) | CAD / printable parts (parametric code-CAD — draft v0 lower body) |
| `firmware/` | Real-time MCU code — balance loop, servo bus (planned) |
| `software/` | Pi / ROS2 high-level brain + tooling (planned) |
| [`LICENSING.md`](LICENSING.md) | Tri-licence (hardware / software / docs) |

## Docs are written AI-first

Most docs assume an **AI assistant is the primary reader** — dense, factual,
cross-referenced, greppable — and every artefact meets the **4Cs**
(Correct · Complete · Coherent · Concise). See [`AGENTS.md`](AGENTS.md).

## License

Tri-licensed — `CERN-OHL-S-2.0` (hardware) · `MIT` (software) · `CC-BY-SA-4.0`
(docs). See [`LICENSING.md`](LICENSING.md). Full licence texts are in `LICENSES/`.

CAD now uses native FreeCAD generators with revision-paired Python/FCStd files (DEC-63):
[workflow and artefacts](docs/freecad.md).
