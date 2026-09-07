# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Private integral roll-servo root, NOT a separately printable bracket.

Roll-local frame: X is the output axis; Z points toward the pelvis.
The rear retention pattern and envelope still require physical validation.
"""
from build123d import Box, Cylinder, Pos, Rot, Align
from .. import params as P
from .. import servo_iface as S

# Six mm nominal walls retain >=3 mm beside the conservative tab keep-out.
WALL = 6.0
BODY_Y = P.SERVO_W / 2 + P.CLEAR_POCKET + WALL
SADDLE_X = 19.0
END_WALL_X = 23.6
BOTTOM = 20.0
END_BOTTOM = 27.0
TOP = P.HIP_ROLL_DROP - P.PELVIS_PLATE[2]
TAB_Z = P.SERVO_AXIS_X - P.SERVO_TAB_X


def build_root():
    part = Pos(0, 0, BOTTOM) * Box(
        2 * SADDLE_X, 2 * BODY_Y, TOP - BOTTOM,
        align=(Align.CENTER, Align.CENTER, Align.MIN))
    for sx in (-1, 1):
        part += Pos(sx * (SADDLE_X + END_WALL_X) / 2, 0, END_BOTTOM) * Box(
            END_WALL_X - SADDLE_X, 2 * BODY_Y, TOP - END_BOTTOM,
            align=(Align.CENTER, Align.CENTER, Align.MIN))
    part -= S.on_axis(Rot(Y=90)) * S.servo_envelope()
    # Preserve the provisional self-tapper clearance pattern, not an M3
    # through-bolt claim. Do not order retention hardware from this alone.
    for y in (-P.SERVO_TAB_Y, P.SERVO_TAB_Y):
        for sx in (-1, 1):
            part -= Pos(sx * (END_WALL_X + 1), y, TAB_Z) * Rot(Y=-90 * sx) * Cylinder(
                P.SELFTAP_CLEAR / 2, END_WALL_X - SADDLE_X + 2.5,
                align=(Align.CENTER, Align.CENTER, Align.MIN))
    return part
