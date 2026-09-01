# firmware/

Real-time MCU code (planned - Phase 1). The "spinal cord".

- Runs the **balance loop** (IMU -> PID -> wheels, ~200-1000 Hz, deterministic), the
  servo-bus driver, encoders, safety.
- **micro-ROS** node exposing the topic contract (see [`../docs/architecture.md`](../docs/architecture.md)).
- MCU: Teensy 4.0 (DEC-18). Licence: `MIT`.
