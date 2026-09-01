# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Part registry: every module exposes build() -> dict(name, part,
orientation, notes); coupons expose BUILDERS."""
from . import pelvis, hip_bracket, hip_link, thigh, e_tray, coupons


def all_builders():
    return [pelvis.build, hip_bracket.build, hip_link.build,
            thigh.build_upper, thigh.build_clamp, e_tray.build,
            *coupons.BUILDERS]
