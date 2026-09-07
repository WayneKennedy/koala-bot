# Bill of Materials — Koala V1

Two halves: **bought** parts (below) and **printed** parts (generated from the
CAD, so it cannot drift from the geometry). Prices are UK, inc VAT, ~2026.
Full sourcing rationale and alternatives: [`sourcing.md`](sourcing.md).

**Status:** V1 electronics and actuators are **ordered** (2026-09-01), and two
test-fit servos are **in hand** (2026-09-07, below) — their box contents settle
the servo screw *sizes*, not the lengths. **The DEC-29 geometry is discarded
(DEC-30, 2026-09-07):** the fastener counts and the generated printed-parts
table below derive from it and are **void** until the restart regenerates them.
Nothing in the fastener table should be ordered.
First coupon printed 2026-09-01 and passed (see [`test-log.md`](test-log.md)); no structural part printed yet.

## Bought — drive & balance base *(purchased 2026-09-01, Pi Hut, ~£159.50)*

| Part | Qty | £ | Role |
|------|-----|---|------|
| Pololu Dual TB9051FTG motor driver | 1 | 30.70 | drive motors (DEC-16) — **lent to wk-devastator 2026-09-07; see OQ-15** |
| 37D 12V 122RPM 38 kg.cm geared motor + encoder | 2 | 55.80 | wheel-foot drive (DEC-31) |
| Pololu 80x10 mm wheel pair | 1 | 8.40 | Ø80 mm control constant (DEC-19) |
| Pololu 6 mm universal mounting hub (2-pack) | 1 | 12.50 | wheel to 6 mm D-shaft |
| Adafruit BNO085 9-DOF IMU | 1 | 27.00 | balance loop attitude |
| Teensy 4.0 + header kit | 1 | 25.10 | MCU / spinal cord (DEC-18) |

## Bought — servos *(purchased 2026-09-01, RCmall AliExpress, ~£302)*

| Part | Qty | £ | Role |
|------|-----|---|------|
| Feetech STS3215 12V 30 kg.cm 6-pack | 2 | ~101 ea | 12 limb joints (6 arm, 4 hip, 2 knee — DEC-31); **no spare** (OQ-16) |
| Feetech STS3032M 6V 4.5 kg.cm 4-pack | 1 | 93.19 | 3 neck (3-RPS) + 1 spare |
| STS3215 metal bracket set | 1 | 7.14 | dimensional reference (DEC-21) |

Of the STS3215s, the **lower body uses 6**: 2 hip-roll + 2 hip-pitch + 2 knee.

### Bought separately — test-fit servos *(Amazon, in hand 2026-09-07)*

| Part | Qty | £ | Role |
|------|-----|---|------|
| Waveshare **ST3215 12V** bus servo | 2 | not recorded | something to test-fit printed parts against, ahead of the RCmall order |

Bought to have real cases on the bench. **What was in the box is a BOM fact:**
M3 servo horn screws **and M2×5 self-tapping screws** for the case fixing
holes — so the retention screw is **M2**, not the M2.5 previously assumed
(`SELFTAP_DIA`, and see [`test-log.md`](test-log.md) 2026-09-07). Whether the
RCmall Feetech 6-packs ship the same accessories is **unverified**; [SPEC 11]
says the bare servo ships with *No Accessories*, which evidently describes the
part, not a retail box. Waveshare's ST3215 is a rebadge of the same Feetech
servo; that its dimensions match `params.py` is assumed, not yet measured.

## Bought — fasteners & consumables *(NOT yet ordered, ~£15–25 + filament)*

Counts are **derived from the current CAD** (v1 lower body), not estimated —
each row names where its quantity comes from. Order spares: these are pennies
each and a missing M3×55 stops an assembly dead.

