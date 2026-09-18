# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Placement/access study: retain the carrier and incline the torso root face.

Run from hardware: .venv/bin/python -m koala_hardware.pitch_socket_tilt_study
No production geometry or saved poses are changed. The mounting face is a
patch of the proposed torso surface, not a separate part or a completed torso.
"""
from pathlib import Path
import hashlib
import json
import tempfile
from math import acos, degrees
from unittest.mock import patch
from build123d import (Pos, Rot, Plane, RectangleRounded, Cylinder, Align,
                      extrude, mirror, Compound, export_step)
from . import params as P, servo_iface as S, assembly as A, body_plan as B, audit
from .parts import links as L, pelvis, torso

ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'docs/design/carrier-orientation'


def mount_face():
    """Five-mm torso face under both modules, in the right socket's frame."""
    w,d=pelvis.plate_outline()
    z=-P.SOCKET_SHELF-P.ROOT_PLATE_T-P.FRAME_PLATE_T
    face=Pos(-P.ROOT_PITCH_Y,0,z)*extrude(
        RectangleRounded(w+2*P.ROOT_PITCH_Y,d,4),amount=P.FRAME_PLATE_T)
    for centre in (0,-2*P.ROOT_PITCH_Y):
        for x,y in pelvis.nut_xy():
            face-=Pos(centre+x,y,z-1)*Cylinder(
                P.CLEAR_HOLE_M3/2,P.FRAME_PLATE_T+2,
                align=(Align.CENTER,Align.CENTER,Align.MIN))
    return face


def socket_frame(pose,tilt):
    # Body Y is the lateral pitch axis in both saved poses. Rotating about
    # this axis moves the case/mounting face, not either joint centre.
    return A.body_location(B.poses()[pose])*Rot(Y=tilt)*pelvis.pitch_socket(False)


def main():
    OUT.mkdir(exist_ok=True)
    records=[]
    face_native=mount_face()
    for pose in ('quadruped','upright'):
        body=B.poses()[pose];limb=body['rear'];body_tf=A.body_location(body)
        carrier_tf=A.segment_frame(limb.root,limb.bend,0)*Rot(Z=-90)
        carrier=carrier_tf*L.carrier(False)
        roll_case=carrier_tf*L.roll_socket_frame(P.ROOT_ROLL_Y)*S.socket_reference()
        for tilt in (0,-30,-45):
            tf=socket_frame(pose,tilt)
            module=tf*pelvis.root_socket();case=tf*S.socket_reference();face=tf*face_native
            axis=(tf*Pos(1,0,P.SOCKET_AXIS_Z)).position-(tf*Pos(0,0,P.SOCKET_AXIS_Z)).position
            centre=(tf*Pos(0,0,P.SOCKET_AXIS_Z)).position
            expected=A.joint_data(pose)['rear']['pitch']
            assert max(abs(a-b) for a,b in zip(centre,expected))<1e-8
            assert abs(abs(axis.Y)-1)<1e-8 and abs(axis.X)+abs(axis.Z)<1e-8
            row={'pose':pose,'socket_tilt_degrees_relative_to_current_mount':tilt,
                 'pitch_axis':list(axis),'pitch_centre_mm':list(centre),'samples':[],
                 'module_old_torso_overlap_mm3':audit.overlap(module,body_tf*torso.solid()),
                 'case_old_torso_overlap_mm3':audit.overlap(case,body_tf*torso.solid())}
            for pitch in (0,-15,-30,-36,-45,-51,30):
                turn=A.joint_transform(A.joint_data(pose)['rear'],'pitch',pitch=pitch)
                overlaps={name:audit.overlap(turn*carrier,obstacle)
                          for name,obstacle in [('root module',module),('pitch case',case),('torso face',face)]}
                overlaps.update({f'roll case / {name}':audit.overlap(turn*roll_case,obstacle)
                          for name,obstacle in [('root module',module),('pitch case',case),('torso face',face)]})
                row['samples'].append({'pitch_delta_degrees':pitch,'intersection_mm3':overlaps})
            # Rearward support reserve is a sample, not a complete interval.
            if tilt==-45:
                assert all(v<.01 for sample in row['samples'] for v in sample['intersection_mm3'].values()),row
                access=[]
                for x,y in pelvis.nut_xy():
                    z=-P.SOCKET_SHELF-P.ROOT_PLATE_T-P.FRAME_PLATE_T
                    driver=tf*Pos(x,y,z-40)*Cylinder(3,40,
                        align=(Align.CENTER,Align.CENTER,Align.MIN))
                    opposite=mirror(module,Plane.XZ)
                    values={name:audit.overlap(driver,item) for name,item in
                            [('own module',module),('pitch case',case),('opposite module',opposite),('torso face',face)]}
                    assert max(values.values())<.01,values
                    access.append({'nut_xy_mm':[x,y],'driver_intersection_mm3':values})
                row['frame_driver_access']=access
                row['module_face_overlap_mm3']=audit.overlap(module,face)
                # The native plate underside and the proposed face top share
                # Z=-11. Volume intersection is zero for this mating surface.
                z=-P.SOCKET_SHELF-P.ROOT_PLATE_T
                row['nominal_bearing_area_mm2']=sum(f.area for f in pelvis.root_socket().faces()
                    if abs(f.center().Z-z)<1e-6 and f.normal_at().Z<-.99)
            records.append(row)
            print(pose,tilt,[(s['pitch_delta_degrees'],round(max(s['intersection_mm3'].values()),4))
                            for s in row['samples']],flush=True)
    # Only own CAD is exported; the local third-party reference stays local.
    tf=socket_frame('quadruped',-45)
    parts=[]
    limb=B.poses()['quadruped']['rear']
    carrier_tf=A.segment_frame(limb.root,limb.bend,0)*Rot(Z=-90)
    for name,shape in [('retained_carrier',carrier_tf*L.carrier(False)),
                       ('retained_root_socket',tf*pelvis.root_socket()),
                       ('proposed_torso_face_patch',tf*face_native)]:
        shape.label=name;parts.append(shape)
    export_step(Compound(children=parts),OUT/'pitch-socket-45.step')
    record={'status':'mounting-face placement study; no production change; torso construction unresolved',
            'tilt_definition':'negative rotation about body +Y, through the existing pitch axis; compared with the current root mounting face',
            'retained':['carrier shape and print orientation','root socket shape and print orientation',
                        'hip pitch and roll axes','saved leg coordinates','four captive M3 nuts per root module'],
            'face':'5 mm patch with eight matching frame holes; intended as part of a future torso, not an extra print',
            'samples':records,
            'limits':['Discrete samples only; no continuous travel interval or gait acceptance.',
                      'The complete torso, wall transitions, driver access through those walls and print orientation remain to be designed.',
                      '45-degree mounting tilt is relative to the current mount; support needs depend on the eventual torso print orientation.',
                      'Cables, guards, physical servo indexing and loaded strength remain unverified.'],
            'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
               for p in (Path(__file__),Path(L.__file__),Path(pelvis.__file__),Path(torso.__file__),Path(A.__file__),Path(B.__file__),Path(P.__file__),Path(S.__file__))}}
    if S._ST3215_STEP.exists():
        record['local_case_reference_sha256']=hashlib.sha256(S._ST3215_STEP.read_bytes()).hexdigest()
    print_tf=torso.build()['orientation']*Rot(Y=-45)*pelvis.pitch_socket(False)
    normal=(print_tf*Pos(0,0,1)).position-print_tf.position
    record['face_angle_to_bed_in_current_torso_print_orientation_degrees']=degrees(acos(abs(normal.Z)))
    (OUT/'pitch-socket-tilt.json').write_text(json.dumps(record,indent=2)+'\n')
    write_viewer(record)
    print('wrote',OUT/'pitch-socket-tilt.json',flush=True)


