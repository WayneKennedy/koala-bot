# Bill of Materials — Koala V1

Two halves: **bought** parts (below) and **printed** parts (generated from the
CAD, so it cannot drift from the geometry). Prices are UK, inc VAT, ~2026.
Full sourcing rationale and alternatives: [`sourcing.md`](sourcing.md).

**Status:** V1 electronics and actuators are **ordered** (2026-09-01). Of the
fasteners, only the **heat-set inserts and an insert tip** are outstanding —
they gate `coupon_seam`, and through it every DEC-23 seam in the design.
First coupon printed 2026-09-01 and passed (see [`test-log.md`](test-log.md)); no structural part printed yet.

## Bought — drive & balance base *(purchased 2026-09-01, Pi Hut, ~£159.50)*

| Part | Qty | £ | Role |
|------|-----|---|------|
| Pololu Dual TB9051FTG motor driver | 1 | 30.70 | drive motors (DEC-16) |
| 37D 12V 122RPM 38 kg.cm geared motor + encoder | 2 | 55.80 | knee-wheel drive |
| Pololu 80x10 mm wheel pair | 1 | 8.40 | Ø80 mm control constant (DEC-19) |
| Pololu 6 mm universal mounting hub (2-pack) | 1 | 12.50 | wheel to 6 mm D-shaft |
| Adafruit BNO085 9-DOF IMU | 1 | 27.00 | balance loop attitude |
| Teensy 4.0 + header kit | 1 | 25.10 | MCU / spinal cord (DEC-18) |

## Bought — servos *(purchased 2026-09-01, RCmall AliExpress, ~£302)*

| Part | Qty | £ | Role |
|------|-----|---|------|
| Feetech STS3215 12V 30 kg.cm 6-pack | 2 | ~101 ea | 10 limb joints + 2 spare |
| Feetech STS3032M 6V 4.5 kg.cm 4-pack | 1 | 93.19 | 3 neck (3-RPS) + 1 spare |
| STS3215 metal bracket set | 1 | 7.14 | dimensional reference (DEC-21) |

Of the STS3215s, the **lower body uses 4**: 2 hip-roll + 2 hip-pitch.

## Bought — fasteners & consumables *(NOT yet ordered, ~£15–25 + filament)*

Counts are **derived from the current CAD** (v1 lower body), not estimated —
each row names where its quantity comes from. Order spares: these are pennies
each and a missing M3×55 stops an assembly dead.

| Part | Need | Buy | Role — where the count comes from |
|------|------|-----|-----------------------------------|
| M3 heat-set inserts, **5.7 mm long × 4.6 mm OD** | 20 | 50–100 | 4 pelvis deck + 8 hip-bracket flanges + 8 thigh seams |
| M3 socket screws 8 mm | 8 | assortment | 4 tray→standoff + 4 driver shield into printed standoffs |
| M3 socket screws 12 mm | 8 | assortment | pelvis deck → hip-bracket flange inserts (4 per side) |
| M3 socket screws 16 mm | 8 | assortment | motor clamp → thigh seam inserts (4 per leg) |
| **M3 socket screws 55 mm** | 4 | 10 | through the hip brackets' end walls as a wrap-around clamp — upstream fits one only to the **base** servo, its highest-load joint, and Koala's hips are the analogue. A through-bolt + nut cuts no thread in the servo. ⚠️ **Provisional** — [OQ-12](open-questions.md) |
| M3 nyloc nuts | 4 | assortment | far side of those tab screws (same caveat) |
| M3 standoffs 10 mm, male/female | 4 | 4–10 | pelvis deck → electronics tray, sets the wiring gap |
| **Servo horns, metal, 25T, 4-hole 9.9 mm square** | 8 | 8 | **2 per driven joint** — drive *and* idler. The idler horn is what makes the joint a supported clevis rather than a cantilever. **None supplied** ([SPEC 11]); check the servo package |
| **M3×6 socket screws** | 32 | 40 | servo horn squares — **8 per driven joint** (4 drive + 4 idler) × 4 joints. **M3, not M2.5**: upstream drills Ø3.2 on this square and their arms assemble; the STEP's Ø2.5 is the M3 tapping drill. **None supplied** ([SPEC 11]) |
| Soldering-iron insert tip | 1 | 1 | setting the heat-set inserts |
| PETG filament, 1 kg | 1 | 1 | one spool; current quantity is pending a fresh slice — see the generated total below |

