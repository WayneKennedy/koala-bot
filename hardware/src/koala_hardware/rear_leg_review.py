# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Rear-leg clearance and viewer for the DEC-57 proposed 45-degree A/B mount.

Run from hardware: .venv/bin/python -m koala_hardware.rear_leg_review
The completed torso, front legs, cables and loaded locomotion are outside this
review. The main assembly retains its previous torso mounting datum.
"""
from functools import lru_cache
from pathlib import Path
from itertools import combinations
from math import radians, cos, sin
from unittest.mock import patch
import argparse
import hashlib
import json
import shutil
import subprocess
import tempfile
from build123d import Pos, Rot, Plane, mirror, Compound, export_step
from . import assembly as A, body_plan as B, params as P, servo_iface as S, audit
from .parts import links as L, pelvis
from .pitch_socket_tilt_study import mount_face, socket_frame

ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'docs/design/rear-leg'
LIVE=ROOT/'hardware/build/viewer/rear-leg'
OUT_OPT=ROOT/'docs/design/rear-leg/thigh-options'
OUT_FLAT=ROOT/'docs/design/rear-leg/thigh-flat'
THIGH_OPTIONS=False   # --thigh-options: left leg = option 1 frame thigh, right leg = option 2 split thigh
THIGH_FLAT=False      # --thigh-flat: both legs = option 3, the owner's one-piece tapered thigh (2026-09-19)


def out_dir():return OUT_FLAT if THIGH_FLAT else OUT_OPT if THIGH_OPTIONS else OUT


def flat_thighs(pose):
    limb=B.poses()[pose]['rear'];upper=A.segment_frame(limb.root,limb.bend,L.rear_axis_y())
    flat=L.rear_thigh_flat(P.BODY_THIGH_MM)
    return [('rear_thigh_right',upper*flat,'#c98fd9','rear_roll',1),('rear_thigh_left',mirror(upper*flat,Plane.XZ),'#c98fd9','rear_roll',-1)]


MOTOR_ITEMS=('rear_motor','rear_shaft','rear_hub','rear_wheel','reference_rear_motor_heads')


def flush_shanks(pose,items):
    """Both shanks with the motor inset (owner's shank option); the bought motor stack moves inboard with it."""
    limb=B.poses()[pose]['rear'];lower=A.segment_frame(limb.bend,limb.axle,L.rear_axis_y())
    shank=L.lower_link(P.BODY_SHANK_MM,False,P.SHANK_MOTOR_INSET);shift=lower*Pos(-P.SHANK_MOTOR_INSET,0,0)*lower.inverse()
    out=[]
    for n,s,c,g,side in items:
        base=n.removesuffix('_right').removesuffix('_left')
        if base=='rear_shank':s=lower*shank if side>0 else mirror(lower*shank,Plane.XZ)
        elif base in MOTOR_ITEMS:s=shift*s if side>0 else mirror(shift*mirror(s,Plane.XZ),Plane.XZ)
        out.append((n,s,c,g,side))
    return out


def option_thighs(pose):
    """Replacement rear-thigh items for the two print-form options (2026-09-19 review)."""
    limb=B.poses()[pose]['rear'];upper=A.segment_frame(limb.root,limb.bend,L.rear_axis_y())
    body,cheek=L.rear_thigh_split(P.BODY_THIGH_MM);frame=L.rear_thigh_frame(P.BODY_THIGH_MM)
    return [('rear_thigh_right',upper*body,'#c98fd9','rear_roll',1),
            ('rear_thigh_cheek_right',upper*cheek,'#f0b8ff','rear_roll',1),
            ('reference_rear_thigh_lap_fixings_right',upper*L.thigh_lap_fixings(),'#aaaaaa','rear_roll',1),
            ('rear_thigh_left',mirror(upper*frame,Plane.XZ),'#c98fd9','rear_roll',-1)]


def frames(pose):
    # DEC-61: the assembly's own frames already carry the 45 degree rear mount.
    return [(n,m,tf) for n,m,tf in A.socket_frames(pose) if '_rear_' in n]


@lru_cache
def nominal(pose):
    out=[]
    for n,s,c,g,side in A.nominal_details(pose):
        if not (n.startswith(('rear_','reference_rear_','pelvis_socket_','reference_pelvis_','torso_frame'))):continue
        out.append((n,s,c,g,side))
    if THIGH_OPTIONS:out=[o for o in out if not o[0].startswith('rear_thigh_')]+option_thighs(pose)
    elif THIGH_FLAT:out=flush_shanks(pose,[o for o in out if not o[0].startswith('rear_thigh_')]+flat_thighs(pose))
    return out


def details(pose='quadruped',roll=0,pitch=0,knee=0):
    out=[];d=A.joint_data(pose)['rear']
    for n,s,c,g,side in nominal(pose):
        if side:
            if side<0:s=mirror(s,Plane.XZ)
            s=A.joint_transform(d,g.split('_')[-1],roll,pitch,knee)*s
            if side<0:s=mirror(s,Plane.XZ)
        out.append((n,s,c,g,side))
    return out


def collisions(pose='quadruped',roll=0,pitch=0,knee=0,cache=None):
    """All rear solids, including rigid hardware pairs and both legs."""
    data=details(pose,roll,pitch,knee);fits={};d=A.joint_data(pose)['rear']
    for n,m,tf in frames(pose):
        joint='fixed' if '_pitch_' in n else 'pitch' if '_roll_' in n else 'roll'
        zone=A.joint_transform(d,joint,roll,pitch,knee)*tf*audit.contact_zone()
        for side in ('right','left'):
            fits[frozenset((n.replace('right',side),m.replace('right',side)))]=zone if side=='right' else mirror(zone,Plane.XZ)
    out=[]
    for (n,a,_,ga,sa),(m,b,_,gb,sb) in combinations(data,2):
        if audit.wheel_hardware(n) and audit.wheel_hardware(m) and sa==sb:continue
        key=(pose,n,m,roll,pitch,knee)
        if cache is not None:
            levels={'fixed':0,'pitch':1,'roll':2,'bend':3}
            if sa==sb or sa==0 or sb==0:
                lo,hi=sorted((levels[ga.split('_')[-1]],levels[gb.split('_')[-1]]))
                key=(pose,n,m,(pitch,roll,knee)[lo:hi])
            if key in cache:
                if cache[key]:out.append(cache[key])
                continue
        hit=None;v=audit.overlap(a,b)
        if v>.01:
            zone=fits.get(frozenset((n,m)))
            if zone is None or v>50 or audit.overlap(a-zone,b)>.01:
                hit={'parts':[n,m],'intersection_mm3':round(v,6)};out.append(hit)
        if cache is not None:cache[key]=hit
    return out


def validate():
    result={'status':'proposed rear assembly; CAD clearance only','local_roll':[],'local_knee':[],
            'assembly':[],'access':{},'source_sha256':{}}
    thigh=L.upper_link(P.BODY_THIGH_MM,True);shank=L.lower_link(P.BODY_SHANK_MM,False,P.SHANK_MOTOR_INSET if THIGH_FLAT else 0.0)
    if THIGH_OPTIONS:
        body,cheek=L.rear_thigh_split(P.BODY_THIGH_MM)
        variants={'frame':L.rear_thigh_frame(P.BODY_THIGH_MM),'split body':body,'split cheek':cheek,'split fixings':L.thigh_lap_fixings()}
        result['status']='thigh print-form options (left: frame, right: split); CAD clearance only'
    elif THIGH_FLAT:
        variants={'flat':L.rear_thigh_flat(P.BODY_THIGH_MM)};result['status']='option 3 one-piece tapered thigh on both legs; CAD clearance only'
    else:variants={'thigh':thigh}
    ct=Pos(-P.ROOT_ROLL_Y,0,0)*Rot(Z=-90)
    with patch.object(S,'case_model',return_value=None):fallback=S.socket_reference.__wrapped__()
    obstacles={'carrier':ct*L.carrier(), 'B imported case':ct*L.roll_socket_frame(P.ROOT_ROLL_Y)*S.socket_reference(),
               'B measured case':ct*L.roll_socket_frame(P.ROOT_ROLL_Y)*fallback}
    # Dense local samples; no free interval is inferred from disconnected endpoints.
    for angle in range(-30,31):
        values={f'{v} vs {n}':audit.overlap(Rot(Y=angle)*part,s) for v,part in variants.items() for n,s in obstacles.items()}
        assert max(values.values())<.01,(angle,{k:x for k,x in values.items() if x>=.01})
        result['local_roll'].append({'degrees':angle,'intersection_mm3':values})
    print('PASS local thigh roll: -30..30, every degree',flush=True)
    knee_tf=L.knee_socket_frame(P.BODY_THIGH_MM,True)
    for angle in range(0,121):
        moving=Pos(0,0,P.BODY_THIGH_MM)*Rot(X=angle)*shank
        values={n:audit.overlap(moving,s) for n,s in list(variants.items())+[('C imported case',knee_tf*S.socket_reference()),
                                                    ('C measured case',knee_tf*fallback)]}
        assert max(values.values())<.01,(angle,{k:x for k,x in values.items() if x>=.01})
        result['local_knee'].append({'degrees':angle,'intersection_mm3':values})
    print('PASS local knee flexion: 0..120, every degree',flush=True)
    # Full hardware and straight approaches after all unions/fillets.
    access={}
    printed=[(n,v) for n,v in variants.items() if n!='split fixings']
    for name,part,tf in [(n,v,Rot(Z=-90)) for n,v in printed]+[('shank',shank,Pos())]:
        access[name+'_horn_heads']=audit.overlap(part,tf*S.horn_head_envelopes())
        for side in ('drive','idler'):
            plate=tf*L.AXIS*S.plate_location(side)
            for x in (-4.95,4.95):
                for y in (-4.95,4.95):
                    from build123d import Cylinder,Align
                    for label,z,r,h in [('bore',-1,(P.CLEAR_HOLE_M3-.02)/2,P.SOCKET_PAD_T+2),
                                         ('driver',P.SOCKET_PLATE_T+.5,P.SOCKET_HEAD_CLEAR/2-.01,35)]:
                        probe=plate*Pos(x,y,z)*Cylinder(r,h,align=(Align.CENTER,Align.CENTER,Align.MIN))
                        access[f'{name}_{side}_{x}_{y}_{label}']=audit.overlap(part,probe)
    for vname,part in printed:
        for n,p in S.socket_keepouts()[1:]:
            access[f'{vname}_C_'+n+str(p.center())]=audit.overlap(part,knee_tf*p)
        access[f'{vname}_C_ear_heads']=audit.overlap(part,knee_tf*S.ear_head_envelopes())
        if vname=='frame':
            # Sideways entry at the pre-insertion offset, then the straight 17 mm into the pocket.
            for shift in (0,5,10,P.SOCKET_DEPTH):
                access[f'frame_C_insertion_{shift}']=audit.overlap(part,knee_tf*Pos(0,0,shift)*S._parametric_case())
            for x in (10,20,30,45,60):
                access[f'frame_C_sideways_{x}']=audit.overlap(part,knee_tf*Pos(x,0,P.SOCKET_DEPTH)*S._parametric_case())
        elif vname!='split cheek':
            for shift in (0,5,15,25,50):
                access[f'{vname}_C_insertion_{shift}']=audit.overlap(part,knee_tf*Pos(0,0,shift)*S._parametric_case())
    assert max(access.values())<.01,[(n,v) for n,v in access.items() if v>.01]
    if THIGH_FLAT:   # the audit's check uses the un-inset motor; repeat it for the moved one
        face=L.motor_face(False,P.SHANK_MOTOR_INSET);length=P.BODY_SHANK_MM
        for shift in (0,-10,-35,-75):
            access[f'flush_motor_insertion_{shift}']=audit.overlap(shank,S._x_hole(face-P.MOTOR_BODY_LEN+shift,face+shift,0,length,P.MOTOR_DIA))
        for i in range(6):
            ang=radians(60*i+30);y=P.MOTOR_BCD/2*cos(ang);z=length+P.MOTOR_BCD/2*sin(ang)
            access[f'flush_motor_driver_{i}']=audit.overlap(shank,S._x_hole(face+P.MOTOR_MOUNT_T,face+40,y,z,P.CAP_M3_DIA+.3))
        assert max(access.values())<.01,[(n,v) for n,v in access.items() if v>.01]
    audit.check_motor_insertion()
    result['access']={'checks_mm3':access,'motor_insertion_and_six_face_drivers':'pass'}
    print('PASS horn bores/heads/drivers, knee ear access/insertion, motor insertion/drivers',flush=True)
    cache={}
    # Baseline and independent meaningful motions, all rear hardware included.
    for pose in ('quadruped','upright'):
        samples=[(0,0,0),(0,-30,0),(0,-45,0),(0,30,0),(30,0,0),(-5,0,0),
                 (0,0,120-B.poses()[pose]['rear'].flexion),
                 (0,0,-B.poses()[pose]['rear'].flexion)]
        for roll,pitch,knee in samples:
            hits=collisions(pose,roll,pitch,knee,cache)
            result['assembly'].append({'pose':pose,'roll':roll,'pitch':pitch,'knee_delta':knee,'collisions':hits})
            print('rear assembly',pose,roll,pitch,round(knee,3),hits,flush=True)
        assert not result['assembly'][-len(samples)]['collisions'],'nominal rear assembly must clear'
    result['limits']=['The local ranges check the named printed link and adjacent case/carrier; they are not full-robot motion limits.',
                      'Both rear legs, wheels and hardware constrain the separate viewer dynamically. Hidden parts remain obstacles.',
                      'Complete torso/front legs, cables, floor constraints, tolerances, physical indexing and loaded walking remain unverified.',
                      'No new slicing or physical print. Motor face boss and screw depth remain supplier/physical checks.']
    for file in (Path(__file__),Path(L.__file__),Path(P.__file__),Path(S.__file__),Path(A.__file__),Path(pelvis.__file__),Path(audit.__file__)):
        result['source_sha256'][str(file.relative_to(ROOT))]=hashlib.sha256(file.read_bytes()).hexdigest()
    if S._ST3215_STEP.exists():result['local_case_reference_sha256']=hashlib.sha256(S._ST3215_STEP.read_bytes()).hexdigest()
    (out_dir()/'clearance.json').write_text(json.dumps(result,indent=2)+'\n')
    return result


def build_viewer():
    from . import viewer as V
    from .meshing import export_mesh
    LIVE.mkdir(parents=True,exist_ok=True)
    # Distributable scene geometry must exclude the local, unlicensed vendor STEP.
    with patch.object(S,'case_model',return_value=None):reference=S.socket_reference.__wrapped__()
    def measured_reference():return reference
    measured_reference.__wrapped__=S.socket_reference.__wrapped__
    with patch.object(S,'socket_reference',new=measured_reference):
        A.nominal_details.cache_clear();nominal.cache_clear()
        with tempfile.TemporaryDirectory() as td:
            tmp=Path(td)
            poses={name:V._assembly_items(tmp,name,details=details(name),frames=frames(name)) for name in B.poses()}
            parts=[]
            builders=([(L.option_thigh_frame,'#c98fd9'),(L.option_thigh_split_body,'#c98fd9'),(L.option_thigh_split_cheek,'#f0b8ff')]
                      if THIGH_OPTIONS else [(L.option_thigh_flat,'#c98fd9')] if THIGH_FLAT else [(L.build_thigh,'#c98fd9')])+[((L.option_shank_flush if THIGH_FLAT else L.build_shank),'#8fd9c9')]
            for index,(builder,colour) in enumerate(builders):
                spec=builder();mesh=export_mesh(spec['orientation']*spec['part'],tmp/f'part{index}.stl')
                # Lay out the prints on separate 200 mm bed diagrams.
                mesh.apply_translation((-mesh.bounds[0][0]+index*140,-mesh.bounds[0][1],-mesh.bounds[0][2]))
                parts.append(V._item(spec['name'],mesh,colour,kind='printed',
                                    printable=spec.get('printable','unknown'),qty=2,notes=spec['notes'],material='PETG'))
        A.nominal_details.cache_clear();nominal.cache_clear()
    data={'poses':poses,'parts':parts,'meta':{'ground_z':0,'grid':20,'bed':[200,200],
          'track':P.BODY_TRACK_TARGET_MM-(2*P.SHANK_MOTOR_INSET if THIGH_FLAT else 0),'stance':P.BODY_STANDING_HEIGHT_MM,'hip_axes':2*L.rear_axis_y(),
          'joints':{name:A.joint_data(name) for name in poses},
          'status':(f'Option 3 (owner, 2026-09-19) on both legs: one-piece DEC-58 thigh, idler-side cheek thickened to the cup-floor plane with a single flat taper to the pad; prints on that plane with tree support. Shank with the 37D moved inboard {P.SHANK_MOTOR_INSET:g} mm so its outer print face is one plane: track {P.BODY_TRACK_TARGET_MM-2*P.SHANK_MOTOR_INSET:g} mm here. Everything else as DEC-57/58. Unprinted; strength unverified.' if THIGH_FLAT else
                    'Thigh print-form options (2026-09-19): LEFT leg = option 1, one print with a closed knee-end frame, stands on the socket to print; RIGHT leg = option 2, body plus bolted cheek piece (pink), both lie flat. Everything else as DEC-57/58. Unprinted; strength unverified.' if THIGH_OPTIONS else
                    'DEC-57 proposal: 45° A socket mount; retained B carrier. Revised thigh and motor shank. Rear assembly only; torso shown as a face patch. Printability unknown. Sampled mechanical ranges; floor, cables, front limbs and loaded motion unverified.')}}
    (LIVE/'scene.json').write_text(json.dumps(data))
    title='Rear leg · option 3 tapered thigh' if THIGH_FLAT else 'Rear leg · thigh options (L: frame, R: split)' if THIGH_OPTIONS else 'Rear leg · DEC-61 45° mount'
    html=V.HTML.read_text().replace('<title>Koala V1</title>',f'<title>Koala {title.lower()}</title>').replace('<h1>Koala V1</h1>',f'<h1>{title}</h1>')
    html=html.replace('Supported · front feet','Quadruped').replace('Upright · head pending','Upright').replace('Knee / elbow adjustment','Knee adjustment')
    (LIVE/'index.html').write_text(html)
    for name in ('mechanical_limits.js',):shutil.copy(V.HTML.with_name(name),LIVE/name)
    for file in (ROOT/'hardware/vendor/viewer').iterdir():
        if file.is_file():shutil.copy(file,LIVE/file.name)
    (LIVE/'layout-reference.json').write_text('null')
    subprocess.run(['node',str(V.HTML.with_name('build_mechanical_limits.cjs')),str(LIVE)],check=True)
    record=json.loads((LIVE/'mechanical-limits.json').read_text())
    (out_dir()/'viewer-limits.json').write_text(json.dumps({
        'scene_sha256':record['scene_sha256'],'engine_sha256':record['engine_sha256'],
        'poses':{n:r['limits'] for n,r in record['poses'].items()}},indent=2)+'\n')
    # Own geometry only in STEP archives; purchased references stay separate.
    for pose in B.poses():
        solids=[]
        for n,s,c,g,side in details(pose):
            if n.startswith('reference_') or audit.wheel_hardware(n):continue
            s=s.moved(Pos());s.label=n;solids.append(s)
        export_step(Compound(children=solids),out_dir()/f'rear-leg-{pose}.step')
    exports=([('thigh_frame',L.option_thigh_frame),('thigh_body',L.option_thigh_split_body),('thigh_cheek',L.option_thigh_split_cheek)]
             if THIGH_OPTIONS else [('thigh_flat',L.option_thigh_flat),('shank_flush',L.option_shank_flush)] if THIGH_FLAT else [('thigh',L.build_thigh),('shank',L.build_shank)])
    for name,builder in exports:
        d=builder();right=d['orientation']*d['part']
        right=Pos(0,0,-right.bounding_box().min.Z)*right
        export_step(right,out_dir()/f'{name}-right.step')
        export_step(mirror(right,Plane.XZ),out_dir()/f'{name}-left.step')
    print('wrote proposed rear-leg viewer',LIVE,flush=True)


def validate_viewer_endpoints():
    """Independent solid-CAD checks of both initial grouped slider endpoints."""
    data=json.loads((LIVE/'mechanical-limits.json').read_text());rows=[];cache={}
    for pose,record in data['poses'].items():
        for axis,bounds in record['limits']['bounds'].items():
            for end in ('min','max'):
                q={'roll':0,'pitch':0,'knee':0};q[axis]=bounds[end]
                hits=collisions(pose,**q,cache=cache)
                rows.append({'pose':pose,'axis':axis,'endpoint':end,'degrees':bounds[end],'collisions':hits})
                print('endpoint',pose,axis,end,bounds[end],hits,flush=True)
        for roll,pitch,knee in [(15,-30,15),(30,-45,30)]:
            hits=collisions(pose,roll,pitch,knee,cache)
            rows.append({'pose':pose,'roll':roll,'pitch':pitch,'knee_delta':knee,'collisions':hits})
            print('combined sample',pose,roll,pitch,knee,hits,flush=True)
    result={'scene_sha256':data['scene_sha256'],'engine_sha256':data['engine_sha256'],
            'scope':'Imported case plus measured horns; all rear solids and both legs. Nominal pocket contact only is allowed.',
            'checks':rows,'all_passed':all(not r['collisions'] for r in rows)}
    (out_dir()/'viewer-endpoints.json').write_text(json.dumps(result,indent=2)+'\n')
    assert result['all_passed'],'Rear viewer endpoints or combined samples intersect; inspect viewer-endpoints.json'


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--viewer-only',action='store_true')
    parser.add_argument('--thigh-options',action='store_true',help='left leg: option 1 frame thigh; right leg: option 2 split thigh')
    parser.add_argument('--thigh-flat',action='store_true',help='both legs: option 3, the one-piece tapered thigh')
    args=parser.parse_args()
    global THIGH_OPTIONS,THIGH_FLAT;THIGH_OPTIONS=args.thigh_options;THIGH_FLAT=args.thigh_flat
    out_dir().mkdir(parents=True,exist_ok=True)
    if not args.viewer_only:validate()
    build_viewer()
    validate_viewer_endpoints()


if __name__=='__main__':main()
