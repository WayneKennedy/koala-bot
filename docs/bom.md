# Bill of Materials — Koala V1

Two halves: **bought** parts (below) and **printed** parts (generated from the
CAD, so it cannot drift from the geometry). Prices are UK, inc VAT, ~2026.
Full sourcing rationale and alternatives: [`sourcing.md`](sourcing.md).

**Status, 2026-09-19:** the generated tables describe the recessed roll-first
front revision and retained rear drives. Root socket v1 is physically proven,
with the recorded ear-hole support caveat; revised front parts, torso and thigh
remain unprinted. Deliveries and allocations are recorded below. The bought
neck set contains three small STS3032M servos plus one spare.
[Current assembly](cad-integrated-design.md) · [Physical evidence](test-log.md).

**DEC-43 (2026-09-10):** retain the bought rear 37D motor, wheel and hub pair
at the ankles. Front motors, wheels and extra drive channels are cancelled.
Integrated forearms now terminate in fixed rounded feet; the generated tables
cover this geometry and two motor mounts. Foot traction, head/neck, guards
and full power/electronics packaging remain open.

**DEC-51 (2026-09-11):** a second 37D pair and two more TB9051FTGs, ordered for the
cancelled four-wheel V1 (DEC-38), arrived and are **not koala-bot's**. This BOM stays at
two motors and one driver; the surplus is pooled in
[wk-robotics `common.md`](https://github.com/WayneKennedy/wk-robotics/blob/main/docs/common.md#drive-motors-drivers-and-mcus-in-hand).

## Bought — drive & balance base *(The Pi Hut #1614498, ordered 2026-09-01, delivered 2026-09-03; £159.50 goods + £3.80 shipping = £163.30)*

| Part | Qty | £ | Role |
|------|-----|---|------|
| Pololu Dual TB9051FTG motor driver | 1 | 30.70 | drive motors (DEC-16); in hand — the 2026-09-07 loan to wk-devastator is dissolved by DEC-51 |
| 37D 12V 122RPM 38 kg.cm geared motor + encoder | 2 | 55.80 | wheel-foot drive (DEC-31) |
| Pololu 80x10 mm wheel pair | 1 | 8.40 | Ø80 mm control constant (DEC-19) |
| Pololu 6 mm universal mounting hub (2-pack) | 1 | 12.50 | wheel to 6 mm D-shaft |
| Adafruit BNO085 9-DOF IMU | 1 | 27.00 | balance loop attitude |
| Teensy 4.0 + header kit | 1 | 25.10 | MCU / spinal cord (DEC-18) |

## Bought — servos *(AliExpress #3075773528793179, ordered 2026-09-01, delivered 2026-09-12; £254.31 paid, no shipping line)*

Line prices are as invoiced (AliExpress order and PayPal receipt, read 2026-09-17); the
earlier ~£302 and per-line figures were listing estimates. The seller is recorded here as
RCmall; the order emails name only AliExpress. No courier VAT or handling charge was found
in the mail.

| Part | Qty | £ | Role |
|------|-----|---|------|
| Feetech STS3215 12V 30 kg.cm 6-pack | 2 | 84.95 ea | 12 limb joints (6 arm, 4 hip, 2 knee — DEC-31). **Eight in hand**: four went to SO-ARM101 on 2026-09-12 ([wk-soarm101 DEC-09](https://github.com/WayneKennedy/wk-soarm101/blob/main/docs/decisions.md)), so four short — **a further 6-pack ordered 2026-09-14** (AliExpress #3076088966873179, £103.15 paid; shipped 2026-09-15, not delivered as of 2026-09-17) to backfill; the four in the arm stay there permanently. On arrival: 14 in hand, 12 fitted, 2 spare (OQ-16) |
| Feetech STS3032M 6V 4.5 kg.cm 4-pack | 1 | 78.38 | 3 neck (3-RPS) + 1 spare. Fixed single cable — chains board-to-board through the supplied 3-port connector boards and link cable, not servo-to-servo (`test-log.md` 2026-09-12) |
| STS3215 metal bracket set | 1 | 6.03 | dimensional reference (DEC-21) |

Of the STS3215s, the **lower body uses 6**: 2 hip-roll + 2 hip-pitch + 2 knee.

### Bought separately — test-fit servos *(Amazon 204-4694570-7173960, ordered 2026-09-02, delivered 2026-09-04)*

| Part | Qty | £ | Role |
|------|-----|---|------|
| Waveshare **ST3215 12V** bus servo | 2 | 31.90 ea (listing names neither Waveshare nor 12 V) | something to test-fit printed parts against, ahead of the RCmall order |

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

### Slice evidence

Current revised parts have [local organic-support review slices](design/front-redesign/README.md#printability-and-service),
using the shared printer profile with Koala's `manufacturing-petg-tree.ini`
overrides: four perimeters, 30% infill, 0.2 mm layers, bed-only organic support
and a 4 mm brim. The record identifies the slicer, exact STL/G-code hashes and
profile hashes. Earlier [manufacturing records](design/manufacturing/README.md)
apply only to matching STL hashes. These estimates and inspected layers do not
establish support removal, strength or creep resistance; physical acceptance
remains open. Any slicer may be used if it meets the design requirements.

## Printed parts

These tables describe the **current integrated chassis**. Every part fits
≤200 × 200 mm in its declared orientation. Surface metrics do not certify
support-free printing or strength. Regenerate with
`cd hardware && uv run python -m koala_hardware.export`.

<!-- BEGIN GENERATED: printed parts -->

*Generated by `koala_hardware.export` - do not hand-edit. Coupons are excluded from the total.*

Figures with a matching STL hash are **slicer estimates** using the recorded PETG/TPU review settings (`docs/design/manufacturing/slices.json` and `docs/design/front-redesign/slices.json`); changed or unsliced parts fall back to a labelled solid-geometry upper bound. All structural parts printed solid would be 990 g.

| Part | Ver | Qty | Printable | Material | Size (mm) | Filament | Print time | Print notes |
|------|-----|-----|-----------|----------|-----------|----------|-----------|-------------|
| `e_tray` | v1 | 1 | assumed | PETG | 96 x 88 x 9 | ~43 g (solid max) | - | clean |
| `forearm_left` | v2 | 1 | unknown | PETG | 49 x 113 x 21 | 34 g | 3h 18m 26s | 1041 mm2 flagged overhang; inspect slice |
| `forearm_right` | v2 | 1 | unknown | PETG | 49 x 113 x 21 | 34 g | 3h 18m 34s | 1041 mm2 flagged overhang; inspect slice |
| `front_contact_pad` | v1 | 2 | assumed | TPU | 32 x 32 x 20 | 15 g | 1h 11m 17s | 4 mm2 flagged overhang; inspect slice |
| `hip_carrier_left` | v1 | 1 | assumed | PETG | 45 x 78 x 51 | ~46 g (solid max) | - | 282 mm2 flagged overhang; inspect slice |
| `hip_carrier_right` | v1 | 1 | assumed | PETG | 45 x 78 x 51 | ~46 g (solid max) | - | 282 mm2 flagged overhang; inspect slice |
| `root_socket_left` | v1 | 2 | proven | PETG | 47 x 37 x 28 | ~60 g (solid max) | - | 70 mm2 flagged overhang; inspect slice |
| `root_socket_right` | v1 | 2 | proven | PETG | 47 x 37 x 28 | ~60 g (solid max) | - | 70 mm2 flagged overhang; inspect slice |
| `shank_left` | v2 | 1 | assumed | PETG | 123 x 46 x 49 | ~45 g (solid max) | - | 1712 mm2 flagged overhang; inspect slice |
| `shank_right` | v2 | 1 | assumed | PETG | 123 x 46 x 49 | ~45 g (solid max) | - | 1712 mm2 flagged overhang; inspect slice |
| `shoulder_carrier_left` | v3 | 1 | unknown | PETG | 49 x 73 x 51 | 40 g | 4h 27m 11s | 562 mm2 flagged overhang; inspect slice |
| `shoulder_carrier_right` | v3 | 1 | unknown | PETG | 49 x 73 x 51 | 39 g | 4h 27m 20s | 562 mm2 flagged overhang; inspect slice |
| `shoulder_mount_left` | v1 | 1 | unknown | PETG | 44 x 47 x 32 | 16 g | 1h 42m 4s | 70 mm2 flagged overhang; inspect slice |
| `shoulder_mount_right` | v1 | 1 | unknown | PETG | 44 x 47 x 32 | 16 g | 1h 42m 7s | 70 mm2 flagged overhang; inspect slice |
| `thigh_left` | v3 | 1 | unknown | PETG | 45 x 110 x 73 | 50 g | 5h 12m 18s | 1924 mm2 flagged overhang; inspect slice |
| `thigh_right` | v3 | 1 | unknown | PETG | 45 x 110 x 73 | 50 g | 5h 14m 57s | 1924 mm2 flagged overhang; inspect slice |
| `torso_frame` | v5 | 1 | unknown | PETG | 164 x 94 x 82 | 165 g | 15h 48m 59s | 4569 mm2 flagged overhang; inspect slice |
| `tray_spacer` | v1 | 4 | assumed | PETG | 7 x 7 x 4 | 1 g | 2m 35s | small contact area; brim / grouped placement |
| `upper_arm_left` | v2 | 1 | unknown | PETG | 62 x 29 x 49 | 32 g | 3h 18m 50s | 1107 mm2 flagged overhang; inspect slice |
| `upper_arm_right` | v2 | 1 | unknown | PETG | 62 x 29 x 49 | 32 g | 3h 18m 19s | 1107 mm2 flagged overhang; inspect slice |
| `coupon_ladder` | v1 | 1 | assumed | PETG | 150 x 60 x 6 | 42 g | 4h 28m 46s | clean |
| `coupon_motor_bore` | v1 | 1 | assumed | PETG | 135 x 50 x 6 | 20 g | 1h 53m 22s | clean |
| `coupon_motor_ring` | v1 | 1 | assumed | PETG | 47 x 47 x 5 | 8 g | 53m 24s | clean |
| `coupon_seam` | v1 | 1 | assumed | PETG | 60 x 75 x 13 | 16 g | 1h 49m 20s | 38 mm2 flagged overhang; inspect slice |
| `coupon_socket_fork` | v1 | 1 | assumed | PETG | 42 x 21 x 49 | ~21 g (solid max) | - | 568 mm2 flagged overhang; inspect slice |
| `coupon_socket_saddle` | v1 | 1 | assumed | PETG | 45 x 29 x 22 | 16 g | 1h 36m 50s | 70 mm2 flagged overhang; inspect slice |
| **Structural total** | | **26** | | | | **~990 g (solid max)** | **-** | |

**Four-limb chassis fastening schedule, derived from the same builders.** Candidate lengths require rig checks; excludes coupon hardware, head/neck mechanisms and supplier-specific wheel/hub fixings.

| Fastener / interface hardware | Qty |
|---|---:|
| M2x5 self-tapper into servo ear | 48 |
| M3 drive-horn centre fixing (supplied kit) | 12 |
| M3 narrow washer OD6 x 0.5, idler horn screws | 48 |
| M3 nut | 10 |
| M3 nut, captive in shoulder cassette | 8 |
| M3 nut, captive under the servo | 16 |
| M3 plain washer | 14 |
| M3x16 Uno driver-board bolt (stack to verify) | 4 |
| M3x16 root screw, from the torso side | 16 |
| M3x20 front-pad screw | 2 |
| M3x20 shoulder cassette-to-frame screw | 8 |
| M3x25 tray through-bolt | 4 |
| M3x6 supplied horn-square pan screw (bottoming to verify) | 96 |
| M3x8 motor-face screw (depth to verify) | 12 |
| Metal 9.9-square horn/idler | 24 |

<!-- END GENERATED -->

Coupons are the **test-fit pieces printed first**: each one verifies a
`[VERIFY]` constant in `hardware/src/koala_hardware/params.py` against the real
hardware. Adjust the constant, regenerate, reprint until it fits — then commit
to the structural parts.
