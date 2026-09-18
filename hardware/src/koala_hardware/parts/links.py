# SPDX-License-Identifier: CERN-OHL-S-2.0
"""DEC-43 integral limbs with DEC-41 root joints. Native X = lateral; +Z down link."""
from functools import lru_cache
from math import cos, sin, radians
from build123d import Pos, Rot, Plane, Sphere, Cylinder, Align, RectangleRounded, extrude, Polygon, Cone, RegularPolygon, loft, Circle, fillet, Axis, mirror, GeomType, Vertex
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
    return rear_thigh(length)


def knee_socket_frame(length,hip=False):
    """Clock the rear case without changing the lateral knee shaft or centre."""
    return Pos(0,0,length)*Rot(X=P.THIGH_KNEE_CLOCK if hip else 0)*AXIS


def _root_fillet(part,selector,radius,count,label):
    edges=[e for e in part.edges() if e.geom_type==GeomType.LINE and selector(e)]
    if len(edges)!=count: raise ValueError(f'{label}: expected {count} edges, got {len(edges)}')
    return fillet(edges,radius)


@lru_cache
def rear_thigh(length):
    """Stepped roll yoke and sideways knee socket; joint centres retained."""
    clip=P.THIGH_PAD_TAIL_Z
    sx=P.SOCKET_CASE_X/2+P.SOCKET_CLEAR+P.SOCKET_WALL+P.THIGH_CHEEK_CLEAR
    t=P.SOCKET_PAD_T; a=P.SOCKET_ARM_HALF_W
    # New structure starts beyond the entire horn region; adding cheeks must
    # never fill the four lower bores/head recesses again.
    part=(Rot(Z=-90)*(fork('drive')+fork('idler')))&S._box(-30,30,-40,40,-P.SOCKET_PLATE_R-1,clip)
    bottom=length-(P.SOCKET_CASE_Y/2+P.SOCKET_CLEAR+2)
    bridge=P.THIGH_BRIDGE_START; back=P.SOCKET_AXIS_Z+P.SOCKET_SHELF
    for sign in (-1,1):
        cheek=S._box(-a,a,min(sign*sx,sign*(sx+t)),max(sign*sx,sign*(sx+t)),P.THIGH_JOIN_START,bottom)
        pad_face=P.SOCKET_DRIVE_FACE if sign<0 else -P.SOCKET_IDLER_FACE
        join=S._box(-a,a,min(sign*pad_face,sign*(sx+t)),max(sign*pad_face,sign*(sx+t)),P.THIGH_JOIN_START,clip)
        part+=cheek+join
    part+=S._box(-a,a,-sx-t,back,bridge,bottom)
    part+=knee_socket_frame(length,True)*S.saddle()
    for z,ys in [(clip,(-sx,sx)),(bridge,(-sx,sx)),(bridge,(sx+t,))]:
        part=_root_fillet(part,lambda e:abs(e.length-2*a)<1e-5 and abs(e.center().Z-z)<1e-5
                          and any(abs(e.center().Y-y)<1e-5 for y in ys),
                          P.REAR_FORK_ROOT_R,len(ys),'thigh yoke root')
    part=_root_fillet(part,lambda e:abs(abs(e.center().X)-a)<1e-5 and abs(e.center().Z-bottom)<1e-5
                      and abs(e.length-(P.SOCKET_DEPTH+P.SOCKET_SHELF))<1e-5,
                      P.SOCKET_WALL,2,'thigh knee-socket roots')
    # The 2 mm side return limits this lip radius, as on the hip carrier.
    lip=P.SOCKET_AXIS_Z-P.SOCKET_DEPTH
    part=_root_fillet(part,lambda e:abs(e.center().Y-lip)<1e-5 and abs(e.center().Z-bottom)<1e-5
                      and abs(e.center().X)<1e-5,P.HIP_SOCKET_LIP_R,1,'thigh socket lip')
    for y in (-P.SOCKET_DRIVE_FACE-t,-P.SOCKET_IDLER_FACE+t):
        part=_root_fillet(part,lambda e:abs(e.center().Y-y)<1e-5 and abs(e.center().Z-P.THIGH_JOIN_START)<1e-5
                          and abs(e.length-2*a)<1e-5,P.THIGH_PAD_RETURN_R,1,'thigh outer pad return')
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
    return motor_shank(length)


