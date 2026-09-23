# SPDX-License-Identifier: CERN-OHL-S-2.0
"""DEC-43 integral limbs with DEC-41 root joints. Native X = lateral; +Z down link."""
from functools import lru_cache
from math import cos, sin, radians
import warnings
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
    return rear_thigh_rounded(length)


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


# --- Thigh print-form options under review (2026-09-19, revision log). Not used by the main assembly. ---
def _thigh_dims(length):
    ret=P.SOCKET_CASE_Y/2+P.SOCKET_CLEAR+2
    return dict(a=P.SOCKET_ARM_HALF_W,t=P.SOCKET_PAD_T,
                sx=P.SOCKET_CASE_X/2+P.SOCKET_CLEAR+P.SOCKET_WALL+P.THIGH_CHEEK_CLEAR,
                bottom=length-ret,end=length+ret,inner=length+ret-2,
                back=P.SOCKET_AXIS_Z+P.SOCKET_SHELF,wall=P.SOCKET_AXIS_Z-P.SOCKET_DEPTH)


def _edge_x(y,z,a):
    """Selector for the union edge along X at (y,z), length 2a."""
    return lambda e:abs(e.length-2*a)<1e-5 and abs(e.center().Y-y)<1e-5 and abs(e.center().Z-z)<1e-5


@lru_cache
def rear_thigh_frame(length):
    """Option 1: the DEC-58 thigh with its knee end closed on the drive-pad side.

    A foot runs from the bridge to the socket's return plane and a bar runs along
    that plane to the cup wall, so the part stands on the knee socket to print with
    both cheeks and pads vertical. Servo C enters sideways (X) at its 17 mm
    pre-insertion offset, then slides into the pocket. Fillet after union.
    """
    d=_thigh_dims(length);a=d['a'];outer=-d['sx']-d['t'];foot_in=outer+P.THIGH_FOOT_T
    part=rear_thigh(length)
    part+=S._box(-a,a,outer,foot_in,d['bottom'],d['end'])
    part+=S._box(-a,a,foot_in,d['wall'],d['inner']+P.THIGH_BAR_CLEAR,d['end'])
    part=_root_fillet(part,_edge_x(foot_in,d['bottom'],a),P.THIGH_FOOT_T,1,'frame foot root')
    part=_root_fillet(part,_edge_x(foot_in,d['inner']+P.THIGH_BAR_CLEAR,a),1.2,1,'frame bar root')
    return part


def _slot(y_or_z_center,axis,x=0.0):
    """Captive M3 nut slot entered from the bridge's window face (Z=THIGH_BRIDGE_START)."""
    from build123d import RegularPolygon
    r=(P.NUT_M3_AF+0.2)/2/cos(radians(30))
    if axis=='Z':   # nut axis along Z at (x, y): hex in XY, slot rises from the window face
        return Pos(x,y_or_z_center,P.THIGH_BRIDGE_START-1)*extrude(RegularPolygon(r,6,rotation=0),amount=P.NUT_M3_T+1.2)
    # nut axis along Y at (x, z): hex in XZ, slot from the window face up to the screw axis
    y=P.THIGH_END_NUT_Y
    hexa=Pos(x,y,y_or_z_center)*Rot(X=90)*extrude(RegularPolygon(r,6,rotation=0),amount=P.NUT_M3_T,both=True)
    drop=S._box(x-P.NUT_M3_AF/2-0.1,x+P.NUT_M3_AF/2+0.1,y-P.NUT_M3_T,y+P.NUT_M3_T,P.THIGH_BRIDGE_START-1,y_or_z_center)
    return hexa+drop


