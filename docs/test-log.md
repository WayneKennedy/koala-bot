# Test log

What printed parts actually showed, including "no change needed" — so the next
person knows a constant was **tested**, not guessed. Constants themselves live
in `hardware/src/koala_hardware/params.py`, tagged with their provenance.

Reference printer per DEC-14 (Ender-5 S1 / Klipper), PETG, the standing
general-purpose profile recorded in [`bom.md`](bom.md).

## 2026-09-08 — calipers on the Waveshare ST3215 with both horns fitted (in progress)

The measurements DEC-33 waived, taken anyway because the DEC-34 review found
the clevis span resting on an upstream CAD figure that upstream's own two
joints disagreed on. Values are added here as they are taken; each moves the
constant it names to `[MEASURED]`.

| # | Measurement | Value | Consequence |
|---|-------------|-------|-------------|
| 1 | Drive horn outer face → idler wheel outer face | **36.4** | `SOCKET_HORN_SPAN` 37.5 → **36.4**. Corroborated independently: the printed SO-101 `Rotation_Pitch` fork is 36.4 inner face to inner face, and `Rotation_Pitch_SO101.step` has its arm faces at Y = 10.0 and 46.4. The 37.5 in `soarm-joint-pattern.md` was a probing error there (an axis probe read a ~1 mm centre recess in the idler-side arm, not the arm face); upstream's CAD was right, as was the 2026-09-02 SO-100 bracket reading. Every span-derived figure in DEC-34 (drive-face datum, crossbar length, motor face, track, bolt grips) shifts by 1.1 mm; `params.py` derives them |

**Superseded the same day by the maintainer's point that the printed-part
STEPs are proven by fit.** Items 4, 5, 8 and most of 7 are now read from the
parts themselves ([`soarm-joint-pattern.md`](soarm-joint-pattern.md), "read
from the printed parts alone"): pocket, lug positions and hole stack, flat
clevis plates with centre recesses, the base joint's 22 mm rear cable window.
What the parts cannot say, because no part file knows where the servo sits
inside it and upstream's assembly mates are ~1.9 mm off at the shoulder:

1. **Which side the 1.5 mm horn stack lives on.** Does the idler wheel stand
   proud of the case's main flat, and by roughly how much? (Depth rod from the
   wheel face to the flat beside it; zero means all 1.5 is on the drive horn.)
   *Partly answered 2026-09-08, maintainer with calipers:* SO-101 **does fit
   the idler**. It is **3.1 thick overall: a 2.1 mm main body, drilled and
   tapped M3 on the same 9.9 square as the drive horn, plus a 1.0 mm boss**.
   The servo's rear face carries a proud round boss ~Ø8 with a centre hole
   (photo IMG_6989). The printed idler-side arms have blind centre recesses of
   Ø6 × 1.0 (Rotation_Pitch) and Ø8 × 1.5 (Upper_arm), which is the room for a
   1 mm feature at the axis. *Further, same day:* the **boss faces inward**,
   engaging the servo's rear boss, and **both the drive horn and the idler
   present flat outer faces when fitted**. So the arms bear on flat metal on
   both sides and the arm centre recesses are clearance for the centre
   fixings, not for a boss. Because the whole stack is only 1.5 over the 34.9
   pocket while the idler body alone is 2.1 thick, the idler body must seat
   below the case main flat, in a pocket in the back face. **Last number
   wanted:** depth-rod from the idler's outer face to the case main flat beside
   it, idler fitted. That is the idler stand-off; the drive horn gets the rest
   of the 1.5.
2. **Where the connectors are and which way the cable leaves.** The Base has a
   22 mm window behind the rear face; the Rotation_Pitch shelf is solid. Look at
   the shoulder servo in the assembled arm.
3. **The fourth lug.** `Motor_holder_Base`'s horn-side boss has a plain Ø4.0
   bore with no 2.2 mm seat, unlike the other three positions. What does the
   servo present there — a Ø4 post, a threaded boss, or a plain lug?

## 2026-09-08 — DEC-34 digital prototype checks (nothing printed)

Replaced both discarded lower-body builders. Export passes the existing bed,
connected-solid and surface checks; explicit handed STLs are generated.
The audit checks the socket and bores, 27 local roll/hip/knee poses with
nominal horn/carrier/motor/lug heads and nuts, and 81 opposing-leg pose pairs.
The browser regression rendered the assembly and matched left/right hip/knee
motion to CAD within 0.1 mm; eight unit tests passed. Scope and remaining
uncertainties are in [`cad-restart-design.md`](cad-restart-design.md).

