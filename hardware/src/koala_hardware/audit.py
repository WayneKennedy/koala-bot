# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Assembly and service-access CAD checks, not a continuous or tolerance-expanded proof."""
import argparse
import itertools
import json
from pathlib import Path
from unittest.mock import patch
from contextlib import nullcontext
from math import cos,sin,radians
from build123d import Pos,Rot,Plane,mirror,Cylinder,Align
from . import params as P,servo_iface as S,assembly as A,validation
from .parts import all_builders,links as L,pelvis,torso,e_tray,shoulder_mount


def volume(s):return sum(p.volume for p in s.solids()) if s is not None else 0.0


def overlap(a,b):
    if not bounds_overlap(a.bounding_box(optimal=False),b.bounding_box(optimal=False)):return 0.0
    # OCC compound booleans can omit touching hardware children. Test the
    # individual solids (notably separate screw heads and idler washers).
    return sum(volume(x&y) for x in a.solids() for y in b.solids()
               if bounds_overlap(x.bounding_box(optimal=False),y.bounding_box(optimal=False)))


def bounds_overlap(a,b):
    return all(min(h,k)-max(l,m)>1e-5 for l,h,m,k in zip(a.min,a.max,b.min,b.max))


def clear(a,b,label,tol=.01):
    v=overlap(a,b)
    assert v<=tol,f'{label}: {v:.3f} mm3'


def contact_zone():
    # The only tolerated STEP discrepancy is on the intended pocket contact.
    return S._box(-P.SOCKET_CASE_X/2-.2,P.SOCKET_CASE_X/2+.2,
                   -P.SOCKET_CASE_Y/2-.2,P.SOCKET_CASE_Y/2+.2,-.2,P.SOCKET_DEPTH+.2)


def check_socket():
    saddle=S.saddle();reference=S.socket_reference()
    hit=saddle&reference
    assert volume(hit)<=50, 'socket fit discrepancy exceeds retained 50 mm3 screen'
    assert volume(hit)<.01 or volume(hit-contact_zone())<.01, 'case intrusion outside the pocket contact region'
    for name,probe in S.socket_keepouts()[1:]:clear(saddle,probe,'saddle '+name)
    for side in ('drive','idler'):
        face=S.ear_face(side);z=P.SOCKET_LUG_DRIVE_Z if side=='drive' else P.SOCKET_LUG_BACK_Z
        for y in (-P.SOCKET_LUG_Y,P.SOCKET_LUG_Y):
            a,b=(face-.1,30) if side=='drive' else (-30,face+.1)
            clear(saddle,S._x_hole(a,b,y,z,P.SOCKET_M2_CLEAR-.02),'M2 through bore')
            # At the ear plane the wall actually bears, without the old mm gaps.
            a,b=(face,face+.15) if side=='drive' else (face-.15,face)
            probe=S._box(a,b,y+.8,y+1.4,z+1.1,z+1.6)
            assert overlap(saddle,probe)>.001,'missing ear bearing boss'
        plate=S.plate_location(side)*S.clevis_plate(side)
        for a in (-P.SERVO_DRIVE_SQ/2,P.SERVO_DRIVE_SQ/2):
            for b in (-P.SERVO_DRIVE_SQ/2,P.SERVO_DRIVE_SQ/2):
                clear(plate,S._x_hole(-30,30,a,P.SOCKET_AXIS_Z+b,P.CLEAR_HOLE_M3-.02),'horn full bore')
        # Supplied head plus narrow washer on Back: no unmodelled proud cap heads.
        flat=S.clevis_plate(side)
        offset=P.HORN_IDLER_WASHER_T if side=='idler' else 0
        for x in (-4.95,4.95):
            for y in (-4.95,4.95):
                head=Pos(x,y,P.SOCKET_PLATE_T+offset)*Cylinder(P.HORN_SCREW_HEAD_DIA/2,P.HORN_SCREW_HEAD_H,align=(Align.CENTER,Align.CENTER,Align.MIN))
                clear(flat,head,'supplied horn head')
                if offset:
                    washer=Pos(x,y,P.SOCKET_PLATE_T)*Cylinder(P.HORN_IDLER_WASHER_OD/2,offset,align=(Align.CENTER,Align.CENTER,Align.MIN))
                    clear(flat,washer,'idler washer')
    pivot=Pos(0,0,P.SOCKET_AXIS_Z)
    for angle in range(-90,91,10):
        fork=pivot*Rot(X=angle)*L.clevis()
        clear(fork,reference,f'rig fork/case {angle}')
        clear(fork,saddle,f'rig fork/saddle {angle}')
        clear(fork,dict(S.socket_keepouts())['cable'],f'rig Back exit {angle}')
    return {'socket_contact_mm3':round(volume(hit),4),'rig_angles':19,
            'nominal_M2_engagement_mm':5-P.SOCKET_M2_SEAT,
            'nominal_idler_engagement_mm':6-P.SOCKET_PLATE_T-P.HORN_IDLER_WASHER_T}


