# References & prior art

- **Swiss-Mile / ANYmal-on-wheels** (ETH Zurich) - wheeled quadruped that walks, rolls,
  and rears to a biped to use front legs as arms. Closest precedent to Koala's concept.
- **SO-ARM / SO-101** (TheRobotStudio) - open robot arm built on ~£15 Feetech STS3215 bus
  servos; the **CAD** half of the ecosystem our servo and joint choices lean on (STL + STEP,
  Apache-2.0). SO-101 supersedes the deprecated SO-100; both sit in the repo still named
  SO-ARM100. <https://github.com/TheRobotStudio/SO-ARM100>
- **LeRobot** (HuggingFace) - the **software** half: control, teleop, dataset recording and
  policy training for those arms. Software only; it ships no CAD.
  <https://github.com/huggingface/lerobot>
- **Petoi Bittle**, **Stanford Mini Pupper** - hobby-scale printed/kit walking quadrupeds
  (proof the walking part is tractable).
- **Stewart platform / 3-RPS parallel mechanisms** - the torso & neck platform family.
  3-RPS gives pitch + roll + heave (no yaw); a full 6-actuator Stewart gives 6-DOF and a
  virtual pivot.
- **InMoov** (Gael Langevin) - open-source printed humanoid; inspiration and a source of
  mechanical lessons (DEC-12). Upstream inactive since 2024.
