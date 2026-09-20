# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Shoulder-girdle provision for the three bought, small STS3032M neck servos.

These are packaging envelopes and a future cartridge interface, not printable
neck parts or a solved 3-RPS mechanism. Body dimensions use the larger published
STS3032 envelope; purchased M cases, ears, horns and fixed lead exits await
measurement. Sources and remaining work: docs/design/neck-provision.md.

Coordinates are the torso frame: X dorsal negative, Y lateral, Z along spine.
Callers supply cap_z if the shoulder cap datum changes.
"""
from build123d import Align, Compound, Cylinder, Pos
from .. import params as P, servo_iface as S

CAP_Z = P.TORSO_SHOULDER_TOP
MOUNT_XY = tuple((x, y) for x in (-28.0, 2.0) for y in (-30.0, 30.0))
OPENING_X = (-50.0, -14.0)  # open at the dorsal edge: fixed leads lift out
OPENING_Y = (-24.0, 24.0)
CASE_SIZE = (23.2, 12.1, 28.5)  # published STS3032, not a measured M case
CASE_X = -32.0
CASE_YS = (-16.0, 0.0, 16.0)
CASE_BOTTOM_FROM_CAP = -28.0
CLEARANCE = 1.0
EAR_SPAN = 32.0
# Older manufacturer's drawing gives ears 20.5..22 mm above the case base.
# Reserve through 23 mm to cover the 1 mm higher catalogued case variant.
EAR_BOTTOM_FROM_CASE = 20.5
EAR_TOP_FROM_CASE = 23.0


def case_envelopes(clearance=0.0, cap_z=CAP_Z):
    """Three case-only reference boxes, without fitting holes or claimed fit."""
    x, y, z = CASE_SIZE
    bottom = cap_z + CASE_BOTTOM_FROM_CAP
    return {
        f'reference_neck_case_{i}': S._box(
            CASE_X - x / 2 - clearance, CASE_X + x / 2 + clearance,
            centre - y / 2 - clearance, centre + y / 2 + clearance,
            bottom - clearance, bottom + z + clearance)
        for i, centre in enumerate(CASE_YS)
    }


def ear_envelopes(clearance=0.0, cap_z=CAP_Z):
    """Conservative full-span ear bands; no guessed M-variant hole positions."""
    bottom = cap_z + CASE_BOTTOM_FROM_CAP
    return {
        f'reference_neck_ears_{i}': S._box(
            CASE_X - EAR_SPAN / 2 - clearance,
            CASE_X + EAR_SPAN / 2 + clearance,
            centre - CASE_SIZE[1] / 2 - clearance,
            centre + CASE_SIZE[1] / 2 + clearance,
            bottom + EAR_BOTTOM_FROM_CASE - clearance,
            bottom + EAR_TOP_FROM_CASE + clearance)
        for i, centre in enumerate(CASE_YS)
    }


def fixed_lead_space(cap_z=CAP_Z):
    """12 mm drop under the pack, open dorsally; connector-board fit is unknown."""
    bottom = cap_z + CASE_BOTTOM_FROM_CAP
    return S._box(CASE_X - CASE_SIZE[0] / 2 - CLEARANCE,
                  CASE_X + CASE_SIZE[0] / 2 + CLEARANCE,
                  -23.05, 23.05, bottom - CLEARANCE - 12, bottom - CLEARANCE)


def output_space(cap_z=CAP_Z):
    """24 mm design allowance above the cap for future horns/links, not a sweep."""
    return S._box(*OPENING_X, *OPENING_Y, cap_z, cap_z + 24)


def clearance_envelopes(cap_z=CAP_Z):
    """Named reserved volumes to check against stationary shoulder structure."""
    return {
        **case_envelopes(CLEARANCE, cap_z),
        **ear_envelopes(CLEARANCE, cap_z),
        'reference_neck_fixed_lead_space': fixed_lead_space(cap_z),
        'reference_neck_output_space': output_space(cap_z),
    }


def reference_items(cap_z=CAP_Z):
    """Non-printing reference solids for a body-local assembly/viewer overlay."""
    cases = case_envelopes(cap_z=cap_z)
    ears = ear_envelopes(cap_z=cap_z)
    return [(f'reference_neck_servo_{i}',
             cases[f'reference_neck_case_{i}'] + ears[f'reference_neck_ears_{i}'],
             '#deba69') for i in range(3)]


def cap_opening(z0, z1):
    """U-shaped cutout through the torso cap, continuing to its dorsal edge."""
    return S._box(*OPENING_X, *OPENING_Y, z0, z1)


def mount_hole_tools(z0, z1):
    """Four generic M3 cartridge holes; no servo-specific fixing is claimed."""
    return Compound(children=[
        Pos(x, y, z0) * Cylinder(P.CLEAR_HOLE_M3 / 2, z1 - z0,
                                 align=(Align.CENTER, Align.CENTER, Align.MIN))
        for x, y in MOUNT_XY
    ])


def driver_envelopes(cap_z=CAP_Z):
    """Straight Ø6 driver access above each cartridge fixing (40 mm reach)."""
    return {
        f'neck_cartridge_driver_{i}': Pos(x, y, cap_z) * Cylinder(
            3, 40, align=(Align.CENTER, Align.CENTER, Align.MIN))
        for i, (x, y) in enumerate(MOUNT_XY)
    }


def clearance_interferences(obstacles, cap_z=CAP_Z):
    """List (reservation, obstacle, mm³) intersections above numerical noise.

    Supply torso plus both complete stationary A socket/servo/cassette modules
    in body coordinates. A zero result validates this allocation only: moving
    limbs, as-bought dimensions, installation and complete head travel are
    separate checks. Keep-out volumes intentionally overlap each other.
    """
    hits = []
    for name, envelope in clearance_envelopes(cap_z).items():
        for other_name, obstacle in obstacles.items():
            overlap = envelope & obstacle
            volume = 0 if overlap is None else overlap.volume
            if volume > 0.01:
                hits.append((name, other_name, round(volume, 4)))
    return hits
