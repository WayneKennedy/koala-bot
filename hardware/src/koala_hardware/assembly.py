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
from .parts import pelvis, links as L, front as F, shoulder_mount as SM, neck_space, e_tray, torso

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
        out[key]={'order':['roll','pitch','bend'] if front else ['pitch','roll','bend'],
                  'roll':[limb.root.x,y,limb.root.z],'roll_axis':[-dz,0,dx],
                  'pitch':[limb.root.x,P.ROOT_PITCH_Y,limb.root.z],
                  'bend':[limb.bend.x,y,limb.bend.z]}
        if front:
            out[key]['roll']=list((body*Pos(0,P.SHOULDER_A_Y,P.BODY_TORSO_LENGTH_MM)).position)
            # Positive roll abducts the right forelimb in supported stance,
            # matching the rear command. The physical A shaft points down
            # the spine; motor calibration supplies that polarity reversal.
            out[key]['roll_axis']=list((body*Pos(0,0,1)).position-body.position)
            out[key]['pitch']=[limb.root.x,y,limb.root.z]
    return out


@lru_cache
def nominal_details(pose_name='quadruped'):
    pose=B.poses()[pose_name];body=body_location(pose)
    items=[]
    def add(n,p,c,g='fixed',side=0): items.append((n,p,c,g,side))
    for front in (False,True):
        tf=body*Pos(0,0,P.BODY_TORSO_LENGTH_MM if front else 0)
        for side in (1,-1):
            module=SM.module() if front else pelvis.module(False)
            add(('shoulder_socket' if front else 'pelvis_socket')+('_right' if side==1 else '_left'),
                (body if front else tf)*(module if side==1 else mirror(module,Plane.XZ)),'#8fb4d9')
            if front:
                mount=SM.solid();fixings=SM.frame_fixings()
                add('shoulder_mount_'+('right' if side==1 else 'left'),body*(mount if side==1 else mirror(mount,Plane.XZ)),'#8fb4d9')
                add('reference_shoulder_cassette_fixings_'+('right' if side==1 else 'left'),body*(fixings if side==1 else mirror(fixings,Plane.XZ)),'#aaaaaa')
    add('torso_frame',body*torso.solid(),'#8fb4d9')
    # DEC-53: sixteen root screws from the torso side and their captive nuts.
    for front in (False,True):
        tf=body*Pos(0,0,P.BODY_TORSO_LENGTH_MM if front else 0)
        env=SM.root_fixings() if front else pelvis.fixing_envelopes(False)
        for i,side in enumerate((1,-1)):
            add(f'reference_{"shoulder" if front else "pelvis"}_frame_fixing_{i}',(body if front else tf)*(env if side==1 else mirror(env,Plane.XZ)),'#aaaaaa')
    for name,solid,colour in neck_space.reference_items():add(name,body*solid,colour)
    add('e_tray',body*e_tray.location()*e_tray.solid(),'#b4d98f')
    for i,(y,z) in enumerate(( (y,z) for y in (-26,26) for z in (torso.LOW+12,torso.HIGH-12))):
        add(f'tray_spacer_{i}',body*S._x_hole(-50,-46,y,z,7)-body*S._x_hole(-51,-45,y,z,P.CLEAR_HOLE_M3),'#b4d98f')
    # Rear chain remains pitch -> roll -> knee, with its existing transforms.
    limb=pose['rear'];y=L.rear_axis_y()
    upper=segment_frame(limb.root,limb.bend,y)
    lower=segment_frame(limb.bend,limb.axle,y)
    roll_frame=segment_frame(limb.root,limb.bend,0)*Rot(Z=-90)
    roll=roll_frame*Pos(0,y,0)
    local=[('carrier',roll_frame*L.carrier(False),'#d9a48f','pitch'),
           ('reference_roll_servo',roll_frame*L.roll_socket_frame(y)*S.socket_reference(),'#e8d44d','pitch'),
           ('reference_pitch_servo',body*pelvis.pitch_socket(False)*S.socket_reference(),'#e8d44d','fixed'),
           ('thigh',upper*L.upper_link(limb.upper,True),'#c98fd9','roll'),
           ('reference_knee_servo',upper*L.knee_socket_frame(limb.upper,True)*S.socket_reference(),'#e8d44d','roll'),
           ('shank',lower*L.lower_link(limb.lower,False),'#8fd9c9','bend')]
    for label,tf,g in [('roll',roll,'roll'),('pitch',roll_frame*L.pitch_fork_frame(),'pitch'),('bend',lower,'bend')]:
        local.append(('reference_'+label+'_horn_heads',tf*S.horn_head_envelopes(),'#aaaaaa',g))
    for label,tf,g in [('roll',roll_frame*L.roll_socket_frame(y),'pitch'),('pitch',body*pelvis.pitch_socket(False),'fixed'),('bend',upper*L.knee_socket_frame(limb.upper,True),'roll')]:
        local.append(('reference_'+label+'_ear_heads',tf*S.ear_head_envelopes(),'#aaaaaa',g))
    face=L.motor_face(False)
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
            n=('reference_rear_'+name.removeprefix('reference_') if name.startswith('reference_') else 'rear_'+name)
            add(n+('_right' if side==1 else '_left'),p if side==1 else mirror(p,Plane.XZ),c,'rear_'+g,side)
    # Shoulder A follows the spine; B and C remain sagittal pitch joints.
    limb=pose['front'];y=P.BODY_SHOULDER_WIDTH_MM/2
    cf=body*SM.carrier_frame();upper=segment_frame(limb.root,limb.bend,y)
    lower=segment_frame(limb.bend,limb.axle,y)
    a_frame=body*SM.socket_frame();b_frame=cf*F.pitch_socket_frame();c_frame=upper*F.elbow_socket_frame(limb.upper)
    local=[('front_carrier',cf*F.carrier(),'#d9a48f','roll'),
           ('reference_front_roll_servo',a_frame*S.socket_reference(),'#e8d44d','fixed'),
           ('reference_front_pitch_servo',b_frame*S.socket_reference(),'#e8d44d','roll'),
           ('front_upper_arm',upper*F.upper_arm(limb.upper),'#c98fd9','pitch'),
           ('reference_front_elbow_servo',c_frame*S.socket_reference(),'#e8d44d','pitch'),
           ('front_forearm',lower*F.forearm(),'#8fd9c9','bend'),
           ('front_contact_pad',lower*L.front_pad(),'#555f66','bend')]
    for label,tf,g in [('roll',cf,'roll'),('pitch',upper,'pitch'),('bend',lower,'bend')]:
        local.append(('reference_front_'+label+'_horn_heads',tf*S.horn_head_envelopes(),'#aaaaaa',g))
    for label,tf,g in [('roll',a_frame,'fixed'),('pitch',b_frame,'roll'),('bend',c_frame,'pitch')]:
        local.append(('reference_front_'+label+'_ear_heads',tf*S.ear_head_envelopes(),'#aaaaaa',g))
    from build123d import Cylinder,Align,RegularPolygon,extrude
    pad_fix=Pos(0,0,110)*Cylinder(3,2.5,align=(Align.CENTER,Align.CENTER,Align.MIN))
    pad_fix+=Pos(0,0,P.FRONT_PAD_NUT_Z)*extrude(RegularPolygon(3.175,6,rotation=30),amount=2.4)
    local.append(('reference_front_pad_fixing',lower*pad_fix,'#aaaaaa','bend'))
    for side in (1,-1):
        for name,p,c,g in local:add(name+('_right' if side==1 else '_left'),p if side==1 else mirror(p,Plane.XZ),c,'front_'+g,side)
    # Neck items reserve catalogue-sized space; head/linkage acceptance remains open.
    return items


