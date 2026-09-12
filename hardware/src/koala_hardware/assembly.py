# SPDX-License-Identifier: CERN-OHL-S-2.0
"""DEC-43 rear ankle drives and fixed front feet, with two dimensionally closed poses.

Head placement/mounting is undecided and is excluded from structural CAD.
Delta angles are inspection controls, not tested controller limits.
"""
from functools import lru_cache
from math import radians, sin, cos
from pathlib import Path
from build123d import Pos, Rot, Plane, mirror, Box, Align, Compound, export_step
from . import params as P, servo_iface as S, body_plan as B
from .parts import pelvis, links as L, e_tray, torso

ROOT=Path(__file__).resolve().parents[2]
GROUND_Z=0.0


def body_location(pose):
    return Pos(pose['rear'].root.x,0,pose['rear'].root.z)*Rot(Y=90-pose['body_angle'])


def segment_frame(a,b,y):
    return Plane(origin=(a.x,y,a.z),x_dir=(0,1,0),z_dir=(b.x-a.x,0,b.z-a.z)).location


def pivot(point,axis,angle):
    p=Pos(*point)
    # Pitch is lateral; downstream roll is perpendicular to the thigh in its sagittal plane.
    from build123d import Axis, Location
    return p*Location((0,0,0),axis,angle)*p.inverse()


def joint_data(pose_name='quadruped'):
    pose=B.poses()[pose_name];body=body_location(pose);out={}
    for key in ('rear','front'):
        limb=pose[key];front=key=='front';y=P.BODY_SHOULDER_WIDTH_MM/2 if front else L.rear_axis_y()
        dx=(limb.bend.x-limb.root.x)/limb.upper
        dz=(limb.bend.z-limb.root.z)/limb.upper
        out[key]={'roll':[limb.root.x,y,limb.root.z],'roll_axis':[-dz,0,dx],
                  'pitch':[limb.root.x,P.ROOT_PITCH_Y,limb.root.z],
                  'bend':[limb.bend.x,y,limb.bend.z]}
    return out


@lru_cache
def nominal_details(pose_name='quadruped'):
    pose=B.poses()[pose_name];body=body_location(pose)
    items=[]
    def add(n,p,c,g='fixed',side=0): items.append((n,p,c,g,side))
    for front in (False,True):
        tf=body*Pos(0,0,P.BODY_TORSO_LENGTH_MM if front else 0)
        for side in (1,-1):
            module=pelvis.module(front)
            add(('shoulder_socket' if front else 'pelvis_socket')+('_right' if side==1 else '_left'),
                tf*(module if side==1 else mirror(module,Plane.XZ)),'#8fb4d9')
    add('torso_frame',body*torso.solid(),'#8fb4d9')
    # All eight root-module bolts and nuts are modelled outside servo bodies.
    for front in (False,True):
        z0=P.ROOT_REAR_MOUNT_Z if not front else P.BODY_TORSO_LENGTH_MM-P.ROOT_MOUNT_Z-P.FRAME_PLATE_T
        for i,(x,y) in enumerate(P.ROOT_FRAME_HOLES):
            # Heads on the accessible servo side; nuts inside the open cage.
            zh=z0-3 if not front else z0+P.FRAME_PLATE_T
            zn=z0+P.FRAME_PLATE_T+5 if not front else z0-5-2.5
            heads=Pos(x,y,zh)*__import__('build123d').Cylinder(3,3,align=(Align.CENTER,Align.CENTER,Align.MIN))
            heads+=Pos(x,y,zn)*__import__('build123d').Cylinder(3.2,2.5,align=(Align.CENTER,Align.CENTER,Align.MIN))
            add(f'reference_{"shoulder" if front else "pelvis"}_frame_fixing_{i}',body*heads,'#aaaaaa')
    add('e_tray',body*e_tray.location()*e_tray.solid(),'#b4d98f')
    for i,(y,z) in enumerate(( (y,z) for y in (-26,26) for z in (torso.LOW+12,torso.HIGH-12))):
        add(f'tray_spacer_{i}',body*S._x_hole(-50,-46,y,z,7)-body*S._x_hole(-51,-45,y,z,P.CLEAR_HOLE_M3),'#b4d98f')
    for key in ('rear','front'):
        front=key=='front';limb=pose[key]
        y=P.BODY_SHOULDER_WIDTH_MM/2 if front else L.rear_axis_y()
        root=body*Pos(0,0,P.BODY_TORSO_LENGTH_MM if front else 0)
        upper=segment_frame(limb.root,limb.bend,y)
        lower=segment_frame(limb.bend,limb.axle,y)
        roll_frame=segment_frame(limb.root,limb.bend,0)*Rot(Z=-90)
        roll=roll_frame*Pos(0,y,0)
        knee=upper*Pos(0,0,limb.upper)
        group=lambda j:key+'_'+j
        local=[('carrier',roll_frame*L.carrier(),'#d9a48f','pitch'),
               ('reference_roll_servo',roll_frame*L.roll_socket_frame(y)*S.socket_reference(),'#e8d44d','pitch'),
               ('reference_pitch_servo',root*pelvis.pitch_socket(front)*S.socket_reference(),'#e8d44d','fixed'),
               ('upper_arm' if front else 'thigh',upper*L.upper_link(limb.upper),'#c98fd9','roll'),
               ('reference_elbow_servo' if front else 'reference_knee_servo',knee*L.AXIS*S.socket_reference(),'#e8d44d','roll'),
               ('forearm' if front else 'shank',lower*L.lower_link(limb.lower,front),'#8fd9c9','bend')]
        for label,tf,g in [('roll',roll,'roll'),('pitch',roll_frame*L.pitch_fork_frame(),'pitch'),('bend',lower,'bend')]:
            local.append(('reference_'+label+'_horn_heads',tf*S.horn_head_envelopes(),'#aaaaaa',g))
        for label,tf,g in [('roll',roll_frame*L.roll_socket_frame(y),'pitch'),('pitch',root*pelvis.pitch_socket(front),'fixed'),('bend',knee*L.AXIS,'roll')]:
            local.append(('reference_'+label+'_ear_heads',tf*S.ear_head_envelopes(),'#aaaaaa',g))
        if front:
            local.append(('contact_pad',lower*L.front_pad(),'#555f66','bend'))
            # Recessed pad screw/washer plus the captive metal nut (no plastic thread).
            from build123d import Cylinder,RegularPolygon,extrude
            pad_fix=Pos(0,0,110)*Cylinder(3,2.5,align=(Align.CENTER,Align.CENTER,Align.MIN))
            pad_fix+=Pos(0,0,P.FRONT_PAD_NUT_Z)*extrude(RegularPolygon(3.175,6,rotation=30),amount=2.4)
            local.append(('reference_pad_fixing',lower*pad_fix,'#aaaaaa','bend'))
        if not front:
            face=L.motor_face(front)
            from build123d import Compound
            heads=[]
            for i in range(6):
                a=radians(60*i+30)
                heads.append(S._x_hole(face+P.MOTOR_MOUNT_T,face+P.MOTOR_MOUNT_T+P.CAP_M3_H,P.MOTOR_BCD/2*cos(a),limb.lower+P.MOTOR_BCD/2*sin(a),P.CAP_M3_DIA))
            local.append(('reference_motor_heads',lower*Compound(children=heads),'#aaaaaa','bend'))
            for name,x0,x1,dia,col in [
                ('motor',face-P.MOTOR_BODY_LEN,face,P.MOTOR_DIA,'#777777'),
                ('shaft',face,face+P.MOTOR_SHAFT_LEN,P.MOTOR_SHAFT_DIA,'#aaaaaa'),
                ('hub',face+P.HUB_STACK-P.HUB_T,face+P.HUB_STACK,P.HUB_DIA,'#bbbbbb'),
                ('wheel',face+P.HUB_STACK,face+P.HUB_STACK+P.WHEEL_W,P.WHEEL_DIA,'#555555')]:
                local.append((name,lower*S._x_hole(x0,x1,0,limb.lower,dia),col,'bend'))
        for side in (1,-1):
            for name,p,c,g in local:
                n=(f'reference_{key}_'+name.removeprefix('reference_') if name.startswith('reference_') else key+'_'+name)
                add(n+('_right' if side==1 else '_left'),p if side==1 else mirror(p,Plane.XZ),c,group(g),side)
    # Head placement is unresolved: the old placeholder is not a CAD obstacle.
    return items


