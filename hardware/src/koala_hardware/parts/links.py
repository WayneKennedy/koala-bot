# SPDX-License-Identifier: CERN-OHL-S-2.0
"""DEC-43 integral limbs with DEC-41 root joints. Native X = lateral; +Z down link."""
from functools import lru_cache
from math import cos, sin, radians
from build123d import Pos, Rot, Plane, Sphere, Cylinder, Align, RectangleRounded, extrude, Polygon, Cone, RegularPolygon, loft, Circle, fillet, Axis
from .. import params as P, servo_iface as S

AXIS=Pos(0,0,-P.SOCKET_AXIS_Z)


def fork(side):
    return AXIS*S.plate_location(side)*S.clevis_plate(side)


@lru_cache
def clevis():
    # Both cheeks and the bridge are one connected print. No seam fasteners.
    return (fork('drive')+fork('idler')+S._box(
        P.SOCKET_IDLER_FACE-P.SOCKET_PAD_T,P.SOCKET_DRIVE_FACE+P.SOCKET_PAD_T,
        -P.SOCKET_ARM_HALF_W,P.SOCKET_ARM_HALF_W,
        P.LINK_BRIDGE_START,P.LINK_BRIDGE_END))


@lru_cache
def upper_link(length):
    bottom=length-P.SOCKET_AXIS_Z
    c=P.LINK_SPINE_HALF
    spine=Pos(0,0,P.LINK_BRIDGE_START)*extrude(RectangleRounded(2*c,2*c,3),amount=bottom-P.LINK_BRIDGE_START)
    part=Rot(Z=-90)*clevis()+spine
    # Tapered root spreads load into the socket floor; no abrupt thin plank.
    start=max(P.LINK_BRIDGE_END,bottom-12)
    part+=loft([Pos(0,0,start)*RectangleRounded(16,16,3),
                Pos(0,0,bottom)*RectangleRounded(36,24,3)])
    part+=Pos(0,0,bottom)*S.saddle()
    return part


def motor_face(front=False):
    root_y=P.BODY_SHOULDER_WIDTH_MM/2 if front else rear_axis_y()
    return P.BODY_TRACK_TARGET_MM/2-P.WHEEL_W/2-P.HUB_STACK-root_y


def rear_axis_y():
    return P.BODY_SHOULDER_WIDTH_MM/2


@lru_cache
def lower_link(length,front=False):
    if front:
        # Broad flat bed face at native Y=-10.4. Rounded rectangular section
        # replaces the cylindrical shaft; a separate TPU pad supplies contact.
        shaft=Pos(0,-1.45,P.LINK_BRIDGE_START)*extrude(
            RectangleRounded(18,17.9,3),amount=P.FRONT_PAD_START-P.LINK_BRIDGE_START)
        part=clevis()+shaft
        part+=Pos(0,0,P.FRONT_PAD_START)*extrude(RectangleRounded(11,12,1),amount=7)
        # Captive metal M3 nut, inserted through the side before pad installation.
        nut=Pos(0,0,P.FRONT_PAD_NUT_Z)*extrude(RegularPolygon(3.3,6,rotation=30),amount=2.6)
        part-=nut+S._box(0,12,-2.9,2.9,P.FRONT_PAD_NUT_Z,P.FRONT_PAD_NUT_Z+2.6)
        part-=Pos(0,0,90)*Cylinder(P.CLEAR_HOLE_M3/2,15,align=(Align.CENTER,Align.CENTER,Align.MIN))
        return part
    face=motor_face(front); t=P.MOTOR_MOUNT_T
    inner=face-P.MOTOR_SUPPORT_OFFSET
    part=clevis()
    # The face plate and inner body ring are joined above the motor body.
    # Open axial insertion from inboard, face screws before hub/wheel.
    part+=S._x_hole(face,face+t,0,length,2*P.MOTOR_MOUNT_R)
    part+=S._x_hole(inner-P.MOTOR_SUPPORT_T,inner,0,length,2*P.MOTOR_MOUNT_R)
    x0=inner-P.MOTOR_SUPPORT_T; x1=face+t
    part+=Pos((x0+x1)/2,0,P.LINK_BRIDGE_START)*extrude(
        RectangleRounded(x1-x0,16,3),amount=length-P.MOTOR_DIA/2-1-P.LINK_BRIDGE_START)
    # Short webs connect fork shoulders to the offset rear motor support.
    x0=min(inner-P.MOTOR_SUPPORT_T,P.SOCKET_IDLER_FACE)
    x1=max(face+t,P.SOCKET_DRIVE_FACE)
    part+=Pos((x0+x1)/2,0,18)*extrude(RectangleRounded(x1-x0,20.8,3),amount=14)
    part-=S._x_hole(inner-P.MOTOR_SUPPORT_T-1,face,0,length,
                    P.MOTOR_DIA+2*P.CLEAR_POCKET)
    part-=S._x_hole(face-1,face+t+1,0,length,P.MOTOR_FACE_BOSS_DIA+1)
    for i in range(P.MOTOR_FACE_SCREWS):
        a=radians(i*60+30)
        part-=S._x_hole(face-1,face+t+1,P.MOTOR_BCD/2*cos(a),
                        length+P.MOTOR_BCD/2*sin(a),P.CLEAR_HOLE_M3)
    return part


def pitch_fork_frame():
    # Common shoulder/hip carrier frame: X roll, Y lateral, Z down upper limb.
    return Plane(origin=(0,P.ROOT_PITCH_Y,0),x_dir=(0,1,0),z_dir=(0,0,-1)).location


