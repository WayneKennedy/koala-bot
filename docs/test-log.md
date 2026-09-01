# Test log

What printed parts actually showed, including "no change needed" — so the next
person knows a constant was **tested**, not guessed. Constants themselves live
in `hardware/src/koala_hardware/params.py`, tagged with their provenance.

Reference printer per DEC-14 (Ender-5 S1 / Klipper), PETG, the standing
general-purpose profile recorded in [`bom.md`](bom.md).

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
