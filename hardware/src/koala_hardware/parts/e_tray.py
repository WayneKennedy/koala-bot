# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Electronics tray - first torso element, sits on the pelvis seam bosses.

Carries: TB9051FTG shield (Arduino Uno hole pattern, verified standard),
Teensy 4.0 (no holes -> zip-tie zone), BNO085 IMU (near the roll axis,
zip/velcro zone until its holes are verified). M3 screws drop through the
tray corners into the pelvis heat-set inserts (DEC-23).
"""
from build123d import Box, Cylinder, Part, Pos, Rot, Align
from .. import params as P
from .. import fasteners as F
from .pelvis import TRAY_BOSS_XY

TRAY = (150.0, 100.0, 4.0)
ZIP_SLOT = (4.0, 10.0)


def build() -> dict:
    tx, ty, tt = TRAY
    part = Part() + Box(tx, ty, tt, align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Uno-pattern standoffs for the TB9051FTG shield, board centred forward
    bx, by = P.UNO_BOARD
    origin = (-bx / 2 + 10, -by / 2)  # slight forward bias, centred in Y
    for (hx, hy) in P.UNO_HOLES:
        part += Pos(origin[0] + hx, origin[1] + hy, tt) * Cylinder(
            3.5, P.STANDOFF_H, align=(Align.CENTER, Align.CENTER, Align.MIN))
        part -= Pos(origin[0] + hx, origin[1] + hy, tt + P.STANDOFF_H + 0.1) * \
            Cylinder(1.4, P.STANDOFF_H + tt + 0.2,
                     align=(Align.CENTER, Align.CENTER, Align.MAX))  # M3 self-tap pilot

    # zip-tie slot fields: Teensy zone (rear-left) and IMU zone (rear-right)
    for zx in (-55, -40, -25):
        for zy in (18, 38, -18, -38):
            part -= Pos(zx, zy, tt + 0.1) * Box(
                ZIP_SLOT[0], ZIP_SLOT[1], tt + 0.2,
                align=(Align.CENTER, Align.CENTER, Align.MAX))

    # corner screw-downs into the pelvis bosses + registration key pockets
    for (cx, cy) in TRAY_BOSS_XY:
        part -= Pos(cx, cy, tt + 0.1) * F.m3_clear(tt + 0.2)
    for ky in (40, -40):
        part -= Pos(0, ky, P.CLEAR_POCKET) * Rot(X=180) * F.registration_key(
            clearance=P.CLEAR_POCKET)

    return {
        "name": "e_tray",
        "part": part,
        "orientation": Rot(),  # prints as-is, flat
        "notes": "Wire pass-throughs and the IMU hard-mount come after "
                 "BNO085 hole positions are verified against the board.",
    }
