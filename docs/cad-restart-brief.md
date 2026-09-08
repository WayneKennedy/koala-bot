# CAD restart brief — lower body v2 (DEC-30, DEC-31)

Handover for the harness doing the redesign. The maintainer has assigned this to
**GPT Astra**; any harness must be able to pick it up from this file alone, so
nothing here depends on chat history. Written 2026-09-07.

**Implementation record:** [`cad-restart-design.md`](cad-restart-design.md) (DEC-34).

**Reading order:** [`../AGENTS.md`](../AGENTS.md) → [`concept.md`](concept.md) →
this brief → [`soarm-joint-pattern.md`](soarm-joint-pattern.md) →
[`decisions.md`](decisions.md) and [`open-questions.md`](open-questions.md) →
[`test-log.md`](test-log.md) → [`../hardware/README.md`](../hardware/README.md).
[`cad-review.md`](cad-review.md) and [`cad-redesign.md`](cad-redesign.md) are the
post-mortems of the two discarded drafts; read them for the failure modes, not
for geometry.

**2026-09-07 amendment (DEC-33):** the maintainer confirms standard ST3215
fit in SO-101 parts in PLA+ and PETG and removes the repeat-gauge/caliper
prerequisite. Use upstream nominal interface dimensions, retaining their
provenance. The single-joint rig, slicing and load-test gates remain.
Requirements and implementation evidence: [`cad-restart-design.md`](cad-restart-design.md).

## 1. Outcome wanted

A new **lower body** as build123d code in `hardware/src/koala_hardware/parts/`:
pelvis, two legs (2-DOF hip, 1-DOF knee, shank, wheel-foot), electronics tray,
and the fit coupons that gate them. It must pass the existing export/audit gates,
and **one printed single-joint rig must fit real hardware and be logged** before
any full leg is printed. Not in scope: arms, head, torso — only their mounting
interfaces on the pelvis/shoulder girdle (DEC-08).

## 2. Invariants — change none without a new DEC entry

| Invariant | Source |
|---|---|
| Overall height **40–50 cm**, mass ~1.5–3 kg, audience 2–5 years | DEC-15 |
| Morphology: front limbs 3-DOF ×2, rear hips 2-DOF ×2, **rear knees 1-DOF ×2**, **wheel at each ankle position as the foot**, 3-RPS head, rigid torso strut | DEC-07 as amended by DEC-31 |
| Every part ≤ 200 × 200 mm in its declared print orientation; PETG; parametric code-CAD | DEC-09, DEC-23 |
| Wheel Ø80 × 10 (Pololu), 6 mm universal hub, 37D 12 V 122 rpm motor with encoder ×2 | DEC-19; `params.py` MOTOR_* / WHEEL_* / HUB_* |
| STS3215 12 V for hips and knees: **12 bought, 12 joints (6 arm + 4 hip + 2 knee), no spare** | DEC-22, DEC-31 |
| Servo mounting = the SO-101 **cradle + collar + clevis** pattern at every powered joint | DEC-21 as amended, `soarm-joint-pattern.md` |
| Socket cap heads proud, no countersinks in plastic; counterbore only where a head fouls | DEC-25 |
| No plastic-on-plastic sliding threads; real bearings where things rotate on plastic | DEC-12 |
| Child-safety: no pinch points, rounded edges, no proud fasteners on touchable surfaces | concept.md 7, OQ-10 |
| Electronics tray hosts the TB9051FTG shield (Uno pattern), Teensy 4.0, BNO085; 12 V single rail, 5 V buck | DEC-16/18/19/20, `params.py` UNO_HOLES etc. |

Track width, stance height, hip axis spacing and thigh/shank lengths are **not**
invariants: they are outputs of this design, to be chosen against the height budget
and recorded (§5).

## 3. What is kept, what is discarded

**Kept, and to be built on:**

- `params.py` — the single source of dimensions with provenance tags
  (`[STEP] [VENDOR] [STD] [SPEC] [VERIFY] [MEASURED] [SUPPLIED]`). Correct wrong
  values in place; never drop a tag. Assembly-layout constants from DEC-26/27/28/29
  (`HIP_ROLL_Y`, `HIP_PITCH_*`, `THIGH_DROP`, `TRACK_HALF`, `PELVIS_PLATE`) are void
  and will be replaced by yours.
- `servo_iface.py` — rewrite around the socket primitive (§4); keep the two-datum
  lesson in its docstring (case datum vs output-axis datum, test-log 2026-09-02).
- `fasteners.py`, `printability.py`, `export.py`, `audit.py`, `validation.py`,
  `viewer.py`, `assembly.py`, `slice_remote.py`, `tests/` — the tooling that caught
  the last defects. Extend `audit.py` to the knee.
