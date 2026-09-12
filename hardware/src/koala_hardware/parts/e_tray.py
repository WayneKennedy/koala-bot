# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Removable electronics tray attached to the rigid torso, outside its rails."""
from functools import lru_cache
from build123d import Cylinder, Pos, Rot, Align, Axis, fillet, Cone
from .. import params as P, servo_iface as S
from . import links as L, torso as T

# Tray local XY corresponds to body YZ; strap zones retain flexible packaging.
@lru_cache
def solid():
    part=S._box(-48,48,-44,44,0,4)
    part=fillet(part.edges().filter_by(Axis.Z),5)
    holes=[(y,z-(T.LOW+T.HIGH)/2) for y in (-26,26) for z in (T.LOW+12,T.HIGH-12)]
    for x,y in P.UNO_HOLES:
        x,y=x-P.UNO_BOARD[0]/2,y-P.UNO_BOARD[1]/2
        part+=Pos(x,y,4)*Cylinder(3.5,5,align=(Align.CENTER,Align.CENTER,Align.MIN))
        part+=Pos(x,y,4)*Cone(5,3.5,1.5,align=(Align.CENTER,Align.CENTER,Align.MIN))
        holes.append((x,y))
    for x,y in holes:
        part-=Pos(x,y,-1)*Cylinder(P.CLEAR_HOLE_M3/2,12,align=(Align.CENTER,Align.CENTER,Align.MIN))
    for x in (-40,40):
        for y in (-26,0,26): part-=S._box(x-1.5,x+1.5,y-4,y+4,-1,5)
    return part


def location():
    from build123d import Plane
    return Plane(origin=(-50,0,(T.LOW+T.HIGH)/2),x_dir=(0,1,0),z_dir=(-1,0,0)).location


def build():
    return L.spec('e_tray',solid(),orientation=Rot(),
        fasteners={'M3x25 tray through-bolt':4,'M3 nut':8,'M3 plain washer':12,'M3x16 Uno driver-board bolt (stack to verify)':4},
        notes='Flat tray, Uno-pattern stand-offs plus strap slots. Four 4 mm spacers to torso; rounded stand-off roots. No support intended; electronics packaging remains open.', printable='assumed')


def build_spacer():
    part=Cylinder(3.5,4,align=(Align.CENTER,Align.CENTER,Align.MIN))-Cylinder(P.CLEAR_HOLE_M3/2,4,align=(Align.CENTER,Align.CENTER,Align.MIN))
    return L.spec('tray_spacer',part,qty=4,orientation=Rot(),notes='Four functional 4 mm tray stand-offs. Print together with brim.', printable='assumed')