def write_viewer(record):
    """Use only own/measured CAD in distributable viewer geometry."""
    from .viewer import _item
    from .meshing import export_mesh
    with patch.object(S,'case_model',return_value=None):
        reference=S.socket_reference.__wrapped__()
    data={'poses':{},'centres':{}}
    with tempfile.TemporaryDirectory() as td:
        td=Path(td)
        for pose in ('quadruped','upright'):
            data['poses'][pose]={}
            limb=B.poses()[pose]['rear']
            data['centres'][pose]=[limb.root.x,0,limb.root.z]
            carrier_tf=A.segment_frame(limb.root,limb.bend,0)*Rot(Z=-90)
            for tilt in (0,-30,-45):
                tf=socket_frame(pose,tilt)
                shapes=[('retained carrier',carrier_tf*L.carrier(False),'#d99fba',False,True),
                        ('retained root socket',tf*pelvis.root_socket(),'#8fb4d9',False,False),
                        ('torso face patch',tf*mount_face(),'#8bbd9e',False,False),
                        ('pitch servo envelope',tf*reference,'#d9c069',True,False),
                        ('roll servo envelope',carrier_tf*L.roll_socket_frame(P.ROOT_ROLL_Y)*reference,'#d9c069',True,True)]
                items=[_item(name,export_mesh(shape,td/f'{i}.stl',tolerance=.08,angular_tolerance=.25),
                             colour,ghost=ghost,moving=moving)
                       for i,(name,shape,colour,ghost,moving) in enumerate(shapes)]
                row=next(r for r in record['samples'] if r['pose']==pose and r['socket_tilt_degrees_relative_to_current_mount']==tilt)
                data['poses'][pose][str(-tilt)]={'items':items,'collisions':{
                    str(s['pitch_delta_degrees']):max(s['intersection_mm3'].values())>.01 for s in row['samples']}}
    html=Path(__file__).with_suffix('.html').read_text().replace('__DATA__',json.dumps(data))
    (OUT/'pitch-socket-tilt.html').write_text(html)
    live=ROOT/'hardware/build/viewer'
    if live.exists():
        (live/'pitch-socket-tilt.html').write_text(html.replace('../../../hardware/vendor/viewer/three-r128.min.js','three-r128.min.js'))


if __name__=='__main__':main()
