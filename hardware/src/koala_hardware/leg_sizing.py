# SPDX-License-Identifier: CERN-OHL-S-2.0
"""DEC-32 analytical study, independent of discarded CAD and unmeasured sockets.

Run: python -m koala_hardware.leg_sizing
X forward, Z up; hip positive moves the knee forward, knee positive folds
the shank aft. Angles are degrees; positions are mm. This is a rigid-link
feasibility screen, not collision clearance or a commissioned motion range.
"""
from dataclasses import dataclass
from math import cos, radians, sin

from . import params as P


@dataclass(frozen=True)
class SagittalPose:
    knee_x: float
    knee_z: float
    axle_x: float
    axle_z: float


def forward(hip_deg, knee_deg, thigh=P.RESTART_THIGH_MM,
            shank=P.RESTART_SHANK_MM):
    """Knee and axle relative to hip-pitch axis, with roll zero."""
    if thigh <= 0 or shank <= 0:
        raise ValueError("Link lengths must be positive")
    hip, shank_angle = radians(hip_deg), radians(hip_deg - knee_deg)
    kx, kz = thigh * sin(hip), -thigh * cos(hip)
    return SagittalPose(kx, kz, kx + shank * sin(shank_angle),
                        kz - shank * cos(shank_angle))


def knee_moment_nm(pose, vertical_n, forward_n=0.0):
    """Signed Y moment of a ground force about the knee: r_z F_x - r_x F_z.

    Contact is directly below the axle (upright wheel). Includes the wheel
    radius in the horizontal-force lever arm. Distal weights, joint/link
    inertia and tyre deformation are omitted; no thermal margin is inferred.
    """
    rx = pose.axle_x - pose.knee_x
    rz = pose.axle_z - P.WHEEL_DIA / 2 - pose.knee_z
    return (rz * forward_n - rx * vertical_n) / 1000


def motor_gap_mm(track, roll_axis_half, roll_to_axle_drop, inward_roll_deg):
    """Conservative lateral gap between bounding intervals of both motors.

    Equal opposing inward roll, matching sagittal poses. Inboard cylinders
    use the full body radius and length. Track is at roll ZERO. Wheel centre
    to motor face uses existing provisional HUB_STACK; this does not validate
    that stack. Negative means overlapping Y intervals, not necessarily solid
    collision (unequal fore/aft poses may separate the motors).
    """
    if not 0 <= inward_roll_deg < 90:
        raise ValueError("Inward roll must be in [0, 90) degrees")
    a = radians(inward_roll_deg)
    reach = P.MOTOR_BODY_LEN + P.HUB_STACK + P.WHEEL_W / 2
    y_tip = roll_axis_half + (track / 2 - roll_axis_half - reach) * cos(a)
    y_tip -= (roll_to_axle_drop + P.MOTOR_DIA / 2) * sin(a)
    return 2 * y_tip


def minimum_track_mm(roll_axis_half, roll_to_axle_drop, inward_roll_deg,
                     gap=P.RESTART_MOTOR_GAP_MM):
    """Track needed for disjoint motor Y bounds, with all inputs explicit."""
    # Gap is affine in track with derivative cos(roll).
    zero = motor_gap_mm(0, roll_axis_half, roll_to_axle_drop, inward_roll_deg)
    return (gap - zero) / cos(radians(inward_roll_deg))


def main():
    weight = P.RESTART_MASS_KG * P.STANDARD_GRAVITY
    print("OQ-16 candidate sizing; no socket geometry, fit or strength approval")
    print("Centered crouch: hip = knee/2, equal links, roll = 0")
    print("knee deg | deck mm | total mm | static knee kgf.cm | +/-0.5g kgf.cm")
    for knee in (0, P.RESTART_KNEE_NOMINAL_DEG, 60, P.RESTART_KNEE_RANGE_DEG[1]):
        pose = forward(knee / 2, knee)
        height = (P.RESTART_DECK_TO_ROLL_MM + P.RESTART_ROLL_TO_PITCH_MM
                  - pose.axle_z + P.WHEEL_DIA / 2)
        static = abs(knee_moment_nm(pose, weight / 2))
        peak = max(abs(knee_moment_nm(pose, weight / 2, sign * weight / 2
                                    * P.RESTART_ACCEL_G)) for sign in (-1, 1))
        factor = 100 / P.STANDARD_GRAVITY
        print(f"{knee:8.1f} | {height:7.1f} | "
              f"{height + P.RESTART_UPPER_HEIGHT_MM:8.1f} | "
              f"{static * factor:18.2f} | {peak * factor:14.2f}")
    drop = P.RESTART_ROLL_TO_PITCH_MM + P.RESTART_THIGH_MM + P.RESTART_SHANK_MM
    print("Straight-leg motor bounds (includes tilted motor radius):")
    for roll in (0, 5, P.RESTART_ROLL_RANGE_DEG[1]):
        track = minimum_track_mm(P.RESTART_ROLL_HALF_MM, drop, roll)
        gap = motor_gap_mm(P.RESTART_TRACK_TARGET_MM, P.RESTART_ROLL_HALF_MM,
                           drop, roll)
        print(f"inward roll {roll:4.1f} deg: track >= {track:.1f} mm; "
              f"at target {P.RESTART_TRACK_TARGET_MM:g} mm, Y gap {gap:.1f} mm")
    print(f"Structural one-wheel target: {weight * P.RESTART_ONE_WHEEL_LOAD_G:.2f} N")
    print("Advertised torque is not a continuous rating; thermal/load tests remain open.")


if __name__ == "__main__":
    main()
