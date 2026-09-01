# koala-bot 🐨🤖

An open-source, 3D-printable family of small companion robots — nature-inspired,
affordable, and fully documented (build video + full BOM + software).

**Status:** pre-alpha — *design phase*. Mechanics, electronics, and software are
still converging; nothing is built yet. This repo currently holds the **design
record**. See [`docs/roadmap.md`](docs/roadmap.md) for direction and
[`docs/open-questions.md`](docs/open-questions.md) for what's undecided.

## What it is

The first family member, **Koala (V1)**, is a **self-balancing, wheel-footed
companion** roughly the size and shape of a koala, printable in **PETG on a
200×200 mm bed**. It sits between *locomotion showpiece* and *desk companion*:
- rolls and balances on two knee-wheels (rear legs);
- leans into turns via 2-DOF leg hips;
- gestures with 3-DOF dual-purpose front limbs (arms *and* forelegs);
- looks at you with a 3-RPS parallel neck (yaw delegated to the mobile base).

Locomotion is ground-based; a **climbing sibling** is a planned later family
member. Full intent, morphology, and principles: [`docs/concept.md`](docs/concept.md).

## Repo map

| Path | Contents |
|------|----------|
| [`docs/`](docs/) | The design record — concept, architecture, decisions, roadmap, sourcing (**start here**) |
| `hardware/` | CAD / printable parts (parametric code-CAD — planned) |
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
