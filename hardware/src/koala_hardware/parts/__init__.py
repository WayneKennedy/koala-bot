# SPDX-License-Identifier: CERN-OHL-S-2.0
"""DEC-40 current builders; legacy seam-based links no longer export."""
from . import pelvis, links, front, shoulder_mount, e_tray, torso, coupons, joint_rig


def all_builders():
    return [pelvis.build,links.build_thigh,links.build_shank,links.build_hip_carrier,links.build_front_pad,
            *front.BUILDERS,shoulder_mount.build,torso.build,
            e_tray.build,e_tray.build_spacer,*joint_rig.BUILDERS,*coupons.BUILDERS]
