# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Thigh (DEC-17): hangs from the hip-pitch servo, carries the 37D drive
motor with the wheel at the outer knee.

Split at a DEC-23 seam into two parts, because a fork and a cross-axis motor
tube have no shared good print orientation:

  thigh_upper  - fork + beam. Printed lying on its side face (Rot(Y=90)) so
                 both fork plates stand on edge and the whole profile is a
                 constant-thickness slab flat on the bed.
  motor_clamp  - ring + tube. Printed with the motor axis vertical, which
                 makes the tube a standing cylinder: no overhang at all.

Frames: thigh_upper origin = the PITCH axis, +Z up, +Y outboard.
        motor_clamp origin = the WHEEL/motor axis, same directions.
Seam plane: thigh-local Z = SEAM_Z, i.e. wheel-local Z = THIGH_DROP + SEAM_Z.
"""
import math
from build123d import Box, Cylinder, Part, Pos, Rot, Align
from .. import params as P
from .. import fasteners as F
from .. import servo_iface as S

FORK_R = 15.0
FORK_T = 5.0
HORN_GAP = 0.2
THICK = 30.0            # slab thickness in X - the thigh's structural depth
FILL_TOP = -12.0        # full-width fill starts below the servo (bottom -10.2)
SEAM_Z = -92.0          # thigh-local; 28 mm above the wheel axis
SEAM_BOLTS = [(-10.0, -14.0), (10.0, -14.0), (-10.0, 8.0), (10.0, 8.0)]

MOTOR_FACE_Y = 14.0
RING_T = 5.0
TUBE_LEN = 34.0
TUBE_WALL = 4.0
TUBE_END_Y = MOTOR_FACE_Y - RING_T - TUBE_LEN   # -25.0
FLANGE_Z = (18.0, 28.0)                         # wheel-local; top = seam


def build_upper() -> dict:
    y_horn = P.SERVO_HORN_TOP + HORN_GAP        # +20.4 (drive side)
    y_idler = P.SERVO_IDLER_BOT - HORN_GAP      # -19.6 (idler side)

    horn_plate = Pos(0, y_horn, 0) * Rot(X=-90) * Cylinder(
        FORK_R, FORK_T, align=(Align.CENTER, Align.CENTER, Align.MIN))
    idler_plate = Pos(0, y_idler, 0) * Rot(X=90) * Cylinder(
        FORK_R, FORK_T, align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Full-width beam from below the servo down to the seam.
    y0, y1 = y_idler - FORK_T, y_horn + FORK_T
    beam = Pos(0, (y0 + y1) / 2, SEAM_Z) * Box(
        THICK, y1 - y0, FILL_TOP - SEAM_Z,
        align=(Align.CENTER, Align.CENTER, Align.MIN))

    part = horn_plate + idler_plate + beam

    # Pitch drive: bolts to the pitch servo's horn through the outboard plate.
    part -= Pos(0, y_horn, 0) * Rot(X=-90) * S.drive_hole_cutters(FORK_T)
    # Idler bore in the inboard plate.
    part -= Pos(0, y_idler - FORK_T - 0.1, 0) * Rot(X=-90) * Cylinder(
        P.SERVO_HORN_DIA / 2 + 0.25, FORK_T + 0.2,
        align=(Align.CENTER, Align.CENTER, Align.MIN))
    # Seam: M3 inserts in the bottom face (screws come up from the clamp).
    for (sx, sy) in SEAM_BOLTS:
        part -= Pos(sx, sy, SEAM_Z - 0.1) * Cylinder(
            P.INSERT_M3_DIA / 2, P.INSERT_M3_LEN,
            align=(Align.CENTER, Align.CENTER, Align.MIN))

    return {
        "name": "thigh_upper",
        "handed": True,
        "part": part,
        "orientation": Rot(Y=90),  # lies on its side face; plates on edge
        "notes": "Draft v1. Mirror in Y for the left thigh.",
    }


def build_clamp() -> dict:
    ring = Pos(0, MOTOR_FACE_Y, 0) * Rot(X=90) * Cylinder(
        P.MOTOR_DIA / 2 + TUBE_WALL + 1.5, RING_T,
        align=(Align.CENTER, Align.CENTER, Align.MIN))
    tube = Pos(0, MOTOR_FACE_Y - RING_T, 0) * Rot(X=90) * Cylinder(
        P.MOTOR_DIA / 2 + TUBE_WALL, TUBE_LEN,
        align=(Align.CENTER, Align.CENTER, Align.MIN))
    # Seam flange; reaches the tube's far end so it also lands on the bed.
    flange = Pos(0, (TUBE_END_Y + MOTOR_FACE_Y) / 2, FLANGE_Z[0]) * Box(
        THICK, MOTOR_FACE_Y - TUBE_END_Y, FLANGE_Z[1] - FLANGE_Z[0],
        align=(Align.CENTER, Align.CENTER, Align.MIN))

    part = ring + tube + flange

    # Motor bores: face-boss recess, body bore, and the 6x M3 face screws.
    part -= Pos(0, MOTOR_FACE_Y + 0.1, 0) * Rot(X=90) * Cylinder(
        P.MOTOR_FACE_BOSS_DIA / 2 + 0.5, RING_T + 0.2,
        align=(Align.CENTER, Align.CENTER, Align.MIN))
    part -= Pos(0, MOTOR_FACE_Y - RING_T, 0) * Rot(X=90) * Cylinder(
        P.MOTOR_DIA / 2 + P.CLEAR_POCKET, TUBE_LEN + 0.1,
        align=(Align.CENTER, Align.CENTER, Align.MIN))
    for i in range(P.MOTOR_FACE_SCREWS):
        a = math.radians(60 * i + 30)
        part -= Pos(P.MOTOR_BCD / 2 * math.cos(a), MOTOR_FACE_Y + 0.1,
                    P.MOTOR_BCD / 2 * math.sin(a)) * Rot(X=90) * Cylinder(
            P.CLEAR_HOLE_M3 / 2, RING_T + 0.2,
            align=(Align.CENTER, Align.CENTER, Align.MIN))
    # Seam clearance holes, screwing up into the thigh's inserts.
    for (sx, sy) in SEAM_BOLTS:
        part -= Pos(sx, sy + P.THIGH_DROP + SEAM_Z - (P.THIGH_DROP + SEAM_Z),
                    FLANGE_Z[1] + 0.1) * F.m3_clear(
            FLANGE_Z[1] - FLANGE_Z[0] + 0.2)

    return {
        "name": "motor_clamp",
        "handed": True,
        "part": part,
        "orientation": Rot(X=-90),  # motor axis vertical, face ring down
        "notes": "Draft v1. Verify MOTOR_LEN and the face boss before "
                 "printing. Mirror in Y for the left.",
    }
