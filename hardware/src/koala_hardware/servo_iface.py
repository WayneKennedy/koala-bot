# SPDX-License-Identifier: CERN-OHL-S-2.0
"""SO-101 cradle/collar/clevis primitive, DEC-33/34.

Servo face words (docs/soarm-joint-pattern.md, Terminology): FRONT = drive-horn
face = +X; BACK = idler/connector face = -X; BOTTOM = the end the servo stands
on = Z 0; TOP = the end nearest the output axis = Z 45.23; SIDES = +-Y. The
cradle has a floor under the Bottom, a Front wall and a Back wall (the pair
34.9 apart), one Side wall and an open Side that the collar's closing wall
shuts. The clevis has a Front plate (drive horn) and a Back plate (idler).
Body mounts use the CASE datum; horns use the OUTPUT AXIS datum. These are
independent feature families (test-log 2026-09-02). Nominal printed-part
interfaces are adopted from SO-101; no pocket derives from a servo model.
"""
from functools import lru_cache
from build123d import Box, Cylinder, Part, Pos, Rot, Align, Rectangle, loft
from . import params as P

# Restart primitive frame: X = output axis, Y = case width, Z = case length.
# BODY features use rear face Z=0; HORN features use Z=SOCKET_AXIS_Z.
# These are independent datums (test-log 2026-09-02); never locate a lug from
# a horn hole.


def _box(x0, x1, y0, y1, z0, z1):
    return Pos(x0, y0, z0) * Box(x1-x0, y1-y0, z1-z0,
        align=(Align.MIN, Align.MIN, Align.MIN))


def _x_hole(x0, x1, y, z, diameter):
    return Pos(x0, y, z) * Rot(Y=90) * Cylinder(diameter/2, x1-x0,
        align=(Align.CENTER, Align.CENTER, Align.MIN))


def _socket_bounds():
    return (P.SOCKET_CASE_X/2 + P.SOCKET_CLEAR,
            P.SOCKET_CASE_Y/2 + P.SOCKET_CLEAR)


def rear_support(z0, half_x, half_y):
    """45°-or-shallower expansion under a socket, within the collar bore.

    Caller supplies the lower rectangle. The upper rectangle matches the
    cradle shelf; collar boss lanes remain open through this support too.
    """
    x,y = _socket_bounds()
    top = -P.SOCKET_SHELF
    if z0 >= top:
        raise ValueError('Support must begin below the shelf')
    part = loft([Pos(0,0,z0)*Rectangle(2*half_x,2*half_y),
                 Pos(0,-P.SOCKET_WALL/2,top)*Rectangle(2*(x+P.SOCKET_WALL),2*y+P.SOCKET_WALL)])
    for cy in (-P.SOCKET_LUG_Y,P.SOCKET_LUG_Y):
        half=P.SOCKET_BOSS_W/2+P.SOCKET_BOSS_CLEAR
        part -= _box(x-P.SOCKET_BOSS_CLEAR,x+P.SOCKET_WALL+1,cy-half,cy+half,z0-1,top+1)
    return part


@lru_cache
def cradle() -> Part:
    """Rear pocket: shelf, back and two sides; open front and top.

    The drive-face side is relieved for the collar's inward lug bosses. The
    screws retain the case through its lugs; no screw threads into the print.
    """
    x, y = _socket_bounds()
    w, h = P.SOCKET_WALL, P.SOCKET_DEPTH
    part = _box(-x-w, x+w, -y-w, y, -P.SOCKET_SHELF, h)
    part -= _box(-x, x, -y, y+1, 0, h+1)
    # Full-height sliding lanes, including the shelf, for collar lug bosses.
    for cy in (-P.SOCKET_LUG_Y, P.SOCKET_LUG_Y):
        half = P.SOCKET_BOSS_W/2 + P.SOCKET_BOSS_CLEAR
        part -= _box(x-P.SOCKET_BOSS_CLEAR, x+w+1, cy-half, cy+half,
                     -P.SOCKET_SHELF-1, h+1)
        part -= _x_hole(-x-w-1, -x+1, cy, P.SOCKET_LUG_BACK_Z, P.SOCKET_M2_CLEAR)
        part -= _x_hole(-x-w-1, -x-P.SOCKET_M2_SEAT, cy,
                        P.SOCKET_LUG_BACK_Z, P.SOCKET_M2_HEAD)
    # Open-front cable channel through the shelf; actual connector is a rig check.
    part -= _box(-P.SOCKET_CABLE_W/2, P.SOCKET_CABLE_W/2, 0, y+1,
                 -P.SOCKET_SHELF-1, 1)
    return part


