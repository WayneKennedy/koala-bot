# SPDX-License-Identifier: CERN-OHL-S-2.0
"""DEC-23 joint primitives: insert bosses, clearance holes, seam pairs.

Convention: functions return either a solid to union (bosses) or a cutter
solid to subtract (holes), always positioned via build123d `Pos`/`Rot` by
the caller.
"""
from build123d import Box, Cylinder, Part, Pos, Align
from . import params as P


def insert_boss(height: float, wall: float = 2.5) -> Part:
    """Boss for an M3 heat-set insert; axis +Z, base at Z=0, hole from the top."""
    outer = Cylinder(P.INSERT_M3_DIA / 2 + wall, height,
                     align=(Align.CENTER, Align.CENTER, Align.MIN))
    hole = Pos(0, 0, height - P.INSERT_M3_LEN) * Cylinder(
        P.INSERT_M3_DIA / 2, P.INSERT_M3_LEN + 0.1,
        align=(Align.CENTER, Align.CENTER, Align.MIN))
    return outer - hole


def m3_clear(depth: float) -> Part:
    """M3 clearance-hole cutter; axis +Z, from Z=0 downward."""
    return Cylinder(P.CLEAR_HOLE_M3 / 2, depth,
                    align=(Align.CENTER, Align.CENTER, Align.MAX))


def m2_5_clear(depth: float) -> Part:
    return Cylinder(P.CLEAR_HOLE_M2_5 / 2, depth,
                    align=(Align.CENTER, Align.CENTER, Align.MAX))


def registration_key(length: float = 8.0, w: float = 4.0, h: float = 2.0,
                     clearance: float = 0.0) -> Part:
    """Rectangular alignment key; male (clearance=0) or female pocket cutter
    (clearance=CLEAR_POCKET). Centred in X/Y, base at Z=0 growing +Z."""
    return Box(length + 2 * clearance, w + 2 * clearance, h + clearance,
               align=(Align.CENTER, Align.CENTER, Align.MIN))
