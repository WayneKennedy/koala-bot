# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Hip link: driven by the roll servo, carries the pitch servo that drives the
thigh. The 2-DOF hip of DEC-07.

Local frame: origin ON THE ROLL AXIS; roll axis = X, +X forward, +Y outboard.
The pitch axis is HIP_PITCH_DROP below, running along Y.

COMPACT LAYOUT. The pitch servo points AFT (-X) and is slid OUTBOARD along its
own axis. Sliding a servo along its output axis does not move that axis, so
this is free in kinematics and buys the whole compaction: the two hip axes sit
26 mm apart instead of 60, and the leg reads as a hip rather than a hip plus a
knee halfway down the thigh.

Clearances that set the shape:
  - The link rotates about the roll axis carrying everything below it, so it
    must clear the ROLL SERVO body (X -19.4..20.2, Y +/-12.4, Z -10.2..35.2)
    and the hip bracket (which now starts at Z=20, well clear).
  - The legs therefore drop at X = +/-20, just outboard of the servo's ends,
    where the field below the axis is open.

DEC-24 print strategy: stands on the cradle's flat outboard face with the roll
axis horizontal, so both fork plates stand on edge - a clevis printed
axis-vertical always leaves its far tine bridging air.
"""
from build123d import Box, Cylinder, Part, Pos, Rot, Align
from .. import params as P
from .. import servo_iface as S

FORK_R = 15.0        # just covers the drive square + idler bore
FORK_T = 5.0
HORN_GAP = 0.2
LEG_W = 26.0         # leg width in Y
LEG_T = 6.0          # leg thickness along X
CRADLE_WALL = 4.0
PITCH_DROP = P.HIP_PITCH_DROP
PITCH_Y = P.HIP_PITCH_Y

# pitch servo extents in this frame, from its own constants
SRV_X0 = -P.SERVO_ABOVE                      # -35.2, body points aft
SRV_X1 = P.SERVO_BELOW                       # +10.2
SRV_Y0 = PITCH_Y + P.SERVO_IDLER_BOT         # inboard face
SRV_Y1 = PITCH_Y + P.SERVO_HORN_TOP          # outboard face
SRV_Z0 = -PITCH_DROP - P.SERVO_W / 2
SRV_Z1 = -PITCH_DROP + P.SERVO_W / 2


def build() -> dict:
    x_horn = P.SERVO_HORN_TOP + HORN_GAP        # +20.4 (drive side)
    x_idler = P.SERVO_IDLER_BOT - HORN_GAP      # -19.6 (idler side)

    horn_plate = Pos(x_horn, 0, 0) * Rot(Y=90) * Cylinder(
        FORK_R, FORK_T, align=(Align.CENTER, Align.CENTER, Align.MIN))
    idler_plate = Pos(x_idler, 0, 0) * Rot(Y=-90) * Cylinder(
        FORK_R, FORK_T, align=(Align.CENTER, Align.CENTER, Align.MIN))

    part = horn_plate + idler_plate

    # Legs: drop from each disc, then run outboard to meet the cradle. They sit
    # at X = +/-20, clear of the roll servo body which ends at X 20.2 / -19.4.
    for x0 in (x_horn, x_idler - LEG_T):
        part += Pos(x0, -LEG_W / 2, SRV_Z1) * Box(
            LEG_T, LEG_W, -SRV_Z1,
            align=(Align.MIN, Align.MIN, Align.MIN))
        # outboard run, from the leg across to the far cradle wall
        part += Pos(x0, -LEG_W / 2, SRV_Z0 - CRADLE_WALL) * Box(
            LEG_T, SRV_Y1 + CRADLE_WALL + LEG_W / 2, SRV_Z1 - SRV_Z0 + CRADLE_WALL,
            align=(Align.MIN, Align.MIN, Align.MIN))

    # Cradle: wraps the pitch servo, open on the outboard face so it slides in.
    part += Pos(SRV_X0 - CRADLE_WALL, SRV_Y0 - CRADLE_WALL, SRV_Z0 - CRADLE_WALL) * Box(
        (SRV_X1 - SRV_X0) + 2 * CRADLE_WALL,
        (SRV_Y1 - SRV_Y0) + 2 * CRADLE_WALL,
        (SRV_Z1 - SRV_Z0) + CRADLE_WALL,
        align=(Align.MIN, Align.MIN, Align.MIN))

    # Pitch servo pocket: axis along +Y, body aft, slid outboard.
    pitch_tf = Pos(0, PITCH_Y, -PITCH_DROP) * S.on_axis(Rot(X=-90))
    part -= pitch_tf * S.servo_envelope()

    # Roll drive: bolts to the roll servo's horn through the forward plate.
    part -= Pos(x_horn, 0, 0) * Rot(Y=90) * S.drive_hole_cutters(FORK_T)
    # Idler side: BOLT to it, don't clear it (second metal horn, same square).
    part -= Pos(x_idler, 0, 0) * Rot(Y=-90) * S.drive_hole_cutters(FORK_T)

    # Pitch-servo retention (OQ-12): 2 screws into the front cradle wall, 2
    # into the back, through the servo's case bores. Clearance in the print.
    tab_x = P.SERVO_AXIS_X - P.SERVO_TAB_X
    for sy in (-P.SERVO_TAB_Y, P.SERVO_TAB_Y):
        for sgn in (-1, 1):
            y = PITCH_Y + sy
            start = SRV_X0 - CRADLE_WALL - 1 if sgn < 0 else SRV_X1 + CRADLE_WALL + 1
            part -= Pos(start, y, -PITCH_DROP) * Rot(Y=-90 * sgn) * Cylinder(
                P.SELFTAP_CLEAR / 2, CRADLE_WALL + 2.5,
                align=(Align.CENTER, Align.CENTER, Align.MIN))

    return {
        "name": "hip_link",
        "handed": True,
        "part": part,
        "orientation": Rot(),  # stands on the cradle floor; fork plates on edge
        "notes": "Compact hip: pitch servo aft and outboard, axes 26 mm apart. "
                 "Retention screw size unverified (OQ-12). Mirror in Y.",
    }
