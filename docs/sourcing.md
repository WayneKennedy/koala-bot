# Sourcing (UK-focused)

Prices ~2026, approximate. UK import: **VAT 20%** applies; the **£135 threshold** (goods
value, excl. shipping) decides *how* - under it the seller charges VAT at checkout (no
fee); over it the courier collects VAT + a ~£8-12 handling fee. Keeping a China order
under ~£135 of goods avoids the fee.

## Confirmed order - drive/balance base (Pi Hut, ~£159.50 inc VAT) [PURCHASED 2026-09-01]

The self-balancing base subsystem (limb/head servos are a separate import order):

| Part | Qty | £ inc VAT |
|------|-----|-----------|
| Pololu Dual TB9051FTG motor driver (DEC-16) — **lent to wk-devastator, OQ-15** | 1 | 30.70 |
| Pi Hut 37D 12V 122RPM 38 kg.cm geared motor + encoder | 2 | 55.80 |
| Pololu Wheel 80x10 mm pair (Ø80 mm = control constant, DEC-19) | 1 | 8.40 |
| Pololu 6 mm universal mounting hub (2-pack) | 1 | 12.50 |
| Adafruit BNO085 9-DOF IMU (fusion, I2C/Qwiic) | 1 | 27.00 |
| Teensy 4.0 (DEC-18) + header kit | 1 | 25.10 |
| **Total** | | **~159.50** |

Not in this order: a **3S LiPo** for bring-up — **DEC-20**, *not* a bench PSU, which this
line previously offered as an equal option and should not have (the exception is servo ID
assignment and current measurement, where a current-limited supply is the safer tool; see
[wk-robotics `common.md`](https://github.com/WayneKennedy/wk-robotics/blob/main/docs/common.md#power-integrity)).
Also outstanding: optional STEMMA QT cable for the BNO085.

## Confirmed order - servos (RCmall on AliExpress, ~£302 inc VAT) [PURCHASED 2026-09-01]

| Part | Qty | £ inc VAT | Role |
|------|-----|-----------|------|
| Feetech STS3215 12V 30 kg 6-pack (FE-URT-1 included each) | 2 | ~101 ea | 10 limb joints + 2 spare |
| Feetech STS3032M 6V 4.5 kg metal-case 4-pack (DEC-22) | 1 | 93.19 | 3 neck (3-RPS) + 1 spare |
| STS3215 metal bracket set | 1 | 7.14 | dimensional reference - **brackets are printed** (DEC-21) |

Neck servos are 6V -> a separate 6V bus segment from the 12V limb bus (same STS protocol).

## Test-fit pair (Amazon, in hand 2026-09-07)

Two **Waveshare ST3215 12V** servos, bought outside the plan to have real cases on
the bench while printed parts are still being fitted. Amazon is the instant-but-dear
route already noted below (~£28 each at the time of that research; this purchase's
price is not recorded). Its value was **what came in the box** - M2x5 self-tapping
case screws and M3 horn screws, which is a BOM fact, recorded in
[`bom.md`](bom.md) and [`test-log.md`](test-log.md). Whether the RCmall Feetech
6-packs ship the same accessories is unverified.

## Part notes & alternatives (pre-purchase research, kept for reference)

- **STS3215 (limbs):** chosen route was RCmall/AliExpress (SO-ARM-style listing,
  ~£17.3 landed). Alternatives: Seeed Studio ~£25 (guaranteed genuine), Amazon UK ~£28
  (instant). One voltage (**12 V**) across all limb servos; the **FE-URT-1** USB
  serial-bus adapter (sets servo IDs) is bundled in many kits.
  What we bought maps exactly onto the **SO-101 "Pro" follower** spec - 12 V, 1:345 gear
  ratio, 30 kg.cm - the official upgraded variant, not an off-standard part, which is what
  makes DEC-21 compatibility concrete rather than assumed. (The SO-101 *leader* arm is 7.4 V
  with three mixed gear ratios; koala-bot has no leader, so all 12 limb servos are a single
  uniform part number and share one spares pool.)
- **Drive motors:** Pi Hut 37D-class 12V 122RPM 38 kg.cm w/encoder (chosen).
  N20+encoder is too weak for the main drive (fine for small joints).
- **Motor driver:** Pololu Dual TB9051FTG (chosen; DEC-16) - 4.5-28 V, current sense
  (~500 mV/A), over-current/thermal protection, low-loss; Arduino *shield* form factor,
  wired as a breakout to the Teensy; watch thermals if heavy. Higher-current
  alternatives: Cytron MDD3A, Pololu G2. Avoid **L298N** (lossy BJT, ~2 V drop).
- **MCU:** Teensy 4.0 (chosen; DEC-18; Pi Hut / Pimoroni / Cool Components).
  RP2040 / ESP32 (~£4-8) are cheaper micro-ROS-capable variants; ESP32 adds wireless.
- **Power:** 3S LiPo (~11.1 V nominal) -> motors + 12 V servos direct; **5 V buck**
  (generous) for the Pi 5.
- **Fasteners (DEC-23/24, not yet ordered):** M3 screws (8/12/16/50 mm — the 50s pass
  through the hip brackets' servo tabs), M3 brass heat-set inserts, M3 standoffs (10 mm,
  pelvis-to-tray), **M2 self-tapping screws** (servo case retention — the horn drive
  square is M3, not M2.5; see [`test-log.md`](test-log.md) 2026-09-02 and 2026-09-07),
  insert tip for a soldering iron — ~£12-18. Counts and lengths live in
  [`bom.md`](bom.md), which derives them from the CAD.