- `parts/coupons.py` — review each coupon; `coupon_servo_cradle` is void (it tested
  the enclosing cradle that no longer exists).
- `vendor/so-arm100/` STEPs, all docs, the BOM's bought-parts half.

**Discarded:** every structural builder — `parts/pelvis.py`, `hip_bracket.py`,
`hip_link.py`, `thigh.py`; `e_tray.py` re-derived around the new pelvis. Both old
geometries stay recoverable in git (`a3f265c`, `4fc188a` = DEC-29). Delete, do not
patch: the review found both drafts were patched into their defects.

## 4. The servo socket primitive — build this first

Implement three functions in `servo_iface.py`, parameterised from `params.py`, and
use them at **every** STS3215 joint. Numbers are upstream CAD nominal
(`soarm-joint-pattern.md`); the `[VERIFY]` ones move when the joint rig supplies evidence (DEC-33).

| Function | What it cuts / adds | Nominal |
|---|---|---|
| `cradle()` | pocket for the rear ~17 mm of the case: back wall + two side walls + shelf; open front and top. Each **side wall** takes one lug at the **rear lateral position** (one drive-face, one back-face): Ø2.0 × 2.2 seat then Ø4.0 counterbore to the outside | pocket 34.9 × 24.7 (zero clearance, `SOCKET_CLEAR`); walls 5 (≥4.8) |
| `collar()` | 3 mm sleeve, ~26 tall, overlapping the cradle by ~9 mm, front wall bearing on the servo's front face; two bosses at the **open front corners** take the two lugs at the **front lateral position**, same Ø2.0 × 2.2 + Ø4.0 stack. No lanes cut through the cradle | inner = cradle outer + 0.2 total |
| `clevis_plate(side)` | 3.5 mm **flat** plate bearing on the flat outer face of the horn or idler (both are flat when fitted, test-log 2026-09-08), 4 × `CLEAR_HOLE_M3` on the 9.9 square, **no horn recess**; drive side: Ø3.2 centre hole with a countersink; idler side: shallow blind centre recess ~Ø8 × 1.5 as clearance for the idler's centre fixing | both horns bolted — the joint is never a cantilever |

