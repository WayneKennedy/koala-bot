# Open Questions (pending decisions)

Unresolved. Resolve -> move to [`decisions.md`](decisions.md).

- **OQ-02 - Rear knee.** Fixed strut vs 1-DOF, and *how the wheel engages* for smooth
  terrain (fold the knee to drop/lift the wheel -> needs a knee DOF; or wheels always
  down and the hip lifts them -> knee can be fixed).
- **OQ-03 - Torso platform's 3 DOF.** pitch + roll + **yaw** (twist, very lifelike) vs
  pitch + roll + **heave** (breathing bob). Can't have all four from 3 actuators.
- **OQ-04 - Head eyes & mass.** Screen/OLED eyes (light, expressive) vs mechanical eye
  servos (mass). Confirm the < ~250-300 g head budget that keeps micro servos viable.
- **OQ-05 - MCU.** Teensy 4.0 (raw control) vs ESP32 (wireless) vs RP2040 (cheapest).
- **OQ-06 - Servo sourcing.** AliExpress SO-ARM100 kit (servos + brackets + FE-URT-1
  board, ~£16 landed) vs Seeed genuine (~£25 landed). Voltage settled: **12 V**. See
  [`sourcing.md`](sourcing.md).
- **OQ-08 - Arm-joint standard.** Align arm joints to the SO-ARM100 servo+bracket
  standard to inherit its ecosystem, or stay fully custom?
- **OQ-09 - Swappable limb-ends in V1.** Design the quick-swap wrist/ankle mount into V1,
  or defer to the climber sibling?
- **OQ-10 - Child-safety spec** (audience 2-5; DEC-15). Resolve during design: pinch-point
  guarding at every joint/linkage; software speed & torque limits + e-stop; graceful-fall
  behaviour; protected/enclosed LiPo; no small detachable parts; rounded edges; no hot
  exposed surfaces. Reference EN 71 (toy safety) for guidance, not as a certification target.