Read-only Moonraker queries on 7 September and at 00:01 BST on 8 September
returned **printing**. No slicing or print was
started. The five `coupon_socket_*` parts are the next fit rig; they include
the same registered cheeks and crossbar interface as the legs. None of these
digital results establishes physical fit, unsupported-layer behaviour or
strength.

## 2026-09-07 — maintainer confirms SO-101 fit in PLA+ and PETG

The maintainer reports that the standard ST3215 servos fit the SO-101 parts
perfectly in **both PLA+ and PETG**, and explicitly removes the requirement
for repeat gauging or caliper measurements before redesign (DEC-33).
The earlier local `3d-printing` entry documents the PLA+ Gauge_0 test;
the PETG evidence here is the maintainer's direct report. No print settings,
new caliper readings or individual PETG job identifiers were supplied.

Adopt the Gauge_0 nominal pocket with zero added servo clearance
(`SOCKET_CLEAR` in `params.py`). This does not validate generic non-servo
pockets, new retention details, or the new joint's loaded behaviour.
The new primitive's lug positions and horn span remain tagged `[STEP]`.

## 2026-09-07 — SO-101 joint pattern, measured from upstream CAD (desk study; nothing printed)

Prompted by the maintainer's SO-101 build: the koala drafts never followed the
mounting pattern DEC-21 named. Upstream's assembly and part STEPs were measured
with booleans and sections; full record and numbers in
[`soarm-joint-pattern.md`](soarm-joint-pattern.md). What changes for koala:

| Finding | Source | Consequence |
|---------|--------|-------------|
| Retention is **cradle + collar + 4 M2 self-taps into the servo's lugs**, then a **clevis on both horns** | Base/Base_motor_holder, Rotation_Pitch/Motor_holder_Base, Upper_arm | DEC-21 amended to say so; both drafts logged as breaches; the restart builds it as one primitive |
| Lug holes sit at **~2.1 mm from the rear face on the back face and ~5.8 mm on the horn face** | Ø2.0 holes in Base roof/floor and Rotation_Pitch walls | `SERVO_TAB_X = −20.7` matches one face only → the open check below gains a second number |
| Case-screw hole in plastic is **Ø2.0 clearance, ~2.2 long, counterbored above** | all four parts | `SERVO_TAB_HOLE` 4.0 → 2.0; the M2×5 "too short" finding is solved by counterboring, not longer screws |
| Pocket **34.9 × 24.7, zero clearance**, press fit in PLA+ on this printer | `Gauge_0`; `3d-printing` print-log 2026-09-06/07 | `CLEAR_POCKET` (0.25, PETG) gets its value from printing `Gauge_0` in PETG, not from a guess |
| Horn pattern **9.9 square**, plates 3.5 thick, holes Ø3.0–3.2, idler bolted too | Upper_arm, Rotation_Pitch | confirms `SERVO_DRIVE_SQ` and the 2026-09-02 idler finding; `CLEAR_HOLE_M3 = 3.4` (measured) stays |
| Upstream's assembly **servo model overlaps its own cradle wall** by ~2 mm | assembly STEP | second servo model found wrong; measure printed parts and real servos only |

**Added to the open caliper checks below (2026-09-02 §Open):** 8. lug offsets from
the rear face on *both* faces; 9. lug pilot depth; 10. horn and idler stand-off
and the full horn stack for the clevis span.

## 2026-09-07 — servo box contents (Waveshare ST3215 12V ×2, Amazon; nothing printed)

Two 12 V ST3215 servos bought from Amazon as test-fit hardware — real cases to
try printed parts against before the RCmall order is committed. **The box, not
the servo, is the finding.**

