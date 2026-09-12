# SPDX-License-Identifier: CERN-OHL-S-2.0
"""DEC-40 current builders; legacy seam-based links no longer export."""
from . import pelvis, links, e_tray, torso, coupons, joint_rig


def all_builders():
    return [pelvis.build,pelvis.build_shoulders,*links.BUILDERS,torso.build,
            e_tray.build,e_tray.build_spacer,*joint_rig.BUILDERS,*coupons.BUILDERS]
