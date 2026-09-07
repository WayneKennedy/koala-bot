# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Open, bolted hip carrier. Coordinates relative to the roll axis.
Cheeks print flat; saddle prints on its floor. All hardware fits provisional.
"""
from build123d import Align, Axis, Box, Cylinder, Plane, Polygon, Pos, Rot, extrude, fillet
from .. import params as P

T = 5.0
DRIVE_X = P.SERVO_HORN_TOP + 0.2
IDLER_X = P.SERVO_IDLER_BOT - 0.2
BASE_Z = -52.0
SEAT_Z = -P.HIP_PITCH_DROP - P.SERVO_W / 2
TOP_Z = -P.HIP_PITCH_DROP + P.SERVO_W / 2
BOLTS = [(-20.0, -47.0), (-12.0, -47.0)]  # Y,Z; M3 through X
POST_X = (P.HIP_PITCH_X - P.SERVO_ABOVE - 6.8,
          P.HIP_PITCH_X + P.SERVO_BELOW + 6.8)


def hole(r, h):
    return Pos(0, 0, -0.1) * Cylinder(r, h + 0.2,
        align=(Align.CENTER, Align.CENTER, Align.MIN))


def horn_plate(profile, radius=15):
    part = extrude(Polygon(*profile, align=Align.NONE), amount=T, dir=(0, 0, 1))
    part = fillet(part.edges().filter_by(Axis.Z), 3)
    part += Cylinder(radius, T, align=(Align.CENTER, Align.CENTER, Align.MIN))
    part -= hole(P.SERVO_HORN_BOSS_DIA / 2 + 0.5, T)
    for a in (-P.SERVO_DRIVE_SQ / 2, P.SERVO_DRIVE_SQ / 2):
        for b in (-P.SERVO_DRIVE_SQ / 2, P.SERVO_DRIVE_SQ / 2):
            part -= Pos(a, b) * hole(P.SERVO_DRIVE_SCREW / 2, T)
    return part


def cheek(drive):
    # Flat XY design: drawing X=assembly Y, drawing Y=assembly Z.
    part = horn_plate([(-10, 0), (8, 0), (-8, -14),
                       (-8, BASE_Z), (-28, BASE_Z), (-28, -18)], radius=12)
    for y, z in BOLTS:
        part -= Pos(y, z) * hole(P.CLEAR_HOLE_M3 / 2, T)
    # Plane.YZ maps the drawing into YZ and the extrusion into +X.
    part = Pos(DRIVE_X if drive else IDLER_X - T, 0, 0) * Plane.YZ.location * part
    return dict(name="hip_roll_drive" if drive else "hip_roll_idler",
                part=part, qty=2, orientation=Rot(Y=-90),
                notes="Flat cheek face on bed; layers in YZ load plane. "
                      "Four unobstructed through-holes per horn. M3x55 carrier bolts; "
                      "horn screw length and idler spacing require physical fit.")


def build_drive():
    return cheek(True)


def build_idler():
    return cheek(False)


def build_saddle():
    # An aft web joins two rails around an OPEN lane for the inner thigh.
    h = SEAT_Z - BASE_Z
    part = Pos(3.2, 4, BASE_Z) * Box(66.4, 64, h,
        align=(Align.CENTER, Align.CENTER, Align.MIN))
    part = fillet(part.edges().filter_by(Axis.Z), 3)
    # Lane extends forward to free space, no enclosing crossbar.
    part -= Pos(-6, -5, BASE_Z - 0.1) * Box(60, 10, h + 0.2,
        align=(Align.MIN, Align.MIN, Align.MIN))
    # Roll plates bound the inboard rail; the aft connecting web remains.
    part -= Pos(-60, -40, BASE_Z - .1) * Box(60 + IDLER_X, 35, h + .2,
        align=(Align.MIN, Align.MIN, Align.MIN))
    part -= Pos(DRIVE_X, -40, BASE_Z - .1) * Box(40, 35, h + .2,
        align=(Align.MIN, Align.MIN, Align.MIN))
    for x in POST_X:
        part += Pos(x, P.HIP_PITCH_Y, BASE_Z) * Cylinder(5.5, TOP_Z - BASE_Z,
            align=(Align.CENTER, Align.CENTER, Align.MIN))
        part -= Pos(x, P.HIP_PITCH_Y, TOP_Z + .1) * Cylinder(
            P.INSERT_M3_DIA / 2, P.INSERT_M3_LEN + .1,
            align=(Align.CENTER, Align.CENTER, Align.MAX))
    for y, z in BOLTS:
        part -= Pos(IDLER_X - .1, y, z) * Rot(Y=90) * Cylinder(
            P.CLEAR_HOLE_M3 / 2, DRIVE_X - IDLER_X + .2,
            align=(Align.CENTER, Align.CENTER, Align.MIN))
    return dict(name="hip_pitch_saddle", part=part, handed=True, orientation=Rot(),
                notes="Floor on bed. Open inner-thigh sweep lane. Two M3x8 clamp "
                      "screws into inserts; two M3x55 cheek through-bolts with nuts. "
                      "Horizontal 3.4 mm bores require a fit/bridge test; case clamp "
                      "friction and creep are unvalidated.")


def build_cap():
    part = Pos(sum(POST_X) / 2, P.HIP_PITCH_Y, TOP_Z) * Box(
        POST_X[1] - POST_X[0] + 11, 12, 4,
        align=(Align.CENTER, Align.CENTER, Align.MIN))
    part = fillet(part.edges().filter_by(Axis.Z), 3)
    for x in POST_X:
        part -= Pos(x, P.HIP_PITCH_Y, TOP_Z) * hole(P.CLEAR_HOLE_M3 / 2, 4)
    return dict(name="hip_pitch_cap", part=part, qty=2, orientation=Rot(),
                notes="Broad face on bed. Removable case clamp, no assumed case "
                      "screw pattern. Fit/preload and cable exit require hardware test.")