**Two rows above are provisional.** The STS3215 is retained by a snug pocket
plus 4 self-tapping screws (2 front, 2 back); the M3×55 is for an *optional*
wrap-around clamp at the highest-load joint. Sizes and positions are blocked on
measuring a physical servo — see [OQ-12](open-questions.md). **Buy the M3×6
with confidence; hold the M3×55 and the self-tappers.**

**Servo horns are included above but may already be in the kit.** [SPEC 11]
says the bare servo ships with *No Accessories*, and the 4-hole drive square
lives on the horn, not the servo. Check the actual package before ordering.

**Insert geometry is a design constant.** `INSERT_M3_DIA` / `INSERT_M3_LEN` in
`params.py` are written to the common **5.7 × 4.6 mm** M3 insert (Ruthex and
equivalents). A different insert profile means re-deriving those constants and
reprinting `coupon_seam` — so match the geometry rather than the brand.

A mixed M3 screw/nut/washer assortment box covers the 8/12/16 mm rows and the
nyloc nuts in one purchase; the M3×55 almost never appears in assortments and
needs buying separately.

Bench power for bring-up (12 V source) is still outstanding — a 3S LiPo is the
DEC-20 answer, not a bench PSU.

## Print settings

What the **design** requires is short, and it is all koala-bot asserts:

- **PETG** (DEC-09), printed in each part's **declared orientation**, with
  **supports off** — every part is support-free by design (DEC-24). If a slicer
  wants support, the part or its orientation is wrong.
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

Every part ≤ 200×200 mm and support-free in its declared orientation
(DEC-09 / DEC-24). Regenerate with
`cd hardware && uv run python -m koala_hardware.export`.

<!-- BEGIN GENERATED: printed parts -->

*Generated by `koala_hardware.export` - do not hand-edit. Coupons are excluded from the total.*

No current hash-matched slice results, so filament is the **solid-geometry upper bound**, not a setting — real use is roughly half. Run `koala_hardware.slice_remote` for measured figures.

| Part | Qty | Size (mm) | Filament | Print time | Print notes |
|------|-----|-----------|----------|-----------|-------------|
| `e_tray` | 1 | 140 x 90 x 9 | ~61 g (solid max) | - | clean |
| `hip_bracket` | 2 | 47 x 52 x 25 | ~54 g (solid max) | - | 287 mm2 self-supporting overhang |
| `hip_link_left` | 1 | 66 x 61 x 57 | ~58 g (solid max) | - | 371 mm2 self-supporting overhang |
| `hip_link_right` | 1 | 66 x 61 x 57 | ~58 g (solid max) | - | 371 mm2 self-supporting overhang |
| `motor_clamp_left` | 1 | 48 x 86 x 39 | ~74 g (solid max) | - | 467 mm2 self-supporting overhang |
| `motor_clamp_right` | 1 | 48 x 86 x 39 | ~74 g (solid max) | - | 467 mm2 self-supporting overhang |
| `pelvis_plate` | 1 | 150 x 170 x 5 | ~157 g (solid max) | - | clean |
| `thigh_upper_left` | 1 | 107 x 71 x 30 | ~141 g (solid max) | - | 467 mm2 self-supporting overhang |
| `thigh_upper_right` | 1 | 107 x 71 x 30 | ~141 g (solid max) | - | 467 mm2 self-supporting overhang |
| `coupon_horn_plate` | 1 | 30 x 30 x 4 | ~4 g (solid max) | - | clean |
| `coupon_ladder` | 1 | 150 x 60 x 6 | ~68 g (solid max) | - | clean |
| `coupon_motor_bore` | 1 | 135 x 50 x 6 | ~26 g (solid max) | - | clean |
| `coupon_motor_ring` | 1 | 47 x 47 x 5 | ~10 g (solid max) | - | clean |
| `coupon_seam` | 1 | 60 x 75 x 13 | ~22 g (solid max) | - | 38 mm2 self-supporting overhang |
| `coupon_servo_cradle` | 1 | 64 x 40 x 30 | ~55 g (solid max) | - | clean |
| **Structural total** | **10** | | **~818 g (solid max)** | **-** | |

<!-- END GENERATED -->

Coupons are the **test-fit pieces printed first**: each one verifies a
`[VERIFY]` constant in `hardware/src/koala_hardware/params.py` against the real
hardware. Adjust the constant, regenerate, reprint until it fits — then commit
to the structural parts.