@lru_cache
def collar() -> Part:
    """Separate open-ended sleeve; two deep bosses bear on drive-face lugs."""
    x, y = _socket_bounds()
    w, c, t = P.SOCKET_WALL, P.SOCKET_COLLAR_CLEAR, P.SOCKET_COLLAR_WALL
    ix, back, front = x+w+c, -y-w-c, y+P.SOCKET_FRONT_CLEAR
    z0, z1 = P.SOCKET_COLLAR_BOTTOM, P.SOCKET_DEPTH
    part = _box(-ix-t, ix+t, back-t, front+t, z0, z1)
    part -= _box(-ix, ix, back, front, z0-1, z1+1)
    for cy in (-P.SOCKET_LUG_Y, P.SOCKET_LUG_Y):
        part += _box(x, ix+t, cy-P.SOCKET_BOSS_W/2, cy+P.SOCKET_BOSS_W/2, z0, z1)
        part -= _x_hole(x-1, ix+t+1, cy, P.SOCKET_LUG_DRIVE_Z, P.SOCKET_M2_CLEAR)
        part -= _x_hole(x+P.SOCKET_M2_SEAT, ix+t+1, cy,
                        P.SOCKET_LUG_DRIVE_Z, P.SOCKET_M2_HEAD)
        # Sleeve must not bury the idler-side cradle screw heads or their tool.
        part -= _x_hole(-ix-t-1, -ix+1, cy, P.SOCKET_LUG_BACK_Z, P.SOCKET_M2_TOOL)
    # Open-bottom front slot keeps the loom outside the rotating clevis lane.
    part -= _box(-P.SOCKET_CABLE_W/2, P.SOCKET_CABLE_W/2, front-1, front+t+1,
                 z0-1, P.SOCKET_CABLE_H)
    return part


@lru_cache
def clevis_plate(side: str) -> Part:
    """Flat XY cheek, horn centre at origin, arm along +Y; drive recess on TOP.

    Prints broad face down. Both plates keep four full-depth M3 holes; the
    drive-side 20.5 mm horn recess is blind. The nominal flush idler uses
    a flat seat to avoid embedding the plate in the case; DEC-34. Only the
    drive side has centre access.
    """
    if side not in ("drive", "idler"):
        raise ValueError("side must be 'drive' or 'idler'")
    t = P.SOCKET_PLATE_T
    part = Cylinder(P.SOCKET_PLATE_R, t, align=(Align.CENTER, Align.CENTER, Align.MIN))
    part += _box(-P.SOCKET_ARM_HALF_W, P.SOCKET_ARM_HALF_W, 0,
                 P.SOCKET_ARM_LENGTH, 0, t)
    if side == "drive":
        part -= Pos(0, 0, t-P.SOCKET_RECESS_DEPTH) * Cylinder(
            P.SOCKET_HORN_RECESS/2, P.SOCKET_RECESS_DEPTH+1,
            align=(Align.CENTER, Align.CENTER, Align.MIN))
    holes = [(a, b, P.CLEAR_HOLE_M3) for a in (-P.SERVO_DRIVE_SQ/2, P.SERVO_DRIVE_SQ/2)
             for b in (-P.SERVO_DRIVE_SQ/2, P.SERVO_DRIVE_SQ/2)]
    holes += [(a, P.SOCKET_BRIDGE_Z, P.CLEAR_HOLE_M3)
              for a in (-P.SOCKET_BRIDGE_BOLT_Y, P.SOCKET_BRIDGE_BOLT_Y)]
    if side == "drive":
        holes.append((0, 0, P.SOCKET_CENTRE_CLEAR))
    for a, b, d in holes:
        part -= Pos(a, b, -1) * Cylinder(d/2, t+2,
            align=(Align.CENTER, Align.CENTER, Align.MIN))
    return part


def plate_location(side):
    """Place a flat cheek in the socket frame; recess bears on the metal horn."""
    from build123d import Plane
    floor = P.SOCKET_PLATE_T - P.SOCKET_RECESS_DEPTH
    if side == "drive":
        return Plane(origin=(P.SOCKET_DRIVE_FACE+floor, 0, P.SOCKET_AXIS_Z),
                     x_dir=(0, -1, 0), z_dir=(-1, 0, 0)).location
    if side == "idler":
        # Upstream nominal idler is flush: recessing this cheek would drive
        # its annulus into the case. Full flat contact, no invented stand-off.
        return Plane(origin=(P.SOCKET_IDLER_FACE-P.SOCKET_PLATE_T, 0, P.SOCKET_AXIS_Z),
                     x_dir=(0, 1, 0), z_dir=(1, 0, 0)).location
    raise ValueError("side must be 'drive' or 'idler'")


_ST3215_STEP = __import__('pathlib').Path(__file__).resolve().parents[2] / 'vendor' / 'st3215' / 'STS3215_c.step'
_ST3215_BOTTOM_X = 35.1117   # model frame: Bottom face at X=+35.11, Top at X=-10.11, axis at X=0
_ST3215_POCKET_SHIFT = 0.4   # model widest faces sit at Y -17.9 / +17.1: shift +0.4 centres the pocket