| Finding | Source | Consequence |
|---------|--------|-------------|
| **The case fixing screws are M2 self-tapping, supplied as M2×5** | in the box | Answers open check 5. `SELFTAP_DIA` 2.5 → **2.0**, `SELFTAP_CLEAR` 2.8 → **2.4**, `SELFTAP_PILOT` 2.1 → 1.7. The 2.5 was a guess and it was wrong |
| **M3 horn screws are in the box** | in the box | [SPEC 11] "No Accessories" describes the bare Feetech part, not this retail box. Treat kit contents as a per-vendor fact from here on; the RCmall 6-packs are still unknown |
| M2×5 is **too short for our walls** | CAD measurement, this session | The screw crosses **3.95 mm** at one end wall of `hip_bracket.build_root()` and **6.35 mm** at the horn-side wall, leaving ~1 mm and ~0 mm of engagement. Buy longer (M2×8 suits the thin wall); better, equalise the walls to one flange thickness first |
| An M2 screw does not thread a Ø4 hole | above + `SERVO_TAB_HOLE` | Reinforces open check 2: the STEP's Ø4 is a recess, a boss OD, or wrong — it is not the thread the supplied screw forms |

**Still unmeasured, and these servos can answer all of it with calipers:** open
checks 1, 2, 3, 4, 6 below, plus the case bore depth the screw length depends
on, and whether the horns themselves were in the box (check 7). Nothing here
came off a caliper yet — it is a screw packet read at face value.

## 2026-09-02 — servo interface review (desk study, nothing printed)

A design review in the 3D viewer asked why nothing in `hip_link` retains the
servo body. Nothing does. Chasing it exposed one real error, one invented
feature, and a category confusion that produced several wrong conclusions
before it was caught.

### The category error, because it will recur

The STS3215 has **two independent feature families on two different datums**:

| | Datum | Where | Rotates? | Fastener |
|---|-------|-------|----------|----------|
| **Body mount** | the **case** | corners, y = ±10.4 (20.8 mm apart, ~2 mm from the edge) | no | self-tapping, into the printed pocket |
| **Horn drive** | the **output axis** | 9.9 mm square on the Ø20 metal horn, + a centre M3×6 into the 25T spline | **yes** | M3 |

`servo_iface.on_axis()` expresses everything relative to the output axis, which
puts both families in one frame and makes them look comparable. They are not.
The axis sits `SERVO_AXIS_X` from the body centre, so **a body feature written
as "distance from the axis" silently depends on the horn datum**. Every wrong
turn this session was a swap between those two columns.

### Settled, with attribution

