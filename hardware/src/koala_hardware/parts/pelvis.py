# SPDX-License-Identifier: CERN-OHL-S-2.0
"""DEC-29 integrated pelvis; deck top Z=0 prints against the bed.
Integral roll roots replace the old flanges. Slice and load tests pending.
"""
from build123d import Axis, Box, Cylinder, Part, Pos, Rot, Align, fillet, mirror, Plane
from .. import params as P

TRAY_BOSS_XY = [(60.0, 35.0), (60.0, -35.0), (-60.0, 35.0), (-60.0, -35.0)]
CABLE_SLOT = (30.0, 8.0)
CORNER_R = 15.0


def build() -> dict:
    px, py, pt = P.PELVIS_PLATE
    deck = Box(px, py, pt, align=(Align.CENTER, Align.CENTER, Align.MAX))
    deck = fillet(deck.edges().filter_by(Axis.Z), CORNER_R)
    part = Part() + deck

    # Tray standoff mounts: M3 heat-set inserts, through-holes (no ceiling).
    for (bx, by) in TRAY_BOSS_XY:
        part -= Pos(bx, by, 0.1) * Cylinder(
            P.INSERT_M3_DIA / 2, pt + 0.2,
            align=(Align.CENTER, Align.CENTER, Align.MAX))

    # Integral roots, without the obsolete 6 mm bolt-on mounting flange.
    from .hip_bracket import build_root
    root = build_root()
    for side in (1, -1):
        part += Pos(0, side * P.HIP_ROLL_Y, -P.HIP_ROLL_DROP) * (
            root if side == 1 else mirror(root, Plane.XZ))

    # Cable pass-throughs, one per side, inboard of the brackets.
    for side in (1, -1):
        part -= Pos(-50, side * 20, 0.1) * Box(
            CABLE_SLOT[0], CABLE_SLOT[1], pt + 0.2,
            align=(Align.CENTER, Align.CENTER, Align.MAX))

    return {
        "name": "pelvis",
        "qty": 1,
        "part": part,
        "orientation": Rot(X=180),
        "notes": "Integrated deck and roll-servo saddles; deck top on bed. "
                 "No bracket flanges or eight mounting screws. Root layers "
                 "still see bending: load/creep test required. Roll retention "
                 "holes remain provisional (OQ-12). Use 4 mm-long tray inserts.",
    }