@lru_cache
def rear_thigh_split(length):
    """Option 2: the DEC-58 thigh as two prints, inside the DEC-58 envelope plus a 5 mm lip.

    Body: cup, bridge (ending at the window face), idler pad and the idler-side
    cheek thickened out to the cup-floor plane, so the body lies on that plane to
    print. Cheek piece: the whole drive-side cheek with its pad and join, plus a
    lip over the bridge's knee-end face. It mates on an L: cheek inner face
    against the bridge end, lip on the bridge's outer face. Two M3 into captive
    nuts entered from the window face: one along Z through the lip, one along Y
    through the cheek (head counterbored flush). Servo C is fitted before the
    cheek piece. Returns (body, cheek).
    """
    from build123d import Cylinder,Align
    d=_thigh_dims(length);a=d['a'];outer=-d['sx']-d['t'];inner=-d['sx']
    full=rear_thigh(length)
    region=S._box(-30,30,-60,inner,-40,120)+S._box(-30,30,-60,-P.SOCKET_DRIVE_FACE+0.4,-40,20)
    cheek=full&region;body=full-region
    body+=S._box(-a,a,d['sx']+d['t'],d['back'],P.THIGH_JOIN_START,d['bottom'])
    cheek+=S._box(-a,a,outer,P.THIGH_LIP_END_Y,d['bottom'],d['bottom']+P.THIGH_LIP_T)
    zs=P.THIGH_END_SCREW_Z;ys=P.THIGH_LIP_SCREW_Y
    lip_hole=Pos(0,ys,P.THIGH_BRIDGE_START-1)*Cylinder(P.CLEAR_HOLE_M3/2,d['bottom']+P.THIGH_LIP_T-P.THIGH_BRIDGE_START+2,align=(Align.CENTER,Align.CENTER,Align.MIN))
    end_hole=Pos(0,outer-1,zs)*Rot(X=-90)*Cylinder(P.CLEAR_HOLE_M3/2,(P.THIGH_END_NUT_Y-outer)+P.NUT_M3_T+2,align=(Align.CENTER,Align.CENTER,Align.MIN))
    bore=Pos(0,outer-1,zs)*Rot(X=-90)*Cylinder(P.CAP_M3_DIA/2+0.3,P.CAP_M3_H+1,align=(Align.CENTER,Align.CENTER,Align.MIN))
    cheek-=lip_hole+end_hole+bore;body-=lip_hole+end_hole
    body-=_slot(ys,'Z');body-=_slot(zs,'Y')
    return body,cheek


@lru_cache
def thigh_lap_fixings():
    """Reference solids for option 2's two screws and captive nuts."""
    from build123d import Cylinder,Align,RegularPolygon
    d=_thigh_dims(P.BODY_THIGH_MM);outer=-d['sx']-d['t'];top=d['bottom']+P.THIGH_LIP_T
    ys=P.THIGH_LIP_SCREW_Y;zs=P.THIGH_END_SCREW_Z;yn=P.THIGH_END_NUT_Y
    s=Pos(0,ys,P.THIGH_BRIDGE_START)*Cylinder(1.5,top-P.THIGH_BRIDGE_START,align=(Align.CENTER,Align.CENTER,Align.MIN))
    s+=Pos(0,ys,top)*Cylinder(2.75,2.5,align=(Align.CENTER,Align.CENTER,Align.MIN))
    s+=Pos(0,ys,P.THIGH_BRIDGE_START)*extrude(RegularPolygon(3.175,6,rotation=0),amount=P.NUT_M3_T)
    s+=Pos(0,outer+P.CAP_M3_H,zs)*Rot(X=-90)*Cylinder(1.5,(yn+P.NUT_M3_T/2)-(outer+P.CAP_M3_H),align=(Align.CENTER,Align.CENTER,Align.MIN))
    s+=Pos(0,outer,zs)*Rot(X=-90)*Cylinder(2.75,P.CAP_M3_H,align=(Align.CENTER,Align.CENTER,Align.MIN))
    s+=Pos(0,yn,zs)*Rot(X=90)*extrude(RegularPolygon(3.175,6,rotation=0),amount=P.NUT_M3_T/2,both=True)
    return s