| Part | Need | Buy | Role — where the count comes from |
|------|------|-----|-----------------------------------|
| M3 heat-set inserts, **5.7 mm long × 4.6 mm OD** | 4 | with spares | 2 pitch-cap posts per hip; fit unverified |
| M3 short inserts, **≤4 mm long** | 4 | after fit test | pelvis tray mounts in 5 mm deck; selected insert OD/bore must match |
| M3 socket screws 8 mm | 12 | assortment | 4 tray→standoff + 4 driver shield mounts + 4 pitch-cap screws; shield mounting remains provisional |
| **M3 socket screws 55 mm** | 8 | 10 | 4 roll-cheek/carrier bolts + 4 thigh/spacer bolts; 50 mm nominal grip, verify washer/nut stack |
| M3 nuts | 8 | assortment | through-bolts; use thin nuts fitting the 3 mm audit envelope or repeat clearance checks |
| M3 washers | 16 | assortment | one under each through-bolt head and nut; verify chosen thickness |
| M3 standoffs 10 mm, male/female | 4 | 4–10 | pelvis deck → electronics tray, sets the wiring gap |
| **Servo horns, metal, 25T, 4-hole 9.9 mm square** | 8 | 8 | **2 per driven joint** — drive *and* idler. The idler horn is what makes the joint a supported clevis rather than a cantilever. [SPEC 11] says none are supplied; the Waveshare retail box does ship M3 **horn screws**, so what else it holds is worth counting before ordering |
| M3 horn-square screws, **length TBD** | 32 | after measurement | 8 per joint × 4 joints; 5 mm printed cheeks plus measured horn engagement, NOT blanket M3×6 |
| Motor face M3 screws, **length TBD** | 12 | after measurement | 6 per motor; M3×8 candidate gives 3 mm engagement through 5 mm plate; verify motor thread depth |
| Roll-servo case-retention screws, **M2 self-tapping, length TBD** | 8 | M2 assortment, 5–10 mm | 4 per servo, OQ-12. **M2 is settled** — supplied with the Waveshare servos (2026-09-07); the CAD clearance is now 2.4 mm. The supplied M2×5 is too short here: the walls the screw crosses are **3.95 mm and 6.35 mm** in `hip_bracket.build_root()`, so no single length yet serves all 8, and case bore depth is unmeasured |
| Soldering-iron insert tip | 1 | 1 | setting the heat-set inserts |
| PETG filament, 1 kg | 1 | 1 | one spool; current quantity is pending a fresh slice — see the generated total below |

**Do not order unverified lengths from this draft.** The M3×55 bolts now join
printed components, not servo case bores. Roll retention *length*, idler
stand-off, horn engagement and motor thread depth remain measurement gates
(OQ-12). Horn centre/axle fixings and wheel/hub fixings must be checked
against the supplied kits; their exact lengths/counts are not yet established
here.

**The M2 length is answered by upstream's geometry, not by buying longer
screws:** SO-101 counterbores the wall so ~2.2 mm of plastic sits under the
head and the supplied M2×5 reaches the lug
([`soarm-joint-pattern.md`](soarm-joint-pattern.md)). The restart's socket
primitive does the same, so the M2 line above becomes "use the supplied M2×5"
once the lug pilot depth is calipered.

**Servo horns are included above but may already be in the kit.** The 4-hole
drive square lives on the horn, not the servo. Check the actual package before
ordering — the Waveshare box's contents already contradicted the "no
accessories" reading once.

**Insert geometry is a design constant.** `INSERT_M3_DIA` / `INSERT_M3_LEN` in
`params.py` target the **5.7 × 4.6 mm** M3 insert at the pitch-cap posts (Ruthex and
equivalents). A different insert profile means re-deriving those constants and
reprinting a fit coupon. The short pelvis inserts need their own bore fit check.

Check existing fastener stock against the revised joints before buying spares.

Bench power for bring-up (12 V source) is still outstanding — a 3S LiPo is the
DEC-20 answer, not a bench PSU.

## Print settings

What the **design** requires is short, and it is all koala-bot asserts:

- **PETG** (DEC-09), printed in each part's **declared orientation**, with
  support-free manufacture as a **target**, not a verified property. Inspect
  sliced layers first, especially pelvis/root bores and saddle posts (DEC-29).
- A **brim** on tall, small-footprint parts — flagged per part in the table.

