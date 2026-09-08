# SPDX-License-Identifier: CERN-OHL-S-2.0
"""DEC-34 lower body with roll -> pitch -> knee -> wheel-foot transforms.

Angles are geometric poses, not controller limits. Hip positive advances the
knee; knee positive folds the shank aft. Ground metadata is the nominal pose.
"""
from math import cos, radians
from build123d import Align, Cylinder, Plane, Pos, Rot, mirror
from . import params as P, servo_iface as S
from .parts import pelvis, links as L, e_tray

ROOT = __import__('pathlib').Path(__file__).resolve().parents[2]
ROLL_Z = -P.V2_ROLL_DROP
PITCH_Z = ROLL_Z
WHEEL_Z = PITCH_Z - P.V2_THIGH*cos(radians(P.V2_HIP_NOMINAL)) - P.V2_SHANK*cos(radians(P.V2_HIP_NOMINAL-P.V2_KNEE_NOMINAL))
GROUND_Z = WHEEL_Z-P.WHEEL_DIA/2
PITCH_ORIGIN = (P.V2_PITCH_X, P.V2_PITCH_Y, 0.)
# Socket orientation: X native = Y robot, Y native = Z robot, Z native = X robot.
PITCH_FRAME = Plane(origin=PITCH_ORIGIN, x_dir=(0,1,0), z_dir=(1,0,0)).location


def leg_parts():
    """Right-leg solids in roll coordinates at the nominal pose, plus groups."""
    items = []
    def add(name, part, colour, group):
        items.append((name, part, colour, group))
    for side in ('drive', 'idler'):
        add('hip_roll_'+side, Rot(X=-90)*L.registered_fork(side), '#d9a48f', 'roll')
    add('hip_crossbar', L.build_hip_bridge()['part'], '#d9a48f', 'roll')
    add('hip_pitch_cradle', L.hip_socket(), '#d9a48f', 'roll')
    add('hip_pitch_collar', L.PITCH_FRAME*S.collar(), '#d9a48f', 'roll')
    add('reference_roll_servo', Rot(X=180)*L.AXIS*S.socket_reference(), '#e8d44d', 'fixed')
    add('roll_collar', Rot(X=180)*L.AXIS*S.collar(), '#d9a48f', 'fixed')
    add('reference_pitch_servo', PITCH_FRAME*L.AXIS*S.socket_reference(), '#e8d44d', 'roll')
    thigh_tf = PITCH_FRAME*Rot(X=90-P.V2_HIP_NOMINAL)
    knee_tf = thigh_tf*Pos(0,0,P.V2_THIGH)
    shank_tf = knee_tf*Rot(X=P.V2_KNEE_NOMINAL)
    for side in ('drive','idler'):
        add('thigh_'+side, thigh_tf*L.registered_fork(side), '#c98fd9', 'pitch')
        add('shank_'+side, shank_tf*L.registered_fork(side), '#8fd9c9', 'knee')
    add('thigh_core', thigh_tf*L.thigh_core(), '#c98fd9', 'pitch')
    add('knee_collar', knee_tf*L.AXIS*S.collar(), '#c98fd9', 'pitch')
    add('reference_knee_servo', knee_tf*L.AXIS*S.socket_reference(), '#e8d44d', 'pitch')
    add('shank_core', shank_tf*L.shank_core(), '#8fd9c9', 'knee')
    add('wheel_foot_face', shank_tf*L.motor_plate(True), '#8fd9c9', 'knee')
    add('wheel_foot_support', shank_tf*L.motor_plate(False), '#8fd9c9', 'knee')
    face, z = P.V2_MOTOR_FACE, P.V2_SHANK
    for name, x0, x1, dia, colour in [
        ('motor',face-P.MOTOR_BODY_LEN,face,P.MOTOR_DIA,'#777777'),
        ('shaft',face,face+P.MOTOR_SHAFT_LEN,P.MOTOR_SHAFT_DIA,'#aaaaaa'),
        ('hub',face+P.HUB_STACK-P.HUB_T,face+P.HUB_STACK,P.HUB_DIA,'#bbbbbb'),
        ('wheel',face+P.HUB_STACK,face+P.HUB_STACK+P.WHEEL_W,P.WHEEL_DIA,'#555555')]:
        add(name,shank_tf*S._x_hole(x0,x1,0,z,dia),colour,'knee')
    return items


def motion(roll=0., hip=P.V2_HIP_NOMINAL, knee=P.V2_KNEE_NOMINAL):
    """Delta transforms from nominal meshes; compose knee, hip, roll."""
    pitch_pos = Pos(*PITCH_ORIGIN)
    hip_tf = pitch_pos*Rot(Y=-(hip-P.V2_HIP_NOMINAL))*pitch_pos.inverse()
    k = (PITCH_FRAME*Rot(X=90-P.V2_HIP_NOMINAL)*Pos(0,0,P.V2_THIGH)).position
    kp = Pos(k.X,k.Y,k.Z)
    knee_tf = kp*Rot(Y=knee-P.V2_KNEE_NOMINAL)*kp.inverse()
    return {'fixed': Pos(), 'roll': Rot(X=roll),
            'pitch': Rot(X=roll)*hip_tf,
            'knee': Rot(X=roll)*hip_tf*knee_tf}


def scene_details(roll=0., hip=P.V2_HIP_NOMINAL, knee=P.V2_KNEE_NOMINAL):
    items = [('pelvis',pelvis.solid(),'#8fb4d9','fixed',0),
             ('e_tray',Pos(0,0,P.TRAY_GAP)*e_tray.solid(),'#b4d98f','fixed',0)]
    transforms = motion(roll,hip,knee)
    for side in (1,-1):
        for name, solid, colour, group in leg_parts():
            solid = transforms[group]*solid
            if side == -1:
                solid = mirror(solid,Plane.XZ)
            solid = Pos(P.V2_ROLL_X,side*P.V2_ROLL_Y,ROLL_Z)*solid
            items.append((name+('_right' if side==1 else '_left'),solid,colour,group,side))
    return items


def build_scene(roll=0., pitch=P.V2_HIP_NOMINAL, knee=P.V2_KNEE_NOMINAL):
    return [(n,s,c) for n,s,c,_,_ in scene_details(roll,pitch,knee)]


def main():
    # Reuse the export renderer so the saved assembly shows the same solids as the viewer.
    import tempfile
    import pathlib
    import trimesh
    from build123d import export_stl
    from .export import render
    meshes=[]
    with tempfile.TemporaryDirectory() as td:
        for i,(_,solid,_) in enumerate(build_scene()):
            path=pathlib.Path(td)/f'{i}.stl'
            export_stl(solid,str(path))
            meshes.append(trimesh.load(path,force='mesh'))
    out=ROOT/'build/renders/assembly.png';out.parent.mkdir(parents=True,exist_ok=True)
    render(trimesh.util.concatenate(meshes),out,'DEC-34 lower body — nominal geometry, fit/strength unverified')
    print(f'wrote {out}')


if __name__=='__main__':
    main()
