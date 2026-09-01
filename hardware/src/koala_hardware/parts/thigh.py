# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Thigh (DEC-17): hangs from the hip-pitch servo, carries the 37D drive
motor in the thigh with the wheel at the outer knee.

Local frame: wheel/motor axis = Y axis at origin; hip-pitch axis = Y axis at
Z=+THIGH_DROP. +Y is outboard (wheel side), +X is robot-forward.
Pitch servo centre sits on the pitch axis with its horn facing outboard
(+Y); the fork clamps horn (outboard, screwed) and idler hub (inboard, bore).
"""
import math
from build123d import Box, Cylinder, Part, Pos, Rot, Align
from .. import params as P
from .. import servo_iface as S

FORK_R = 25.0       # fork plate radius around the pitch axis
FORK_T = 4.0
HORN_GAP = 0.2      # face clearance to horn / idler
MOTOR_FACE_Y = 14.0 # motor faceplate position (local y)
RING_T = 5.0        # motor face ring thickness
TUBE_WALL = 4.0
TUBE_LEN = 34.0     # clamp length over the gearbox


def build() -> dict:
    zp = P.THIGH_DROP  # pitch axis height
    # fork plate positions (pitch servo centre at y=0 on the pitch axis)
    y_horn_in = P.SERVO_HORN_TOP + HORN_GAP            # 20.4
    y_idler_in = P.SERVO_IDLER_BOT - HORN_GAP          # -19.6

    horn_plate = Pos(0, y_horn_in, zp) * Rot(X=-90) * Cylinder(
        FORK_R, FORK_T, align=(Align.CENTER, Align.CENTER, Align.MIN))
    idler_plate = Pos(0, y_idler_in, zp) * Rot(X=90) * Cylinder(
        FORK_R, FORK_T, align=(Align.CENTER, Align.CENTER, Align.MIN))

    # web joining the fork plates on the forward (+X) side, clear of the
    # servo body's swept envelope (max radial reach ~20 => web starts at 22)
    web = Pos(20, y_idler_in - FORK_T, zp - 14) * Box(
        14, (y_horn_in + FORK_T) - (y_idler_in - FORK_T), 28,
        align=(Align.MIN, Align.MIN, Align.MIN))

    # beam from web down the front to the motor clamp
    beam = Pos(18, -24, -10) * Box(18, 48.4, zp - 14 + 10,
                                   align=(Align.MIN, Align.MIN, Align.MIN))

    # motor clamp: face ring + tube, axis Y at origin
    ring = Pos(0, MOTOR_FACE_Y, 0) * Rot(X=90) * Cylinder(
        P.MOTOR_DIA / 2 + TUBE_WALL + 1.5, RING_T,
        align=(Align.CENTER, Align.CENTER, Align.MIN))
    tube = Pos(0, MOTOR_FACE_Y - RING_T, 0) * Rot(X=90) * Cylinder(
        P.MOTOR_DIA / 2 + TUBE_WALL, TUBE_LEN,
        align=(Align.CENTER, Align.CENTER, Align.MIN))

    part = horn_plate + idler_plate + web + beam + ring + tube

    # --- cutters ---
    # pitch-servo drive interface through the outboard (horn) plate
    part -= Pos(0, y_horn_in, zp) * Rot(X=-90) * S.drive_hole_cutters(FORK_T)
    # idler bore through the inboard plate
    part -= Pos(0, y_idler_in - FORK_T - 0.1, zp) * Rot(X=-90) * Cylinder(
        P.SERVO_HORN_DIA / 2 + 0.25, FORK_T + 0.2,
        align=(Align.CENTER, Align.CENTER, Align.MIN))
    # motor bore (body + face boss + shaft path) through ring & tube
    part -= Pos(0, MOTOR_FACE_Y + 0.1, 0) * Rot(X=90) * Cylinder(
        P.MOTOR_FACE_BOSS_DIA / 2 + 0.5, RING_T + 0.2,
        align=(Align.CENTER, Align.CENTER, Align.MIN))
    part -= Pos(0, MOTOR_FACE_Y - RING_T, 0) * Rot(X=90) * Cylinder(
        P.MOTOR_DIA / 2 + P.CLEAR_POCKET, TUBE_LEN + 0.1,
        align=(Align.CENTER, Align.CENTER, Align.MIN))
    # 6x M3 face screws on the motor BCD (hex pattern)
    for i in range(P.MOTOR_FACE_SCREWS):
        a = math.radians(60 * i + 30)  # offset so no screw lands on the beam web
        part -= Pos(P.MOTOR_BCD / 2 * math.cos(a), MOTOR_FACE_Y + 0.1,
                    P.MOTOR_BCD / 2 * math.sin(a)) * Rot(X=90) * Cylinder(
            P.CLEAR_HOLE_M3 / 2, RING_T + 0.2,
            align=(Align.CENTER, Align.CENTER, Align.MIN))

    return {
        "name": "thigh_right",
        "part": part,
        "orientation": Rot(X=-90),   # print lying on the inboard fork face
        "notes": "Draft v0. Verify MOTOR_LEN/boss before final print; "
                 "mirror in Y for the left thigh.",
    }
