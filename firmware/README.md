# firmware/

Real-time MCU code (planned - Phase 1). The "spinal cord".

- Runs the **balance loop** (IMU -> PID -> wheels, ~200-1000 Hz, deterministic), the
  servo-bus driver, encoders, safety.
- **micro-ROS** node exposing the topic contract (see [*Koala Bot Architecture*](memory://main/robotics/koala-bot/koala-bot-architecture)).
- MCU: Teensy 4.0 (DEC-18). Licence: `MIT`.
