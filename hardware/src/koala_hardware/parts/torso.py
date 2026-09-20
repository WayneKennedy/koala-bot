# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Rigid V1 torso frame. Real crossmember contact; head remains an envelope."""
from functools import lru_cache
from build123d import Pos, Rot, Cylinder, Align, Axis, fillet, Rectangle, loft, Plane, mirror
from .. import params as P, servo_iface as S
from . import links as L, pelvis, neck_space

LOW=P.ROOT_REAR_MOUNT_Z+P.ROOT_PLATE_T
HIGH=P.BODY_TORSO_LENGTH_MM-P.ROOT_MOUNT_Z-P.ROOT_PLATE_T
# HIGH remains the electronics-tray mounting datum; the shoulder frame now
# wraps the former exposed A volume without moving the 150 mm joint spacing.
TOP=P.TORSO_SHOULDER_TOP


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
    F=P.TORSO_HALF_WIDTH;R=F-4;tilt=Rot(Y=P.REAR_SOCKET_TILT)
    part=S._box(-46,20,-F,F,LOW,LOW+5)
    # Dorsal shoulder rails taper inward before the A horn span. This opens
    # the roll sweep without increasing torso depth; the smaller neck pack
    # fits between the rails. Ventral rails step forward below the shoulder.
    for y in (-R,R):
        inner_y=29 if y>0 else -29
        part+=S._box(-46,-36,y-4,y+4,LOW,106)
        part+=loft([Pos(-41,y,106)*Rectangle(10,8),Pos(-41,inner_y,122)*Rectangle(10,8)])
        part+=S._box(-46,-36,inner_y-4,inner_y+4,122,TOP)
        part+=S._box(10,20,y-4,y+4,LOW,118)
        part+=loft([Pos(15,y,118)*Rectangle(10,8),Pos(31,y,130)*Rectangle(10,8)])
        part+=S._box(26,36,y-4,y+4,130,TOP)
    for z in (135,165):part+=S._box(26,36,-F,F,z-5,z+5)
    # Removable future neck cartridge: three small STS3032M envelopes fit in
    # the dorsal slot; the four M3 attachment points are independent of their
    # unmeasured ear pattern and the still-open 3-RPS linkage geometry.
    cap=S._box(-46,36,-F,F,TOP-5,TOP)
    cap-=neck_space.cap_opening(TOP-6,TOP+1)
    cap-=neck_space.mount_hole_tools(TOP-6,TOP+1)
    part+=cap
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
    # Rear root service: drill the actual straight screwdriver corridors
    # through the retained horizontal flange and inner rear rail edges.
    tf=pelvis.pitch_socket(False)
    zhead=-P.SOCKET_SHELF-P.ROOT_PLATE_T-P.FRAME_PLATE_T
    for a,b in pelvis.nut_xy():
        driver=tf*Pos(a,b,zhead-40)*Cylinder(3.3,40,align=(Align.CENTER,Align.CENTER,Align.MIN))
        part-=driver+mirror(driver,Plane.XZ)
    # Cassette fasteners remain accessible from the front with both A servos
    # installed. The unchanged root screws are fitted to each cassette on bench.
    for y,z in P.SHOULDER_CASSETTE_BOLTS:
        for sign in (-1,1):part-=S._x_hole(25,37,sign*y,z,P.CLEAR_HOLE_M3)
    return part


def build():
    return L.spec('torso_frame',solid(),orientation=Rot(Y=-90),version=5,
        fasteners={},
        notes='Rigid 150 mm hip-to-shoulder spacing; frame extended to Z183.5 around the recessed roll-first A modules. '
        '47 mm half-width gives a 10 mm socket-lip recess; dorsal shoulder rails taper inward for roll clearance. Front-access removable shoulder cassettes; 45 degree rear plate with open full-length driver corridors. '
        'Dorsal shoulder slot and four M3 holes reserve a removable three-STS3032M neck cartridge; final servo retention and 3-RPS linkage remain open. '
        'Dorsal face down; bed-only support under opposing rails, cap and flange roofs, removable through open cage. Unprinted.',printable='unknown')
