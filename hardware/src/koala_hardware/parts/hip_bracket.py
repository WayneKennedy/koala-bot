# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Hip-roll servo bracket - saddle that hangs the roll servo under the pelvis.

Local frame: origin ON THE ROLL AXIS, +X forward, +Y outboard, +Z up. The
flange top (Z = FLANGE_TOP) bolts to the pelvis underside.

DEC-24 print strategy: printed flipped (flange face on the bed) the servo
cavity opens upward, every wall is vertical, and the only horizontal faces
point up. Support-free.

The saddle is X-limited so the hip-link fork discs (radius FORK_R about the
roll axis) swing clear; the retention walls sit ABOVE that swept circle.
"""
from build123d import Box, Cylinder, Part, Pos, Rot, Align
from .. import params as P
from .. import fasteners as F
from .. import servo_iface as S

WALL = 4.0
CAV_Y = P.SERVO_W / 2 + P.CLEAR_POCKET      # 12.65
BODY_Y = CAV_Y + WALL                       # 16.65
SADDLE_X = 19.0          # half-width; must stay inside the fork discs
FLANGE_Y = 26.0
FLANGE_T = 6.0
# No floor under the servo: a closed bottom becomes a bridged ceiling once the
# part is flipped for printing. The servo is carried by its rear-tab screws
# (its designed mounting feature) and clamped by the fork on both faces.
FLOOR = 0.0
END_WALL_X = 23.6        # retention walls, outboard of the fork discs
FORK_CLEAR_R = 27.0      # fork discs sweep to r=FORK_R; walls start above it

FLANGE_TOP = P.HIP_ROLL_DROP - P.PELVIS_PLATE[2]     # 44.0
BOTTOM = -(P.SERVO_BELOW + FLOOR)                    # -15.2
TAB_Z = P.SERVO_AXIS_X - P.SERVO_TAB_X               # 33.2 above the axis


def build() -> dict:
    # Saddle body: full-height block, cavity carved by the servo envelope.
    part = Part() + Pos(0, 0, BOTTOM) * Box(
        2 * SADDLE_X, 2 * BODY_Y, FLANGE_TOP - BOTTOM,
        align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Retention end walls fore & aft, above the fork sweep, tying into the flange.
    for sx in (1, -1):
        part += Pos(sx * (SADDLE_X + END_WALL_X) / 2, 0, FORK_CLEAR_R) * Box(
            END_WALL_X - SADDLE_X, 2 * BODY_Y, FLANGE_TOP - FORK_CLEAR_R,
            align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Mounting flange (ears in Y) at the top.
    part += Pos(0, 0, FLANGE_TOP - FLANGE_T) * Box(
        2 * END_WALL_X, 2 * FLANGE_Y, FLANGE_T,
        align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Servo cavity: open fore/aft and downward, closed by the floor.
    part -= S.on_axis(Rot(Y=90)) * S.servo_envelope()

    # Retention screws: M3 through both end walls and the servo's rear tabs.
    for sy in (-P.SERVO_TAB_Y, P.SERVO_TAB_Y):
        part -= Pos(-END_WALL_X - 1, sy, TAB_Z) * Rot(Y=90) * Cylinder(
            P.CLEAR_HOLE_M3 / 2, 2 * END_WALL_X + 2,
            align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Flange inserts (through-holes; screws come down from the pelvis).
    from .pelvis import BRACKET_BOLTS
    for (bx, by) in BRACKET_BOLTS:
        part -= Pos(bx, by, FLANGE_TOP + 0.1) * Cylinder(
            P.INSERT_M3_DIA / 2, FLANGE_T + 0.2,
            align=(Align.CENTER, Align.CENTER, Align.MAX))

    return {
        "name": "hip_bracket_right",
        "part": part,
        "orientation": Rot(X=180),  # flange on the bed, cavity opening up
        "notes": "Servo slides in fore/aft, sits on the floor, retained by "
                 "2x M3 through the rear tabs. Mirror in Y for the left.",
    }
