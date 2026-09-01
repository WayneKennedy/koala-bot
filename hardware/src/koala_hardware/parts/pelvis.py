# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Pelvis plate - the structural deck.

DEC-24: kept as a FLAT plate with features on one face only. The hip-roll
servos live in separate `hip_bracket` parts bolted underneath, and the
electronics tray stands off above on bought M3 standoffs; nothing protrudes
from the top face. Result: prints flat on the bed, zero support.

Local frame: plate top face = Z=0, robot centre at origin, +X forward.
"""
from build123d import Box, Cylinder, Part, Pos, Rot, Align
from .. import params as P
from .. import fasteners as F

# Hip-bracket bolt pattern (through the plate, into inserts in the flange)
BRACKET_BOLTS = [(bx, by) for bx in (-12.0, 12.0) for by in (-21.0, 21.0)]
TRAY_BOSS_XY = [(60.0, 35.0), (60.0, -35.0), (-60.0, 35.0), (-60.0, -35.0)]
CABLE_SLOT = (30.0, 8.0)


def build() -> dict:
    px, py, pt = P.PELVIS_PLATE
    part = Part() + Box(px, py, pt, align=(Align.CENTER, Align.CENTER, Align.MAX))

    # Tray standoff mounts: M3 heat-set inserts, through-holes (no ceiling).
    for (bx, by) in TRAY_BOSS_XY:
        part -= Pos(bx, by, 0.1) * Cylinder(
            P.INSERT_M3_DIA / 2, pt + 0.2,
            align=(Align.CENTER, Align.CENTER, Align.MAX))

    # Hip brackets bolt up from below: clearance holes, screw head on top.
    for side in (1, -1):
        for (bx, by) in BRACKET_BOLTS:
            part -= Pos(bx, side * P.HIP_ROLL_Y + by, 0.1) * F.m3_clear(pt + 0.2)

    # Cable pass-throughs, one per side, inboard of the brackets.
    for side in (1, -1):
        part -= Pos(-50, side * 20, 0.1) * Box(
            CABLE_SLOT[0], CABLE_SLOT[1], pt + 0.2,
            align=(Align.CENTER, Align.CENTER, Align.MAX))

    return {
        "name": "pelvis_plate",
        "qty": 1,
        "part": part,
        "orientation": Rot(),  # flat, top face up; either face works
        "notes": "Flat deck (DEC-24). Hip brackets bolt underneath; tray "
                 "stands off above on M3 standoffs.",
    }
