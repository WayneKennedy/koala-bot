# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Flat twin-cheek thigh: motor face and rear support replace the old seam.
Local origin at pitch axis, X forward, Y outboard, Z up.
"""
import math
from build123d import Align, Cylinder, Plane, Pos, Rot
from .. import params as P
from .hip_link import horn_plate, hole

T = 5.0
DRIVE_Y = P.HIP_PITCH_Y + P.SERVO_HORN_TOP + 0.2
IDLER_Y = P.HIP_PITCH_Y + P.SERVO_IDLER_BOT - 0.2
MOTOR_FACE_Y = DRIVE_Y
SPACER_Z = (-65.0, -110.0)
SPACER_LEN = DRIVE_Y - IDLER_Y


def cheek(drive):
    # Drawing XY = assembly XZ; full profile prints flat in just 5 mm height.
    part = horn_plate([(-12, 0), (12, 0), (16, -60), (19, -P.THIGH_DROP),
                       (-19, -P.THIGH_DROP), (-16, -60)])
    part += Pos(0, -P.THIGH_DROP) * Cylinder(24, T,
        align=(Align.CENTER, Align.CENTER, Align.MIN))
    for z in SPACER_Z:
        part -= Pos(0, z) * hole(P.CLEAR_HOLE_M3 / 2, T)
    part -= Pos(0, -P.THIGH_DROP) * hole(
        P.MOTOR_FACE_BOSS_DIA / 2 + .5 if drive
        else P.MOTOR_DIA / 2 + P.CLEAR_POCKET, T)
    if drive:
        for i in range(P.MOTOR_FACE_SCREWS):
            a = math.radians(60 * i + 30)
            part -= Pos(P.MOTOR_BCD / 2 * math.cos(a),
                        -P.THIGH_DROP + P.MOTOR_BCD / 2 * math.sin(a)) * hole(
                            P.CLEAR_HOLE_M3 / 2, T)
    # Plane.XZ normal is -Y: drive cheek extrudes inward from outer face.
    part = Pos(0, DRIVE_Y + T if drive else IDLER_Y, 0) * Plane.XZ.location * part
    return dict(name="thigh_outer" if drive else "thigh_inner",
                part=part, qty=2, orientation=Rot(X=90),
                notes="Full cheek face on bed; layers follow hip-to-knee load path. "
                      + ("Motor face attaches here; install screws before hub/wheel."
                         if drive else "37 mm motor-body support; coupon-fit bore.")
                      + " Two M3x55 spacer through-bolts per thigh; no heat-set "
                        "insert seam. Strength and fatigue unvalidated.")


def build_outer():
    return cheek(True)


def build_inner():
    return cheek(False)


def build_spacer():
    part = Cylinder(12, SPACER_LEN, align=(Align.CENTER, Align.CENTER, Align.MIN))
    part -= hole(P.CLEAR_HOLE_M3 / 2, SPACER_LEN)
    return dict(name="thigh_spacer", part=part, qty=4, orientation=Rot(),
                notes="Flat circular end on bed, bore vertical. M3x55 through-bolt "
                      "clamps the 40 mm spacer between 5 mm cheeks. Layers mainly "
                      "in compression; bolted-joint slip/creep still require testing.")


def placed_spacers():
    p = build_spacer()["part"]
    return [Pos(0, IDLER_Y, z) * Rot(X=-90) * p for z in SPACER_Z]
