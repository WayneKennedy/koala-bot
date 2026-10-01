# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Reproducible footed-link travel screen and installed endpoint checks.

Run with hardware/freecad-run -m koala_hardware.bend_clearance.
No calibrated motor stops, continuous sweep or physical-load claim is made.
"""
import hashlib
import json
from pathlib import Path
from unittest.mock import patch
from . import assembly as A, body_plan as B, servo_iface as S, params as P, audit
from .parts import front as F, links as L, foot_shank as FS
from .cad import Pos, Rot
from .bend_limits import SIGNED_BEND_LIMITS, FIRST_BLOCKED_SAMPLES, REVIEW_POSES, ANGULAR_RESERVE_DEG


def local_geometry(key):
    front=key=='front';length=P.BODY_UPPER_ARM_MM if front else P.BODY_THIGH_MM
    frame=F.elbow_socket_frame() if front else L.knee_socket_frame(length,True)
    with patch.object(S,'case_model',return_value=None):fallback=S.socket_reference.__wrapped__()
    moving=(F.forearm()+L.front_pad()+A.pad_fixing()) if front else FS.solid()+FS.pad_location()*(L.front_pad()+A.pad_fixing())
    moving+=S.horn_head_envelopes()
    cup=F.upper_arm() if front else L.upper_link(length,True)
    return length,moving,[('printed_cup',cup),('vendor_case',frame*S.socket_reference()),
                         ('fallback_case',frame*fallback),('ear_heads',frame*S.ear_head_envelopes())]


def local_sample(key, angle, geometry=None):
    length,moving,obstacles=geometry or local_geometry(key)
    placed=Pos(0,0,length)*Rot(X=angle)*moving
    return {'angle_deg':angle,'overlap_mm3':{n:audit.overlap(placed,s) for n,s in obstacles},
            # Other solids include intended mating contact, so gap is cup-only.
            'printed_cup_gap_mm':placed.fc.distToShape(obstacles[0][1].fc)[0]}


def main():
    report={'angular_reserve_deg':ANGULAR_RESERVE_DEG,'signed_limits_deg':SIGNED_BEND_LIMITS,
            'angle_convention':'Native X rotation from straight links; front flexion is negative, rear flexion positive.',
            'interior_step_deg':1.,'boundary_step_deg':.25,'local':{},'installed':[]}
    for key,(lo,hi) in SIGNED_BEND_LIMITS.items():
        geometry=local_geometry(key)
        angles={lo,hi,*range(int(lo)+1,int(hi)+1)}
        samples=[local_sample(key,a,geometry) for a in sorted(angles)]
        for row in samples:assert max(row['overlap_mm3'].values())<=.01,(key,row)
        boundaries=[]
        for sign,first in zip((-1,1),FIRST_BLOCKED_SAMPLES[key]):
            for tick in range(-2,2):
                angle=first+sign*tick*.25
                boundaries.append(local_sample(key,angle,geometry))
            hit=local_sample(key,first,geometry)
            assert max(hit['overlap_mm3'].values())>.01,(key,first)
        report['local'][key]={'clear_samples':samples,'boundary_samples':boundaries}
        print('PASS local',key,lo,hi,len(samples),'clear samples',flush=True)
    for fallback in (False,True):
        with patch.object(S,'case_model',return_value=None) if fallback else patch.object(S,'case_model',wraps=S.case_model):
            S.socket_reference.cache_clear();A.nominal_details.cache_clear()
            for name,targets in REVIEW_POSES.items():
                items=A.bend_review_details(name)
                with patch.object(A,'scene_details',return_value=items):pairs=audit.check_scene('walking')
                report['installed'].append({'review':name,'reference':'fallback' if fallback else 'vendor',
                                             'signed_bend_deg':targets,'boolean_pairs':pairs})
                print('PASS installed',name,'fallback' if fallback else 'vendor',pairs,flush=True)
    package=Path(__file__).resolve().parent
    report['source_sha256']={str(p.relative_to(package)):hashlib.sha256(p.read_bytes()).hexdigest()
                             for p in sorted(package.rglob('*.py'))}
    report['scope']='Local footed packages including pads/fixings/horn heads against owning cups, both case envelopes and ear heads; whole walking robot at three endpoint combinations with fixed hips/shoulders. No continuous path, arbitrary combined joints, complete cables, floor contact or loaded validation.'
    out=package.parents[2]/'docs/design/flat-links/bend-clearance.json'
    out.write_text(json.dumps(report,indent=2)+'\n')
    print('Wrote',out,flush=True)

if __name__=='__main__':main()