@lru_cache
def motor_shank(length):
    """Open knee fork, filleted spine, 37D face and axial body support."""
    face=motor_face(False); t=P.MOTOR_MOUNT_T
    inner=face-P.MOTOR_SUPPORT_OFFSET
    a=P.SOCKET_ARM_HALF_W; start=P.SHANK_BRIDGE_START; end=P.SHANK_BRIDGE_END
    # Crop generic flared tails before extending the straight fork necks.
    part=(fork('drive')+fork('idler'))&S._box(-30,30,-30,30,-P.SOCKET_PLATE_R-1,20)
    for lo,hi in [(P.SOCKET_IDLER_FACE-P.SOCKET_PAD_T,P.SOCKET_IDLER_FACE),
                  (P.SOCKET_DRIVE_FACE,P.SOCKET_DRIVE_FACE+P.SOCKET_PAD_T)]:
        part+=S._box(lo,hi,-a,a,20,end)
    part+=S._box(P.SOCKET_IDLER_FACE-P.SOCKET_PAD_T,max(face+t,P.SOCKET_DRIVE_FACE+P.SOCKET_PAD_T),-a,a,start,end)
    x0=inner-P.MOTOR_SUPPORT_T; x1=face+t
    top=length-P.MOTOR_DIA/2-1
    part+=S._box(x0,x1,-a,a,start,top)
    part+=S._x_hole(face,face+t,0,length,2*P.MOTOR_MOUNT_R)
    part+=S._x_hole(inner-P.MOTOR_SUPPORT_T,inner,0,length,2*P.MOTOR_MOUNT_R)
    # Fillet structural unions before cutting the insertion bore and screw
    # patterns, so added root material cannot obstruct those interfaces.
    meet=length-(P.MOTOR_MOUNT_R**2-a*a)**.5
    for y in (-a,a):
        part=_root_fillet(part,lambda e:abs(e.length-t)<1e-5 and abs(e.center().Y-y)<1e-5
                          and abs(e.center().Z-meet)<1e-5,P.REAR_MOTOR_ROOT_R,2,'motor ring/spine roots')
    for z,xs,r in [(start,(P.SOCKET_IDLER_FACE,P.SOCKET_DRIVE_FACE),P.REAR_FORK_ROOT_R),
                   (end,(x0,),P.REAR_MOTOR_ROOT_R),(top,(face,inner),P.REAR_MOTOR_ROOT_R)]:
        part=_root_fillet(part,lambda e:abs(e.length-2*a)<1e-5 and abs(e.center().Z-z)<1e-5
                          and any(abs(e.center().X-x)<1e-5 for x in xs),r,len(xs),'shank root')
    part-=S._x_hole(inner-P.MOTOR_SUPPORT_T-1,face,0,length,
                    P.MOTOR_DIA+2*P.CLEAR_POCKET)
    part-=S._x_hole(face-1,face+t+1,0,length,P.MOTOR_FACE_BOSS_DIA+1)
    for i in range(P.MOTOR_FACE_SCREWS):
        a=radians(i*60+30)
        part-=S._x_hole(face-1,face+t+1,P.MOTOR_BCD/2*cos(a),
                        length+P.MOTOR_BCD/2*sin(a),P.CLEAR_HOLE_M3)
    part=_root_fillet(part,lambda e:abs(e.center().X-(P.SOCKET_DRIVE_FACE+P.SOCKET_PAD_T))<1e-5
                      and abs(e.center().Z-start)<1e-5 and abs(e.length-2*P.SOCKET_ARM_HALF_W)<1e-5,
                      P.SHANK_OUTER_STEP_R,1,'shank outer fork step')
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
    rear: DEC-55/56 hip carrier. Fork-width block below A's nose, filleted
    structural joins and bevelled inner block edges. B stands Bottom-down;
    the block and socket floor retain one flat build face."""
    if front:
        axis_y=P.BODY_SHOULDER_WIDTH_MM/2
        edge=axis_y-P.SOCKET_CASE_Y/2-1.5
        floor=-P.SOCKET_AXIS_Z-P.SOCKET_SHELF
        inner=P.ROOT_PITCH_Y+P.SOCKET_IDLER_FACE-P.SOCKET_PAD_T
        return (pitch_fork_frame()*clevis()+
                S._box(-8,8,inner,edge,floor,-25)+
                roll_socket_frame(axis_y,True)*S.saddle())
    return hip_carrier()


@lru_cache
def hip_carrier():
    """DEC-56 refinement of the rear carrier, keeping both servo interfaces."""
    w=P.HIP_BLOCK_HALF_W
    top=P.SOCKET_AXIS_Z-P.SOCKET_DEPTH  # flush with the roll socket wall ends
    floor=P.SOCKET_AXIS_Z+P.SOCKET_SHELF
    inner=P.ROOT_PITCH_Y+P.SOCKET_IDLER_FACE-P.SOCKET_PAD_T
    socket_y=P.ROOT_ROLL_Y-P.SOCKET_CASE_Y/2-P.SOCKET_CLEAR-2.0
    roots=(P.ROOT_PITCH_Y+P.SOCKET_IDLER_FACE,P.ROOT_PITCH_Y+P.SOCKET_DRIVE_FACE)
    # The generic fork tails flare below this junction. Crop them before
    # adding the narrower block, so buried tails cannot protrude through it.
    forks=mirror(pitch_fork_frame()*(fork('drive')+fork('idler')),Plane.XY)
    r=P.SOCKET_PLATE_R+1
    forks &= S._box(-r,r,inner-1,socket_y+1,-r,top)
    part=(forks+S._box(-w,w,inner,socket_y+1,top,floor)+
          roll_socket_frame(P.ROOT_ROLL_Y)*S.saddle())
    # Fillet the assembled structural joins, selected by their datums rather
    # than OCC edge numbers. Mating pocket corners remain the accepted saddle.
    edges=[e for e in part.edges() if e.geom_type==GeomType.LINE
           and abs(e.center().Z-top)<1e-5 and abs(e.length-2*w)<1e-5
           and any(abs(e.center().Y-y)<1e-5 for y in roots)]
    if len(edges)!=2: raise ValueError('Hip carrier: expected two inner fork roots')
    part=fillet(edges,P.HIP_FORK_ROOT_R)
    edges=[e for e in part.edges() if e.geom_type==GeomType.LINE
           and abs(abs(e.center().X)-w)<1e-5 and abs(e.center().Y-socket_y)<1e-5
           and abs(e.length-(floor-top))<1e-5]
    if len(edges)!=2: raise ValueError('Hip carrier: expected two block/socket roots')
    part=fillet(edges,P.HIP_SOCKET_ROOT_R)
    edges=[e for e in part.edges() if e.geom_type==GeomType.LINE
           and abs(e.center().X)<1e-5 and abs(e.center().Y-socket_y)<1e-5
           and abs(e.center().Z-top)<1e-5]
    if len(edges)!=1: raise ValueError('Hip carrier: expected the outer fork/socket lip')
    part=fillet(edges,P.HIP_SOCKET_LIP_R)
    # Explicit tapered bevels stop at the fillet feet. A tangent-chain
    # chamfer would continue up the forks and cut the horn-pad edges.
    b=P.HIP_EDGE_BEVEL
    start,end=roots[0]+P.HIP_FORK_ROOT_R,roots[1]-P.HIP_FORK_ROOT_R
    if end-start<=2*b or not 0<b<w: raise ValueError('Hip carrier: bevels exceed the clear bridge')
    profile=Plane.XZ*Polygon((w-b,top),(w,top+b),(w,top),align=None)
    bevel=loft([Vertex(w,start,top),Pos(0,start+b,0)*profile,
                Pos(0,end-b,0)*profile,Vertex(w,end,top)],ruled=True)
    return part-bevel-mirror(bevel,Plane.YZ)


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
    notes=(f'One {length:g} mm thigh: stepped roll yoke with R6.3 roots and sideways knee socket. '
           'Orientation to review; no slice yet.' if hip else
           f'One {length:g} mm link: roll-axis horn forks, bridge, spine and perpendicular knee/elbow saddle. '
           'Outer horn pad on bed; remove supports from inner fork and saddle. No structural seam bolts.')
    return spec(name,upper_link(length,hip),handed=True,orientation=Rot(X=90),
        fasteners=HORN_FASTENERS|{'M2x5 self-tapper into servo ear':4},
        notes=notes, printable='unknown' if hip else 'assumed')


def lower_spec(name,length,front):
    return spec(name,lower_link(length,front),handed=True,
        fasteners=HORN_FASTENERS|{'M3x8 motor-face screw (depth to verify)':6},
        notes=f'One {length:g} mm link: extended open knee fork, R6.3 fork roots, R5 motor-support roots. '+
        'Slide motor from inboard; install face screws before hub and wheel. Remove support from body bore. No slice of this revision.', printable='unknown')


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
        notes='DEC-55/56 hip carrier: fork-width 16 mm block, tapered 2 mm inner-edge bevels, '
        'R6.3 fork-root and R5 socket-root fillets, R1.5 at the narrow socket lip. '
        'Roll socket alongside with the servo Bottom down. '
        f'Roll centres {2*P.ROOT_ROLL_Y:.1f} mm apart. Flat back (block and socket floor) on the bed, forks rising; '
        'accessible local hole-roof supports. Fit all four roll ear screws before the thigh.', printable='unknown')


BUILDERS=[build_thigh,build_upper_arm,build_shank,build_forearm,build_root_carrier,build_hip_carrier,build_front_pad]
