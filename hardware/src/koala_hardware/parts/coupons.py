# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Test-fit coupons - PRINT THESE FIRST (before any structural part).

Each coupon verifies one [VERIFY] constant in params.py against the real
hardware; adjust the constant, regenerate, reprint until it fits.
"""
import math
from build123d import Box, Cylinder, Part, Pos, Rot, Align, Text, extrude
from .. import params as P
from .. import fasteners as F
from .. import servo_iface as S


def build_servo_cradle() -> dict:
    """STS3215 drops in; two screws through the rear tabs. Verifies
    CLEAR_POCKET and the tab hole positions."""
    block = Pos(0, 0, P.SERVO_BODY_BOT - 6) * Box(
        64, 40, 30, align=(Align.CENTER, Align.CENTER, Align.MIN))
    part = block - S.servo_envelope()
    part -= S.tab_screw_cutters(boss_top_z=P.SERVO_BODY_BOT + 24, depth=30)
    return {"name": "coupon_servo_cradle", "part": part,
            "orientation": Rot(), "notes": "Servo should seat snug, tabs on the bosses."}


def build_horn_plate() -> dict:
    """Bolts to the servo horn: 4x M2.5 + centre clearance. Verifies the
    drive-square measurement."""
    plate = Box(30, 30, 4, align=(Align.CENTER, Align.CENTER, Align.MIN))
    part = plate - S.drive_hole_cutters(4.0)
    return {"name": "coupon_horn_plate", "part": part,
            "orientation": Rot(), "notes": "All 4 screws should start without force."}


def build_motor_ring() -> dict:
    """Motor face ring: bore over the centre boss + 6x M3 on BCD31.
    Verifies MOTOR_FACE_BOSS_DIA and the hex pattern."""
    ring = Cylinder(P.MOTOR_DIA / 2 + 5, 5,
                    align=(Align.CENTER, Align.CENTER, Align.MIN))
    part = ring - Cylinder(P.MOTOR_FACE_BOSS_DIA / 2 + 0.5, 12,
                           align=(Align.CENTER, Align.CENTER, Align.CENTER))
    for i in range(6):
        a = math.radians(60 * i)
        part -= Pos(P.MOTOR_BCD / 2 * math.cos(a),
                    P.MOTOR_BCD / 2 * math.sin(a), 5.1) * F.m3_clear(5.2)
    return {"name": "coupon_motor_ring", "part": part,
            "orientation": Rot(), "notes": "Face-boss + BCD only; the body "
            "bore is coupon_motor_bore."}


def _label(txt: str, x: float, y: float, size: float = 5.0,
           depth: float = 0.6) -> Part:
    """Engraved size label, cut into the top face at Z=6."""
    sketch = Pos(x, y, 6 - depth) * Text(txt, font_size=size)
    return extrude(sketch, amount=depth + 0.1)


def build_ladder() -> dict:
    """Hole ladder: M3 clearance 3.2/3.4/3.6 and insert bores 3.8/4.0/4.2,
    each engraved with its nominal size. Deliberately a large flat slab - it
    doubles as the bed-adhesion / corner-lift test for a big footprint.

    Motor bores live on their own coupon: at Ø37+ they cannot be enclosed in
    this slab alongside these rows.
    """
    part = Part() + Box(150, 60, 6,
                        align=(Align.CENTER, Align.CENTER, Align.MIN))
    for i, d in enumerate((3.2, 3.4, 3.6)):
        x = -60 + i * 18
        part -= Pos(x, 18, 6.1) * Cylinder(
            d / 2, 6.2, align=(Align.CENTER, Align.CENTER, Align.MAX))
        part -= _label(f"{d}", x - 5, 6)
    for i, d in enumerate((3.8, 4.0, 4.2)):
        x = -60 + i * 18
        part -= Pos(x, -8, 6.1) * Cylinder(
            d / 2, 6.2, align=(Align.CENTER, Align.CENTER, Align.MAX))
        part -= _label(f"{d}", x - 5, -20)
    part -= _label("M3 CLEAR", 5, 16, size=6)
    part -= _label("INSERT", 5, -10, size=6)
    return {"name": "coupon_ladder", "part": part, "orientation": Rot(),
            "notes": "Smallest that ACCEPTS the real screw/insert wins - fit, "
                     "not calipers. Outer 150.0 x 60.0 x 6.0 is the machine's "
                     "dimensional-accuracy datum."}


def build_motor_bore() -> dict:
    """Motor body-bore ladder, 37.3/37.5/37.7 - print when the 37D is in hand.
    Sized so every bore is fully enclosed with a real wall around it."""
    part = Part() + Box(135, 50, 6,
                        align=(Align.CENTER, Align.CENTER, Align.MIN))
    for i, d in enumerate((37.3, 37.5, 37.7)):
        x = -42 + i * 42
        part -= Pos(x, 0, 6.1) * Cylinder(
            d / 2, 6.2, align=(Align.CENTER, Align.CENTER, Align.MAX))
        part -= _label(f"{d}", x - 7, 20, size=4.5)
    return {"name": "coupon_motor_bore", "part": part, "orientation": Rot(),
            "notes": "Smallest bore the 37D gearbox slides into wins."}


def build_seam() -> dict:
    """One DEC-23 seam: boss + key on a base; mating lid with clearance
    holes + key pockets. Doubles as heat-set-insert practice."""
    base = Box(60, 30, 5, align=(Align.CENTER, Align.CENTER, Align.MIN))
    base = Part() + base
    for x in (-20, 20):
        base += Pos(x, 0, 5) * F.insert_boss(8)
    base += Pos(0, 8, 5) * F.registration_key()
    lid = Pos(0, -45, 0) * (
        Part() + Box(60, 30, 4, align=(Align.CENTER, Align.CENTER, Align.MIN))
        - Pos(-20, 0, 4.1) * F.m3_clear(4.2)
        - Pos(20, 0, 4.1) * F.m3_clear(4.2)
        - Pos(0, 8, P.CLEAR_POCKET) * Rot(X=180) * F.registration_key(
            clearance=P.CLEAR_POCKET))
    return {"name": "coupon_seam", "part": base + lid,
            "orientation": Rot(), "notes": "Set inserts, screw the lid down flat."}


BUILDERS = [build_servo_cradle, build_horn_plate, build_motor_ring,
            build_motor_bore,
            build_ladder, build_seam]
