# Sourcing (UK-focused)

Prices ~2026, approximate. UK import: **VAT 20%** applies; the **£135 threshold** (goods
value, excl. shipping) decides *how* - under it the seller charges VAT at checkout (no
fee); over it the courier collects VAT + a ~£8-12 handling fee. Keeping a China order
under ~£135 of goods avoids the fee.

## Confirmed order - drive/balance base (Pi Hut, ~£159.50 inc VAT) [PURCHASED 2026-09-01]

The self-balancing base subsystem (limb/head servos are a separate import order):

| Part | Qty | £ inc VAT |
|------|-----|-----------|
| Pololu Dual TB9051FTG motor driver (DEC-16) — in hand; the 2026-09-07 loan to wk-devastator is dissolved by DEC-51 | 1 | 30.70 |
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

## Confirmed order - servos (RCmall on AliExpress, ~£302 inc VAT) [PURCHASED 2026-09-01, ARRIVED 2026-09-12]

| Part | Qty | £ inc VAT | Role |
|------|-----|-----------|------|
| Feetech STS3215 12V 30 kg 6-pack (listed with FE-URT-1 — **none shipped**, 2026-09-12) | 2 | ~101 ea | 12 limb joints (DEC-31). **Four reallocated to SO-ARM101 2026-09-12**; eight remain, four to re-order — see `bom.md` |
| Feetech STS3032M 6V 4.5 kg metal-case 4-pack (DEC-22) | 1 | 93.19 | 3 neck (3-RPS) + 1 spare |
| STS3215 metal bracket set | 1 | 7.14 | dimensional reference - **brackets are printed** (DEC-21). Arrived 2026-09-12; the servos themselves ship without brackets |

Neck servos are 6V -> a separate 6V bus segment from the 12V limb bus (same STS protocol).

**Arrived 2026-09-12** — 12 × STS3215 and 4 × STS3032M, counts confirmed by the owner.
**Each STS3215 ships with a drive horn, an idler horn, M3×6 pan-head horn screws and
M2×6 self-tapping case screws — and no serial-bus adapter.** The listing's FE-URT-1 was
not in either 6-pack; the family's adapters cover it (Waveshare Bus Servo Adapter (A),
FE-URT-2). **Each STS3032M ships with a fixed single cable — no pass-through port — plus
one aluminium and three plastic horns, mounting screws, a small 3-port connector board and
a separate cable to daisy-chain the boards.** Full contents tables in [`test-log.md`](test-log.md)
2026-09-12.

## Test-fit pair (Amazon, in hand 2026-09-07)

Two **Waveshare ST3215 12V** servos, bought outside the plan to have real cases on
the bench while printed parts are still being fitted. Amazon is the instant-but-dear
route already noted below (~£28 each at the time of that research; this purchase's
price is not recorded). Its value was **what came in the box** - M2x5 self-tapping
case screws and M3 horn screws, which is a BOM fact, recorded in
[`bom.md`](bom.md) and [`test-log.md`](test-log.md). Whether the RCmall Feetech
6-packs ship the same accessories is unverified.

**Reallocated 2026-09-09:** both units are now SO-ARM101 follower servos (`shoulder_pan`
ID 1, `shoulder_lift` ID 2) — see [wk-soarm101 `docs/servos.md`](https://github.com/WayneKennedy/wk-soarm101/blob/main/docs/servos.md). The koala-bot bench had
no STS3215 from then until the 6-packs arrived on 2026-09-12.

## Four-wheel hardware (DEC-38) — arrived 2026-09-11, surplus

Two more 37D 12 V 122 rpm 38 kg.cm motors + encoders and **two** more Pololu Dual
TB9051FTGs, ordered for DEC-38's four driven wheels some time after 2026-09-08. DEC-43
cancelled the front drives on 2026-09-10, before they arrived. Order date, supplier and
price are not recorded; the part numbers match the Pi Hut order above. **Not koala-bot's**
— allocated by DEC-51: one driver is wk-devastator's own (ending its loan), the other
driver and both motors are pooled in [wk-robotics `common.md`](https://github.com/WayneKennedy/wk-robotics/blob/main/docs/common.md#drive-motors-drivers-and-mcus-in-hand).

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
