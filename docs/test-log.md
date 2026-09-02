# Test log

What printed parts actually showed, including "no change needed" — so the next
person knows a constant was **tested**, not guessed. Constants themselves live
in `hardware/src/koala_hardware/params.py`, tagged with their provenance.

Reference printer per DEC-14 (Ender-5 S1 / Klipper), PETG, the standing
general-purpose profile recorded in [`bom.md`](bom.md).

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
| **No screws are supplied** | [SPEC 11] "No Accessories" | Buy M3×6. Also: no horn ships with the servo, so **horn geometry is not servo geometry** |
| Case is PA+GF, 55 g, 45.23 × 24.73 × 35 | [SPEC 6-1/6-3/6-8] | Recorded `[SPEC]`. Pocket constants stay on the STEP's 45.4 × 24.8 — 0.2 mm generous is the safe error |
| `SERVO_AXIS_X` = 12.5 and `SERVO_TAB_Y` = ±10.4 | dimensioned on / corroborated by the Feetech drawing | The two numbers that were in doubt are now the two that are solid |
| Retention is **pocket + 4 self-tapping screws**, 2 front + 2 back | [SO-ARM101 assembly video](https://www.youtube.com/watch?v=rVP1XQ0PeM4) | `hip_bracket`'s architecture is right in kind. `hip_link` has none at all |
| A **wrap-around bracket** is fitted to the **base servo only** | same video, later frames | Optional reinforcement for the highest-load joint — not the standard mount. Koala's **hips are the direct analogue**, so it likely applies there and nowhere else |

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
5. **Screw sizes** for the four body screws, and **whether a horn is included**
   in the Waveshare package — the BOM has no line for horns.

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
