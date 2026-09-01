# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Hip link: driven by the roll servo (pelvis), carries the pitch servo that
drives the thigh. The 2-DOF hip of DEC-07.

Local frame: origin ON THE ROLL AXIS; roll axis = X, +X forward, +Y outboard.
The pitch axis is HIP_PITCH_DROP below, running along Y.

DEC-24 print strategy: printed as-modelled it stands on the cradle's flat
bottom with the roll axis horizontal, so both fork plates stand on edge (a
clevis printed axis-vertical always leaves its far tine bridging air). The
fork plates are small discs on vertical legs rather than large discs, so the
only overhang left is the lower arc of each disc rim.
"""
from build123d import Box, Cylinder, Part, Pos, Rot, Align
from .. import params as P
from .. import servo_iface as S

FORK_R = 15.0        # just covers the drive square + idler bore
FORK_T = 5.0
HORN_GAP = 0.2
LEG_W = 30.0         # leg width (Y), also the spine width
BRACKET_CLEAR_R = 24.0   # hip bracket's swept radius about the roll axis
CRADLE_WALL = 4.0
PITCH_DROP = P.HIP_PITCH_DROP


def build() -> dict:
    x_horn = P.SERVO_HORN_TOP + HORN_GAP        # +20.4 (drive side)
    x_idler = P.SERVO_IDLER_BOT - HORN_GAP      # -19.6 (idler side)

    horn_plate = Pos(x_horn, 0, 0) * Rot(Y=90) * Cylinder(
        FORK_R, FORK_T, align=(Align.CENTER, Align.CENTER, Align.MIN))
    idler_plate = Pos(x_idler, 0, 0) * Rot(Y=-90) * Cylinder(
        FORK_R, FORK_T, align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Legs: vertical slabs carrying each disc down past the bracket's swing.
    for x, sgn in ((x_horn, 1), (x_idler, -1)):
        horn_leg = Pos(x if sgn > 0 else x - FORK_T, -LEG_W / 2,
                       -BRACKET_CLEAR_R - 6) * Box(
            FORK_T, LEG_W, BRACKET_CLEAR_R + 6,
            align=(Align.MIN, Align.MIN, Align.MIN))
        if sgn > 0:
            horn_plate += horn_leg
        else:
            idler_plate += horn_leg

    # Spine: joins the legs below the bracket's swept circle.
    span_x0, span_x1 = x_idler - FORK_T, x_horn + FORK_T
    spine = Pos(span_x0, -LEG_W / 2, -BRACKET_CLEAR_R - 6) * Box(
        span_x1 - span_x0, LEG_W, 6,
        align=(Align.MIN, Align.MIN, Align.MIN))

    # Pitch-servo cradle hanging below the spine.
    cav_x = P.SERVO_W / 2 + P.CLEAR_POCKET
    cradle_bot = -PITCH_DROP - P.SERVO_BELOW - 4
    cradle = Pos(0, -LEG_W / 2, cradle_bot) * Box(
        2 * (cav_x + CRADLE_WALL), LEG_W,
        (-BRACKET_CLEAR_R - 6) - cradle_bot,
        align=(Align.CENTER, Align.MIN, Align.MIN))

    part = horn_plate + idler_plate + spine + cradle

    # Pitch servo: output axis along +Y at the pitch axis, body rising above it.
    pitch_tf = Pos(0, 0, -PITCH_DROP) * S.on_axis(Rot(Y=90), Rot(X=-90))
    part -= pitch_tf * S.servo_envelope()

    # Roll drive: bolts to the roll servo's horn through the forward plate.
    part -= Pos(x_horn, 0, 0) * Rot(Y=90) * S.drive_hole_cutters(FORK_T)
    # Idler bore in the aft plate.
    part -= Pos(x_idler - FORK_T - 0.1, 0, 0) * Rot(Y=90) * Cylinder(
        P.SERVO_HORN_DIA / 2 + 0.25, FORK_T + 0.2,
        align=(Align.CENTER, Align.CENTER, Align.MIN))

    return {
        "name": "hip_link",
        "handed": True,
        "part": part,
        "orientation": Rot(),  # stands on the cradle bottom
        "notes": "Draft v1. Pitch-servo retention screws after the cradle "
                 "fit coupon. Mirror in Y for the left.",
    }
