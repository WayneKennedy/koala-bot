# Architecture — the "nervous system"

Two-tier compute, split by the reflex-vs-intent boundary.

## Compute tiers

| Tier | Hardware | Role | Rule |
|------|----------|------|------|
| **Spinal cord** | real-time MCU (Teensy 4.0 leading; ESP32 / RP2040 candidates) | motor/servo output, IMU read, **the balance loop**, encoders, safety | fast (~200-1000 Hz), deterministic |
| **Cerebrum** | Raspberry Pi 5 + ROS2 | perception, SLAM, mission/behaviour, LLM "personality", networking | not real-time |

### The load-bearing rule

**The balance loop lives on the MCU - never on the Pi.** Linux isn't real-time and
ROS2-over-USB adds jitter that destabilises an inverted pendulum. IMU -> PID -> wheel
output closes on the MCU; the Pi only sends setpoints and reads telemetry.

### Bridge & contract

- **micro-ROS** on the MCU makes it a native ROS2 node (DDS-XRCE over serial). It runs
  against a **micro-ROS Agent** process on the Pi, which bridges XRCE into the real DDS
  graph; the MCU then appears in `ros2 topic list` like any other node. Full explanation,
  shared with the rest of the family:
  [wk-robotics/docs/common.md](https://github.com/WayneKennedy/wk-robotics/blob/main/docs/common.md#micro-ros-how-the-mcu-joins-the-graph).
- **Board support caveat — [OQ-14](open-questions.md).** micro-ROS upstream has **not
  tested the Teensy 4.0** that DEC-18 selected and bought, while listing the 4.1 as
  Supported. The board table, the checked date and the reason it is nonetheless expected
  to work are family facts and live once, upstream:
  [wk-robotics/docs/common.md](https://github.com/WayneKennedy/wk-robotics/blob/main/docs/common.md#micro-ros-how-the-mcu-joins-the-graph).
  What is koala's alone: **DEC-04 makes this bridge load-bearing**, so close it cheaply
  — flash a micro-ROS example to the 4.0 before firmware is written around it. If it
  fails, the fallback is a 4.1 or the ESP32 already named above, not a redesign.
- The **topic contract is the shared-brain backbone** of the family - fix it once and
  every member inherits it: `/cmd_vel`, `/joint_commands`, `/imu`, `/joint_states`,
  `/wheel_odom`, `/telemetry`. Bodies change; the spinal-cord protocol does not.

## Actuation map

| Joint group | Actuator | Why |
|-------------|----------|-----|
| Limbs (hip, knee, shoulder, elbow) | Feetech **STS3215** 12V bus servo (~30 kg.cm, feedback) | load-bearing; feedback for coordinated/balance motion; one serial bus |
| Head / neck (3-RPS) | **Feetech STS3032M** (6V, 4.5 kg.cm, STS-protocol bus, feedback) + CF pushrods | small feedback servo on its own 6V bus; servos mount at the shoulder girdle, head stays light. **Fixed single cable per servo** — the 6V bus chains through the supplied 3-port connector boards and link cable, one board per servo lead, not servo-to-servo (`test-log.md` 2026-09-12) |
| Rear ankle wheels (DEC-43) | **12V geared DC** (37D-class) + encoder | continuous rotation + torque |
| Front feet (DEC-43) | Fixed rounded printed ends; no drive actuator | ground support and stepping |
| *(climber, later)* grippers / winch / clutch | mixed (see backlog) | passive-latch hang, ballistic swing, winch haul |

Head mass is a hard budget (< ~250-300 g) so micro servos suffice; offload eye
expression to **screen/OLED "eyes"** rather than eye-servos where possible.

DEC-43 needs **two motor channels and two encoder inputs** for the bought
rear ankle-drive pair. The dual-channel shield covers that count and is in
hand (DEC-51 dissolved the loan to wk-devastator). Front feet support the
robot with the rear wheel contacts, then lift for balanced driving. Establish
power/thermal duty for body support and contact transfer on the assembled robot.

## Power

- Single **~12 V rail (3S LiPo)** feeds both the 12V motors and the 12V servos
  (unified - no separate 7.4V servo buck). **3S only**: a full 3S is 12.6 V (within the
  STS3215 12V rating); a 4S (16.8 V) would destroy the servos.
- **5 V buck** for the Pi 5, sized generously; the Pi 5 is power-hungry and brown-outs
  are a known failure mode. Keep motor/servo current off the Pi rail.

### Power integrity (DEC-20)

**The four rules, their InMoov origin and the underlying mechanism live once, in
[wk-robotics](https://github.com/WayneKennedy/wk-robotics/blob/main/docs/common.md#power-integrity)**
- prototype from a stiff LiPo rather than a bench PSU, isolate the logic rail, bulk caps
across the servo/motor bus, fuse the pack lead. They are not restated here: this copy had
already drifted from the canonical one by 2026-09-07. **DEC-20** is koala-bot's commitment
to them.

What is koala-bot's alone:
- The **fuse pairs with the child-safe enclosure** (OQ-10).
- The single 12 V rail above puts servo and motor transients on **one bus**, so the bulk
  capacitance is load-bearing here rather than belt-and-braces.
- Per-servo current figures for sizing that fuse are in the same family document
  ([Actuators](https://github.com/WayneKennedy/wk-robotics/blob/main/docs/common.md#actuators)):
  twelve STS3215 stalled (DEC-31's count) is **~32 A** at the 2.7 A per-servo figure.

## Compute placement

Camera-eyes are **CSI** (short ribbon) so a Pi must sit near them. Clean split:
**Pi 5 in/near the head** for vision + brain; **MCU in the body** for servos - the same
head/body split as the two tiers.

## Modelling & tooling

- **URDF + RViz** - serial kinematics (limbs, base-yaw, head); the file the robot's ROS2
  stack uses. Drag joints with `joint_state_publisher_gui`.
- **CAD motion study** (Onshape / FreeCAD / Fusion) - for the **parallel** torso & neck:
  *URDF cannot represent closed kinematic loops*, so parallel mechanisms are modelled in
  CAD (workspace, collisions, singularities) or a loop-capable sim.
- **Physics** - Gazebo (ROS2-native) or PyBullet / MuJoCo for balance & gait.
