# SPDX-License-Identifier: CERN-OHL-S-2.0
"""DEC-34 new pelvis master: two SO-101 roll cradles under a flat deck."""
from functools import lru_cache
from build123d import Align, Axis, Box, Cylinder, Pos, Rot, fillet, Plane, mirror
from .. import params as P, servo_iface as S

TRAY_BOSS_XY = P.V2_TRAY_HOLES


def roll_socket(side):
    return Pos(P.V2_ROLL_X, side*P.V2_ROLL_Y, -P.V2_ROLL_DROP) * Rot(X=180) * Pos(0, 0, -P.SOCKET_AXIS_Z)


@lru_cache
def solid():
    lx, ly, t = P.V2_DECK_SIZE
    part = Pos(P.V2_DECK_X, 0, -t) * Box(lx, ly, t,
        align=(Align.CENTER, Align.CENTER, Align.MIN))
    part = fillet(part.edges().filter_by(Axis.Z), 8)
    for side in (-1, 1):
        tf = roll_socket(1)
        # Stem inside the collar's open bore; sleeve stops below the deck.
        stem = S._box(-P.SOCKET_CASE_X/2, P.SOCKET_CASE_X/2,
                      -P.SOCKET_CASE_Y/2, P.SOCKET_CASE_Y/2,
                      -(P.V2_ROLL_DROP-P.SOCKET_AXIS_Z), 0)
        core = S.cradle() + stem + S.rear_support(-10, P.SOCKET_CASE_X/2, P.SOCKET_CASE_Y/2)
        core -= S._box(-P.SOCKET_CABLE_W/2, P.SOCKET_CABLE_W/2,
                       0, P.SOCKET_CASE_Y/2+1, -P.SOCKET_SHELF-1, 1)
        placed = tf * core
        part += placed if side == 1 else mirror(placed, Plane.XZ)
    for x, y in TRAY_BOSS_XY:
        part -= Pos(x, y, -t-1) * Cylinder(P.CLEAR_HOLE_M3/2, t+2,
            align=(Align.CENTER, Align.CENTER, Align.MIN))
    # Rigid torso strut mounting interface: four through-bolts, metal nuts.
    # Future parallel platform positions remain OQ-03, not invented actuator mounts.
    for x in (-20., 20.):
        for y in (-20., 20.):
            part -= Pos(x, y, -t-1) * Cylinder(P.CLEAR_HOLE_M3/2, t+2,
                align=(Align.CENTER, Align.CENTER, Align.MIN))
    return part


def build():
    return dict(name='pelvis', part=solid(), qty=1, orientation=Rot(X=180),
        fasteners={'M2x5 self-tapper into servo lug':4,
                   'M3 female/female standoff, 10 mm':len(P.V2_TRAY_HOLES),
                   'M3x10 lower tray-standoff screw':len(P.V2_TRAY_HOLES)},
        notes='Deck top down, integral roll cradles grow upward. Four M3 through-bolts '
              'for tray standoffs, four reserved for torso strut. Socket screw/cable access '
              'and root layer strength require the rig and load tests.')
