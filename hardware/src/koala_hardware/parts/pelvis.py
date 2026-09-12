# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Independent pitch-servo socket modules, bench assembled before frame fitting."""
from functools import lru_cache
from build123d import Pos, Rot, Plane, mirror, Axis, fillet, Cylinder, Align
from .. import params as P, servo_iface as S
from . import links as L


def pitch_socket(front=False):
    # Rear case points forward in the torso frame; rotate about its existing
    # lateral output axis, preserving pitch, centres and horn-face handedness.
    shoulder=Plane(origin=(0,P.ROOT_PITCH_Y,0),x_dir=(0,1,0),z_dir=(0,0,1)).location*L.AXIS
    return shoulder if front else Rot(Y=-90)*shoulder


@lru_cache
def module(front=False):
    z0=P.ROOT_REAR_MOUNT_Z if not front else -P.ROOT_MOUNT_Z-P.FRAME_PLATE_T
    floor=P.SOCKET_AXIS_Z+P.SOCKET_SHELF
    plate=S._box(-46,16 if front else floor,P.ROOT_MODULE_GAP/2,47,z0,z0+P.FRAME_PLATE_T)
    plate=fillet(plate.edges().filter_by(Axis.Z),4)
    part=plate+pitch_socket(front)*S.saddle()
    if not front:
        # Socket floor is perpendicular to the raised torso flange. Its
        # full-width return grows from the bed when printed socket-floor down.
        web=S._box(floor-5,floor,P.ROOT_MODULE_GAP/2,47,-16,z0+P.FRAME_PLATE_T)
        part+=fillet(web.edges().filter_by(Axis.X),3)
    for x,y in P.ROOT_FRAME_HOLES:
        if y>0:
            part-=Pos(x,y,z0-1)*Cylinder(P.CLEAR_HOLE_M3/2,P.FRAME_PLATE_T+2,align=(Align.CENTER,Align.CENTER,Align.MIN))
    # Blind locating pockets in the frame datum: the flat face remains a
    # broad build face. The small pocket roofs bridge just 4.4 mm.
    z=z0 if front else z0+P.FRAME_PLATE_T-P.ROOT_LOCATOR_DEPTH-.3
    for y in (12,26):
        part-=Pos(-28,y,z)*Cylinder((P.ROOT_LOCATOR_DIA+.4)/2,P.ROOT_LOCATOR_DEPTH+.3,align=(Align.CENTER,Align.CENTER,Align.MIN))
    return part


@lru_cache
def solid(front=False):
    """Both installed modules, retained for layout/access studies."""
    right=module(front)
    return right+mirror(right,Plane.XZ)


def _build(front):
    # Enclosing pocket opens upwards in both declared print orientations.
    return L.spec('shoulder_socket' if front else 'pelvis_socket',module(front),
        handed=True,orientation=Rot() if front else Rot(Y=90),
        fasteners={'M2x5 self-tapper into servo ear':4},
        notes='Independent enclosing pitch socket. Secure all four servo ear screws on the bench. '
        'Fit module onto frame locating pins and two accessible M3 through-bolts at x=-30/-20. ' +
        ('Flat frame face down, socket opening up. ' if front else
         'Socket-floor face down, opening up; perpendicular flange grows as a vertical wall. ') +
        'Bridge the 4.4 mm locator-pocket roofs; '
        'ear-hole roofs use accessible local support.', printable='assumed')


def build(): return _build(False)
def build_shoulders(): return _build(True)
