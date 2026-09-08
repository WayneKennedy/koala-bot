# SPDX-License-Identifier: CERN-OHL-S-2.0
"""New serial-link master geometry. Native X output axis, +Z down the link.

Every proximal fork uses servo_iface.clevis_plate on BOTH horns. Cradles and
collars are the same primitive at hip roll, hip pitch and knee. Flat cheeks
bolt against crossbars; seams have concentric registration shoulders.
"""
from functools import lru_cache
from math import cos, sin, radians
from build123d import Align, Cylinder, Plane, Pos, Rot
from .. import params as P, servo_iface as S
from . import joint_rig as J

B0, B1 = J.BRIDGE_MIN_X, J.BRIDGE_MAX_X
AXIS = Pos(0, 0, -P.SOCKET_AXIS_Z)


def fork(side):
    return AXIS * S.plate_location(side) * S.clevis_plate(side)


def _crossbar():
    return AXIS * J.bridge()


def _crossbar_holes(part):
    for y in (-P.SOCKET_BRIDGE_BOLT_Y, P.SOCKET_BRIDGE_BOLT_Y):
        part -= S._x_hole(B0-1, B1+1, y, P.SOCKET_BRIDGE_Z, P.CLEAR_HOLE_M3)
    return part


def _register(part, positions):
    # A broad rectangular shoulder gives registration AND a >=300 mm² flat
    # print footprint. Small pegs alone would stand the entire core on pinpoints.
    if any(y for y, _ in positions):
        part += S._box(B0-P.V2_REGISTER_H, B1+P.V2_REGISTER_H,
                       -10, 10, P.SOCKET_BRIDGE_Z-8, P.SOCKET_BRIDGE_Z+8)
    for y, z in positions:
        if y == 0:
            part += S._x_hole(B0-P.V2_REGISTER_H, B1+P.V2_REGISTER_H,
                              y, z, P.V2_REGISTER_DIA)
        part -= S._x_hole(B0-P.V2_REGISTER_H-1, B1+P.V2_REGISTER_H+1,
                          y, z, P.CLEAR_HOLE_M3)
    return part


def registered_fork(side):
    part = fork(side)
    x0, x1 = ((B1, B1+P.V2_REGISTER_H) if side == 'drive'
              else (B0-P.V2_REGISTER_H, B0))
    c = P.V2_REGISTER_CLEAR/2
    part -= S._box(x0, x1, -10-c, 10+c,
                   P.SOCKET_BRIDGE_Z-8-c, P.SOCKET_BRIDGE_Z+8+c)
    return part


@lru_cache
def thigh_core():
    rear = P.V2_THIGH-P.SOCKET_AXIS_Z
    c = P.V2_CORE_HALF
    part = _crossbar() + S._box(-c, c, -c, c, P.SOCKET_BRIDGE_Z, rear)
    part += Pos(0, 0, rear) * (S.cradle() + S.rear_support(
        P.SOCKET_BRIDGE_Z+P.SOCKET_BRIDGE_H/2-rear, c, c))
    part -= S._box(-P.SOCKET_CABLE_W/2, P.SOCKET_CABLE_W/2, 0, c+2,
                   rear-P.SOCKET_SHELF-1, rear+1)
    part = _crossbar_holes(part)
    return _register(part, [(y, P.SOCKET_BRIDGE_Z) for y in
                            (-P.SOCKET_BRIDGE_BOLT_Y, P.SOCKET_BRIDGE_BOLT_Y)])


@lru_cache
def shank_core():
    c = P.V2_CORE_HALF
    part = _crossbar() + S._box(B0, B1, -c, c,
                               P.SOCKET_BRIDGE_Z, P.V2_MOTOR_BOLTS_Z[-1]+4)
    part = _crossbar_holes(part)
    return _register(part,
        [(y, P.SOCKET_BRIDGE_Z) for y in (-P.SOCKET_BRIDGE_BOLT_Y, P.SOCKET_BRIDGE_BOLT_Y)]
        + [(0, z) for z in P.V2_MOTOR_BOLTS_Z])


