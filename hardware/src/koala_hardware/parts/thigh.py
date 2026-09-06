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
from build123d import (Axis, Box, Cylinder, Part, Plane, Polygon, Pos, Rot,
                       Align, extrude, fillet)
from .. import params as P
from .. import fasteners as F
from .. import servo_iface as S

FORK_R = 15.0
FORK_T = 5.0
HORN_GAP = 0.2
THICK = 30.0            # slab thickness in X - the thigh's structural depth
FILL_TOP = -P.SERVO_W / 2 - 2   # fill starts below the servo (half-WIDTH
                        # now, since the pitch servo lies aft, not upright)
SEAM_Z = -92.0          # thigh-local; 28 mm above the wheel axis
SEAM_BOLTS = [(-10.0, -14.0), (10.0, -14.0), (-10.0, 8.0), (10.0, 8.0)]

MOTOR_FACE_Y = 14.0
RING_T = 5.0
TUBE_LEN = 34.0
TUBE_WALL = 4.0
TUBE_END_Y = MOTOR_FACE_Y - RING_T - TUBE_LEN   # -25.0
# Derived from the shared seam datum: DEC-26 increased THIGH_DROP by 34 mm,
# and a hard-coded old value here previously left the clamp floating 34 mm
# below the upper thigh in the assembly.
SEAM_WHEEL_Z = P.THIGH_DROP + SEAM_Z
# The flange is the structural bridge from the motor tube to the seam, so its
# bottom overlaps the tube instead of floating at only the upper ten mm.
FLANGE_Z = (18.0, SEAM_WHEEL_Z)                 # wheel-local; top = seam
BEAM_CORNER_R = 4.0
FLANGE_CORNER_R = 4.0
FLANGE_RIB_W = 11.0


def build_upper() -> dict:
    # The pitch servo is slid OUTBOARD by HIP_PITCH_Y (see params: sliding a
    # servo along its own output axis is free), so the fork follows it out.
    # The beam still has to reach the motor clamp inboard, so the thigh is a
    # shallow dogleg: fork outboard at the hip, beam spanning down to the seam.
    y_horn = P.HIP_PITCH_Y + P.SERVO_HORN_TOP + HORN_GAP
    y_idler = P.HIP_PITCH_Y + P.SERVO_IDLER_BOT - HORN_GAP

    horn_plate = Pos(0, y_horn, 0) * Rot(X=-90) * Cylinder(
        FORK_R, FORK_T, align=(Align.CENTER, Align.CENTER, Align.MIN))
    idler_plate = Pos(0, y_idler, 0) * Rot(X=90) * Cylinder(
        FORK_R, FORK_T, align=(Align.CENTER, Align.CENTER, Align.MIN))

    # The beam must span both the outboard fork and the inboard motor seam, but
    # it does not need to carry that maximum rectangle all the way down. A
    # rounded, tapered YZ profile follows the load path and gives the thigh a
    # soft limb silhouette while retaining a constant X thickness for its
    # support-free side-on print orientation (DEC-28).
    y0 = min(y_idler - FORK_T, TUBE_END_Y)
    y1 = max(y_horn + FORK_T, MOTOR_FACE_Y)
    profile = Plane.YZ * Polygon(
        (y0, SEAM_Z), (MOTOR_FACE_Y, SEAM_Z),
        (24.0, -70.0), (43.0, -25.0), (y1, -10.0),
        (40.0, -10.0), (35.0, FILL_TOP), (y_idler - FORK_T, FILL_TOP),
        (-8.0, -28.0), (-17.0, -65.0),
        align=Align.NONE)
    beam = extrude(profile, amount=THICK / 2, both=True)
    beam = fillet(beam.edges().filter_by(Axis.X), BEAM_CORNER_R)

    part = horn_plate + idler_plate + beam

    # Pitch drive: bolts to the pitch servo's horn through the outboard plate.
    part -= Pos(0, y_horn, 0) * Rot(X=-90) * S.drive_hole_cutters(FORK_T)
    # Idler side: BOLT to it (second metal horn, same 4-hole square, free-
    # spinning). A plain bore here made the knee a single-sided cantilever.
    part -= Pos(0, y_idler, 0) * Rot(X=90) * S.drive_hole_cutters(FORK_T)
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
        "notes": "Rounded, tapered structural beam (DEC-28). Mirror in Y "
                 "for the left thigh.",
    }


def build_clamp() -> dict:
    ring = Pos(0, MOTOR_FACE_Y, 0) * Rot(X=90) * Cylinder(
        P.MOTOR_DIA / 2 + TUBE_WALL + 1.5, RING_T,
        align=(Align.CENTER, Align.CENTER, Align.MIN))
    tube = Pos(0, MOTOR_FACE_Y - RING_T, 0) * Rot(X=90) * Cylinder(
        P.MOTOR_DIA / 2 + TUBE_WALL, TUBE_LEN,
        align=(Align.CENTER, Align.CENTER, Align.MIN))
    # Twin seam ribs follow the two bolt columns from the motor tube to the
    # upper thigh. Each has a full 3.3 mm edge around its M3 holes; the open
    # centre removes a broad, non-functional slab from the silhouette.
    flange = Part()
    for sx in (-10.0, 10.0):
        rib = Pos(sx, (TUBE_END_Y + MOTOR_FACE_Y) / 2, FLANGE_Z[0]) * Box(
            FLANGE_RIB_W, MOTOR_FACE_Y - TUBE_END_Y,
            FLANGE_Z[1] - FLANGE_Z[0],
            align=(Align.CENTER, Align.CENTER, Align.MIN))
        flange += fillet(rib.edges().filter_by(Axis.Y), FLANGE_CORNER_R)

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
