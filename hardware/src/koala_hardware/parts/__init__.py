# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Part registry: every module exposes build() -> dict(name, part,
orientation, notes); coupons expose BUILDERS."""
from . import pelvis, hip_link, thigh, e_tray, coupons


def all_builders():
    return [pelvis.build, hip_link.build_drive, hip_link.build_idler,
            hip_link.build_saddle, hip_link.build_cap,
            thigh.build_outer, thigh.build_inner, thigh.build_spacer, e_tray.build,
            *coupons.BUILDERS]
