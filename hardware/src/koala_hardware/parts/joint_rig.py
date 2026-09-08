# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Single-joint fit rig. All three powered joints reuse this socket interface."""
from functools import lru_cache
from build123d import Rot
from .. import params as P, servo_iface as S


BRIDGE_MIN_X = P.SOCKET_IDLER_FACE
BRIDGE_MAX_X = P.SOCKET_DRIVE_FACE - P.SOCKET_RECESS_DEPTH
BRIDGE_SPAN = BRIDGE_MAX_X - BRIDGE_MIN_X


@lru_cache
def bridge():
    z = P.SOCKET_AXIS_Z + P.SOCKET_BRIDGE_Z
    part = S._box(BRIDGE_MIN_X, BRIDGE_MAX_X,
                  -P.SOCKET_ARM_HALF_W, P.SOCKET_ARM_HALF_W,
                  z-P.SOCKET_BRIDGE_H/2, z+P.SOCKET_BRIDGE_H/2)
    for y in (-P.SOCKET_BRIDGE_BOLT_Y, P.SOCKET_BRIDGE_BOLT_Y):
        part -= S._x_hole(BRIDGE_MIN_X-1, BRIDGE_MAX_X+1,
                          y, z, P.CLEAR_HOLE_M3)
    return part


def build_cradle():
    return dict(name="coupon_socket_cradle", part=S.cradle(), orientation=Rot(),
                notes="Rear shelf on bed; SO-101 nominal pocket. Two M2x5 into "
                      "idler-face lugs, 2.2 mm seats. Collar boss lanes open upward.")


def build_collar():
    return dict(name="coupon_socket_collar", part=S.collar(), orientation=Rot(),
                notes="Sleeve rim on bed, open both ends. Two M2x5 into drive-face "
                      "lugs; nominal 2.8 mm engagement. Check driver/head fit and cable slot.")


def build_drive():
    from . import links
    d = links.build_fork_drive()
    return dict(d, name='coupon_socket_drive', qty=1)


def build_idler():
    from . import links
    d = links.build_fork_idler()
    return dict(d, name='coupon_socket_idler', qty=1)


def build_bridge():
    from . import links
    return dict(name='coupon_socket_bridge',
                part=links._register(links._crossbar(),
                    [(y,P.SOCKET_BRIDGE_Z) for y in
                     (-P.SOCKET_BRIDGE_BOLT_Y,P.SOCKET_BRIDGE_BOLT_Y)]),
                orientation=Rot(Y=-90),
                notes='Registered compression crossbar, same shoulders as the leg. '
                      'Broad end on bed. Two M3x50, nuts and washers; nominal grip '
                      '43.7 mm. Verify registration and horn span without plate preload.')


BUILDERS = [build_cradle, build_collar, build_drive, build_idler, build_bridge]
