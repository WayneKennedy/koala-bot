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

- **micro-ROS** on the MCU makes it a native ROS2 node (DDS-XRCE over serial).
- The **topic contract is the shared-brain backbone** of the family - fix it once and
  every member inherits it: `/cmd_vel`, `/joint_commands`, `/imu`, `/joint_states`,
  `/wheel_odom`, `/telemetry`. Bodies change; the spinal-cord protocol does not.

## Actuation map

| Joint group | Actuator | Why |
|-------------|----------|-----|
| Limbs (hip, knee, shoulder, elbow) | Feetech **STS3215** 12V bus servo (~30 kg.cm, feedback) | load-bearing; feedback for coordinated/balance motion; one serial bus |
| Head / neck (3-RPS) | **micro servo** (MG90S-class or small Feetech SCS bus) + CF pushrods | light load; keep mass off the top of the pendulum |
| Drive wheel-feet | **12V geared DC** (37D-class) + encoder | continuous rotation + torque |
| *(climber, later)* grippers / winch / clutch | mixed (see backlog) | passive-latch hang, ballistic swing, winch haul |

Head mass is a hard budget (< ~250-300 g) so micro servos suffice; offload eye
expression to **screen/OLED "eyes"** rather than eye-servos where possible.

## Power

- Single **~12 V rail (3S LiPo)** feeds both the 12V motors and the 12V servos
  (unified - no separate 7.4V servo buck).
- **5 V buck** for the Pi 5, sized generously; the Pi 5 is power-hungry and brown-outs
  are a known failure mode. Keep motor/servo current off the Pi rail.

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