Parts are **not** printed solid; strength comes from perimeters and orientation,
not from filling the part.

### The profile the figures were measured with

Not a koala-bot decision — this is the reference printer's (DEC-14) standing
**general-purpose** PETG profile, and the numbers below are what it produced.
Recorded so the measurements are reproducible, not as a recommendation:

| Setting | Value |
|---------|-------|
| Nozzle / filament | 0.4 mm, PETG at 240 °C / bed 80 °C |
| Layer height | 0.2 mm (0.24 first layer) |
| Perimeters | 3 |
| Top / bottom layers | 4 / 4 |
| Infill | 15 %, grid |

**Whether load-bearing parts need more than this is open — see
[OQ-11](open-questions.md).** Do not read the table as settled: it is a general
profile that happens to be what measured these parts, and the perimeter count
for structural parts is to be decided on evidence from the first structural
print. Filament and time totals will move when it is.

Anyone reproducing the build can use any slicer; nothing in the design depends
on this profile beyond the requirements above.

## Printed parts

**This table reflects the discarded DEC-29 geometry** (DEC-30) and stands only
until the restart's first export overwrites it. Every part fits ≤ 200×200 mm in
its declared orientation. Surface metrics do not certify support-free printing
or strength. Regenerate with `cd hardware && uv run python -m koala_hardware.export`.

<!-- BEGIN GENERATED: printed parts -->

*Generated by `koala_hardware.export` - do not hand-edit. Coupons are excluded from the total.*

No current hash-matched slice results, so filament is the **solid-geometry upper bound**, not a print setting. Run `koala_hardware.slice_remote` for measured figures.

| Part | Qty | Size (mm) | Filament | Print time | Print notes |
|------|-----|-----------|----------|-----------|-------------|
| `e_tray` | 1 | 140 x 90 x 9 | ~61 g (solid max) | - | clean |
| `hip_pitch_cap` | 2 | 70 x 12 x 4 | ~8 g (solid max) | - | clean |
| `hip_pitch_saddle_left` | 1 | 72 x 64 x 34 | ~45 g (solid max) | - | 217 mm2 flagged overhang; inspect slice |
| `hip_pitch_saddle_right` | 1 | 72 x 64 x 34 | ~45 g (solid max) | - | 217 mm2 flagged overhang; inspect slice |
| `hip_roll_drive` | 2 | 64 x 40 x 5 | ~15 g (solid max) | - | clean |
| `hip_roll_idler` | 2 | 64 x 40 x 5 | ~15 g (solid max) | - | clean |
| `pelvis` | 1 | 150 x 170 x 24 | ~188 g (solid max) | - | 560 mm2 flagged overhang; inspect slice |
| `thigh_inner` | 2 | 48 x 193 x 5 | ~65 g (solid max) | - | clean |
| `thigh_outer` | 2 | 48 x 193 x 5 | ~77 g (solid max) | - | clean |
| `thigh_spacer` | 4 | 24 x 24 x 40 | ~90 g (solid max) | - | clean |
| `coupon_horn_plate` | 1 | 30 x 30 x 4 | ~4 g (solid max) | - | clean |
| `coupon_ladder` | 1 | 150 x 60 x 6 | ~68 g (solid max) | - | clean |
| `coupon_motor_bore` | 1 | 135 x 50 x 6 | ~26 g (solid max) | - | clean |
| `coupon_motor_ring` | 1 | 47 x 47 x 5 | ~10 g (solid max) | - | clean |
| `coupon_seam` | 1 | 60 x 75 x 13 | ~22 g (solid max) | - | 38 mm2 flagged overhang; inspect slice |
| `coupon_servo_cradle` | 1 | 64 x 40 x 30 | ~55 g (solid max) | - | clean |
| **Structural total** | **18** | | **~609 g (solid max)** | **-** | |

<!-- END GENERATED -->

Coupons are the **test-fit pieces printed first**: each one verifies a
`[VERIFY]` constant in `hardware/src/koala_hardware/params.py` against the real
hardware. Adjust the constant, regenerate, reprint until it fits — then commit
to the structural parts.
