# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Two-print acceptance rig uses the production saddle and integral clevis."""
from build123d import Rot
from .. import servo_iface as S
from . import links as L


def build_saddle():
    return L.spec('coupon_socket_saddle',S.saddle(),orientation=Rot(),
        notes='Production four-ear saddle. M2x5 through 2.2 mm seats; enclosing Side returns and open insertion face. Floor down. Accessible support beneath ear-hole roofs. Fit/removal and screw engagement check.', printable='assumed')


def build_fork():
    return L.spec('coupon_socket_fork',L.clevis(),orientation=Rot(Y=90),
        notes='Production integral double fork. Flat 36.4 mm horn contact span; 3.5 mm web, 6 mm pan-head pockets and blind Back boss relief. Outer horn pad down; removable support beneath opposite cheek. Fit before full limbs.', printable='assumed')

BUILDERS=[build_saddle,build_fork]
