# SPDX-License-Identifier: CERN-OHL-S-2.0
"""20.8 mm footed-link CAD inspection limits, not calibrated servo limits.

Signed native X rotation from a straight upper/lower link. Limits stop 2 degrees
inside the last clear 0.25-degree sample preceding pocket contact. Interior
travel is sampled at 1 degree; installed poses need their own collision check.
Evidence: docs/design/flat-links/bend-clearance.json and README.md.
"""
from math import atan2, degrees

ANGULAR_RESERVE_DEG = 2.0
SIGNED_BEND_LIMITS = {'front': (-112.75, 112.75), 'rear': (-22.75, 121.25)}
FIRST_BLOCKED_SAMPLES = {'front': (-115., 115.), 'rear': (-25., 123.5)}


def nominal_angle(limb):
    # Both frames use +X along the right-hand lateral shaft.
    from .assembly import segment_frame
    m = (segment_frame(limb.root, limb.bend, 0).inverse()
         * segment_frame(limb.bend, limb.axle, 0)).matrix()
    return degrees(atan2(m[2][1], m[1][1]))


def delta_bounds(limb, key):
    rest = nominal_angle(limb)
    return tuple(v-rest for v in SIGNED_BEND_LIMITS[key])


# Two opposite travel endpoints plus the simultaneous anatomical fold.
REVIEW_POSES = {
    'max-fold': {'front': SIGNED_BEND_LIMITS['front'][0], 'rear': SIGNED_BEND_LIMITS['rear'][1]},
    'bend-min': {key: bounds[0] for key,bounds in SIGNED_BEND_LIMITS.items()},
    'bend-max': {key: bounds[1] for key,bounds in SIGNED_BEND_LIMITS.items()},
}
