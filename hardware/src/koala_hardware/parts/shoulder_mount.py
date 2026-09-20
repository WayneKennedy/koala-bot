# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Removable shoulder cassette: fit the proven A module on the bench.

Native coordinates are body coordinates. The cassette bolts to the ventral
frame, so recessed root screws never need a driver through the opposite servo.
"""
from functools import lru_cache
from math import sqrt
from build123d import Pos, Rot, Plane, Cylinder, Align, RectangleRounded, RegularPolygon, extrude, fillet, GeomType
from .. import params as P, servo_iface as S
from . import links as L, pelvis


def carrier_frame():
    return Plane(origin=(0,P.SHOULDER_A_Y,P.BODY_TORSO_LENGTH_MM),
                 x_dir=(0,0,-1),z_dir=(1,0,0)).location


def socket_frame():
    return carrier_frame()*Rot(X=-90)*L.AXIS


def module():
    return socket_frame()*pelvis.root_socket()


def root_fixings():
    # The root module and flange stack are unchanged; only placement differs.
    return socket_frame()*pelvis.pitch_socket(False).inverse()*pelvis.fixing_envelopes(False)


@lru_cache
def solid():
    tf=socket_frame();w,d=pelvis.plate_outline()
    part=tf*Pos(0,0,-P.SOCKET_SHELF-P.ROOT_PLATE_T-P.FRAME_PLATE_T)*extrude(RectangleRounded(w,d,4),amount=P.FRAME_PLATE_T)
    # Flat Y=4 build face; continuous web carries the module to a broad front
    # flange. The two cassettes have 2 mm between their root screw heads.
    part+=S._box(16,26,4,9,130,170)
    part+=S._box(20,26,4,36,130,170)
    edges=[e for e in part.edges() if e.geom_type==GeomType.LINE
           and abs(e.center().X-20)<1e-6 and abs(e.center().Y-9)<1e-6 and e.length>30]
    if len(edges)!=1:raise ValueError('Shoulder cassette: missing inside load-path edge')
    # The proven root plate reaches X=18.35: a larger inside radius would
    # intrude into its underside. R1.5 leaves 0.15 mm at the plate edge.
    part=fillet(edges,1.5)
    for a,b in pelvis.nut_xy():
        part-=tf*Pos(a,b,-17)*Cylinder(P.CLEAR_HOLE_M3/2,7,align=(Align.CENTER,Align.CENTER,Align.MIN))
    for y,z in P.SHOULDER_CASSETTE_BOLTS:
        part-=S._x_hole(19,27,y,z,P.CLEAR_HOLE_M3)
        # Nuts entered from the accessible back of this flange before fitting.
        part-=Pos(19.99,y,z)*Rot(Y=90)*extrude(RegularPolygon((P.NUT_M3_AF+.2)/sqrt(3),6),amount=2.61)
    # Round exposed flange ends without rounding mating faces or holes.
    edges=[e for e in part.edges() if e.geom_type==GeomType.LINE and e.length>30
           and abs(e.center().Y-36)<1e-6 and any(abs(e.center().X-x)<1e-6 for x in (20,26))]
    if edges:part=fillet(edges,1.5)
    return part


def frame_fixings():
    parts=[]
    for y,z in P.SHOULDER_CASSETTE_BOLTS:
        parts.append(S._x_hole(36,39,y,z,6))
        parts.append(Pos(20.1,y,z)*Rot(Y=90)*extrude(RegularPolygon(P.NUT_M3_AF/sqrt(3),6),amount=P.NUT_M3_T))
    from build123d import Compound
    return Compound(children=parts)


def build():
    return L.spec('shoulder_mount',solid(),handed=True,orientation=Rot(X=90),
        fasteners={'M3x20 shoulder cassette-to-frame screw':4,'M3 nut, captive in shoulder cassette':4},
        notes='Removable recessed A mounting cassette. Y=4 broad face on bed; open flange nut pockets and bore roofs need accessible bed-only support. '
        'On the bench, preload all four cassette nuts before bolting the unchanged root_socket v1 onto it with four M3x16. '
        'Slide the complete module in from the side and secure it with four front-access M3x20. Withdraw laterally outward for root service. '
        '10 mm recess measured from torso side envelope to enclosing socket lip; A horns and moving carrier remain outside.',printable='unknown')
