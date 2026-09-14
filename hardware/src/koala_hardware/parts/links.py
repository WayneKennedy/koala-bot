# SPDX-License-Identifier: CERN-OHL-S-2.0
"""DEC-43 integral limbs with DEC-41 root joints. Native X = lateral; +Z down link."""
from functools import lru_cache
from math import cos, sin, radians
from build123d import Pos, Rot, Plane, Sphere, Cylinder, Align, RectangleRounded, extrude, Polygon, Cone, RegularPolygon, loft, Circle, fillet, Axis, mirror
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
def upper_link(length,hip=False):
    bottom=length-P.SOCKET_AXIS_Z
    c=P.LINK_SPINE_HALF
    if not hip:
        spine=Pos(0,0,P.LINK_BRIDGE_START)*extrude(RectangleRounded(2*c,2*c,3),amount=bottom-P.LINK_BRIDGE_START)
        part=Rot(Z=-90)*clevis()+spine
        # Tapered root spreads load into the socket floor; no abrupt thin plank.
        start=max(P.LINK_BRIDGE_END,bottom-12)
        part+=loft([Pos(0,0,start)*RectangleRounded(16,16,3),
                    Pos(0,0,bottom)*RectangleRounded(36,24,3)])
        part+=Pos(0,0,bottom)*S.saddle()
        return part
    # DEC-55 thigh: B stands Bottom-down in the hip carrier, so the forks cannot
    # pass its nose. Pads grip the horn and idler, short tails stop above B's
    # socket walls, cheeks step outboard of the walls and run down to a slab that
    # passes under the socket floor and is the knee socket's shelf.
    clip=P.HIP_FORK_CLIP_Z; sx=P.SOCKET_CASE_X/2+P.SOCKET_CLEAR+P.SOCKET_WALL+P.HIP_FORK_CLEAR   # 23.45 along the roll axis
    t=P.SOCKET_PAD_T; a=P.SOCKET_ARM_HALF_W
    pads=(Rot(Z=-90)*clevis())&S._box(-30,30,-30,30,-P.SOCKET_PLATE_R-1,clip)
    part=pads
    slab_top=P.SOCKET_AXIS_Z+P.SOCKET_SHELF+2.0        # 42.1: 2 mm under B's socket floor
    for sign in (-1,1):
        cheek=S._box(-a,a,min(sign*sx,sign*(sx+t)),max(sign*sx,sign*(sx+t)),clip-10,bottom)
        pad_face=P.SOCKET_DRIVE_FACE if sign<0 else -P.SOCKET_IDLER_FACE   # pad inner faces after Rot(Z=-90): drive at -y, idler at +y
        join=S._box(-a,a,min(sign*pad_face,sign*(sx+t)),max(sign*pad_face,sign*(sx+t)),clip-10,clip)
        part+=cheek+join
    part+=S._box(-a,a,-(sx+t),sx+t,slab_top,bottom)
    x,y=S._socket_bounds(); y+=2.0
    part+=S._box(-(x+P.SOCKET_WALL),x+P.SOCKET_WALL,-y,y,slab_top,bottom)   # slab fills to the knee socket outline
    part+=Pos(0,0,bottom)*S.saddle()
    return part


def motor_face(front=False):
    root_y=P.BODY_SHOULDER_WIDTH_MM/2 if front else rear_axis_y()
    return P.BODY_TRACK_TARGET_MM/2-P.WHEEL_W/2-P.HUB_STACK-root_y


def rear_axis_y():
    return P.ROOT_ROLL_Y   # DEC-55 hip roll centre; the front keeps BODY_SHOULDER_WIDTH_MM/2 until DEC-54's chain is drawn


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


def roll_socket_frame(axis_y,front=False):
    if front:
        return Pos(0,axis_y,0)*AXIS                      # DEC-49 front: B nose down, socket on the torso side
    # DEC-55 hip: B Bottom-down in a socket below the pitch axis, nose toward the torso.
    return Plane(origin=(0,axis_y,P.SOCKET_AXIS_Z),x_dir=(1,0,0),z_dir=(0,0,-1)).location


