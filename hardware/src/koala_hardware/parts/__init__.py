# SPDX-License-Identifier: CERN-OHL-S-2.0
"""DEC-40 current builders; legacy seam-based links no longer export."""
from . import pelvis, links, front, foot_shank, shoulder_mount, e_tray, torso, coupons, joint_rig


def all_builders():
    return [pelvis.build,links.build_thigh,links.build_shank,foot_shank.build,links.build_hip_carrier,links.build_front_pad,
            *front.BUILDERS,shoulder_mount.build,torso.build,
            e_tray.build,e_tray.build_spacer,*joint_rig.BUILDERS,*coupons.BUILDERS]


def configuration_specs(configuration):
    """One robot's quantities; alternatives are never added to the same BOM."""
    if configuration not in ('walking','wheeled'):
        raise ValueError(f'Unknown build configuration: {configuration}')
    for builder in all_builders():
        spec=builder()
        if configuration not in spec.get('configurations',('walking','wheeled')):
            continue
        yield spec | {'qty':spec.get('configuration_qty',{}).get(configuration,spec.get('qty',1))}
