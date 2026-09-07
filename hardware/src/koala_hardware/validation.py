# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Datum checks; exact sampled collision regressions live in audit.py."""
from . import params as P
from .parts.thigh import MOTOR_FACE_Y


def check_layout():
    motor_gap = 2 * (P.HIP_ROLL_Y + MOTOR_FACE_Y - P.MOTOR_BODY_LEN)
    expected_track = P.HIP_ROLL_Y + MOTOR_FACE_Y + P.HUB_STACK + P.WHEEL_W / 2
    if motor_gap < 2:
        raise ValueError("Drive motor bodies overlap at neutral")
    if abs(P.TRACK_HALF - expected_track) > .01:
        raise ValueError("Wheel track inconsistent with motor face/hub stack")
    if P.MOTOR_SHAFT_LEN < P.HUB_STACK:
        raise ValueError("Shaft does not reach hub stack")
    return [f"neutral motor gap {motor_gap:.1f} mm",
            f"wheel track {2 * P.TRACK_HALF:.1f} mm",
            "prototype only; run sampled joint checks separately"]