@lru_cache
def motor_plate(drive):
    # Drawing XY -> native YZ. Mating face at drawing Z=0, counterbores up
    # after flipping for the declared print orientation.
    t = P.V2_MOTOR_PLATE_T
    part = Pos(0, P.V2_SHANK) * Cylinder(P.V2_MOTOR_PLATE_R, t,
        align=(Align.CENTER, Align.CENTER, Align.MIN))
    part += S._box(-P.V2_CORE_HALF, P.V2_CORE_HALF,
                   P.V2_MOTOR_BOLTS_Z[0]-7, P.V2_SHANK, 0, t)
    holes = [(0, z, P.CLEAR_HOLE_M3) for z in P.V2_MOTOR_BOLTS_Z]
    holes.append((0, P.V2_SHANK, P.MOTOR_FACE_BOSS_DIA+1 if drive
                  else P.MOTOR_DIA+2*P.CLEAR_POCKET))
    if drive:
        for i in range(P.MOTOR_FACE_SCREWS):
            a = radians(i*60+30)
            holes.append((P.MOTOR_BCD/2*cos(a), P.V2_SHANK+P.MOTOR_BCD/2*sin(a),
                          P.CLEAR_HOLE_M3))
    for y, z, d in holes:
        part -= Pos(y, z, -1) * Cylinder(d/2, t+2,
            align=(Align.CENTER, Align.CENTER, Align.MIN))
    for z in P.V2_MOTOR_BOLTS_Z:
        part -= Pos(0, z, -1) * Cylinder((P.V2_REGISTER_DIA+P.V2_REGISTER_CLEAR)/2,
            P.V2_REGISTER_H+1, align=(Align.CENTER, Align.CENTER, Align.MIN))
    loc = Plane(origin=(B1 if drive else B0, 0, 0), x_dir=(0, 1 if drive else -1, 0),
                z_dir=(1 if drive else -1, 0, 0)).location
    return loc * part


# Orthogonal hip carrier is in roll-axis coordinates, already rotated into
# its outward rest direction: X roll axis, +Y outboard, Z up.
PITCH_FRAME = Plane(origin=(P.V2_PITCH_REAR_X, P.V2_PITCH_Y, 0),
                    x_dir=(0, 1, 0), z_dir=(1, 0, 0)).location


@lru_cache
def hip_socket():
    c = P.V2_CORE_HALF
    part = PITCH_FRAME * S.cradle()
    part += S._box(P.V2_HIP_STEM_X, P.V2_PITCH_REAR_X,
                   P.V2_PITCH_Y-P.SOCKET_CASE_X/2-P.SOCKET_WALL,
                   P.V2_PITCH_Y+P.SOCKET_CASE_X/2+P.SOCKET_WALL,
                   -P.SOCKET_CASE_Y/2-P.SOCKET_WALL, P.SOCKET_CASE_Y/2)
    # Preserve the collar boss lanes through the extended rear support.
    for cy in (-P.SOCKET_LUG_Y,P.SOCKET_LUG_Y):
        x=P.SOCKET_CASE_X/2
        half=P.SOCKET_BOSS_W/2+P.SOCKET_BOSS_CLEAR
        part -= PITCH_FRAME*S._box(x-P.SOCKET_BOSS_CLEAR,x+P.SOCKET_WALL+1,
                                    cy-half,cy+half,-20,1)
    # Recessed carrier heads are installed BEFORE the pitch servo. Their
    # counterbores open at the rear-case seat, not behind an inaccessible wall.
    for z in (-P.SOCKET_BRIDGE_BOLT_Y, P.SOCKET_BRIDGE_BOLT_Y):
        part -= S._x_hole(P.V2_HIP_STEM_X-1, P.V2_PITCH_REAR_X+1,
                          P.V2_PITCH_Y, z, P.CLEAR_HOLE_M3)
        part -= S._x_hole(P.V2_PITCH_REAR_X-P.CAP_M3_H,
                          P.V2_PITCH_REAR_X+1, P.V2_PITCH_Y, z, P.CAP_M3_DIA+.3)
    return part


