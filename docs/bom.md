# Bill of Materials — Koala V1

Two halves: **bought** parts (below) and **printed** parts (generated from the
CAD, so it cannot drift from the geometry). Prices are UK, inc VAT, ~2026.
Full sourcing rationale and alternatives: [`sourcing.md`](sourcing.md).

**Status:** V1 electronics and actuators are **ordered** (2026-09-01), and two
test-fit servos are **in hand** (2026-09-07). The generated tables now describe
**DEC-43's integrated four-limb chassis**. The maintainer confirms SO-101
fit in PLA+ and PETG (DEC-33); the new joint rig remains unprinted. Fastener
lengths below are candidates for that rig, not demonstrated engagement.
First coupon printed 2026-09-01 and passed (see [`test-log.md`](test-log.md)); no structural part printed yet.

**DEC-43 (2026-09-10):** retain the bought rear 37D motor, wheel and hub pair
at the ankles. Front motors, wheels and extra drive channels are cancelled.
Integrated forearms now terminate in fixed rounded feet; the generated tables
cover this geometry and two motor mounts. Foot traction, head/neck, guards
and full power/electronics packaging remain open.

**DEC-51 (2026-09-11):** a second 37D pair and two more TB9051FTGs, ordered for the
cancelled four-wheel V1 (DEC-38), arrived and are **not koala-bot's**. This BOM stays at
two motors and one driver; the surplus is pooled in
[wk-robotics `common.md`](https://github.com/WayneKennedy/wk-robotics/blob/main/docs/common.md#drive-motors-drivers-and-mcus-in-hand).

## Bought — drive & balance base *(purchased 2026-09-01, Pi Hut, ~£159.50)*

| Part | Qty | £ | Role |
|------|-----|---|------|
| Pololu Dual TB9051FTG motor driver | 1 | 30.70 | drive motors (DEC-16); in hand — the 2026-09-07 loan to wk-devastator is dissolved by DEC-51 |
| 37D 12V 122RPM 38 kg.cm geared motor + encoder | 2 | 55.80 | wheel-foot drive (DEC-31) |
| Pololu 80x10 mm wheel pair | 1 | 8.40 | Ø80 mm control constant (DEC-19) |
| Pololu 6 mm universal mounting hub (2-pack) | 1 | 12.50 | wheel to 6 mm D-shaft |
| Adafruit BNO085 9-DOF IMU | 1 | 27.00 | balance loop attitude |
| Teensy 4.0 + header kit | 1 | 25.10 | MCU / spinal cord (DEC-18) |

## Bought — servos *(purchased 2026-09-01, RCmall AliExpress, ~£302; servos arrived 2026-09-12)*

| Part | Qty | £ | Role |
|------|-----|---|------|
| Feetech STS3215 12V 30 kg.cm 6-pack | 2 | ~101 ea | 12 limb joints (6 arm, 4 hip, 2 knee — DEC-31). **Eight in hand**: four went to SO-ARM101 on 2026-09-12 ([wk-soarm101 DEC-09](https://github.com/WayneKennedy/wk-soarm101/blob/main/docs/decisions.md)), so **four short, re-order needed** (OQ-16) |
| Feetech STS3032M 6V 4.5 kg.cm 4-pack | 1 | 93.19 | 3 neck (3-RPS) + 1 spare. Fixed single cable — chains board-to-board through the supplied 3-port connector boards and link cable, not servo-to-servo (`test-log.md` 2026-09-12) |
| STS3215 metal bracket set | 1 | 7.14 | dimensional reference (DEC-21) |

Of the STS3215s, the **lower body uses 6**: 2 hip-roll + 2 hip-pitch + 2 knee.

### Bought separately — test-fit servos *(Amazon, in hand 2026-09-07)*

| Part | Qty | £ | Role |
|------|-----|---|------|
| Waveshare **ST3215 12V** bus servo | 2 | not recorded | something to test-fit printed parts against, ahead of the RCmall order |

Bought to have real cases on the bench. **What was in the box is a BOM fact:**
M3 servo horn screws **and M2×5 self-tapping screws** for the case fixing
holes — so the retention screw is **M2**, not the M2.5 previously assumed
(`SELFTAP_DIA`, and see [`test-log.md`](test-log.md) 2026-09-07). **The RCmall
Feetech 6-packs ship the same accessories (owner report 2026-09-12): two metal
horns per servo, M3×6 pan-head horn screws, and M2 self-tappers — read as M2×6,
against Waveshare's M2×5, unmeasured.** No bus adapter. [SPEC 11]
says the bare servo ships with *No Accessories*, which evidently describes the
part, not a retail box. Waveshare's ST3215 is a rebadge of the same Feetech
servo; the maintainer confirms fit against the SO-101 printed interfaces in
PLA+ and PETG (DEC-33), without claiming new caliper readings.

## Bought — fasteners & consumables *(NOT yet ordered, ~£15–25 + filament)*

The **generated fastening schedule below** replaces the discarded draft's
counts. It covers all twelve limb joints: 24 metal horns/idlers, 96 horn-square screws,
twelve drive-centre fixings, 48 M2×5 ear screws and 48 narrow OD6 × 0.5 mm
Back-horn washers. Both rear motor-face mounts are included.
Check kit contents and stock before buying; the rig must establish actual
engagement, head clearance and horn span. Wheel/hub fixings depend on the
supplied kits and remain outside this count.

PETG filament remains a consumable; a 1 kg spool is the sourcing unit, not a
measured requirement. Inserts and an insert tip are needed only for the
retained seam/insert coupons; the torso's structural seams use
through-bolts and metal nuts. Assembly order and candidate stacks are in
[`cad-integrated-design.md`](cad-integrated-design.md).

Bench power for bring-up (12 V source) is still outstanding — a 3S LiPo is the
DEC-20 answer, not a bench PSU.

## Print settings

What the **design** requires is short, and it is all koala-bot asserts:

- **PETG** (DEC-09), printed in each part's **declared orientation**, with
  integrated structures and accessible local supports allowed (DEC-39). Inspect
  sliced layers first, especially the opposite fork, saddle, motor ring and screw-head pockets.
- A **brim** on tall, small-footprint parts — flagged per part in the table.

Parts are **not** printed solid; strength comes from perimeters and orientation,
not from filling the part.

### The profile the figures were measured with

Not a koala-bot decision — this is the reference printer's (DEC-14) standing
**general-purpose** PETG profile, used for historical slice measurements. No current DEC-40 part has a
hash-matched slice result; this is not a measured profile for the new parts.
Recorded so the measurements are reproducible, not as a recommendation:

| Setting | Value |
|---------|-------|
| Nozzle / filament | 0.4 mm, PETG at 240 °C / bed 80 °C |
| Layer height | 0.2 mm (0.24 first layer) |
| Perimeters | 3 |
| Top / bottom layers | 4 / 4 |
| Infill | 15 %, grid |

**Whether load-bearing parts need more than this is open — see
[OQ-11](open-questions.md).** Do not read the table as settled: it is a historical general-purpose
profile, and the perimeter count
for structural parts is to be decided on evidence from the first structural
print. Filament and time totals will move when it is.

Anyone reproducing the build can use any slicer; nothing in the design depends
on this profile beyond the requirements above.

## Printed parts

These tables describe the **DEC-40 digital chassis**. Every part fits
≤200 × 200 mm in its declared orientation. Surface metrics do not certify
support-free printing or strength. Regenerate with
`cd hardware && uv run python -m koala_hardware.export`.

<!-- BEGIN GENERATED: printed parts -->

*Generated by `koala_hardware.export` - do not hand-edit. Coupons are excluded from the total.*

Figures with a matching STL hash are **slicer estimates** using the recorded PETG/TPU review settings (`docs/design/manufacturing/slices.json`); changed or unsliced parts fall back to a labelled solid-geometry upper bound. All structural parts printed solid would be 911 g.

| Part | Qty | Printable | Material | Size (mm) | Filament | Print time | Print notes |
|------|-----|-----------|----------|-----------|----------|-----------|-------------|
| `e_tray` | 1 | assumed | PETG | 96 x 88 x 9 | 32 g | 3h 48m 48s | clean |
| `forearm_left` | 1 | assumed | PETG | 49 x 113 x 21 | 30 g | 2h 59m 46s | 1375 mm2 flagged overhang; inspect slice |
| `forearm_right` | 1 | assumed | PETG | 49 x 113 x 21 | 30 g | 2h 59m 52s | 1375 mm2 flagged overhang; inspect slice |
| `front_contact_pad` | 2 | assumed | TPU | 32 x 32 x 20 | 15 g | 1h 11m 17s | 4 mm2 flagged overhang; inspect slice |
| `pelvis_socket_left` | 1 | assumed | PETG | 67 x 47 x 86 | 43 g | 4h 5m 35s | 114 mm2 flagged overhang; inspect slice |
| `pelvis_socket_right` | 1 | assumed | PETG | 67 x 47 x 86 | 43 g | 4h 5m 18s | 114 mm2 flagged overhang; inspect slice |
| `root_carrier_left` | 2 | assumed | PETG | 45 x 88 x 51 | 73 g | 3h 57m 6s | 331 mm2 flagged overhang; inspect slice |
| `root_carrier_right` | 2 | assumed | PETG | 45 x 88 x 51 | 73 g | 3h 56m 32s | 331 mm2 flagged overhang; inspect slice |
| `shank_left` | 1 | assumed | PETG | 123 x 46 x 49 | 53 g | 4h 29m 12s | 3119 mm2 flagged overhang; inspect slice |
| `shank_right` | 1 | assumed | PETG | 123 x 46 x 49 | 53 g | 4h 29m 13s | 3119 mm2 flagged overhang; inspect slice |
| `shoulder_socket_left` | 1 | assumed | PETG | 62 x 47 x 27 | 26 g | 2h 38m 54s | 100 mm2 flagged overhang; inspect slice |
| `shoulder_socket_right` | 1 | assumed | PETG | 62 x 47 x 27 | 26 g | 2h 38m 40s | 100 mm2 flagged overhang; inspect slice |
| `thigh_left` | 1 | assumed | PETG | 45 x 77 x 49 | 41 g | 3h 48m 29s | 2416 mm2 flagged overhang; inspect slice |
| `thigh_right` | 1 | assumed | PETG | 45 x 77 x 49 | 41 g | 3h 47m 58s | 2416 mm2 flagged overhang; inspect slice |
| `torso_frame` | 1 | assumed | PETG | 58 x 80 x 62 | 73 g | 6h 0m 0s | 957 mm2 flagged overhang; inspect slice |
| `tray_spacer` | 4 | assumed | PETG | 7 x 7 x 4 | 1 g | 2m 35s | small contact area; brim / grouped placement |
| `upper_arm_left` | 1 | assumed | PETG | 45 x 62 x 49 | 36 g | 3h 20m 52s | 2153 mm2 flagged overhang; inspect slice |
| `upper_arm_right` | 1 | assumed | PETG | 45 x 62 x 49 | 36 g | 3h 21m 0s | 2153 mm2 flagged overhang; inspect slice |
| `coupon_ladder` | 1 | assumed | PETG | 150 x 60 x 6 | 42 g | 4h 28m 46s | clean |
| `coupon_motor_bore` | 1 | assumed | PETG | 135 x 50 x 6 | 20 g | 1h 53m 22s | clean |
| `coupon_motor_ring` | 1 | assumed | PETG | 47 x 47 x 5 | 8 g | 53m 24s | clean |
| `coupon_seam` | 1 | assumed | PETG | 60 x 75 x 13 | 16 g | 1h 49m 20s | 38 mm2 flagged overhang; inspect slice |
| `coupon_socket_fork` | 1 | assumed | PETG | 42 x 21 x 49 | 19 g | 1h 45m 3s | 568 mm2 flagged overhang; inspect slice |
| `coupon_socket_saddle` | 1 | assumed | PETG | 45 x 29 x 22 | 16 g | 1h 36m 50s | 70 mm2 flagged overhang; inspect slice |
| **Structural total** | **24** | | | | **723 g** | **70h 53m** | |

**Four-limb chassis fastening schedule, derived from the same builders.** Candidate lengths require rig checks; excludes coupon hardware, head/neck mechanisms and supplier-specific wheel/hub fixings. **Supplied by the servo packs, not to buy** (2026-09-12): all 24 horns/idlers, and M3×6 horn screws and M2 self-tappers in per-servo quantities not yet counted against the 96 and 48 below.

| Fastener / interface hardware | Qty |
|---|---:|
| M2x5 self-tapper into servo ear | 48 |
| M3 drive-horn centre fixing (supplied kit) | 12 |
| M3 narrow washer OD6 x 0.5, idler horn screws | 48 |
| M3 nut | 18 |
| M3 plain washer | 30 |
| M3x14 torso-crossmember bolt | 8 |
| M3x16 Uno driver-board bolt (stack to verify) | 4 |
| M3x20 front-pad screw | 2 |
| M3x25 tray through-bolt | 4 |
| M3x6 supplied horn-square pan screw (bottoming to verify) | 96 |
| M3x8 motor-face screw (depth to verify) | 12 |
| Metal 9.9-square horn/idler | 24 |

<!-- END GENERATED -->

Coupons are the **test-fit pieces printed first**: each one verifies a
`[VERIFY]` constant in `hardware/src/koala_hardware/params.py` against the real
hardware. Adjust the constant, regenerate, reprint until it fits — then commit
to the structural parts.
