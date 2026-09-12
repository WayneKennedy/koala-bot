# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Rigid V1 torso frame. Real crossmember contact; head remains an envelope."""
from functools import lru_cache
from build123d import Pos, Rot, Cylinder, Align, Axis, fillet, Cone
from .. import params as P, servo_iface as S
from . import links as L

LOW=P.ROOT_REAR_MOUNT_Z+P.FRAME_PLATE_T
HIGH=P.BODY_TORSO_LENGTH_MM-P.ROOT_MOUNT_Z-P.FRAME_PLATE_T


def holes(part,z0,z1):
    for x,y in P.ROOT_FRAME_HOLES:
        part-=Pos(x,y,z0-1)*Cylinder(P.CLEAR_HOLE_M3/2,z1-z0+2,align=(Align.CENTER,Align.CENTER,Align.MIN))
    return part


@lru_cache
def solid():
    part=S._box(-46,16,-40,40,LOW,LOW+5)
    part+=S._box(-46,16,-40,40,HIGH-5,HIGH)
    # Two side rails keep the centre accessible to harnesses and electronics.
    for y in (-36,36):
        part+=S._box(-46,-36,y-4,y+4,LOW,HIGH)
        part+=S._box(6,16,y-4,y+4,LOW,HIGH)
    part=holes(part,LOW,LOW+5);part=holes(part,HIGH-5,HIGH)
    # Electronics tray mounting holes across the rear plane.
    for y in (-26,26):
        for z in (LOW+12,HIGH-12):
            part+=S._box(-46,-36,y-5,y+5,z-5,z+5)
            part+=S._box(-46,-36,min(y,-36) if y<0 else y,max(y,-36) if y<0 else 36,z-5,z+5)
            part-=S._x_hole(-47,-35,y,z,P.CLEAR_HOLE_M3)
    # Rounded exposed vertical corners of each rail/flange silhouette.
    vertical=[e for e in part.edges().filter_by(Axis.Z) if e.length>8]
    part=fillet(vertical,1.5)
    # Integral locating pins register the independently removable sockets.
    for y in (-26,-12,12,26):
        for z in (LOW-P.ROOT_LOCATOR_DEPTH,HIGH):
            part+=Pos(-28,y,z)*Cylinder(P.ROOT_LOCATOR_DIA/2,P.ROOT_LOCATOR_DEPTH,align=(Align.CENTER,Align.CENTER,Align.MIN))
    return part


def build():
    return L.spec('torso_frame',solid(),orientation=Rot(Y=-90),
        fasteners={'M3x14 torso-crossmember bolt':8,'M3 nut':8,'M3 plain washer':16},
        notes='Rigid 150 mm pitch-axis torso. Flanges contact crossmembers. Eight through-bolts with nuts and socket-module locating pockets; rear face down. Support the opposite rails and flange/slot roofs; all supports are removable through the open cage.', printable='assumed')
