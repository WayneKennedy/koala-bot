# Bill of Materials — Koala V1

Two halves: **bought** parts (below) and **printed** parts (generated from the
CAD, so it cannot drift from the geometry). Prices are UK, inc VAT, ~2026.
Full sourcing rationale and alternatives: [`sourcing.md`](sourcing.md).

**Status:** V1 electronics and actuators are **ordered** (2026-09-01), and two
test-fit servos are **in hand** (2026-09-07). The generated tables now describe
**DEC-34's replacement prototype**, not DEC-29. The maintainer confirms SO-101
fit in PLA+ and PETG (DEC-33); the new joint rig remains unprinted. Fastener
lengths below are candidates for that rig, not demonstrated engagement.
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
servo; the maintainer confirms fit against the SO-101 printed interfaces in
PLA+ and PETG (DEC-33), without claiming new caliper readings.

## Bought — fasteners & consumables *(NOT yet ordered, ~£15–25 + filament)*

The **generated fastening schedule below** replaces the discarded draft's
counts. It includes twelve metal horns (two per joint), 48 horn-square screws,
six centre screws and 24 M2x5 lug screws for the six lower-body servos.
Check kit contents and stock before buying; the rig must establish actual
engagement, head clearance and horn span. Wheel/hub fixings depend on the
supplied kits and remain outside this count.

PETG filament remains a consumable; a 1 kg spool is the sourcing unit, not a
measured requirement. Inserts and an insert tip are needed only for the
retained seam/insert coupons; the new lower body's structural seams use
through-bolts and metal nuts. Assembly order and candidate stacks are in
[`cad-restart-design.md`](cad-restart-design.md).

Bench power for bring-up (12 V source) is still outstanding — a 3S LiPo is the
DEC-20 answer, not a bench PSU.

## Print settings

What the **design** requires is short, and it is all koala-bot asserts:

- **PETG** (DEC-09), printed in each part's **declared orientation**, with
  support-free manufacture as a **target**, not a verified property. Inspect
  sliced layers first, especially socket shelves, crossbar bores and collar cable openings (DEC-34).
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

These tables describe the **DEC-34 digital prototype**. Every part fits
≤200 × 200 mm in its declared orientation. Surface metrics do not certify
support-free printing or strength. Regenerate with
`cd hardware && uv run python -m koala_hardware.export`.

<!-- BEGIN GENERATED: printed parts -->

*Generated by `koala_hardware.export` - do not hand-edit. Coupons are excluded from the total.*

No current hash-matched slice results, so filament is the **solid-geometry upper bound**, not a print setting. Run `koala_hardware.slice_remote` for measured figures.

| Part | Qty | Size (mm) | Filament | Print time | Print notes |
|------|-----|-----------|----------|-----------|-------------|
| `e_tray` | 1 | 140 x 90 x 9 | ~63 g (solid max) | - | clean |
| `hip_crossbar` | 2 | 22 x 16 x 39 | ~32 g (solid max) | - | 32 mm2 flagged overhang; inspect slice |
| `hip_pitch_cradle_left` | 1 | 30 x 45 x 29 | ~28 g (solid max) | - | 24 mm2 flagged overhang; inspect slice |
| `hip_pitch_cradle_right` | 1 | 30 x 45 x 29 | ~28 g (solid max) | - | 24 mm2 flagged overhang; inspect slice |
| `joint_drive_cheek` | 6 | 56 x 28 x 4 | ~27 g (solid max) | - | clean |
| `joint_idler_cheek` | 6 | 56 x 28 x 4 | ~29 g (solid max) | - | clean |
| `pelvis` | 1 | 180 x 150 x 32 | ~216 g (solid max) | - | 48 mm2 flagged overhang; inspect slice |
| `servo_collar_left` | 3 | 51 x 36 x 26 | ~51 g (solid max) | - | 95 mm2 flagged overhang; inspect slice |
| `servo_collar_right` | 3 | 51 x 36 x 26 | ~51 g (solid max) | - | 95 mm2 flagged overhang; inspect slice |
| `shank_core` | 2 | 39 x 22 x 53 | ~105 g (solid max) | - | brim (tall, small footprint); 448 mm2 flagged overhang; inspect slice |
| `thigh_core_left` | 1 | 45 x 30 x 56 | ~52 g (solid max) | - | brim (tall, small footprint); 233 mm2 flagged overhang; inspect slice |
| `thigh_core_right` | 1 | 45 x 30 x 56 | ~52 g (solid max) | - | brim (tall, small footprint); 233 mm2 flagged overhang; inspect slice |
| `wheel_foot_face` | 2 | 66 x 48 x 5 | ~25 g (solid max) | - | clean |
| `wheel_foot_support` | 2 | 66 x 48 x 5 | ~14 g (solid max) | - | clean |
| `coupon_ladder` | 1 | 150 x 60 x 6 | ~68 g (solid max) | - | clean |
| `coupon_motor_bore` | 1 | 135 x 50 x 6 | ~26 g (solid max) | - | clean |
| `coupon_motor_ring` | 1 | 47 x 47 x 5 | ~10 g (solid max) | - | clean |
| `coupon_seam` | 1 | 60 x 75 x 13 | ~22 g (solid max) | - | 38 mm2 flagged overhang; inspect slice |
| `coupon_socket_bridge` | 1 | 16 x 22 x 39 | ~16 g (solid max) | - | 32 mm2 flagged overhang; inspect slice |
| `coupon_socket_collar` | 1 | 51 x 36 x 26 | ~17 g (solid max) | - | 95 mm2 flagged overhang; inspect slice |
| `coupon_socket_cradle` | 1 | 45 x 30 x 22 | ~16 g (solid max) | - | 24 mm2 flagged overhang; inspect slice |
| `coupon_socket_drive` | 1 | 56 x 28 x 4 | ~4 g (solid max) | - | clean |
| `coupon_socket_idler` | 1 | 56 x 28 x 4 | ~5 g (solid max) | - | clean |
| **Structural total** | **32** | | **~775 g (solid max)** | **-** | |

**Lower-body fastening schedule, derived from the same builders.** Candidate lengths require rig checks; excludes coupon hardware, torso, arms/head, and supplier-specific wheel/hub fixings.

| Fastener / interface hardware | Qty |
|---|---:|
| M2x5 self-tapper into servo lug | 24 |
| M3 female/female standoff, 10 mm | 4 |
| M3 nut | 20 |
| M3 plain washer | 28 |
| M3x10 lower tray-standoff screw | 4 |
| M3x16 driver-shield screw (board stack to verify) | 4 |
| M3x50 crossbar screw | 8 |
| M3x55 motor-plate seam screw | 4 |
| M3x6 horn centre screw (kit specification) | 6 |
| M3x6 horn-square screw (engagement to verify) | 48 |
| M3x60 crossbar screw | 4 |
| M3x8 motor-face screw (engagement to verify) | 12 |
| M3x8 upper tray-standoff screw | 4 |
| Metal 9.9-square servo horn | 12 |

<!-- END GENERATED -->

Coupons are the **test-fit pieces printed first**: each one verifies a
`[VERIFY]` constant in `hardware/src/koala_hardware/params.py` against the real
hardware. Adjust the constant, regenerate, reprint until it fits — then commit
to the structural parts.
