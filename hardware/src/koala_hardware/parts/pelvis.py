# SPDX-License-Identifier: CERN-OHL-S-2.0
"""DEC-53 root socket module: one design at all four limb roots, handed, two per hand.

The plate faces the torso. Four M3 nuts sit captive in the socket shelf under the
servo Bottom; the fitted servo covers them and the screws come from the torso
side. A rear module is a front module turned 180 deg about the pitch axis, so the
case stands into the torso at both roots. Bench assembled before frame fitting."""
from functools import lru_cache
from math import sqrt
from build123d import Pos, Rot, Plane, mirror, Axis, Cylinder, Align, extrude, RectangleRounded, RegularPolygon
from .. import params as P, servo_iface as S
from . import links as L


def pitch_socket(front=False):
    # Same physical part at both roots: the shoulder case points down the torso,
    # the pelvis case points up it. 180 deg about the lateral pitch axis.
    loc=Plane(origin=(0,P.ROOT_PITCH_Y,0),x_dir=(0,1,0),z_dir=(0,0,1 if front else -1)).location*L.AXIS
    # DEC-61: the rear sockets mount on the torso's 45° face; the rotation is about
    # the pitch axis, so the leg's saved coordinates and joint axes are unchanged.
    return loc if front else Rot(Y=P.REAR_SOCKET_TILT)*loc


def nut_xy():
    """Captive-nut centres in the socket frame (along the axis, across it)."""
    return [(a,b) for a in (-P.ROOT_NUT_DX,P.ROOT_NUT_DX) for b in (-P.ROOT_NUT_DY,P.ROOT_NUT_DY)]


def plate_outline():
    x,y=S._socket_bounds(); y+=2.0
    return 2*(x+P.SOCKET_WALL+P.ROOT_PLATE_FLANGE_X),2*(y+P.ROOT_PLATE_FLANGE)


@lru_cache
def root_socket():
    """Socket frame: Z up from the servo Bottom; shelf -5..0; plate below it."""
    w,d=plate_outline(); t=P.ROOT_PLATE_T
    plate=Pos(0,0,-P.SOCKET_SHELF-t)*extrude(RectangleRounded(w,d,4),amount=t)
    # Union first, then features: no separately rounded bodies overlapped
    # (integrated-links rule, 2026-09-14).
    part=plate+S.saddle()
    pocket_d=P.NUT_M3_T+P.NUT_POCKET_CLEAR
    r=(P.NUT_M3_AF+P.NUT_POCKET_CLEAR)/sqrt(3)
    for a,b in nut_xy():
        part-=Pos(a,b,-pocket_d)*extrude(RegularPolygon(r,6),amount=pocket_d+0.01)
        part-=Pos(a,b,-P.SOCKET_SHELF-t-1)*Cylinder(P.CLEAR_HOLE_M3/2,P.SOCKET_SHELF+t+2,align=(Align.CENTER,Align.CENTER,Align.MIN))
    return part


@lru_cache
def module(front=False):
    return pitch_socket(front)*root_socket()


@lru_cache
def solid(front=False):
    """Both installed modules, retained for layout/access studies."""
    right=module(front)
    return right+mirror(right,Plane.XZ)


def fixing_envelopes(front=False):
    """Screw heads beyond the torso flange and captive nuts, socket frame, one side."""
    t=P.ROOT_PLATE_T; z_flange=-P.SOCKET_SHELF-t-P.FRAME_PLATE_T
    parts=None
    for a,b in nut_xy():
        head=Pos(a,b,z_flange-3)*Cylinder(3,3,align=(Align.CENTER,Align.CENTER,Align.MIN))
        nut=Pos(a,b,-P.NUT_M3_T-0.1)*extrude(RegularPolygon(P.NUT_M3_AF/sqrt(3),6),amount=P.NUT_M3_T)
        parts=head+nut if parts is None else parts+head+nut
    return pitch_socket(front)*parts


def build():
    return L.spec('root_socket',root_socket(),qty=2,handed=True,orientation=Rot(),
        fasteners={'M2x5 self-tapper into servo ear':4,f'{P.ROOT_SCREW} root screw, from the torso side':4,'M3 nut, captive under the servo':4},
        notes='Proven v1, plate 1, PETG, 2026-09-19: four printed and main fit passed. Ear holes need drilling to '
        '2.2 mm on those prints because support entered them; bed-only support is now set for reprints. '
        'One unchanged module at all four roots, two per hand. Drop four M3 nuts into the shelf, then fit the '
        'servo and all four ear screws on the bench. Rear modules bolt to the inclined torso flange; front '
        'modules bolt to removable shoulder cassettes on the bench before the cassettes enter the frame. '
        'Use four M3x16 per module. Flat plate face down, socket opening up; accessible ear-roof support. '
        'Cable routing, screw bottoming and loaded retention remain unverified.', printable='proven')
