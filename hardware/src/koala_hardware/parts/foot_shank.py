# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Interchangeable rear walking shank; same knee horns and TPU pad as V1.

Native X is the knee shaft; +Z runs from knee to pad centre. The shared
front lower-link construction preserves its open fork and keyed pad seat.
No ankle joint, wheel mounting or drive-motor hardware is present.
"""
from build123d import Pos, Rot
from .. import params as P
from . import front, links as L


def solid():
    return front.forearm(P.BODY_SHANK_MM)


def pad_location():
    return Pos(0,0,P.BODY_SHANK_MM-P.BODY_FOREARM_MM-P.BODY_HAND_MM)


def build():
    result=L.spec('foot_shank',solid(),handed=True,orientation=Rot(X=90),version=1,
        fasteners=L.HORN_FASTENERS|{'M3x20 TPU-pad screw':1,'M3 nut':1,'M3 plain washer':1},
        notes='Rear walking variant: 90 mm knee-to-pad centre, original knee horn interfaces, '
        'long open fork, R6.3 roots and rounded taper. Uses the unchanged front_contact_pad v1. '
        'Broad native -Y face down; accessible support at fork holes and nut-slot roof. '
        'Insert captive M3 nut before keyed pad, then recessed M3x20 with washer. '
        'Exchange the complete shank at the knee for wheeled shank v2. Unprinted.')
    result['configurations']=('walking',)
    return result
