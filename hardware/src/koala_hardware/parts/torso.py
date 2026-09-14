# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Rigid V1 torso frame. Real crossmember contact; head remains an envelope."""
from functools import lru_cache
from build123d import Pos, Rot, Cylinder, Align, Axis, fillet, Cone
from .. import params as P, servo_iface as S
from . import links as L

LOW=P.ROOT_REAR_MOUNT_Z+P.ROOT_PLATE_T
HIGH=P.BODY_TORSO_LENGTH_MM-P.ROOT_MOUNT_Z-P.ROOT_PLATE_T


def holes(part,z0,z1):
    for x,y in P.ROOT_FRAME_HOLES:
        part-=Pos(x,y,z0-1)*Cylinder(P.CLEAR_HOLE_M3/2,z1-z0+2,align=(Align.CENTER,Align.CENTER,Align.MIN))
    return part


@lru_cache
def solid():
    # DEC-53: flanges cover the 36.7 mm root plates; front rails moved out to
    # clear the root screws at x = +-6. Torso shape is otherwise deferred.
    part=S._box(-46,20,-40,40,LOW,LOW+5)
    part+=S._box(-46,20,-40,40,HIGH-5,HIGH)
    # Two side rails keep the centre accessible to harnesses and electronics.
    for y in (-36,36):
        part+=S._box(-46,-36,y-4,y+4,LOW,HIGH)
        part+=S._box(10,20,y-4,y+4,LOW,HIGH)
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
    # DEC-53: no locating pins; the root modules are fixed through the flanges
    # into their captive nuts. Torso shape itself is deferred (DEC-53, OQ-23).
    return part


def build():
    return L.spec('torso_frame',solid(),orientation=Rot(Y=-90),
        fasteners={},
        notes='Rigid 150 mm pitch-axis torso, shape deferred (DEC-53). Flanges contact the root modules; sixteen M3x16 root screws pass the flanges into the modules. Rear face down. Support the opposite rails and flange/slot roofs; all supports are removable through the open cage.', printable='assumed')