*Corrected 2026-09-08 from the printed-part STEPs
([`soarm-joint-pattern.md`](soarm-joint-pattern.md), "read from the printed
parts alone"). The first version of this table split the lugs by face and
specified a Ø20.5 horn recess; both were wrong and DEC-34 implemented them.*

Lug positions (from upstream printed parts, **adopted under DEC-33; check the new rig**): lateral
±10.4; from the case's rear face **~2.1 on the back face, ~5.8 on the horn face**.
`SERVO_TAB_HOLE = 4.0` is wrong for a screw hole and becomes 2.0 clearance.

## 5. Leg architecture (DEC-31) and the choices left to you

Chain per leg: pelvis → **hip roll** (STS3215, cradle in the pelvis) → **hip pitch**
(STS3215) → thigh → **knee pitch** (STS3215) → shank → **wheel-foot** (37D motor +
hub + Ø80 wheel). No ankle DOF in V1. Record each choice below as a DEC entry (or
an OQ-16 sub-item if it stays open):

| Choice | Default assumption | What decides it |
|---|---|---|
| Drive motor placement | 37D in the shank, **direct drive**, motor axis = wheel axis, motor body inboard | 69 mm motor body vs shank width vs inner-leg clearance at full knee flex |
| Thigh / shank lengths and nominal knee angle | pick so deck height lands the robot in the 40–50 cm total with the head fitted, knee nominally bent (not locked) for crouch/stand range | height budget, knee servo torque |
| Knee range | ~0–90° from straight | swept-envelope check, cable exit |
| Hip axis order and spacing | roll then pitch, axes as close as the sockets allow (the DEC-26 "one long thigh" lesson holds; its numbers do not) | packaging |
| Knee servo torque check | 30 kg.cm nominal vs (mass share × horizontal moment arm at worst crouch); record the number | DEC-15 mass, your geometry |
| Track width | as narrow as the two motors and inward hip roll allow; any widening is a recorded tradeoff | balance geometry, DEC-27 |
| Cable routing | through-joint slots like SO-101's wiring holders; no cable crosses a pinch line | OQ-10 |

The wheel diameter, hub and motor are fixed (DEC-19); the wheel is the only ground
contact and the pair is a two-wheel inverted pendulum, so the knee and hip together
set ride height and the CoM height the balance loop sees.

## 6. Process, in order, with gates

0. **Fit basis accepted (DEC-33):** the maintainer confirms standard ST3215
   fit in SO-101 parts in PLA+ and PETG. Use the upstream nominal dimensions;
   no caliper prerequisite and no repeat gauge print. Preserve provenance.
1. **Record the fit basis:** `SOCKET_CLEAR=0` is specific to Gauge_0's pocket;
   generic `CLEAR_POCKET` stays separate. The report is in `test-log.md`.
   Printer rules live in `3d-printing`: **never slice while a print is running.**
2. **Bank requirements** as DEC entries before geometry: joint ranges, load cases
   (stance, lean, wheel accel/brake, lateral shove, being picked up), mass budget,
   target deck height and track. The review's step 1 — never done for either draft.
3. **Envelopes before structure.** Model case + both horns + screw heads + driver
   access + cable exit as one keep-out per servo; sweep hip and knee ranges; reserve
   the swept volumes; only then add structure. Carrier and driven link are designed
   *together*.
4. **Design with the primitives**, run `export` (bed fit, surface screen, connected
   solids), `audit` (posed intersections, full-depth hole probes — extend to the knee),
   `tests`, and the viewer. Regenerate the BOM table through the build.
5. **Slice and inspect layers** (`slice_remote`, printer idle), then print **one joint
   rig** (one cradle + collar + clevis on a real servo), log it in `test-log.md`, then
   one full leg, then the pair. Load-test per OQ-11 and record.
6. Update `bom.md` (fastener counts derived from the CAD), `decisions.md`,
   `open-questions.md`. The brief closes when a full lower body passes fit and a
   documented load test.

## 7. Lessons that cost two drafts — do not repeat

- **No pocket or retention from a servo model.** Both `STS3215_03a.step` and
  upstream's assembly servo are wrong in places; the printed parts and calipers win.
- **No invented retention.** Every joint uses §4; a friction cap or screws into an
  unmeasured case wall is a DEC-21 breach.
- **`printability.py` is a screen, not proof.** Support-free is shown by a slice
  inspection and a print, and said so in the docs.
- **Design carrier and driven fork together** around swept envelopes; do not
  clear one collision by moving the other part.
- **Do not widen the track to escape a packaging clash** without a DEC that names
  the tradeoff (DEC-29 went 180 → 258.8 mm this way).
- **Two datums.** Case features are positioned from the case; horn features from the
  output axis. Mixing them produced a run of wrong conclusions.
- **Design each fastener stack as one interface:** head seat, tool access, engagement
  length, assembly order. Blind holes and 44 mm screw paths came from skipping this.
- **Features on one face; no closed cavity floors; forks print axis-horizontal**
  (`hardware/README.md`, "Designing a part that passes").

## 8. Conventions and commands

- **The 4Cs** (Correct, Complete, Coherent, Concise) govern every artefact; label
  speculation; "unverified" is a valid answer. Repo docs are written for an AI
  reader: dense, cross-referenced, greppable.
- Decided → `decisions.md` (`DEC-nn`, newest first); open → `open-questions.md`;
  move items as they resolve; never state an open question as settled.
- Every print, including "no change needed", goes in `test-log.md`; constants live
  only in `params.py` with a provenance tag.
- `bom.md`'s printed-parts table is **generated** by the export; never hand-edit.
- Parts marked `handed` export both `_left` and `_right`.
- Commits: imperative subject saying *why*, body with what changed and what is
  still unverified.

```sh
cd hardware
uv run python -m koala_hardware.export      # STL + renders + gates + BOM table
uv run python -m koala_hardware.audit       # posed intersections, hole probes
uv run python -m unittest discover -s tests
uv run python -m koala_hardware.viewer      # http://localhost:8017
uv run python -m koala_hardware.slice_remote   # only when the printer is idle
```

## 9. Deliverable checklist

- [x] Servo fit basis recorded in `params.py` and `test-log.md`; caliper/repeat-gauge requirement removed by DEC-33
- [x] Requirements and packaging banked as DEC-32/34 (ranges, loads, mass, height, track)
- [x] `servo_iface` socket primitive (§4, amended by DEC-34 for the flush idler) and five-part joint rig
- [x] New `parts/` for pelvis, hip, thigh, knee, shank, wheel-foot, e-tray; old builders deleted
- [x] `export`, `audit` (incl. knee), `tests` green; viewer scene and browser/CAD pose parity checked
- [ ] Slice inspection recorded; one joint rig printed and fitted; one leg; the pair
- [x] `bom.md` regenerated, fastener counts derived; `decisions.md`, `open-questions.md`, `AGENTS.md` status, `hardware/README.md` updated
