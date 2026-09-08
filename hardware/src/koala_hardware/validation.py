# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Assembly datums; sampled solid and fastener checks live in audit.py."""
from . import params as P


def check_layout():
    expected=2*(P.V2_ROLL_Y+P.V2_PITCH_Y+P.V2_MOTOR_FACE+P.HUB_STACK+P.WHEEL_W/2)
    if abs(expected-P.V2_TRACK)>.001:
        raise ValueError('Wheel track disagrees with motor/hub stack')
    gap=2*(P.V2_ROLL_Y+P.V2_PITCH_Y+P.V2_MOTOR_FACE-P.MOTOR_BODY_LEN)
    if gap<2:
        raise ValueError('Neutral motors overlap')
    if abs(P.V2_PITCH_X-(P.V2_PITCH_REAR_X+P.SOCKET_AXIS_Z))>.001:
        raise ValueError('Pitch axis must be derived from socket rear face')
    if P.HUB_STACK>P.MOTOR_SHAFT_LEN:
        raise ValueError('Shaft does not reach nominal hub stack')
    return [f'neutral motor gap {gap:.1f} mm', f'wheel track {expected:.1f} mm',
            'roll/pitch/knee prototype; physical gates remain open']