def _spec(name, part, orientation, notes, qty=2):
    handed = name in ('thigh_core', 'hip_pitch_cradle', 'servo_collar')
    count = qty//2 if handed else qty
    fasteners = {}
    if name in ('joint_drive_cheek','joint_idler_cheek'):
        fasteners = {'M3x6 horn-square screw (engagement to verify)': 4,
                     'Metal 9.9-square servo horn': 1}
        if name == 'joint_drive_cheek':
            fasteners['M3x6 horn centre screw (kit specification)'] = 1
    if name in ('thigh_core','hip_pitch_cradle','servo_collar'):
        fasteners['M2x5 self-tapper into servo lug'] = 2
    bolt = {'thigh_core':'M3x50','shank_core':'M3x50','hip_pitch_cradle':'M3x60'}.get(name)
    if bolt:
        fasteners[bolt+' crossbar screw'] = 2
        fasteners['M3 nut'] = 2
        fasteners['M3 plain washer'] = 2 if name == 'hip_pitch_cradle' else 4
    if name == 'wheel_foot_face':
        fasteners.update({'M3x8 motor-face screw (engagement to verify)': P.MOTOR_FACE_SCREWS,
                          'M3x55 motor-plate seam screw': len(P.V2_MOTOR_BOLTS_Z),
                          'M3 nut': len(P.V2_MOTOR_BOLTS_Z),
                          'M3 plain washer': 2*len(P.V2_MOTOR_BOLTS_Z)})
    return dict(name=name, part=part, orientation=orientation, qty=count,
                handed=handed, notes=notes, fasteners=fasteners)


def build_fork_drive():
    return _spec('joint_drive_cheek', registered_fork('drive'), Rot(Y=90),
        'Horn recess and registration pockets up; broad face on bed. Four M3x6 on drive horn. '
        'Two through-bolts per crossbar; no tightening against an unverified horn span.', qty=6)


def build_fork_idler():
    return _spec('joint_idler_cheek', registered_fork('idler'), Rot(Y=-90),
        'Flat idler seat; registration pockets up. Four M3x6 to idler horn, no centre hole.', qty=6)


def build_thigh():
    return _spec('thigh_core', thigh_core(), Rot(),
        'One crossbar, central spine and knee cradle. Crossbar end on bed; tapered support under the shelf. Axial/lateral strength needs tests. '
        'Two registered M3x50 through-bolts at proximal fork. Knee collar slides on separately.')


def build_shank():
    return _spec('shank_core', shank_core(), Rot(),
        'Spine and compression crossbar. Registered M3x50 fork bolts; M3x55 motor-plate bolts. '
        'Motor body remains clear of the spine; axial bore access before wheel installation.')


def build_motor_drive():
    return _spec('wheel_foot_face', motor_plate(True), Rot(Y=90),
        'Flat plate; registration pockets face up. Six M3x8 into motor face (3 mm nominal '
        'engagement); check bore depth. Install before hub/wheel. Direct drive fixed at ankle.')


def build_motor_idler():
    return _spec('wheel_foot_support', motor_plate(False), Rot(Y=-90),
        'Flat plate, registration pockets up. Motor-body bore uses separate coupon fit.')


def build_hip_socket():
    return _spec('hip_pitch_cradle', hip_socket(), Rot(Y=-90),
        'Rear mounting face on bed. Two M3x60 carrier bolts recessed under servo rear; '
        'fit bolts before servo. Cradle uses the shared SO-101 socket, not a friction cap.')


def build_hip_bridge():
    return _spec('hip_crossbar', Rot(X=-90)*_register(_crossbar(),
        [(y, P.SOCKET_BRIDGE_Z) for y in (-P.SOCKET_BRIDGE_BOLT_Y, P.SOCKET_BRIDGE_BOLT_Y)]),
        Rot(Y=-90), 'Registered crossbar between both roll cheeks; M3x60 crosses hip socket stem.')


def build_collar():
    return _spec('servo_collar', S.collar(), Rot(),
        'Sleeve rim on bed. Two M2x5 drive-face lug screws; idler-side driver ports. '
        'Shared unchanged at roll, pitch and knee.', qty=6)


BUILDERS = [build_fork_drive, build_fork_idler, build_thigh, build_shank,
            build_motor_drive, build_motor_idler, build_hip_socket, build_hip_bridge,
            build_collar]
