# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Roll-first shoulders and parallel-axis front links.

Carrier frame: X is the longitudinal A roll axis, Y is outboard along the
B pitch shaft, Z points down the arm at zero pitch. Link frames retain X as
their pitch shaft and +Z towards the next joint. Mirroring makes the left hand.
All dimensions are design allocations, not evidence of printed fit or loads.
"""
from functools import lru_cache

from build123d import Pos, Rot, Plane, mirror, extrude, Polygon

from .. import params as P, servo_iface as S
from . import links as L


PITCH_OFFSET = P.SHOULDER_PITCH_OFFSET
FORK_START = 46.0
FORK_END = 56.0


def roll_socket_frame():
    """A Bottom points inward; its output axis is carrier X at the origin."""
    return Rot(X=-90) * L.AXIS


def pitch_socket_frame():
    """B output at (0,PITCH_OFFSET,0), shaft +Y, Bottom towards carrier -Z."""
    return Plane(origin=(0, PITCH_OFFSET, -P.SOCKET_AXIS_Z),
                 x_dir=(0, 1, 0), z_dir=(0, 0, 1)).location


def pitch_link_frame():
    """Zero-pitch upper link: its X shaft follows carrier Y."""
    return Pos(0, PITCH_OFFSET, 0) * Rot(Z=90)


def elbow_socket_frame(length=P.BODY_UPPER_ARM_MM):
    return Pos(0, 0, length) * L.AXIS


@lru_cache
def carrier():
    """Open A clevis to B pocket, sharing one broad planar print face.

    The A forks point away from its inward-facing case. The B pocket sits
    beside them, with its case behind the outgoing arm. No hidden support
    chamber or bolted carrier seam is introduced.
    """
    floor = -P.SOCKET_AXIS_Z-P.SOCKET_SHELF
    top = -24.0
    inner = PITCH_OFFSET-P.SOCKET_CASE_X/2-P.SOCKET_WALL
    a = P.SOCKET_ARM_HALF_W
    x0 = P.SOCKET_IDLER_FACE-P.SOCKET_PAD_T
    x1 = P.SOCKET_DRIVE_FACE+P.SOCKET_PAD_T
    forks = mirror(L.fork('drive')+L.fork('idler'), Plane.XY)
    forks &= S._box(x0-1, x1+1, -12, 12, -20, P.SOCKET_PLATE_R+1)
    for lo,hi in ((x0,P.SOCKET_IDLER_FACE),(P.SOCKET_DRIVE_FACE,x1)):
        forks += S._box(lo,hi,-a,a,top,-19.9)
    part = forks + S._box(x0, x1, -a, inner+1, floor, top)
    part += pitch_socket_frame()*S.saddle()
    part = L._root_fillet(part,
        lambda e: abs(e.center().Z-top)<1e-5 and abs(e.length-2*a)<1e-5
        and any(abs(e.center().X-x)<1e-5 for x in (P.SOCKET_IDLER_FACE, P.SOCKET_DRIVE_FACE)),
        P.REAR_FORK_ROOT_R, 2, 'shoulder roll fork roots')
    # Straight open tunnels through the bridge expose the two inner ear
    # screws; their countersinks and 2.2 mm bearing seats stay in the cup.
    for name,probe in S.socket_keepouts()[1:]:
        if name=='idler_lug_driver':part-=pitch_socket_frame()*probe
    return L.round_convex_edges(part,2,exclude=lambda c:c.Z>-12 or c.Y>inner-1)


@lru_cache
def upper_arm(length=P.BODY_UPPER_ARM_MM):
    """Parallel pitch/elbow shafts with an outer face shared by fork and cup.

    The drive-side cup wall is thickened outward to the proximal horn-pad
    plane. Recutting the existing ear counterbore preserves its 2.2 mm seat.
    The opposite fork and open socket use externally removable support.
    """
    bottom = length-P.SOCKET_AXIS_Z
    outer = P.SOCKET_DRIVE_FACE+P.SOCKET_PAD_T
    x0 = P.SOCKET_IDLER_FACE-P.SOCKET_PAD_T
    a = P.SOCKET_ARM_HALF_W
    # A short, broad plate joins the fork bridge to the complete cup floor.
    part = L.clevis()+S._box(x0, outer, -a, a, P.LINK_BRIDGE_START, bottom)
    cup = S.saddle()
    w = P.SOCKET_CASE_Y/2+2
    cup += S._box(P.SOCKET_CASE_X/2+P.SOCKET_WALL-1, outer,
                  -w+2, w-2, -P.SOCKET_SHELF, P.SOCKET_DEPTH)
    for y in (-P.SOCKET_LUG_Y, P.SOCKET_LUG_Y):
        cup -= S._x_hole(S.ear_face('drive')+P.SOCKET_M2_SEAT,
                         outer+1, y, P.SOCKET_LUG_DRIVE_Z, P.SOCKET_M2_HEAD)
    part += Pos(0,0,bottom)*cup
    part=L._root_fillet(part,
        lambda e:abs(e.length-2*a)<1e-5 and abs(e.center().Z-P.LINK_BRIDGE_START)<1e-5
        and any(abs(e.center().X-x)<1e-5 for x in (P.SOCKET_IDLER_FACE,P.SOCKET_DRIVE_FACE)),
        P.REAR_FORK_ROOT_R,2,'front upper fork roots')
    # Round only the two load-carrying shoulders where the bridge reaches
    # the cup. Interface seats, horn bores and the flat print face stay fixed.
    return L.round_convex_edges(part,2,
        exclude=lambda c:c.Z<14 or (c.Z>bottom-P.SOCKET_SHELF-.1 and abs(c.X)<22))


@lru_cache
def forearm():
    """Long open elbow fork and a tapered flat shaft to the existing TPU key."""
    a=P.SOCKET_ARM_HALF_W
    x0=P.SOCKET_IDLER_FACE-P.SOCKET_PAD_T
    x1=P.SOCKET_DRIVE_FACE+P.SOCKET_PAD_T
    part=(L.fork('drive')+L.fork('idler'))&S._box(-30,30,-30,30,-12,20)
    for lo,hi in ((x0,P.SOCKET_IDLER_FACE),(P.SOCKET_DRIVE_FACE,x1)):
        part+=S._box(lo,hi,-a,a,20,FORK_START+4)
    part+=S._box(x0,x1,-a,a,FORK_START,FORK_START+4)
    # Flat native -Y surface continues from the broad shaft to the fork nose.
    profile=Plane.XZ*Polygon((x0,FORK_START),(x1,FORK_START),(x1,FORK_END),
                             (9,74),(9,P.FRONT_PAD_START),(-9,P.FRONT_PAD_START),
                             (-9,74),(x0,FORK_END),align=None)
    face=profile.faces()[0]
    corners=[v for v in face.vertices() if any(abs(v.Z-z)<1e-5 for z in (FORK_END,74))]
    profile=face.fillet_2d(3,corners)
    part+=Pos(0,P.SOCKET_PLATE_R,0)*extrude(profile,amount=2*P.SOCKET_PLATE_R)
    part=L._root_fillet(part,
        lambda e:abs(e.length-2*a)<1e-5 and abs(e.center().Z-FORK_START)<1e-5
        and any(abs(e.center().X-x)<1e-5 for x in (P.SOCKET_IDLER_FACE,P.SOCKET_DRIVE_FACE)),
        P.REAR_FORK_ROOT_R,2,'front elbow fork roots')
    # Reuse only the terminal pad key, nut slot and bore; the old short fork
    # and shaft do not participate in this longer elbow-clearance geometry.
    terminal=L.lower_link(P.BODY_FOREARM_MM+P.BODY_HAND_MM,True)
    part+=terminal&S._box(-15,15,-15,15,80,110)
    from build123d import Cylinder, Align, RegularPolygon
    nut=Pos(0,0,P.FRONT_PAD_NUT_Z)*extrude(RegularPolygon(3.3,6,rotation=30),amount=2.6)
    part-=nut+S._box(0,12,-2.9,2.9,P.FRONT_PAD_NUT_Z,P.FRONT_PAD_NUT_Z+2.6)
    part-=Pos(0,0,90)*Cylinder(P.CLEAR_HOLE_M3/2,15,align=(Align.CENTER,Align.CENTER,Align.MIN))
    return part


def build_carrier():
    return L.spec('shoulder_carrier',carrier(),handed=True,orientation=Rot(),version=3,
        fasteners=L.HORN_FASTENERS|{'M2x5 self-tapper into servo ear':4},
        notes='Roll-first shoulder: longitudinal A fork, B pitch 40 mm outboard. '
        'The complete moving upper fork and horn screws clear A at +/-30 degrees; '
        'nominal caliper-case gap at the upper fork is 1.765 mm at those endpoints. '
        'R6.3 fork roots, shared flat block/socket floor on the bed. Fit B and '
        'its four ear screws on the bench before the upper arm. Unprinted.')


def build_upper_arm():
    return L.spec('upper_arm',upper_arm(),handed=True,orientation=Rot(Y=90),version=2,
        fasteners=L.HORN_FASTENERS|{'M2x5 self-tapper into servo ear':4},
        notes='70 mm parallel-axis upper arm: enclosing elbow pocket and proximal '
        'pitch clevis, R6.3 fork roots and R2 accessible outer edges. Seven '
        'short or narrow outer junction edges resist R2 and remain sharp. '
        'Drive outer face and thickened cup wall share the bed. '
        'Support under the opposite fork and inside the open cup is accessible. '
        'Fit elbow servo and all four ear screws before forearm. Unprinted.')


def build_forearm():
    return L.spec('forearm',forearm(),handed=True,orientation=Rot(X=90),version=2,
        fasteners=L.HORN_FASTENERS|{'M3x20 front-pad screw':1,'M3 nut':1,'M3 plain washer':1},
        notes='100 mm elbow-to-contact: long open fork, R6.3 roots, R3 taper corners, flat '
        'shaft and unchanged keyed TPU contact. Broad native -Y face down; '
        'fork, nut-slot and hole-roof support remains externally accessible. '
        'Insert the captive nut before fitting the pad. Unprinted.')


BUILDERS=[build_carrier,build_upper_arm,build_forearm]