def roll_socket_frame(axis_y):
    return Pos(0,axis_y,0)*AXIS


@lru_cache
def carrier():
    """One unchamfered front-style carrier, used twice per hand (DEC-49)."""
    axis_y=P.BODY_SHOULDER_WIDTH_MM/2
    edge=axis_y-P.SOCKET_CASE_Y/2-1.5
    floor=-P.SOCKET_AXIS_Z-P.SOCKET_SHELF
    inner=P.ROOT_PITCH_Y+P.SOCKET_IDLER_FACE-P.SOCKET_PAD_T
    # The fork bridge and socket floor share a continuous flat bed face.
    # No head-driven bevel: head position and mounting are unresolved.
    return (pitch_fork_frame()*clevis()+
            S._box(-8,8,inner,edge,floor,-25)+
            roll_socket_frame(axis_y)*S.saddle())


HORN_FASTENERS={'M3x6 supplied horn-square pan screw (bottoming to verify)':8,
                'Metal 9.9-square horn/idler':2,
                'M3 drive-horn centre fixing (supplied kit)':1,
                'M3 narrow washer OD6 x 0.5, idler horn screws':4}


def spec(name,part,qty=1,orientation=None,fasteners=None,notes='',handed=False,material='PETG',printable='unknown'):
    return dict(name=name,part=part,qty=qty,orientation=orientation or Rot(Y=90),
                handed=handed,fasteners=fasteners or {},supports=True,
                printable=printable,material=material,
                notes=notes+' Accessible local supports permitted; inspect layers. Physical fit/load unverified.')


def upper_spec(name,length):
    return spec(name,upper_link(length),handed=True,orientation=Rot(X=90),
        fasteners=HORN_FASTENERS|{'M2x5 self-tapper into servo ear':4},
        notes=f'One {length:g} mm link: roll-axis horn forks, bridge, spine and perpendicular knee/elbow saddle. '+
        'Outer horn pad on bed; remove supports from inner fork and saddle. No structural seam bolts.', printable='assumed')


def lower_spec(name,length,front):
    return spec(name,lower_link(length,front),handed=True,
        fasteners=HORN_FASTENERS|{'M3x8 motor-face screw (depth to verify)':6},
        notes=f'One {length:g} mm link: both forks and integrated 37D face/body support. '+
        'Slide motor from inboard; install face screws before hub and wheel. Remove support from body bore.', printable='assumed')


def build_thigh(): return upper_spec('thigh',P.BODY_THIGH_MM)
def build_upper_arm(): return upper_spec('upper_arm',P.BODY_UPPER_ARM_MM)
def build_shank(): return lower_spec('shank',P.BODY_SHANK_MM,False)
def front_pad():
    length=P.BODY_FOREARM_MM+P.BODY_HAND_MM
    part=Pos(0,0,length)*Sphere(P.BODY_FRONT_FOOT_RADIUS_MM)
    part &= S._box(-20,20,-20,20,P.FRONT_PAD_START,length+20)
    # Keyed cavity, opening on the bed. Its roof tapers to the through bore
    # at <=45 degrees instead of bridging a closed TPU socket.
    part-=Pos(0,0,P.FRONT_PAD_START-1)*extrude(RectangleRounded(11.6,12.6,1),amount=8.3)
    part-=loft([Pos(0,0,103.2)*RectangleRounded(11.6,12.6,1),Pos(0,0,110)*Circle(P.CLEAR_HOLE_M3/2)])
    part-=Pos(0,0,103)*Cylinder(P.CLEAR_HOLE_M3/2,20,align=(Align.CENTER,Align.CENTER,Align.MIN))
    part-=Pos(0,0,110)*Cylinder(3.6,12,align=(Align.CENTER,Align.CENTER,Align.MIN))
    return part


def build_forearm():
    return spec('forearm',lower_link(P.BODY_FOREARM_MM+P.BODY_HAND_MM,True),handed=True,orientation=Rot(X=90),
        fasteners=HORN_FASTENERS|{'M3x20 front-pad screw':1,'M3 nut':1,'M3 plain washer':1},
        notes='One flat-section forearm; elbow fork and keyed TPU-pad seat. Broad native -Y face on bed. '
        'Insert captive M3 nut from side; fit pad and recessed M3x20 screw with washer. '
        'Local support under nut-slot roof and fork hole roofs is accessible from outside.', printable='assumed')


def build_front_pad():
    return spec('front_contact_pad',front_pad(),qty=2,orientation=Rot(),material='TPU',
        notes='Replaceable rounded TPU ground contact at the accepted 100 mm elbow-to-ball centre. '
        'Truncated mating face on bed; tapered keyed cavity avoids a flat internal roof. '
        'No support intended; recessed screw/washer remains above contact surface. Traction/wear untested.', printable='assumed')

def build_root_carrier():
    return spec('root_carrier',carrier(),qty=2,handed=True,orientation=Rot(),
        fasteners=HORN_FASTENERS|{'M2x5 self-tapper into servo ear':4},
        notes='Common hip/shoulder pitch fork and enclosing roll socket: print two of each hand. '
        'Roll centres 149 mm apart. Unbevelled common flat back on bed; accessible local hole-roof supports. '
        'Fit all four roll ear screws before the upper link.', printable='assumed')


BUILDERS=[build_thigh,build_upper_arm,build_shank,build_forearm,build_root_carrier,build_front_pad]
