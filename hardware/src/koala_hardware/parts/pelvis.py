# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Pelvis: structural plate carrying the two hip-roll servos underneath and
the electronics tray (torso element) on top via DEC-23 seam bosses.

Local frame: plate top face = Z=0, robot centre at origin, +X forward.
Roll servos: output axis along +X at (0, +/-ROLL_Y, -ROLL_DROP); the servo
body hangs vertically (output end down, rear tabs up near the plate), so the
hip-link fork plates swing in clear air on both sides of the tub.
"""
from build123d import Box, Cylinder, Part, Pos, Rot, Align
from .. import params as P
from .. import fasteners as F
from .. import servo_iface as S

ROLL_Y = 33.0
ROLL_DROP = 32.0     # plate top -> roll axis (fork disc r25 + plate clearance)
BOSS_H = 8.0
TRAY_BOSS_XY = [(60, 35), (60, -35), (-60, 35), (-60, -35)]


def servo_tf(side: int):
    """Roll-servo placement (side=+1 right, -1 left): Rot(Y=90) maps the
    output axis (+Z local) to +X and the body long axis (+X local) to -Z,
    i.e. body hanging down with the rear tabs up near the plate."""
    return Pos(0, side * ROLL_Y, -ROLL_DROP) * Rot(Y=90)


def build() -> dict:
    px, py, pt = P.PELVIS_PLATE
    plate = Pos(0, 0, -pt) * Box(px, py, pt,
                                 align=(Align.CENTER, Align.CENTER, Align.MIN))

    part = Part() + plate
    # Servo tubs: boxes hanging under the plate that the servo envelopes
    # carve into. X extent stays strictly between the hip-link fork planes
    # (idler face -19.4 .. horn face +20.2) so the fork swings free.
    for side in (1, -1):
        tub = Pos(0.5, side * ROLL_Y, -pt + 0.1) * Box(
            39, 40, 54, align=(Align.CENTER, Align.CENTER, Align.MAX))
        part += tub
    for side in (1, -1):
        part -= servo_tf(side) * S.servo_envelope()
        part -= servo_tf(side) * S.tab_screw_cutters(boss_top_z=30, depth=44)

    # DEC-23 seam to the electronics tray: 4x M3 insert bosses + keys on top
    for (bx, by) in TRAY_BOSS_XY:
        part += Pos(bx, by, 0) * F.insert_boss(BOSS_H)
    part += Pos(0, 40, 0) * F.registration_key()
    part += Pos(0, -40, 0) * F.registration_key()

    return {
        "name": "pelvis",
        "part": part,
        "orientation": Rot(X=180),  # print plate-top down
        "notes": "Draft v0. Roll range ~+/-25 deg before the hip-link web "
                 "meets the plate; lightening cutouts and cable routing "
                 "to follow.",
    }
