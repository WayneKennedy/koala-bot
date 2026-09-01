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
is **Koala V1** — a self-balancing, knee-wheeled, gesturing companion. Full intent
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

## Working conventions

- **No project fact lives only in chat.** Record durable decisions in `decisions.md`;
  put anything unresolved in `open-questions.md`. Move items between them as they resolve.
- **Distinguish decided from open.** `decisions.md` = committed; `open-questions.md` =
  still debated. Never state an open question as settled.
- **Guiding rules** (see `concept.md`): *DOF budget = cost budget* · *actuator matched
  to task* · *every part ≤ 200×200 mm* · *finish V1 end-to-end before the family*.

## Status

**Phase 1 (V1 vertical slice) — CAD started, nothing printed yet.** V1 hardware
is ordered (DEC-19/22); a draft v0 lower body lives in `hardware/`
(see its README). Frontier: test-fit coupons -> prototype prints -> electronics
bring-up ([`docs/roadmap.md`](docs/roadmap.md)).
