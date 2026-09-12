# CAD restart brief — lower body v2 (DEC-30, DEC-31)

Handover for the harness doing the redesign. The maintainer has assigned this to
**GPT Astra**; any harness must be able to pick it up from this file alone, so
nothing here depends on chat history. Written 2026-09-07.

**Current implementation:** [cad-integrated-design.md](cad-integrated-design.md)
(DEC-40); the DEC-34 [record](cad-restart-design.md) below is historical.

**Current morphology (DEC-36/37/38, 2026-09-08):** use the compact 4×4
[body master](body-layout.md): driven wrist wheels as well as driven ankle
wheels, 70/75 mm front links and 85/90 mm rear links. The old 100/100 mm links,
deck/track targets and 150 mm upper allocation below are historical study
inputs. DEC-40 implements the full four-limb chassis at 220 mm track; the shared-interface requirements
remain load-bearing, and the old builders have been replaced.
**Part strategy (DEC-39):** use integrated SO-101-style links; forks, bridge,
spine and distal socket/motor mount form one structural print by default.
Separate collars/retainers only for their installation or service function.
Accessible local supports are allowed. See [integrated-links.md](integrated-links.md).

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

**Historical brief below:** the DEC-40 implementation record takes precedence
for current builders, part boundaries, dimensions and acceptance-rig names.
The original requirements and failure lessons remain here for traceability.

## 1. Outcome wanted

A new **lower body** as build123d code in `hardware/src/koala_hardware/parts/`:
pelvis, two legs (2-DOF hip, 1-DOF knee, shank, wheel-foot), electronics tray,
and the fit coupons that gate them. It must pass the existing export/audit gates,
and **one printed single-joint rig must fit real hardware and be logged** before
any full leg is printed. The current review starts at the pelvis and lower body;
DEC-38/39 extends the same integrated-link approach to the driven forelimbs.
Head and torso mechanisms remain separate detailed design work.

## 2. Invariants — change none without a new DEC entry

| Invariant | Source |
|---|---|
| Overall height **40–50 cm**, mass ~1.5–3 kg, audience 2–5 years | DEC-15 |
| Morphology: front limbs 3-DOF ×2 with driven wrist wheels, rear hips 2-DOF ×2, rear knees 1-DOF ×2 with driven ankle wheels; 3-RPS head, rigid torso strut | DEC-07/31/36/37/38 |
| Every part ≤ 200 × 200 mm in its declared print orientation; PETG; parametric code-CAD | DEC-09, DEC-23 |
| Wheel Ø80 × 10, 6 mm hub, four 37D 12 V geared/encoder motor envelopes (four motors bought; DEC-43 uses the rear two, the other pair is surplus — DEC-51) | DEC-19/38; `params.py` MOTOR_* / WHEEL_* / HUB_* |
| STS3215 12 V for hips and knees: **12 bought, 12 joints (6 arm + 4 hip + 2 knee), no spare** | DEC-22, DEC-31 |
| Servo mounting = measured SO-101 cradle/collar or four-ear saddle, with both horn forks integrated into the link | DEC-21/39; `soarm-joint-pattern.md` |
| Socket cap heads proud, no countersinks in plastic; counterbore only where a head fouls | DEC-25 |
| No plastic-on-plastic sliding threads; real bearings where things rotate on plastic | DEC-12 |
| Child-safety: no pinch points, rounded edges, no proud fasteners on touchable surfaces | concept.md 7, OQ-10 |
| Electronics tray hosts the TB9051FTG shield (Uno pattern), Teensy 4.0, BNO085; 12 V single rail, 5 V buck | DEC-16/18/19/20, `params.py` UNO_HOLES etc. |

DEC-36/37 now supply the link lengths, track and nominal pose dimensions.
Physical hip-axis packaging must fit that master or receive an explicit
engineering revision; do not silently restore the discarded body proportions.

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
use them at **every** STS3215 joint. Servo faces are named per
`soarm-joint-pattern.md` (Front = drive horn, Back = idler and connectors, Bottom
= the end it stands on, Top, Sides). Numbers come from the printed-part STEPs and
from calipers on the servo (test-log 2026-09-08); the remaining `[VERIFY]` ones
move when the joint rig supplies evidence.

These functions define interface geometry, **not mandatory part boundaries**.
Under DEC-39 the two horn plates and their connecting structure become one
link. A separate collar is needed only for the selected retention/assembly
pattern; the SO-101 elbow saddle is an allowed alternative.

| Function | What it cuts / adds | Nominal |
|---|---|---|
| `cradle()` | floor under the servo's Bottom, a **Front wall** and a **Back wall** 34.9 apart that **boss inward to 31.8 at the M2 holes**, one **Side wall**; open Side and open Top; holds the bottom ~17 mm. Each of Front and Back wall takes one M2 at the ear nearer the Side wall: Ø2.0 × 2.2 seat, then Ø4.0 counterbore outward | pocket 34.9 × 24.7 (zero clearance, `SOCKET_CLEAR`); walls 5, ~7.5 at the bosses |
| `collar()` | 3 mm sleeve, 26 tall, 9 below the floor, top flush with the cradle at 17 so the Back's connector bay clears it; closing wall shuts the open Side 0.16 from the servo; two bosses at the open-Side corners take the other two M2s, same stack. No lanes through the cradle, no cable slot | inner = cradle outer + 0.2 total |
| `clevis_plate(side)` | 3.5 mm **flat** plate on the flat outer face of the horn or idler, 4 × `CLEAR_HOLE_M3` on the 9.9 square with counterbores for the **supplied** M3×6 pan heads (`HORN_SCREW_HEAD_DIA` 5.2 × `HORN_SCREW_HEAD_H` 2.0 → ≥Ø6 × ≥2.5 over a 3.5 web, pad ~6 thick); Front plate: Ø3.2 centre hole plus countersink for the drive horn's pan-head; Back plate: blind centre recess ≥0.7 for the servo boss. Plate outline must stay clear of any height where the case is at full width | idler face −17.0, drive face +19.4 in the pocket frame; span 36.4 |

*Corrected 2026-09-08 from the printed-part STEPs and the bench
([`soarm-joint-pattern.md`](soarm-joint-pattern.md), "Corrections the koala
primitive needs"). The first version of this table split the lugs by face,
specified a Ø20.5 horn recess and a cable slot; all three were wrong and DEC-34
implemented them.*

Lug positions (from upstream printed parts, **adopted under DEC-33; check the new rig**): lateral
±10.25; heights from the Bottom **2.2–2.3 on the Back side, 5.7–6.1 on the Front side**.
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

Reassessed against `f541600` on 2026-09-08: the new measurements invalidate
the earlier socket/audit acceptance. See [impact assessment](cad-measurement-impact.md).

- [x] Servo fit basis recorded in `params.py` and `test-log.md`; caliper/repeat-gauge requirement removed by DEC-33
- [x] Requirements and packaging banked as DEC-32/34 (ranges, loads, mass, height, track)
- [ ] Correct `servo_iface` and the five-part rig to the measured interface in §4; DEC-34's earlier primitive is not accepted
- [x] New `parts/` for pelvis, hip, thigh, knee, shank, wheel-foot, e-tray; old builders deleted
- [ ] Rerun `export`, `audit` (incl. knee), tests and viewer/browser-CAD parity after correction; current audit fails at the plate centre
- [ ] Slice inspection recorded; one joint rig printed and fitted; one leg; the pair
- [ ] Regenerate `bom.md` and fastener metadata after correction; reconcile dimensions and assembly notes across the design/status docs
