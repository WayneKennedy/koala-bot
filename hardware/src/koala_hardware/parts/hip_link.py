# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Hip link: driven by the roll servo (in the pelvis, axis along X), and
cradles the pitch servo (axis along Y) that drives the thigh.

Local frame: roll axis = X axis at origin; +X forward (horn side), +Y
outboard, -Z down. The pitch servo centre sits at PITCH_DROP below the roll
axis, output +Y (outboard), body long axis pointing down (-Z).
"""
from build123d import Box, Cylinder, Part, Pos, Rot, Align
from .. import params as P
from .. import servo_iface as S

FORK_R = 25.0
FORK_T = 4.0
HORN_GAP = 0.2
PITCH_DROP = 60.0    # roll axis -> pitch axis
CRADLE_WALL = 4.0


def build() -> dict:
    x_horn_in = P.SERVO_HORN_TOP + HORN_GAP
    x_idler_in = P.SERVO_IDLER_BOT - HORN_GAP

    # fork plates perpendicular to X (clamping the roll servo horn/idler)
    horn_plate = Pos(x_horn_in, 0, 0) * Rot(Y=90) * Cylinder(
        FORK_R, FORK_T, align=(Align.CENTER, Align.CENTER, Align.MIN))
    idler_plate = Pos(x_idler_in, 0, 0) * Rot(Y=-90) * Cylinder(
        FORK_R, FORK_T, align=(Align.CENTER, Align.CENTER, Align.MIN))

    # web joining the plates underneath (-Z), clear of the servo swept reach
    web = Pos(x_idler_in - FORK_T, -12, -34) * Box(
        (x_horn_in + FORK_T) - (x_idler_in - FORK_T), 24, 12,
        align=(Align.MIN, Align.MIN, Align.MIN))

    # cradle block for the pitch servo, hanging below the web.
    # Pitch servo frame: local +Z (output) -> robot +Y ; local +X (long axis,
    # toward the output end) -> robot -Z (down) => Rot(X=-90) then Rot(Y=90)?
    # We use: Rot(Y=-90) maps +Z->+X.. build with explicit transform below.
    servo_tf = Pos(0, 0, -PITCH_DROP) * Rot(X=-90) * Rot(Z=-90)
    # cradle block sized around the rotated servo envelope; Y extent stays
    # strictly between the thigh fork planes (idler -19.4 .. horn +20.2),
    # and the top overlaps the web by 1 mm so the solids fuse.
    cradle = Pos(-16, -18, -PITCH_DROP - 32) * Box(
        32, 37, 59, align=(Align.MIN, Align.MIN, Align.MIN))

    part = horn_plate + idler_plate + web + cradle
    part -= servo_tf * S.servo_envelope()
    # retention screws into the servo rear tabs (tabs now at the top; screw
    # axis follows the servo's local Z which is robot +Y): reuse the tab
    # cutter in the servo frame.
    part -= servo_tf * S.tab_screw_cutters(boss_top_z=30, depth=44)

    # roll drive interface through the forward (horn) plate
    part -= Pos(x_horn_in, 0, 0) * Rot(Y=90) * S.drive_hole_cutters(FORK_T)
    # idler bore
    part -= Pos(x_idler_in - FORK_T - 0.1, 0, 0) * Rot(Y=90) * Cylinder(
        P.SERVO_HORN_DIA / 2 + 0.25, FORK_T + 0.2,
        align=(Align.CENTER, Align.CENTER, Align.MIN))

    return {
        "name": "hip_link_right",
        "part": part,
        "orientation": Rot(Y=90),  # print on the idler plate face
        "notes": "Draft v0. Cradle is oversized; will be sculpted after the "
                 "first render/print review. Mirror for left.",
    }