def fit_pairs(pose,angles=(0,0,0),asymmetric=False):
    # Transform the allowed contact region with its actual owning saddle.
    # This also makes an independently checked nonzero pose meaningful.
    out={};joints=A.joint_data(pose)
    groups={n:g for n,s,c,g,side in A.nominal_details(pose)}
    for ref,mount,tf in A.socket_frames(pose):
        key,j=groups[ref].split('_',1)
        for side in (1,-1):
            r,h,k=angles;sign=-1 if asymmetric and side==-1 else 1
            zone=A.joint_transform(joints[key],j,r,sign*h,sign*k)*tf*contact_zone()
            hand=lambda n:n if side==1 else n.replace('_right','_left')
            out[frozenset((hand(ref),hand(mount)))]=zone if side==1 else mirror(zone,Plane.XZ)
    return out


def wheel_hardware(n):return any('_'+s+'_' in n for s in ('motor','shaft','hub','wheel'))


def relative_configuration(joints,ga,sa,gb,sb,angles,asymmetric=False):
    """Joint values affecting a pair after cancelling its shared rigid prefix."""
    def chain(group,side):
        if not side or group.endswith('fixed'):return None,[]
        limb,joint=group.split('_',1)
        order=joints[limb].get('order',('pitch','roll','bend'))
        return limb,order[:order.index(joint)+1]
    limb_a,a=chain(ga,sa);limb_b,b=chain(gb,sb);common=0
    if sa==sb and limb_a==limb_b:
        while common<min(len(a),len(b)) and a[common]==b[common]:common+=1
    values=dict(zip(('roll','pitch','bend'),angles))
    return tuple((joint,-values[joint] if asymmetric and side==-1 and joint!='roll' else values[joint])
                 for stages,side in ((a,sa),(b,sb)) for joint in stages[common:])


def check_scene(pose,angles=(0,0,0),static_cache=None,asymmetric=False):
    # Optimal BREP bounds are expensive for imported cases; calculate once.
    items=[(n,s,g,side,s.bounding_box(optimal=False)) for n,s,c,g,side in A.scene_details(*angles,pose=pose,asymmetric=asymmetric)]
    fits=fit_pairs(pose,angles,asymmetric);joints=A.joint_data(pose);fail=[];count=0
    for (n,a,ga,sa,ba),(m,b,gb,sb,bb) in itertools.combinations(items,2):
        if not bounds_overlap(ba,bb):continue
        # Only coaxial purchased pieces of the SAME wheel intentionally overlap.
        if wheel_hardware(n) and wheel_hardware(m) and n.split('_')[0]==m.split('_')[0] and n.split('_')[-1]==m.split('_')[-1]:continue
        relative=relative_configuration(joints,ga,sa,gb,sb,angles,asymmetric)
        key=(pose,n,m,relative)
        if static_cache is not None and key in static_cache:continue
        count+=1
        hits=[x&y for x in a.solids() for y in b.solids()
              if bounds_overlap(x.bounding_box(optimal=False),y.bounding_box(optimal=False))]
        v=sum(volume(hit) for hit in hits)
        if v>.01:
            zone=fits.get(frozenset((n,m)))
            # Fitted reference, owning print and allowed contact region move together.
            if zone is None or v>50 or sum(volume(hit-zone) for hit in hits if volume(hit)>.000001)>.01:
                fail.append((n,m,round(v,3)))
        if static_cache is not None:static_cache.add(key)
    assert not fail,f'{pose} {angles}: {fail}'
    return count


