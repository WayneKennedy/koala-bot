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
    # DEC-53: flanges cover the root plates; torso shape is otherwise deferred.
    # DEC-60: flange and rails follow the hip pitch spacing (40/36 at the old 24).
    # DEC-61 (as built 2026-09-19 after the owner rejected a rotated flange): the
    # box torso is unchanged; a bracket under the rear face carries the 45 degree
    # pelvis plate on two side gussets, open at the back so the module screws and
    # their driver reach the plate from behind. The plate is the rear flange's
    # geometry rotated about the pitch axis with the modules, so contact and the
    # hole pattern follow `pelvis.pitch_socket` exactly.
    F=P.ROOT_PITCH_Y+16;R=P.ROOT_PITCH_Y+12;tilt=Rot(Y=P.REAR_SOCKET_TILT)
    part=S._box(-46,20,-F,F,LOW,LOW+5)
    part+=S._box(-46,20,-F,F,HIGH-5,HIGH)
    # Two side rails keep the centre accessible to harnesses and electronics.
    for y in (-R,R):
        part+=S._box(-46,-36,y-4,y+4,LOW,HIGH)
        part+=S._box(10,20,y-4,y+4,LOW,HIGH)
    part=holes(part,HIGH-5,HIGH)
    # Electronics tray mounting holes across the rear (dorsal) rail.
    for y in (-26,26):
        for z in (LOW+12,HIGH-12):
            part+=S._box(-46,-36,y-5,y+5,z-5,z+5)
            part+=S._box(-46,-36,min(y,-R) if y<0 else y,max(y,-R) if y<0 else R,z-5,z+5)
            part-=S._x_hole(-47,-35,y,z,P.CLEAR_HOLE_M3)
    # Rounded exposed vertical corners of each rail/flange silhouette.
    vertical=[e for e in part.edges().filter_by(Axis.Z) if e.length>8]
    part=fillet(vertical,1.5)
    # The inclined pelvis plate: the rear flange's plane, rotated with the modules.
    x0,x1=P.TORSO_REAR_PLATE_X
    plate=tilt*holes(S._box(x0,x1,-F,F,LOW,LOW+5),LOW,LOW+5)
    # Side gussets fill the triangle between plate and flange, outboard of the screw pattern.
    below=S._box(-46,20,-F,F,LOW-60,LOW)                    # the space under the rear face
    above_plate=tilt*S._box(-300,300,-300,300,LOW,LOW+400)   # torso side of the inclined plane
    for y0,y1 in ((-F,-F+P.TORSO_GUSSET_T),(F-P.TORSO_GUSSET_T,F)):
        part+=(S._box(-46,20,y0,y1,LOW-60,LOW)&above_plate)
    part+=plate&(below+S._box(-46,20,-F,F,LOW,LOW+5))         # the plate, clipped to the torso footprint
    return part


def build():
    return L.spec('torso_frame',solid(),orientation=Rot(Y=-90),version=3,
        fasteners={},
        notes='Rigid 150 mm pitch-axis torso, shape deferred (DEC-53); a bracket under its rear face carries the 45 degree pelvis plate (DEC-61). Flanges contact the root modules; sixteen M3x16 root screws pass the flanges into the modules. Rear face down. Support the opposite rails and flange/slot roofs; all supports are removable through the open cage.', printable='assumed')