@lru_cache
def carrier(front=False):
    """Root carrier: pitch-horn clevis to roll-servo socket.

    front: the DEC-49 shoulder carrier, unchanged until DEC-54's chain replaces it.
    rear: DEC-55 hip carrier. Clevis bridge under A's nose, one block from the fork
    tails to B's socket, B Bottom-down beside A's drive pad, flat back at the
    bottom. Nothing on the torso side of the pitch axis, so the sweep clears
    the root module and A at every pitch the poses use."""
    if front:
        axis_y=P.BODY_SHOULDER_WIDTH_MM/2
        edge=axis_y-P.SOCKET_CASE_Y/2-1.5
        floor=-P.SOCKET_AXIS_Z-P.SOCKET_SHELF
        inner=P.ROOT_PITCH_Y+P.SOCKET_IDLER_FACE-P.SOCKET_PAD_T
        return (pitch_fork_frame()*clevis()+
                S._box(-8,8,inner,edge,floor,-25)+
                roll_socket_frame(axis_y,True)*S.saddle())
    axis_y=P.ROOT_ROLL_Y; w=P.HIP_BLOCK_HALF_W
    floor=P.SOCKET_AXIS_Z+P.SOCKET_SHELF
    inner=P.ROOT_PITCH_Y+P.SOCKET_IDLER_FACE-P.SOCKET_PAD_T
    edge=axis_y-P.SOCKET_CASE_Y/2-P.SOCKET_CLEAR-2.0+1.0
    clevis_nose=mirror(pitch_fork_frame()*clevis(),Plane.XY)
    return (clevis_nose+S._box(-w,w,inner,edge,P.LINK_BRIDGE_START,floor)+
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


def upper_spec(name,length,hip=False):
    notes=(f'One {length:g} mm thigh (DEC-55): horn/idler pads, short tails, cheeks outboard of the roll socket, slab into the knee shelf. '
           'Orientation to review; no slice yet.' if hip else
           f'One {length:g} mm link: roll-axis horn forks, bridge, spine and perpendicular knee/elbow saddle. '
           'Outer horn pad on bed; remove supports from inner fork and saddle. No structural seam bolts.')
    return spec(name,upper_link(length,hip),handed=True,orientation=Rot(X=90),
        fasteners=HORN_FASTENERS|{'M2x5 self-tapper into servo ear':4},
        notes=notes, printable='unknown' if hip else 'assumed')


def lower_spec(name,length,front):
    return spec(name,lower_link(length,front),handed=True,
        fasteners=HORN_FASTENERS|{'M3x8 motor-face screw (depth to verify)':6},
        notes=f'One {length:g} mm link: both forks and integrated 37D face/body support. '+
        'Slide motor from inboard; install face screws before hub and wheel. Remove support from body bore.', printable='assumed')


def build_thigh(): return upper_spec('thigh',P.BODY_THIGH_MM,hip=True)
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
    return spec('shoulder_carrier',carrier(True),qty=1,handed=True,orientation=Rot(),
        fasteners=HORN_FASTENERS|{'M2x5 self-tapper into servo ear':4},
        notes='DEC-49 shoulder carrier, retained until the DEC-54 roll-first shoulder chain replaces it. '
        'Roll centres 149 mm apart. Flat back on bed; accessible local hole-roof supports.', printable='assumed')


def build_hip_carrier():
    return spec('hip_carrier',carrier(False),qty=1,handed=True,orientation=Rot(X=180),
        fasteners=HORN_FASTENERS|{'M2x5 self-tapper into servo ear':4},
        notes='DEC-55 hip carrier: clevis on the pitch horn, block, roll socket alongside with the servo Bottom down. '
        f'Roll centres {2*P.ROOT_ROLL_Y:.1f} mm apart. Flat back (block and socket floor) on the bed, forks rising; '
        'accessible local hole-roof supports. Fit all four roll ear screws before the thigh.', printable='unknown')


BUILDERS=[build_thigh,build_upper_arm,build_shank,build_forearm,build_root_carrier,build_hip_carrier,build_front_pad]
