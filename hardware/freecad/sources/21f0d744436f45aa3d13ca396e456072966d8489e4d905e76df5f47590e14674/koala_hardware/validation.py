# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Shared body / motor datums; solid and interface checks live in audit.py."""
from . import params as P, body_plan as B
from .parts import links as L, torso as T


def check_layout():
    result=B.check()
    for front,y in [(False,L.rear_axis_y())]:
        expected=2*(y+L.motor_face(front)+P.HUB_STACK+P.WHEEL_W/2)
        assert abs(expected-P.BODY_TRACK_TARGET_MM)<1e-8
    assert P.HUB_STACK<=P.MOTOR_SHAFT_LEN
    assert T.HIGH>T.LOW+10
    assert abs(P.SOCKET_DRIVE_FACE-P.SOCKET_IDLER_FACE-P.SOCKET_HORN_SPAN)<1e-9
    return [f"motor end gap {result['motor_end_gap_mm']:.1f} mm",
            f'wheel track {P.BODY_TRACK_TARGET_MM:g} mm',
            'four integrated limbs; physical acceptance pending']
