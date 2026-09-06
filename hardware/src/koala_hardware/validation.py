# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Critical assembly-layout checks that part-local print tests cannot see."""
from . import params as P
from .parts.pelvis import BRACKET_BOLTS
from .parts.thigh import FLANGE_Z, MOTOR_FACE_Y, SEAM_Z


MIN_MOTOR_GAP = 2.0
MIN_HOLE_EDGE = P.WALL


def check_layout() -> list[str]:
    """Return concise pass messages or raise for an impossible assembly.

    These are datum checks, not a general collision engine. They cover the two
    failures that were previously hidden because the assembly render omitted
    purchased motors and boolean cuts outside a plate fail silently.
    """
    errors = []
    px, py, _ = P.PELVIS_PLATE
    max_bx = max(abs(x) for x, _ in BRACKET_BOLTS)
    max_by = max(abs(y) for _, y in BRACKET_BOLTS)
    edge_x = px / 2 - (max_bx + P.CLEAR_HOLE_M3 / 2)
    edge_y = py / 2 - (P.HIP_ROLL_Y + max_by + P.CLEAR_HOLE_M3 / 2)
    if edge_x < MIN_HOLE_EDGE or edge_y < MIN_HOLE_EDGE:
        errors.append(
            "pelvis does not contain every hip-bracket hole with a 3 mm edge")

    motor_gap = 2 * (P.HIP_ROLL_Y + MOTOR_FACE_Y - P.MOTOR_BODY_LEN)
    if motor_gap < MIN_MOTOR_GAP:
        errors.append(
            f"inward-facing drive motors overlap/leave only {motor_gap:.1f} mm")

    expected_track = (P.HIP_ROLL_Y + MOTOR_FACE_Y + P.HUB_STACK
                      + P.WHEEL_W / 2)
    if abs(P.TRACK_HALF - expected_track) > 0.01:
        errors.append(
            f"wheel track datum is {P.TRACK_HALF:.1f}, expected {expected_track:.1f}")
    if P.MOTOR_SHAFT_LEN < P.HUB_STACK:
        errors.append("motor shaft does not reach the wheel hub stack")

    seam_error = abs(FLANGE_Z[1] - (P.THIGH_DROP + SEAM_Z))
    if seam_error > 0.01:
        errors.append(f"thigh/motor-clamp seam is disconnected by {seam_error:.1f} mm")

    if errors:
        raise ValueError("; ".join(errors))
    return [f"hip-hole edge {edge_y:.1f} mm",
            f"motor centre gap {motor_gap:.1f} mm",
            "thigh seam connected",
            f"wheel track {2 * P.TRACK_HALF:.1f} mm"]
