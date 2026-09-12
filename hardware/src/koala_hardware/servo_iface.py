# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Koala four-ear saddle and integrated-fork interfaces, DEC-33/40.

Servo face words (docs/soarm-joint-pattern.md, Terminology): FRONT = drive-horn
face = +X; BACK = idler/connector face = -X; BOTTOM = the end the servo stands
on = Z 0; TOP = the end nearest the output axis = Z 45.23; SIDES = +-Y. The
saddle has a floor under the Bottom, a Front wall and a Back wall (the pair
34.9 apart away from the ear bosses), with enclosing Side returns and a rounded outer footprint. The clevis has a Front plate (drive horn) and a Back plate (idler).
Body mounts use the CASE datum; horns use the OUTPUT AXIS datum. These are
independent feature families (test-log 2026-09-02). Nominal printed-part
interfaces are adopted from SO-101; no pocket derives from a servo model.
"""
from functools import lru_cache
from build123d import Box, Cylinder, Part, Pos, Rot, Align, Axis, fillet, RectangleRounded, extrude, Polygon
from . import params as P

# Restart primitive frame: X = output axis, Y = case width, Z = case length.
# BODY features use rear face Z=0; HORN features use Z=SOCKET_AXIS_Z.
# These are independent datums (test-log 2026-09-02); never locate a lug from
# a horn hole.


def _box(x0, x1, y0, y1, z0, z1):
    return Pos(x0, y0, z0) * Box(x1-x0, y1-y0, z1-z0,
        align=(Align.MIN, Align.MIN, Align.MIN))


def _x_hole(x0, x1, y, z, diameter):
    return Pos(x0, y, z) * Rot(Y=90) * Cylinder(diameter/2, x1-x0,
        align=(Align.CENTER, Align.CENTER, Align.MIN))


def _socket_bounds():
    return (P.SOCKET_CASE_X/2 + P.SOCKET_CLEAR,
            P.SOCKET_CASE_Y/2 + P.SOCKET_CLEAR)


def ear_face(side):
    return P.SOCKET_SEAT_OFFSET + (1 if side == 'drive' else -1)*P.SOCKET_EAR_X/2


def ear_holes(part, side, ys):
    face = ear_face(side)
    z = P.SOCKET_LUG_DRIVE_Z if side == 'drive' else P.SOCKET_LUG_BACK_Z
    for y in ys:
        part -= _x_hole(-30, 30, y, z, P.SOCKET_M2_CLEAR)
        if side == 'drive':
            part -= _x_hole(face+P.SOCKET_M2_SEAT, 30, y, z, P.SOCKET_M2_HEAD)
        else:
            part -= _x_hole(-30, face-P.SOCKET_M2_SEAT, y, z, P.SOCKET_M2_HEAD)
    return part


@lru_cache
def saddle():
    """Enclosing four-ear pocket; slides onto the servo Bottom before assembly.

    Side returns retain the accepted Gauge_0 pocket. The open top remains
    below the connector bay. Drive/idler slots follow the unequal SO-101
    widths and starts; ear planes and screw datums are unchanged.
    """
    x, y = _socket_bounds()
    y += 2.0                 # material beyond each ear for the head pockets
    part = _box(-x-P.SOCKET_WALL, x+P.SOCKET_WALL, -y, y, -P.SOCKET_SHELF, 0)
    for side, sign in [('drive',1), ('idler',-1)]:
        a,b = (x,x+P.SOCKET_WALL) if sign == 1 else (-x-P.SOCKET_WALL,-x)
        wall = _box(a,b,-y,y, -P.SOCKET_SHELF,P.SOCKET_DEPTH)
        face = ear_face(side)
        for sy in (-1,1):
            edge=(P.SOCKET_DRIVE_SLOT_Y if side=='drive' else P.SOCKET_IDLER_SLOT_Y)/2
            ya,yb = (edge,y) if sy == 1 else (-y,-edge)
            lo,hi = (face,x+P.SOCKET_WALL) if sign == 1 else (-x-P.SOCKET_WALL,face)
            wall += _box(lo,hi,ya,yb,0,P.SOCKET_DEPTH)
        if side=='idler':
            # Upstream's wider Back recess starts above the low ear screws.
            # The continuous lower seat avoids the former bore/strip tangency.
            wall += _box(-x-P.SOCKET_WALL,face,-y,y,0,P.SOCKET_IDLER_SLOT_Z)
        # Cut each wall separately: a Front counterbore must not drill the Back seat.
        part += ear_holes(wall,side,(-P.SOCKET_LUG_Y,P.SOCKET_LUG_Y))
    # Enclosing Side returns: support the case instead of only the screws.
    # Keep the 24.7 mm pocket and both straight ear-driver approaches.
    for sign in (-1,1):
        a,b=(P.SOCKET_CASE_Y/2,y) if sign==1 else (-y,-P.SOCKET_CASE_Y/2)
        part += _box(-x,x,a,b,-P.SOCKET_SHELF,P.SOCKET_DEPTH)
    # Round the outside without changing the stepped contact surfaces.
    outside=Pos(0,0,-P.SOCKET_SHELF)*extrude(
        RectangleRounded(2*(x+P.SOCKET_WALL),2*y,2),
        amount=P.SOCKET_DEPTH+P.SOCKET_SHELF)
    part &= outside
    # Floor also needs the low Back screw's counterbore continuation.
    for side in ('drive','idler'):
        face=ear_face(side); z=P.SOCKET_LUG_DRIVE_Z if side=='drive' else P.SOCKET_LUG_BACK_Z
        for y in (-P.SOCKET_LUG_Y,P.SOCKET_LUG_Y):
            a,b=(face+P.SOCKET_M2_SEAT,30) if side=='drive' else (-30,face-P.SOCKET_M2_SEAT)
            part -= _x_hole(a,b,y,z,P.SOCKET_M2_HEAD)
    return part


@lru_cache
def clevis_plate(side: str):
    """Native XY plate, contact at Z=0; +Y runs along the driven link.

    Flat horn contact, 3.5 mm web, 2.8 mm head recesses. A 10.4 mm circular
    root clears the Back bay in every angular orientation; the four bolt pads
    fit within it. A narrower tail connects it to the integral bridge.
    """
    if side not in ('drive','idler'): raise ValueError(side)
    t=P.SOCKET_PAD_T
    part=Cylinder(P.SOCKET_PLATE_R,t,align=(Align.CENTER,Align.CENTER,Align.MIN))
    # Broad, tapered fork roots with rounded end corners, within a compact
    # envelope; keep the R10.4 nose for the measured connector corridor.
    tail=extrude(Polygon((-8,0),(8,0),(8,22),(10.4,28),(10.4,32),(-10.4,32),(-10.4,28),(-8,22),align=None),amount=t)
    tail=fillet(tail.edges().filter_by(Axis.Z),2)
    part+=tail
    for a in (-P.SERVO_DRIVE_SQ/2,P.SERVO_DRIVE_SQ/2):
        for b in (-P.SERVO_DRIVE_SQ/2,P.SERVO_DRIVE_SQ/2):
            part-=Pos(a,b,-1)*Cylinder(P.CLEAR_HOLE_M3/2,t+2,align=(Align.CENTER,Align.CENTER,Align.MIN))
            part-=Pos(a,b,P.SOCKET_PLATE_T)*Cylinder(P.SOCKET_HEAD_CLEAR/2,t+1,align=(Align.CENTER,Align.CENTER,Align.MIN))
    if side=='drive':
        part-=Cylinder(3.2/2,t+1,align=(Align.CENTER,Align.CENTER,Align.MIN))
        part-=Cylinder((P.HORN_SCREW_HEAD_DIA+.6)/2,P.HORN_SCREW_HEAD_H+.4,align=(Align.CENTER,Align.CENTER,Align.MIN))
    else:
        part-=Cylinder((P.SOCKET_BOSS_DIA+.6)/2,P.SOCKET_IDLER_BOSS_PROUD+.4,align=(Align.CENTER,Align.CENTER,Align.MIN))
    return part


def plate_location(side):
    from build123d import Plane
    if side=='drive':
        return Plane(origin=(P.SOCKET_DRIVE_FACE,0,P.SOCKET_AXIS_Z),x_dir=(0,1,0),z_dir=(1,0,0)).location
    if side=='idler':
        return Plane(origin=(P.SOCKET_IDLER_FACE,0,P.SOCKET_AXIS_Z),x_dir=(0,-1,0),z_dir=(-1,0,0)).location
    raise ValueError(side)


_ST3215_STEP = __import__('pathlib').Path(__file__).resolve().parents[2] / 'vendor' / 'st3215' / 'STS3215_c.step'
_ST3215_BOTTOM_X = 35.1117   # model frame: Bottom face at X=+35.11, Top at X=-10.11, axis at X=0
_ST3215_POCKET_SHIFT = 0.4   # model widest faces sit at Y -17.9 / +17.1: shift +0.4 centres the pocket


@lru_cache
def case_model() -> Part | None:
    """The bare STS3215 case from vendor/st3215/STS3215_c.step, in the socket frame.

    Model frame -> socket frame: model +Y (drive side) -> Front +X; model Z
    (Sides) -> -Y; model X (height, Bottom at +35.11) -> Z with the Bottom at
    Z=0. Only the three case solids ('Middle', 'Top', 'Bottom' in the file) are
    used; the file's horns, screws, connectors and label are dropped because
    its horn stack is 0.85 wider than the measured 36.4 (test-log 2026-09-08)
    and the koala horn stack comes from calipers instead. None if the file is
    absent, and socket_reference() falls back to the parametric profile.
    """
    if not _ST3215_STEP.exists():
        return None
    from build123d import import_step, Plane
    model = import_step(str(_ST3215_STEP))
    loc = Plane(origin=(_ST3215_POCKET_SHIFT, 0, _ST3215_BOTTOM_X),
                x_dir=(0, 0, -1), z_dir=(0, -1, 0)).location
    part = None
    for child in model.children:
        if child.label in ('Middle', 'Top', 'Bottom'):
            for s in child.solids():
                part = s if part is None else part + s
    part=loc*part
    # The imported Back centre projection is 1.2 mm proud; measured boss is
    # composed separately below. Clip only the boss cylinder outside its seat.
    seat_b=P.SOCKET_SEAT_OFFSET-P.SOCKET_HORN_SEAT_X/2
    part-=_x_hole(-40,seat_b,0,P.SOCKET_AXIS_Z,P.SOCKET_BOSS_DIA+.6)
    return part


def case_boxes():
    """Conservative case boxes, shared by BREP and viewer collision checks.

    Back heights are caliper based. Front pad width comes from SO-101's slot;
    its upper extent covers the supplied STEP's raised plane. Neither case
    envelope sets the accepted pocket or measured ear/horn datums.
    """
    y,off,L=P.SOCKET_CASE_Y/2,P.SOCKET_SEAT_OFFSET,P.SOCKET_CASE_L
    seat_f,seat_b=off+P.SOCKET_HORN_SEAT_X/2,off-P.SOCKET_HORN_SEAT_X/2
    ear_f,ear_b=off+P.SOCKET_EAR_X/2,off-P.SOCKET_EAR_X/2
    wide=P.SOCKET_CASE_X/2;za,zb=P.SOCKET_REGION_Z
    front=P.SOCKET_DRIVE_SLOT_Y/2;back=P.SOCKET_IDLER_SLOT_Y/2
    return [((ear_b,-y,0),(ear_f,y,zb)),
            ((seat_f,-front,0),(wide,front,P.SOCKET_DRIVE_PAD_TOP)),
            ((-wide,-back,za),(ear_b,back,zb)),
            ((seat_b,-y,zb),(seat_f,y,L))]


def _parametric_case() -> Part:
    """Fallback stepped profile with distinct Front and Back raised pads."""
    part=None
    for (x0,y0,z0),(x1,y1,z1) in case_boxes():
        box=_box(x0,x1,y0,y1,z0,z1)
        part=box if part is None else part+box
    return part


@lru_cache
def socket_reference():
    """Case (vendor STEP, or the parametric profile) plus the MEASURED horn stack.

    Pocket frame: X=0 is the pocket centre; the seat mid-plane sits
    SOCKET_SEAT_OFFSET toward the Front. The idler (3.1) plus the servo boss
    (0.7 proud) sit on the Back seat; the drive horn plus its pan-head centre
    screw sit on the Front seat (test-log 2026-09-08).
    """
    off = P.SOCKET_SEAT_OFFSET
    seat_f, seat_b = off + P.SOCKET_HORN_SEAT_X/2, off - P.SOCKET_HORN_SEAT_X/2
    part = case_model()
    if part is None:
        part = _parametric_case()
    z = P.SOCKET_AXIS_Z
    part += _x_hole(P.SOCKET_IDLER_FACE, seat_b, 0, z, P.SOCKET_HORN_DIA)           # idler
    part += _x_hole(P.SOCKET_IDLER_FACE - P.SOCKET_IDLER_BOSS_PROUD,
                    P.SOCKET_IDLER_FACE, 0, z, P.SOCKET_BOSS_DIA)                   # servo boss
    part += _x_hole(seat_f, P.SOCKET_DRIVE_FACE, 0, z, P.SOCKET_HORN_DIA)           # drive horn
    part += _x_hole(P.SOCKET_DRIVE_FACE, P.SOCKET_DRIVE_FACE + P.HORN_SCREW_HEAD_H,
                    0, z, P.HORN_SCREW_HEAD_DIA)                                     # its pan head
    return part


def socket_keepouts():
    """Back bay exits along -X; straight drivers are pre-clevis assembly checks."""
    result=[('case_and_horns',socket_reference())]
    for side in ('drive','idler'):
        face=ear_face(side); z=P.SOCKET_LUG_DRIVE_Z if side=='drive' else P.SOCKET_LUG_BACK_Z
        a,b=(face+P.SOCKET_M2_SEAT,face+35) if side=='drive' else (face-35,face-P.SOCKET_M2_SEAT)
        for y in (-P.SOCKET_LUG_Y,P.SOCKET_LUG_Y):
            result.append((side+'_lug_driver',_x_hole(a,b,y,z,P.SOCKET_M2_HEAD)))
    result.append(('cable',_box(-45,-P.SOCKET_CASE_X/2,-P.SOCKET_CABLE_W/2,P.SOCKET_CABLE_W/2,*P.SOCKET_BAY_Z)))
    return result


@lru_cache
def horn_head_envelopes():
    """Eight supplied square-fixing heads, plus four narrow Back washers.

    Output-axis frame, matching an integral link. Threads are not solid
    envelopes; engagement is accounted for separately in the fastening stack.
    """
    from build123d import Compound
    items=[]
    for side in ('drive','idler'):
        tf=Pos(0,0,-P.SOCKET_AXIS_Z)*plate_location(side)
        extra=P.HORN_IDLER_WASHER_T if side=='idler' else 0
        for x in (-P.SERVO_DRIVE_SQ/2,P.SERVO_DRIVE_SQ/2):
            for y in (-P.SERVO_DRIVE_SQ/2,P.SERVO_DRIVE_SQ/2):
                items.append(tf*Pos(x,y,P.SOCKET_PLATE_T+extra)*Cylinder(P.HORN_SCREW_HEAD_DIA/2,P.HORN_SCREW_HEAD_H,align=(Align.CENTER,Align.CENTER,Align.MIN)))
                if extra:items.append(tf*Pos(x,y,P.SOCKET_PLATE_T)*Cylinder(P.HORN_IDLER_WASHER_OD/2,extra,align=(Align.CENTER,Align.CENTER,Align.MIN)))
    return Compound(children=items)


@lru_cache
def ear_head_envelopes():
    """Four case-lug heads, case datum. Driver paths are separate keep-outs."""
    from build123d import Compound
    items=[]
    for side in ('drive','idler'):
        face=ear_face(side);z=P.SOCKET_LUG_DRIVE_Z if side=='drive' else P.SOCKET_LUG_BACK_Z
        a,b=(face+P.SOCKET_M2_SEAT,face+P.SOCKET_M2_SEAT+P.SOCKET_M2_HEAD_H) if side=='drive' else (face-P.SOCKET_M2_SEAT-P.SOCKET_M2_HEAD_H,face-P.SOCKET_M2_SEAT)
        for y in (-P.SOCKET_LUG_Y,P.SOCKET_LUG_Y):items.append(_x_hole(a,b,y,z,P.SOCKET_M2_HEAD-.3))
    return Compound(children=items)
