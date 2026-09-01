# Sourcing (UK-focused)

Prices ~2026, approximate. UK import: **VAT 20%** applies; the **£135 threshold** (goods
value, excl. shipping) decides *how* - under it the seller charges VAT at checkout (no
fee); over it the courier collects VAT + a ~£8-12 handling fee. Keeping a China order
under ~£135 of goods avoids the fee.

## Servos - Feetech STS3215, **12 V / 30 kg.cm** (limbs)
Genuine sources, landed cost for ~8 (of ~10-12) servos:

| Route | Unit (ex-VAT) | ~Landed/servo | Notes |
|-------|---------------|---------------|-------|
| **AliExpress SO-ARM100 kit** | ~£13-16 (est) | ~£16 | often bundles metal brackets + FE-URT-1 board; buy from a top-rated seller; the "official Feetech store" is elusive - target SO-ARM100 listings |
| **Seeed Studio** (China wh) | $22 ($20.90/10+) | ~£25 | guaranteed genuine, low-drama |
| Amazon UK | £28 (inc VAT, delivered) | £28 | instant, no vetting |

Grab an **FE-URT-1** USB serial-bus adapter (~£6) to set servo IDs (bundled in many
SO-ARM100 kits). Order **one voltage** (12 V) across all servos.

## Drive motors - The Pi Hut (confirmed UK stock)
- **Metal DC Geared Motor w/Encoder - 12V 122RPM 38 kg.cm** (37D class) x2 - the drive
  knee-wheels. N20+encoder is too weak for the main drive (fine for small joints).

## Motor driver
- **Pololu Dual TB9051FTG** - 4.5-28 V, **2.6 A cont / 5 A peak per channel**, current
  sense (~500 mV/A), integrated over-current/thermal protection, low-loss. Suitable for
  the 37D at koala scale; watch thermals if heavy. Arduino *shield* form factor -> wire as
  a breakout to a Teensy. Higher-current alternatives: Cytron MDD3A, Pololu G2. Avoid
  **L298N** (lossy BJT, ~2 V drop).

## MCU
- **Teensy 4.0** (~£23; Pi Hut / Pimoroni / Cool Components) - control workhorse.
- **RP2040 / ESP32** (~£4-8) - cheaper, micro-ROS-capable; ESP32 adds wireless.

## Power
- **3S LiPo** (~11.1 V) -> motors + 12 V servos direct; **5 V buck** (generous) for Pi 5.