def check_motor_insertion():
    for length,front in [(P.BODY_SHANK_MM,False)]:
        p=L.lower_link(length,front);face=L.motor_face(front)
        for shift in (0,-10,-35,-75):
            clear(p,S._x_hole(face-P.MOTOR_BODY_LEN+shift,face+shift,0,length,P.MOTOR_DIA),'motor axial insertion')
        # Six straight tool approaches, before wheel/hub is fitted.
        for i in range(6):
            a=radians(60*i+30);y=P.MOTOR_BCD/2*cos(a);z=length+P.MOTOR_BCD/2*sin(a)
            clear(p,S._x_hole(face+P.MOTOR_MOUNT_T,face+40,y,z,P.CAP_M3_DIA+.3),'motor driver')
            clear(p,S._x_hole(face-1,face+P.MOTOR_MOUNT_T+1,y,z,P.CLEAR_HOLE_M3-.02),'motor screw bore')


def check_frame():
    """Bench root access and installed rear/front fixings, including the torso."""
    assert abs(torso.LOW-(P.ROOT_REAR_MOUNT_Z+P.ROOT_PLATE_T))<1e-9
    frame=torso.solid();rear_tf=pelvis.pitch_socket(False);front_tf=shoulder_mount.socket_frame()
    root_seat=-P.SOCKET_SHELF-P.ROOT_PLATE_T
    zhead=root_seat-P.FRAME_PLATE_T;z1=-(P.NUT_M3_T+P.NUT_POCKET_CLEAR)+.05
    right=[('rear module',pelvis.module(False)),('rear servo',rear_tf*S.socket_reference()),
           ('shoulder cassette',shoulder_mount.solid()),('front module',shoulder_mount.module()),
           ('front servo',front_tf*S.socket_reference())]
    obstacles=[('torso',frame)]+[(name+' '+hand,p if side==1 else mirror(p,Plane.XZ))
        for hand,side in (('right',1),('left',-1)) for name,p in right]

    def bearing(a,b,seat,direction,label):
        # A 0.1 mm slab on each side of the mating plane must contain broad
        # bearing material around the screw, not merely a tangent edge.
        for part,start in ((a,-.1),(b,0)):
            probe=seat*direction*Pos(0,0,start)*Cylinder(4,.1,align=(Align.CENTER,Align.CENTER,Align.MIN))
            assert overlap(part,probe)>3,label+' lacks a broad bearing seat'

    for label,tf,module,base in (('rear',rear_tf,pelvis.module(False),frame),
                                 ('front bench',front_tf,shoulder_mount.module(),shoulder_mount.solid())):
        assert module.distance_to(base)<1e-6,label+' module does not touch its flange'
        clear(base,module,label+' root interference')
        for name,probe in S.socket_keepouts()[1:]:clear(module,tf*probe,label+' module '+name)
        for shift in (0,5,15,25,50):
            clear(module,tf*Pos(0,0,shift)*S._parametric_case(),label+' module insertion')
        for a,b in pelvis.nut_xy():
            bearing(base,module,tf*Pos(a,b,root_seat),Pos(),label+' root')
            shaft=tf*Pos(a,b,zhead)*Cylinder((P.CLEAR_HOLE_M3-.02)/2,z1-zhead,align=(Align.CENTER,Align.CENTER,Align.MIN))
            driver=tf*Pos(a,b,zhead-40)*Cylinder(3,40,align=(Align.CENTER,Align.CENTER,Align.MIN))
            head=tf*Pos(a,b,zhead-3)*Cylinder(3,3,align=(Align.CENTER,Align.CENTER,Align.MIN))
            if label=='rear':
                for hand,side in (('right',1),('left',-1)):
                    for probe,kind in ((shaft,'shaft'),(head,'head'),(driver,'driver')):
                        probe=probe if side==1 else mirror(probe,Plane.XZ)
                        for name,part in obstacles:clear(part,probe,f'rear {hand} {name} {kind}')
            else:
                # Fit these recessed root screws before installing the cassette.
                for name,part in (('cassette',base),('module',module),('servo',tf*S.socket_reference())):
                    for probe,kind in ((shaft,'shaft'),(head,'head'),(driver,'driver')):
                        clear(part,probe,f'front bench {name} {kind}')

    clear(shoulder_mount.solid(),frame,'shoulder cassette/frame interference')
    for y,z in P.SHOULDER_CASSETTE_BOLTS:
        bearing(shoulder_mount.solid(),frame,Pos(26,y,z),Rot(Y=90),'shoulder cassette/frame')
        for hand,side in (('right',1),('left',-1)):
            # M3x20 measured from the X=36 under-head plane: include the
            # 4 mm protruding beyond the cassette's X=20 back/nut entrance.
            for probe,kind in ((S._x_hole(16,36,side*y,z,P.CLEAR_HOLE_M3-.02),'shaft'),
                               (S._x_hole(36,39,side*y,z,6),'head'),
                               (S._x_hole(36,76,side*y,z,6),'driver')):
                for name,part in obstacles:clear(part,probe,f'front {hand} {name} {kind}')


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--fallback',action='store_true');ap.add_argument('--nominal-only',action='store_true');args=ap.parse_args()
    context=patch.object(S,'case_model',return_value=None) if args.fallback else nullcontext()
    with context:
        validation.check_layout()
        parts=[]
        for f in all_builders():
            d=f();p=d['part'];assert p.is_valid and (d.get('multi_body') or len(p.solids())==1),d['name']
            assert all(0<v<=200.001 for v in (d['orientation']*p).bounding_box().size),d['name']
            parts.append(d['name'])
        result=check_socket();print('PASS socket',result,flush=True)
        check_motor_insertion();check_frame();print('PASS motor insertion, screws and frame seams',flush=True)
        cache=set();samples=[]
        angles=[(0,0,0)]
        if not args.nominal_only:angles += [q for q in itertools.product((-5,0,5),repeat=3) if q!=(0,0,0)]
        for pose in ('quadruped','upright'):
            for q in angles:
                count=check_scene(pose,q,cache);samples.append({'pose':pose,'delta_degrees':q,'boolean_pairs':count})
                print('PASS assembly',pose,q,count,'pairs',flush=True)
            if not args.nominal_only:
                for h,k in itertools.product((-5,5),repeat=2):
                    q=(-5,h,k)
                    count=check_scene(pose,q,cache,asymmetric=True)
                    samples.append({'pose':pose,'delta_degrees':q,'opposed_left_pitch_bend':True,'boolean_pairs':count})
                    print('PASS asymmetric',pose,q,count,'pairs',flush=True)
        result.update({'reference':'parametric' if args.fallback else ('STEP + measured stack' if S.case_model() is not None else 'parametric'),
                       'part_designs':len(parts),'assembly_samples':samples,
                       'limits':'Nominal geometry only; no continuous sweep, tolerance expansion, complete loom, slices or physical load acceptance.'})
        out=A.ROOT/'build'/('audit-fallback.json' if args.fallback else 'audit.json');out.parent.mkdir(exist_ok=True);out.write_text(json.dumps(result,indent=2)+'\n')
        print('PASS',out,flush=True)


if __name__=='__main__':main()