| Finding | Source | Consequence |
|---------|--------|-------------|
| **Drive-square screws are M3, not M2.5** | upstream's bracket drills Ø3.2 (M3 clearance) on the 9.8 mm square, and their arms assemble | `SERVO_DRIVE_SCREW` was 2.9. **An M3 will not pass 2.9.** Fixed. The STEP models these at 2.5 — the M3 *tapping drill* — which read as M2.5 |
| Spec 6-13 M3×6 is the **horn centre screw** | [SPEC 6-13] 出力轴螺丝, singular; drawing leader points at the spline | It is *not* evidence about the drive square. An earlier claim that "three independent sources agree" was wrong — two were TheRobotStudio files with a common author, the third was this |
| **No screws are supplied** | [SPEC 11] "No Accessories" | Buy M3×6. Also: no horn ships with the servo, so **horn geometry is not servo geometry**. *Superseded in part 2026-09-07: the Waveshare retail box does ship screws* |
| Case is PA+GF, 55 g, 45.23 × 24.73 × 35 | [SPEC 6-1/6-3/6-8] | Recorded `[SPEC]`. Pocket constants stay on the STEP's 45.4 × 24.8 — 0.2 mm generous is the safe error |
| `SERVO_AXIS_X` = 12.5 and `SERVO_TAB_Y` = ±10.4 | dimensioned on / corroborated by the Feetech drawing | The two numbers that were in doubt are now the two that are solid |
| Retention is **pocket + 4 self-tapping screws**, 2 front + 2 back | [SO-ARM101 assembly video](https://www.youtube.com/watch?v=rVP1XQ0PeM4) | `hip_bracket`'s architecture is right in kind. `hip_link` has none at all |
| A **wrap-around bracket** is fitted to the **base servo only** | same video, later frames | Optional reinforcement for the highest-load joint — not the standard mount. Koala's **hips are the direct analogue**, so it likely applies there and nowhere else |

### The idler is a second horn, not a bearing surface

From the assembly video: the idler face carries **another metal horn with the
same 4-hole square**, free-spinning about the output axis, there to give the
joint axial alignment. Three sources agree once you look: the STEP shows the
9.9 mm square at **both** Z ends, upstream's bracket carries the pattern on
**two walls 36.4 mm apart**, and `drive_hole_cutters()`'s own docstring already
said *"bolts onto the horn (or idler)"*.

**No part used it that way.** `hip_link` and `thigh_upper` both put a plain
Ø20.5 clearance bore through the aft plate — removing exactly the material that
should bolt to the idler horn, and leaving every driven joint a **cantilever
hanging off one horn** where upstream builds a supported clevis. Fixed: both
forks now bolt 4 × M3 on each plate, 8 per joint.

This sits in the *horn* family, which is settled, so it did not need to wait for
measurement. What does: **how far the idler horn stands proud of the case.** The
STEP models it recessed, `servo_envelope()` models it 2 mm proud, and they
cannot both be right. If it stands proud, the aft fork plate must move outboard.

### Why the STEP misled us

`STS3215_03a.step` models the servo **with horn and idler fitted**; the Feetech
drawing shows the **bare** servo. That single fact explains every discrepancy —
the Ø20 disc, the 9.9 mm square, and the 39.6 mm height against a 35 mm case.
The file is not wrong; it depicts a different object. Its author is **unknown**
— TheRobotStudio distributes it, but it models 45.4 × 24.8 where Feetech states
45.23 × 24.73, which is not what an export from the maker's own data looks like.

### Open — measure the physical servos (arriving Fri 2026-09-04)

1. **`SERVO_TAB_X` = −20.7.** From the STEP only; the drawing gives no X
   dimension. It positions every retention screw. *Measure: hole centre to the
   end face of the case, along the long axis.*
2. **Bore or pillar?** `SERVO_TAB_HOLE = 4.0` is an interpretation — a STEP
   cylinder does not say which side is material, so this may be a hole or a
   clamshell post. *Measure: does a pin pass through?*
3. **The rear-tab flange.** `servo_iface.servo_envelope()` adds a block 5 mm
   past the case end and ~3 mm proud each side, on no drawing and in no photo.
   It thins `hip_bracket`'s nominal 4 mm walls. *Measure: are there ears?*
4. **Drive-square radius.** 6.93 mm (9.8 square) or 9.8 mm (bolt circle)?
   *Measure: spline centre to one hole.* Also turn the horn and watch whether
   the rear square turns with it.
5. **Screw sizes** for the four body screws. *Answered 2026-09-07: M2
   self-tapping, supplied as M2×5. The bore depth they thread into is not.*
6. **Idler horn stand-off** — how far the aft disc sits proud of the case face.
   *Measure: case rear face to idler horn outer face.* The aft fork plate
   position (`SERVO_IDLER_BOT`) depends on it.
7. **How many horns are in the box.** Each driven joint needs **two** — drive
   and idler — so the lower body needs **8**, and Feetech supplies none
   ([SPEC 11]). The BOM now has a line for them. *Still open 2026-09-07: the
   Waveshare box held horn screws; the horn count in it was not recorded.*

## 2026-09-01 — `coupon_ladder` (pre-fix revision)

First koala-bot part ever printed. Three questions asked, three answered.

| Check | Result | Consequence |
|-------|--------|-------------|
| **M3 clearance hole** | **3.4 mm is the fit.** Slides free. 3.2 is a tad tight — threads in by hand rather than sliding. 3.6 untested (3.4 already correct) | `CLEAR_HOLE_M3 = 3.4` **confirmed, unchanged** — no reprints needed |
| **Dimensional accuracy** | 150 × 60 × 6 mm came out accurate | The calibration confound is **cleared for this machine**: coupon results can now be folded into `params.py` |
| **Flatness / corner lift** | No corner lifted; slab flat | Large flat footprints print true here. `pelvis_plate` (150 × 100) and `e_tray` are the parts that depended on this |

**Not answered:** the insert bores (3.8 / 4.0 / 4.2) could not be fit-tested —
heat-set inserts not yet in hand, so `INSERT_M3_DIA` stays `[VERIFY]`. The
motor-bore row on this revision was **invalid** (all three broke out of the
slab edge; the Ø37.7 was a scallop, not a hole) and has moved to
`coupon_motor_bore`, to print when the 37D arrives.

**Side observation, not adopted:** a 3.2 mm hole takes an M3 thread by hand.
That is a weak, one-shot thread in PETG and is *not* a substitute for heat-set
inserts on any load path (DEC-12, DEC-23). Recorded only because it bounds how
tight a clearance hole may be before it stops being one.
