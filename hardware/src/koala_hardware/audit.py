# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Nominal CAD checks for DEC-40/41, not a continuous or tolerance-expanded proof."""
import argparse
import itertools
import json
from pathlib import Path
from unittest.mock import patch
from contextlib import nullcontext
from math import cos,sin,radians
from build123d import Pos,Rot,Plane,mirror,Cylinder,Align
from . import params as P,servo_iface as S,assembly as A,validation
from .parts import all_builders,links as L,pelvis,torso,e_tray


def volume(s):return sum(p.volume for p in s.solids()) if s is not None else 0.0


def overlap(a,b):
    if not bounds_overlap(a.bounding_box(optimal=False),b.bounding_box(optimal=False)):return 0.0
    return volume(a&b)


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


def check_scene(pose,angles=(0,0,0),static_cache=None,asymmetric=False):
    # Optimal BREP bounds are expensive for imported cases; calculate once.
    items=[(n,s,g,side,s.bounding_box(optimal=False)) for n,s,c,g,side in A.scene_details(*angles,pose=pose,asymmetric=asymmetric)]
    fits=fit_pairs(pose,angles,asymmetric);fail=[];count=0
    for (n,a,ga,sa,ba),(m,b,gb,sb,bb) in itertools.combinations(items,2):
        if not bounds_overlap(ba,bb):continue
        # Only coaxial purchased pieces of the SAME wheel intentionally overlap.
        if wheel_hardware(n) and wheel_hardware(m) and n.split('_')[0]==m.split('_')[0] and n.split('_')[-1]==m.split('_')[-1]:continue
        # Cache relative configurations, not just whole-scene angles. A common
        # rigid parent transform cannot change an intersection. Across different
        # limbs retain all three angles and the left/right asymmetry flag.
        common_limb=sa==sb and sa!=0 and ga.split('_')[0]==gb.split('_')[0]
        global_fixed=ga.endswith('fixed') and gb.endswith('fixed')
        if global_fixed:
            relative=()
        elif common_limb or ga=='fixed' or gb=='fixed':
            levels={'fixed':0,'pitch':1,'roll':2,'bend':3}
            lo,hi=sorted((levels[ga.split('_')[-1]],levels[gb.split('_')[-1]]))
            side=sa or sb
            effective=(angles[0],*(-a for a in angles[1:])) if asymmetric and side==-1 else angles
            relative=(effective[1],effective[0],effective[2])[lo:hi]
        else:
            relative=(*angles,asymmetric)
        key=(pose,n,m,relative)
        if static_cache is not None and key in static_cache:continue
        count+=1;hit=a&b;v=volume(hit)
        if v>.01:
            zone=fits.get(frozenset((n,m)))
            # Fitted reference, owning print and allowed contact region move together.
            if zone is None or v>50 or volume(hit-zone)>.01:
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
    # Each seam has actual face contact and a clear full-depth screw shaft.
    assert abs(torso.LOW-(P.ROOT_REAR_MOUNT_Z+P.FRAME_PLATE_T))<1e-9
    assert abs(torso.HIGH-(P.BODY_TORSO_LENGTH_MM-P.ROOT_MOUNT_Z-P.FRAME_PLATE_T))<1e-9
    assert torso.solid().distance_to(pelvis.solid())<1e-6
    assert torso.solid().distance_to(Pos(0,0,P.BODY_TORSO_LENGTH_MM)*pelvis.solid(True))<1e-6
    for x,y in P.ROOT_FRAME_HOLES:
        for z0,z1,base in [(P.ROOT_REAR_MOUNT_Z,torso.LOW+5,pelvis.solid()),(torso.HIGH-5,P.BODY_TORSO_LENGTH_MM-P.ROOT_MOUNT_Z,Pos(0,0,P.BODY_TORSO_LENGTH_MM)*pelvis.solid(True))]:
            shaft=Pos(x,y,z0-1)*Cylinder((P.CLEAR_HOLE_M3-.02)/2,z1-z0+2,align=(Align.CENTER,Align.CENTER,Align.MIN))
            clear(base,shaft,'crossmember bolt');clear(torso.solid(),shaft,'torso flange bolt')


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