def joint_transform(d,j,roll=0.,pitch=0.,knee=0.):
    """Canonical right-hand hierarchy; callers mirror the whole result left."""
    ht=pivot(d['pitch'],(0,1,0),pitch)
    rt=pivot(d['roll'],d['roll_axis'],roll)
    kt=pivot(d['bend'],(0,1,0),knee)
    return {'fixed':Pos(),'pitch':ht,'roll':ht*rt,'bend':ht*rt*kt}[j]


def scene_details(roll=0.,pitch=0.,knee=0.,pose='quadruped',asymmetric=False):
    joints=joint_data(pose);out=[]
    for n,p,c,g,side in nominal_details(pose):
        if side:
            key,j=g.split('_',1);d=joints[key]
            # Transform the canonical right side then mirror, matching the STL hand.
            if side==-1:p=mirror(p,Plane.XZ)
            sign=-1 if asymmetric and side==-1 else 1
            tf=joint_transform(d,j,roll,sign*pitch,sign*knee)
            p=tf*p
            if side==-1:p=mirror(p,Plane.XZ)
        out.append((n,p,c,g,side))
    return out


def build_scene(roll=0.,pitch=0.,knee=0.,pose='quadruped'):
    return [(n,p,c) for n,p,c,_,_ in scene_details(roll,pitch,knee,pose)]


def main():
    out=ROOT/'build/step';out.mkdir(parents=True,exist_ok=True)
    for pose in B.poses():
        children=[]
        for n,s,c in build_scene(pose=pose):
            s=s.moved(Pos());s.label=n;children.append(s)
        export_step(Compound(children=children),out/f'koala-{pose}.step')
        print('wrote',out/f'koala-{pose}.step',flush=True)


if __name__=='__main__':main()


def socket_frames(pose_name):
    """Right-side case datums and their owning print, for fit/access checks."""
    pose=B.poses()[pose_name];body=body_location(pose);out=[]
    for key in ('rear','front'):
        front=key=='front';limb=pose[key];y=P.BODY_SHOULDER_WIDTH_MM/2 if front else L.rear_axis_y()
        root=body*Pos(0,0,P.BODY_TORSO_LENGTH_MM if front else 0)
        upper=segment_frame(limb.root,limb.bend,y)
        roll_frame=segment_frame(limb.root,limb.bend,0)*Rot(Z=-90)
        out.extend([
            (f'reference_{key}_pitch_servo_right','shoulder_socket_right' if front else 'pelvis_socket_right',root*pelvis.pitch_socket(front)),
            (f'reference_{key}_roll_servo_right',f'{key}_carrier_right',roll_frame*L.roll_socket_frame(y)),
            (f'reference_{key}_'+('elbow' if front else 'knee')+'_servo_right',f'{key}_'+('upper_arm' if front else 'thigh')+'_right',upper*Pos(0,0,limb.upper)*L.AXIS)])
    return out
