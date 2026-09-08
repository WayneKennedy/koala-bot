# SPDX-License-Identifier: CERN-OHL-S-2.0
"""New removable tray with metal through-fasteners; no printed screw threads."""
from functools import lru_cache
from build123d import Align, Axis, Box, Cylinder, Pos, Rot, fillet
from .. import params as P


@lru_cache
def solid():
    lx, ly, t = P.V2_TRAY_SIZE
    part = Box(lx, ly, t, align=(Align.CENTER, Align.CENTER, Align.MIN))
    part = fillet(part.edges().filter_by(Axis.Z), 8)
    holes = list(P.V2_TRAY_HOLES)
    for x, y in P.UNO_HOLES:
        x, y = x-P.UNO_BOARD[0]/2+15, y-P.UNO_BOARD[1]/2
        part += Pos(x,y,t)*Cylinder(3.5,P.STANDOFF_H,
            align=(Align.CENTER,Align.CENTER,Align.MIN))
        holes.append((x,y))
    for x, y in holes:
        part -= Pos(x,y,-1)*Cylinder(P.CLEAR_HOLE_M3/2,t+P.STANDOFF_H+2,
            align=(Align.CENTER,Align.CENTER,Align.MIN))
    # Separate board zones, secured by straps until BNO085 holes are confirmed.
    for x in (-60., -40.):
        for y in (-27., -3., 7., 33.):
            part -= Pos(x,y,t/2)*Box(3,8,t+2)
    return part


def build():
    return dict(name='e_tray',part=solid(),qty=1,orientation=Rot(),
        fasteners={'M3x8 upper tray-standoff screw':len(P.V2_TRAY_HOLES),
                   'M3x16 driver-shield screw (board stack to verify)':len(P.UNO_HOLES),
                   'M3 nut':len(P.UNO_HOLES)},
        notes='Flat bottom on bed. Uno shield on four through-bolted 5 mm standoffs; '
              'Teensy and BNO085 occupy separate strap zones. Four bought 10 mm '
              'standoffs attach tray to pelvis; use metal nuts, no plastic threads.')
