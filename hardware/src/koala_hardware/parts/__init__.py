# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Part registry: every module exposes build() -> dict(name, part,
orientation, notes); coupons expose BUILDERS."""
from . import pelvis, hip_link, thigh, e_tray, coupons


def all_builders():
    return [pelvis.build, hip_link.build, thigh.build, e_tray.build,
            *coupons.BUILDERS]
