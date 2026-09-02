# SPDX-License-Identifier: CERN-OHL-S-2.0
"""STS3215 interface geometry, built from measured constants (params [STEP]).

Servo local frame follows the vendor STEP: body box centred in X/Y on the
origin, output (spline) axis vertical (+Z) through (SERVO_AXIS_X, 0).
Horn on top, idler hub underneath (double-sided clamp joint).
"""
from build123d import Box, Cylinder, Part, Pos, Align
from . import params as P
from . import fasteners as F


def on_axis(*rot) -> Pos:
    """Compose a servo placement whose OUTPUT AXIS lands on the local origin.

    The servo's output axis is offset SERVO_AXIS_X from its body centre, so a
    bare rotation leaves the axis 12.5 mm off where you meant it. Always place
    servos with this helper: `on_axis(Rot(Y=90))` etc.
    """
    tf = Pos(0, 0, 0)
    for r in rot:
        tf = tf * r
    return tf * Pos(-P.SERVO_AXIS_X, 0, 0)


def servo_envelope(clearance: float = P.CLEAR_POCKET) -> Part:
    """Simplified servo keep-out solid (body + tabs + horn/idler cylinders).
    Subtract from a printed part to make a cradle pocket."""
    c = clearance
    body = Pos(0, 0, P.SERVO_BODY_BOT - c) * Box(
        P.SERVO_L + 2 * c, P.SERVO_W + 2 * c,
        (P.SERVO_BODY_TOP - P.SERVO_BODY_BOT) + 2 * c,
        align=(Align.CENTER, Align.CENTER, Align.MIN))
    # rear tab block (spans the -X end above the case, full width incl. ears)
    tabs = Pos((P.SERVO_TAB_X - 3) / 1, 0, P.SERVO_BODY_BOT - c) * Box(
        8 + 2 * c, P.SERVO_W + 6 + 2 * c,
        (P.SERVO_TAB_TOP - P.SERVO_BODY_BOT) + 2 * c,
        align=(Align.CENTER, Align.CENTER, Align.MIN))
    horn = Pos(P.SERVO_AXIS_X, 0, P.SERVO_BODY_TOP) * Cylinder(
        P.SERVO_HORN_DIA / 2 + c, (P.SERVO_HORN_TOP - P.SERVO_BODY_TOP) + 2,
        align=(Align.CENTER, Align.CENTER, Align.MIN))
    idler = Pos(P.SERVO_AXIS_X, 0, P.SERVO_IDLER_BOT - 2) * Cylinder(
        P.SERVO_HORN_DIA / 2 + c, 6,
        align=(Align.CENTER, Align.CENTER, Align.MIN))
    return body + tabs + horn + idler


def drive_hole_cutters(plate_t: float) -> Part:
    """Cutter for a plate that bolts onto the horn (or idler): 4x M3
    clearance on the DRIVE_SQ square + centre boss clearance. Plate lies on
    Z=0..plate_t with the drive axis at the local origin.

    M3, not M2.5: the servo spec item 6-13 gives the output-shaft screw as
    M3x6, and none are supplied ([SPEC 11] "No Accessories").
    """
    s = P.SERVO_DRIVE_SQ / 2
    cut = Pos(0, 0, plate_t + 0.1) * Cylinder(
        P.SERVO_HORN_BOSS_DIA / 2 + 0.5, plate_t + 0.2,
        align=(Align.CENTER, Align.CENTER, Align.MAX))
    for sx in (-s, s):
        for sy in (-s, s):
            cut += Pos(sx, sy, plate_t + 0.1) * F.m3_clear(plate_t + 0.2)
    return cut


def tab_screw_cutters(boss_top_z: float, depth: float = 12.0) -> Part:
    """Cutters for the two rear-tab retention screws (vertical, at the
    measured tab positions). Cut from boss_top_z downward."""
    cut = None
    for sy in (-P.SERVO_TAB_Y, P.SERVO_TAB_Y):
        c = Pos(P.SERVO_TAB_X, sy, boss_top_z) * Cylinder(
            P.SERVO_TAB_HOLE / 2, depth,
            align=(Align.CENTER, Align.CENTER, Align.MAX))
        cut = c if cut is None else cut + c
    return cut
