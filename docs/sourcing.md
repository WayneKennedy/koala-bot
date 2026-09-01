# Sourcing (UK-focused)

Prices ~2026, approximate. UK import: **VAT 20%** applies; the **£135 threshold** (goods
value, excl. shipping) decides *how* - under it the seller charges VAT at checkout (no
fee); over it the courier collects VAT + a ~£8-12 handling fee. Keeping a China order
under ~£135 of goods avoids the fee.

## Confirmed order - drive/balance base (Pi Hut, ~£159.50 inc VAT) [PURCHASED 2026-09-01]

The self-balancing base subsystem (limb/head servos are a separate import order):

| Part | Qty | £ inc VAT |
|------|-----|-----------|
| Pololu Dual TB9051FTG motor driver (DEC-16) | 1 | 30.70 |
| Pi Hut 37D 12V 122RPM 38 kg.cm geared motor + encoder | 2 | 55.80 |
| Pololu Wheel 80x10 mm pair (Ø80 mm = control constant, DEC-19) | 1 | 8.40 |
| Pololu 6 mm universal mounting hub (2-pack) | 1 | 12.50 |
| Adafruit BNO085 9-DOF IMU (fusion, I2C/Qwiic) | 1 | 27.00 |
| Teensy 4.0 (DEC-18) + header kit | 1 | 25.10 |
| **Total** | | **~159.50** |

Not in this order (bench-power for bring-up): a **12 V source** (bench PSU or 3S LiPo);
optional STEMMA QT cable for the BNO085.

## Confirmed order - servos (RCmall on AliExpress, ~£302 inc VAT) [PURCHASED 2026-09-01]

| Part | Qty | £ inc VAT | Role |
|------|-----|-----------|------|
| Feetech STS3215 12V 30 kg 6-pack (FE-URT-1 included each) | 2 | ~101 ea | 10 limb joints + 2 spare |
| Feetech STS3032M 6V 4.5 kg metal-case 4-pack (DEC-22) | 1 | 93.19 | 3 neck (3-RPS) + 1 spare |
| STS3215 metal bracket set | 1 | 7.14 | dimensional reference - **brackets are printed** (DEC-21) |

Neck servos are 6V -> a separate 6V bus segment from the 12V limb bus (same STS protocol).

## Part notes & alternatives (pre-purchase research, kept for reference)

- **STS3215 (limbs):** chosen route was RCmall/AliExpress (SO-ARM100-style listing,
  ~£17.3 landed). Alternatives: Seeed Studio ~£25 (guaranteed genuine), Amazon UK ~£28
  (instant). One voltage (**12 V**) across all limb servos; the **FE-URT-1** USB
  serial-bus adapter (sets servo IDs) is bundled in many kits.
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
  pelvis-to-tray), M2.5 screws (servo horns), insert tip for a soldering iron — ~£12-18.
