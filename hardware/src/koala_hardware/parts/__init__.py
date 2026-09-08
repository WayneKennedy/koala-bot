# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Current printable parts; discarded DEC-29 builders are deliberately absent."""
from . import pelvis, links, e_tray, coupons, joint_rig


def all_builders():
    return [pelvis.build, *links.BUILDERS, e_tray.build, *joint_rig.BUILDERS,
            *coupons.BUILDERS]