@lru_cache
def case_model() -> Part | None:
    """The bare STS3215 case from vendor/st3215/STS3215_c.step, in the socket frame.

    Model frame -> socket frame: model +Y (drive side) -> Front +X; model Z
    (Sides) -> -Y; model X (height, Bottom at +35.11) -> Z with the Bottom at
    Z=0. Only the three case solids ('Middle', 'Top', 'Bottom' in the file) are
    used; the file's horns, screws, connectors and label are dropped because
    its horn stack is 0.85 wider than the measured 36.4 (test-log 2026-09-08)
    and the koala horn stack comes from calipers instead. None if the file is
    absent, and socket_reference() falls back to the parametric profile.
    """
    if not _ST3215_STEP.exists():
        return None
    from build123d import import_step, Plane
    model = import_step(str(_ST3215_STEP))
    loc = Plane(origin=(_ST3215_POCKET_SHIFT, 0, _ST3215_BOTTOM_X),
                x_dir=(0, 0, -1), z_dir=(0, -1, 0)).location
    part = None
    for child in model.children:
        if child.label in ('Middle', 'Top', 'Bottom'):
            for s in child.solids():
                part = s if part is None else part + s
    return loc * part


def _parametric_case() -> Part:
    """Fallback stepped profile from the caliper constants (conservative)."""
    y, off, L = P.SOCKET_CASE_Y/2, P.SOCKET_SEAT_OFFSET, P.SOCKET_CASE_L
    seat_f, seat_b = off + P.SOCKET_HORN_SEAT_X/2, off - P.SOCKET_HORN_SEAT_X/2
    ear_f, ear_b = off + P.SOCKET_EAR_X/2, off - P.SOCKET_EAR_X/2
    wide = P.SOCKET_CASE_X/2
    zA, zB = P.SOCKET_REGION_Z
    pad = P.SOCKET_WIDE_PAD_Y/2
    part = _box(ear_b, ear_f, -y, y, 0, zB)          # ear plane over the whole Bottom region
    part += _box(-wide, wide, -pad, pad, zA, zB)     # widest: a centred pad the pocket grips
    part += _box(seat_b, seat_f, -y, y, zB, L)       # seat level to the Top (conservative)
    return part


@lru_cache
def socket_reference():
    """Case (vendor STEP, or the parametric profile) plus the MEASURED horn stack.

    Pocket frame: X=0 is the pocket centre; the seat mid-plane sits
    SOCKET_SEAT_OFFSET toward the Front. The idler (3.1) plus the servo boss
    (0.7 proud) sit on the Back seat; the drive horn plus its pan-head centre
    screw sit on the Front seat (test-log 2026-09-08).
    """
    off = P.SOCKET_SEAT_OFFSET
    seat_f, seat_b = off + P.SOCKET_HORN_SEAT_X/2, off - P.SOCKET_HORN_SEAT_X/2
    part = case_model()
    if part is None:
        part = _parametric_case()
    z = P.SOCKET_AXIS_Z
    part += _x_hole(P.SOCKET_IDLER_FACE, seat_b, 0, z, P.SOCKET_HORN_DIA)           # idler
    part += _x_hole(P.SOCKET_IDLER_FACE - P.SOCKET_IDLER_BOSS_PROUD,
                    P.SOCKET_IDLER_FACE, 0, z, P.SOCKET_BOSS_DIA)                   # servo boss
    part += _x_hole(seat_f, P.SOCKET_DRIVE_FACE, 0, z, P.SOCKET_HORN_DIA)           # drive horn
    part += _x_hole(P.SOCKET_DRIVE_FACE, P.SOCKET_DRIVE_FACE + P.HORN_SCREW_HEAD_H,
                    0, z, P.HORN_SCREW_HEAD_DIA)                                     # its pan head
    return part


def socket_keepouts():
    """Separate volumes for case/horns, straight drivers and a cable corridor.

    Access is checked before the driven plates are fitted. Driver envelopes
    stop at the head seats, not inside the screw shaft holes.
    """
    x, y = _socket_bounds()
    result = [("case_and_horns", socket_reference())]
    for cy in (-P.SOCKET_LUG_Y, P.SOCKET_LUG_Y):
        result += [
            ("idler_lug_driver", _x_hole(-x-35, -x-P.SOCKET_M2_SEAT,
              cy, P.SOCKET_LUG_BACK_Z, P.SOCKET_M2_HEAD)),
            ("drive_lug_driver", _x_hole(x+P.SOCKET_M2_SEAT, x+35,
              cy, P.SOCKET_LUG_DRIVE_Z, P.SOCKET_M2_HEAD)),
        ]
    result.append(("cable", _box(-P.SOCKET_CABLE_W/2, P.SOCKET_CABLE_W/2,
                   0, y+12, -P.SOCKET_SHELF, 0)))
    return result