def joint_transform(d,j,roll=0.,pitch=0.,knee=0.):
    """Canonical right-hand hierarchy; callers mirror the whole result left."""
    ht=pivot(d['pitch'],(0,1,0),pitch)
    rt=pivot(d['roll'],d['roll_axis'],roll)
    kt=pivot(d['bend'],(0,1,0),knee)
    if j=='fixed':return Pos()
    result=Pos()
    for stage in d.get('order',['pitch','roll','bend']):
        result=result*{'pitch':ht,'roll':rt,'bend':kt}[stage]
        if stage==j:return result
    raise ValueError(f'Unknown joint stage {j}')


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
    limb=pose['rear'];y=L.rear_axis_y()
    upper=segment_frame(limb.root,limb.bend,y)
    roll_frame=segment_frame(limb.root,limb.bend,0)*Rot(Z=-90)
    out.extend([
        ('reference_rear_pitch_servo_right','pelvis_socket_right',body*pelvis.pitch_socket(False)),
        ('reference_rear_roll_servo_right','rear_carrier_right',roll_frame*L.roll_socket_frame(y)),
        ('reference_rear_knee_servo_right','rear_thigh_right',upper*L.knee_socket_frame(limb.upper,True))])
    limb=pose['front'];upper=segment_frame(limb.root,limb.bend,P.BODY_SHOULDER_WIDTH_MM/2)
    out.extend([
        ('reference_front_roll_servo_right','shoulder_socket_right',body*SM.socket_frame()),
        ('reference_front_pitch_servo_right','front_carrier_right',body*SM.carrier_frame()*F.pitch_socket_frame()),
        ('reference_front_elbow_servo_right','front_upper_arm_right',upper*F.elbow_socket_frame(limb.upper))])
    return out