def round_convex_edges(part,radius,min_len=8.0,exclude=lambda c:False):
    """Round selected convex corners without restoring earlier sharp geometry.

    Remember the original straight segments, then reselect their surviving
    portions on the current solid before every attempt. A neighbouring fillet
    may shorten or consume a segment. Never reuse its old edge/topo_parent.
    Rejected groups are bisected; rejected single edges produce a warning.
    """
    edge_faces={}
    for f in part.faces():
        for e in f.edges():
            if e.geom_type==GeomType.LINE:
                edge_faces.setdefault(e,[]).append(f)
    chosen=[]
    for e in part.edges():
        if e.geom_type!=GeomType.LINE or e.length<min_len:continue
        c=e.center()
        if exclude(c):continue
        fs=edge_faces.get(e,[])
        if len(fs)!=2:continue
        n1=fs[0].normal_at(c);n2=fs[1].normal_at(c)
        if abs(n1.dot(n2))>0.2 or part.is_inside(c+(n1+n2)*0.5):continue
        chosen.append((e.position_at(0),e.position_at(1)))

    def reselect(segments):
        edges=[]
        for e in part.edges():
            if e.geom_type!=GeomType.LINE:continue
            ends=(e.position_at(0),e.position_at(1))
            for start,end in segments:
                axis=(end-start).normalized();length=(end-start).length
                if any((p-start).cross(axis).length>1e-5 for p in ends):continue
                along=sorted((p-start).dot(axis) for p in ends)
                if min(along[1],length)-max(along[0],0)>1e-5:
                    edges.append(e);break
        return edges

    todo=[chosen];failed=[]
    while todo:
        group=todo.pop()
        edges=reselect(group)
        if not edges:continue
        try:
            rounded=part.fillet(radius,edges)
            if len(rounded.solids())!=len(part.solids()):
                raise ValueError('rounding changed the number of solids')
            part=rounded
        except ValueError:
            remaining=[(e.position_at(0),e.position_at(1)) for e in edges]
            if len(remaining)==1:failed.extend(remaining)
            else:todo+= [remaining[:len(remaining)//2],remaining[len(remaining)//2:]]
    sharp=reselect(failed) if failed else []
    if sharp:
        centres=[tuple(round(v,3) for v in e.center()) for e in sharp]
        warnings.warn(f'round_convex_edges: {len(sharp)} edge(s) left sharp at R{radius}; '
                      f'centres={centres}',RuntimeWarning,stacklevel=2)
    return part


@lru_cache
def rear_thigh_rounded(length):
    """Production thigh since 2026-09-19 (owner): the tapered one-piece form
    (`rear_thigh_flat`) with the rounding pass — R2 on the yoke, bridge and taper,
    R1.5 on the knee cup's outer edges; fork pads, joins and every interface
    face untouched. Printed on the cup-floor plane with tree support."""
    d=_thigh_dims(length)
    cup=lambda c:c.Z>d['bottom']-0.1 and c.Y>d['wall']-0.1          # the knee cup, entry plane included
    entry=lambda c:abs(c.Y-d['wall'])<0.1                            # pocket entry lip: interface, stays sharp
    cup_outer=lambda c:cup(c) and not entry(c) and (abs(c.X)>22.0 or c.Y>d['back']-0.1)   # wall and floor outer faces only
    part=round_convex_edges(rear_thigh_flat(length),2.0,exclude=lambda c:c.Z<14 or cup(c))
    return round_convex_edges(part,1.5,exclude=lambda c:not cup_outer(c))


@lru_cache
def rear_thigh_flat(length):
    """Option 3 (owner, 2026-09-19): one print of the DEC-58 thigh, lying on the cup-floor plane.

    The idler-side cheek is thickened out to the cup-floor plane so cup floor and
    cheek share the bed. The step from that cheek to the idler pad is replaced by
    one flat taper (the owner's red line): tangent to the pad's outer top edge and
    to the join's outer face, reaching the cheek's outer face at THIGH_CHAMFER_Z.
    The drive-side cheek and both pads stay as DEC-58; the print relies on tree
    support under them.
    """
    from build123d import Polygon
    d=_thigh_dims(length);a=d['a']
    part=rear_thigh(length)+S._box(-a,a,d['sx']+d['t'],d['back'],P.THIGH_JOIN_START,d['bottom'])
    y0=-P.SOCKET_IDLER_FACE+P.SOCKET_PAD_T+0.1;z0=-P.SOCKET_PLATE_R-1     # just outside the pad's outer top edge
    y1=d['back'];z1=P.THIGH_CHAMFER_Z
    cut=extrude(Plane.YZ*Polygon((y0,z0),(y1,z1),(y1+60,z1),(y1+60,z0-60),(y0,z0-60)),amount=30,both=True)
    return part-cut


def option_thigh_flat():
    return spec('thigh_flat',rear_thigh_flat(P.BODY_THIGH_MM),handed=True,orientation=Rot(X=-90),
        fasteners=HORN_FASTENERS|{'M2x5 self-tapper into servo ear':4},
        notes='Option 3 (owner, 2026-09-19): DEC-58 thigh in one print with the idler-side cheek thickened to the '
        'cup-floor plane and a single flat taper from that cheek to the idler pad. Prints on the cup-floor plane with '
        'tree (organic) support under the drive-side cheek and both pads. Straight servo insertion unchanged. Unprinted.')


def option_shank_flush():
    return spec('shank_flush',lower_link(P.BODY_SHANK_MM,False,P.SHANK_MOTOR_INSET,rounded=False),handed=True,version=2,
        fasteners=HORN_FASTENERS|{'M3x8 motor-face screw (depth to verify)':6},
        notes=f'Shank option (owner, 2026-09-19): 37D moved inboard {P.SHANK_MOTOR_INSET:g} mm so the motor-mount face '
        'and the drive fork\'s outer face are one plane, the print face. Track and neutral motor gap narrow by '
        f'{2*P.SHANK_MOTOR_INSET:g} mm. Slide motor from inboard; face screws before hub and wheel. Unprinted.')


def option_thigh_frame():
    return spec('thigh_frame',rear_thigh_frame(P.BODY_THIGH_MM),handed=True,orientation=Rot(X=180),
        fasteners=HORN_FASTENERS|{'M2x5 self-tapper into servo ear':4},
        notes='Option 1 (2026-09-19 review), fitted on the LEFT leg: DEC-58 thigh with the knee end closed on the '
        'drive-pad side by a 4 mm foot and a 2 mm bar on the socket return plane. Prints standing on the knee socket: '
        'cheeks and pads vertical; one 45.9 mm span bridged over the empty case space. Servo C enters sideways at the '
        '17 mm pre-insertion offset, then slides into the pocket. Layers lie across the cheeks\' bending load. Unprinted.')


def option_thigh_split_body():
    body,_=rear_thigh_split(P.BODY_THIGH_MM)
    return spec('thigh_body',body,handed=True,orientation=Rot(X=-90),
        fasteners=HORN_FASTENERS|{'M2x5 self-tapper into servo ear':4,'M3 nut, captive in the bridge':2},
        notes='Option 2 body (2026-09-19 review), fitted on the RIGHT leg: cup, bridge to the window face, idler pad and '
        'the idler-side cheek thickened to the cup-floor plane. Prints on that plane; the idler pad needs one small '
        'external support block. Fit servo C, then bolt the cheek piece. Unprinted.')


def option_thigh_split_cheek():
    _,cheek=rear_thigh_split(P.BODY_THIGH_MM)
    return spec('thigh_cheek',cheek,handed=True,orientation=Rot(X=90),
        fasteners={'M3x16 pan, through the lip into the captive nut':1,'M3x10 pan, counterbored, through the cheek into the bridge end':1},
        notes='Option 2 cheek piece: the whole drive-side cheek with pad and join, plus a 5 mm lip over the bridge end. '
        'Mates on an L (bridge end face + lip); two M3 into captive nuts entered from the window face. Prints on its '
        'outer face; the drive pad needs one small support block under its free part (driver side). Fitted after '
        'servo C. Torque path through two screws and the L faces: unverified. Unprinted.')


def motor_face(front=False,inset=0.0):
    root_y=P.BODY_SHOULDER_WIDTH_MM/2 if front else rear_axis_y()
    return P.BODY_TRACK_TARGET_MM/2-P.WHEEL_W/2-P.HUB_STACK-root_y-inset


def rear_axis_y():
    return P.ROOT_ROLL_Y   # Rear B roll centre; front B spacing is independent.


@lru_cache
def lower_link(length,front=False,inset=0.0,rounded=True):
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
    part=motor_shank(length,inset)
    if not rounded:return part
    # Owner's rounding pass: R2 on the spine, bridge and fork necks; pads, motor face and ring untouched.
    return round_convex_edges(part,2.0,exclude=lambda c:c.Z<14 or c.Z>length-P.MOTOR_MOUNT_R-2)


@lru_cache
def motor_shank(length,inset=0.0):
    """Open knee fork, filleted spine, 37D face and axial body support.

    `inset` moves the motor inboard (owner's 2026-09-19 shank option): at
    SHANK_MOTOR_INSET the mount face and the drive fork's outer face are one plane.
    """
    face=motor_face(False,inset); t=P.MOTOR_MOUNT_T
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
    if face+t>P.SOCKET_DRIVE_FACE+P.SOCKET_PAD_T+1e-6:   # no step, no return, when the faces are flush
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


def spec(name,part,qty=1,orientation=None,fasteners=None,notes='',handed=False,material='PETG',printable='unknown',version=1):
    # `version` is the part's design version (part-versions.json); bump it whenever the geometry changes.
    verification=' Loaded assembly unverified.' if printable=='proven' else ' Physical fit/load unverified.'
    return dict(name=name,part=part,qty=qty,orientation=orientation or Rot(Y=90),version=version,
                handed=handed,fasteners=fasteners or {},supports=True,
                printable=printable,material=material,
                notes=notes+' Accessible local supports permitted; inspect layers.'+verification)


def upper_spec(name,length,hip=False):
    notes=(f'One {length:g} mm thigh v3 (2026-09-19): stepped roll yoke and sideways knee socket, idler-side cheek '
           'thickened to the cup-floor plane with one flat taper to the pad, convex edges rounded R2 (cup R1.5). Prints '
           'on the cup-floor plane with tree (organic) support under the drive-side cheek and pads. Corrected rounding '
           'preserves every successful fillet group. Current bed-only organic slice reviewed; physical support removal and fit remain unknown.' if hip else
           f'One {length:g} mm link: roll-axis horn forks, bridge, spine and perpendicular knee/elbow saddle. '
           'Outer horn pad on bed; remove supports from inner fork and saddle. No structural seam bolts.')
    return spec(name,upper_link(length,hip),handed=True,orientation=Rot(X=-90) if hip else Rot(X=90),
        fasteners=HORN_FASTENERS|{'M2x5 self-tapper into servo ear':4},
        notes=notes, printable='unknown' if hip else 'assumed', version=3 if hip else 1)


def lower_spec(name,length,front):
    return spec(name,lower_link(length,front),handed=True,
        fasteners=HORN_FASTENERS|{'M3x8 motor-face screw (depth to verify)':6},
        notes=f'One {length:g} mm link v2 (owner, 2026-09-19): extended open knee fork, R6.3 fork roots, R5 motor-support roots; '
        'motor-mount face flush with the drive fork (DEC-60 spacing), convex edges rounded R2. Prints on that outer face. '
        'Slide motor from inboard; install face screws before hub and wheel. Remove support from body bore. '
        'Assumed: owner-directed form and print face; the rounding pass is unreviewed. Bed-only organic v2 slices are recorded in OQ-22; physical fit and bore-roof quality remain unverified.', printable='assumed', version=2)


def build_thigh(): return upper_spec('thigh',P.BODY_THIGH_MM,hip=True)
def build_upper_arm(): return upper_spec('upper_arm',P.BODY_UPPER_ARM_MM)
def build_shank():
    return lower_spec('shank',P.BODY_SHANK_MM,False) | {'configurations':('wheeled',)}
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
        fasteners=HORN_FASTENERS|{'M3x20 TPU-pad screw':1,'M3 nut':1,'M3 plain washer':1},
        notes='One flat-section forearm; elbow fork and keyed TPU-pad seat. Broad native -Y face on bed. '
        'Insert captive M3 nut from side; fit pad and recessed M3x20 screw with washer. '
        'Local support under nut-slot roof and fork hole roofs is accessible from outside.', printable='assumed')


def build_front_pad():
    return spec('front_contact_pad',front_pad(),qty=2,orientation=Rot(),material='TPU',
        notes='Common rounded TPU ground contact: front forearm or interchangeable rear foot_shank. '
        'Truncated mating face on bed; tapered keyed cavity avoids a flat internal roof. '
        'No support intended; recessed screw/washer remains above contact surface. Traction/wear untested.', printable='assumed') | {'configuration_qty':{'walking':4,'wheeled':2}}

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
        'accessible local hole-roof supports. Fit all four roll ear screws before the thigh. '
        'Assumed: owner visual review of the rear-leg viewer, 2026-09-18 (revision log). Plate 2 bed-only slices are recorded; no physical result is recorded.', printable='assumed')


BUILDERS=[build_thigh,build_upper_arm,build_shank,build_forearm,build_root_carrier,build_hip_carrier,build_front_pad]
