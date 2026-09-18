# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Unselected carrier study: forks down/rearward at 45°, B socket retained.

Run from hardware: .venv/bin/python -m koala_hardware.carrier_fork_study
Writes a separate CAD snapshot and checks; does not change production builders.
"""
from functools import lru_cache
from math import atan2, degrees, radians, sin, cos, hypot
from pathlib import Path
import hashlib
import json

from build123d import (Plane, Pos, Rot, Polygon, Vertex, Cylinder, Align,
                      extrude, loft, mirror, fillet, GeomType, export_step)
from . import params as P, servo_iface as S, body_plan as B, assembly as A, audit
from .parts import links as L, pelvis
from .meshing import export_mesh
from .printability import metrics

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'docs/design/carrier-orientation'


def fork_angle():
    limb = B.poses()['quadruped']['rear']
    return degrees(atan2(limb.bend.z-limb.root.z, limb.bend.x-limb.root.x)) + 135


@lru_cache
def candidate():
    w = P.HIP_BLOCK_HALF_W
    top, floor = P.SOCKET_AXIS_Z-P.SOCKET_DEPTH, P.SOCKET_AXIS_Z+P.SOCKET_SHELF
    inner = P.ROOT_PITCH_Y+P.SOCKET_IDLER_FACE-P.SOCKET_PAD_T
    socket_y = P.ROOT_ROLL_Y-P.SOCKET_CASE_Y/2-P.SOCKET_CLEAR-2
    forks = mirror(L.pitch_fork_frame()*(L.fork('drive')+L.fork('idler')), Plane.XY)
    forks &= S._box(-12,12,inner-1,socket_y+1,-12,top)
    angle = fork_angle()
    s,c = sin(radians(angle)),cos(radians(angle))
    def point(x,z): return (x*c+z*s,-x*s+z*c)
    a,b,d = point(-w,top),point(w,top),point(w,floor)
    foot = (w,floor)
    # One continuous wedge joins the angled cradle to a flat base coplanar
    # with B's socket floor. This is deliberately a bulky first construction.
    profile = Plane.XZ*Polygon(a,b,d,(d[0],floor),foot,align=None)
    bridge = Pos(0,socket_y,0)*extrude(profile,amount=socket_y-inner)
    part = Rot(Y=angle)*forks + bridge + L.roll_socket_frame(P.ROOT_ROLL_Y)*S.saddle()
    mid = ((a[0]+b[0])/2,(a[1]+b[1])/2)
    roots = (P.ROOT_PITCH_Y+P.SOCKET_IDLER_FACE,P.ROOT_PITCH_Y+P.SOCKET_DRIVE_FACE)
    edges = [e for e in part.edges() if e.geom_type==GeomType.LINE
             and abs(e.length-2*w)<1e-5 and abs(e.center().X-mid[0])<1e-5
             and abs(e.center().Z-mid[1])<1e-5
             and any(abs(e.center().Y-y)<1e-5 for y in roots)]
    assert len(edges)==2, 'expected both fork roots'
    part = fillet(edges,P.HIP_FORK_ROOT_R)
    edges = [e for e in part.edges() if e.geom_type==GeomType.LINE
             and abs(e.center().Y-socket_y)<1e-5
             and abs(e.center().Z-(top+floor)/2)<1e-5
             and w<e.center().X<2*w]
    assert len(edges)==1, 'expected the sloping bridge/socket join'
    part = fillet(edges,P.HIP_SOCKET_ROOT_R)
    # Fill the concave join at the socket's existing rounded outside corner
    # with an R5 gusset, preserving the four straight ear-driver corridors.
    x = P.SOCKET_CASE_X/2+P.SOCKET_CLEAR+P.SOCKET_WALL
    r = P.HIP_SOCKET_ROOT_R
    gusset = S._box(x-2,x+r,socket_y-1,socket_y+r,top,floor)
    gusset -= Pos(x+r,socket_y+r,top-1)*Cylinder(
        r,floor-top+2,align=(Align.CENTER,Align.CENTER,Align.MIN))
    for _,probe in S.socket_keepouts()[1:]:
        gusset -= L.roll_socket_frame(P.ROOT_ROLL_Y)*probe
    part += gusset
    edges = [e for e in part.edges() if e.geom_type==GeomType.LINE
             and abs(e.center().Y-socket_y)<1e-5
             and abs(e.center().Z-top)<1e-5 and e.center().X>mid[0]]
    assert len(edges)==1, 'expected the narrow socket lip'
    part = fillet(edges,P.HIP_SOCKET_LIP_R)
    # Two small bevels along the exposed cradle edges, tapering out before
    # the fork fillets. The horn pads remain complete in their rotated frame.
    bevel = P.HIP_EDGE_BEVEL
    start,end = roots[0]+P.HIP_FORK_ROOT_R,roots[1]-P.HIP_FORK_ROOT_R
    def along(origin,target):
        dx,dz=target[0]-origin[0],target[1]-origin[1]
        scale=bevel/hypot(dx,dz)
        return origin[0]+scale*dx,origin[1]+scale*dz
    for vertex,previous,following in ((a,foot,b),(b,a,d)):
        profile = Plane.XZ*Polygon(vertex,along(vertex,previous),along(vertex,following),align=None)
        cut = loft([Vertex(vertex[0],start,vertex[1]),Pos(0,start+bevel,0)*profile,
                    Pos(0,end-bevel,0)*profile,Vertex(vertex[0],end,vertex[1])],ruled=True)
        part -= cut
    assert part.is_valid and len(part.solids())==1
    return part


def main():
    OUT.mkdir(exist_ok=True)
    part=candidate()
    record={'status':'unselected construction study; printable unknown; no slice or physical print',
            'fork_direction':'45 degrees below world rearward in the saved quadruped pose',
            'fork_angle_relative_to_production_degrees':fork_angle(),
            'roll_socket':'position and orientation unchanged from production',
            'valid':part.is_valid,'solids':len(part.solids()),
            'volume_mm3':part.volume,'production_volume_mm3':L.carrier(False).volume}
    record['pitch_case_reference'] = ({'kind':'local imported case plus measured horn stack',
        'file':str(S._ST3215_STEP.relative_to(ROOT)),
        'sha256':hashlib.sha256(S._ST3215_STEP.read_bytes()).hexdigest()}
        if S._ST3215_STEP.exists() else {'kind':'measured parametric case plus horn stack'})
    export_step(part,OUT/'angled-fork.step')
    printed=Rot(X=180)*part
    printed=Pos(0,0,-printed.bounding_box().min.Z)*printed
    mesh=export_mesh(printed,OUT/'angled-fork.stl')
    record['print_orientation']='native Z=socket floor on bed, rotated X=180 and translated to Z=0'
    record['print_metrics']=metrics(mesh)
    record['watertight']=mesh.is_watertight
    checks=[]
    def check(name,a,b):
        overlap=audit.overlap(a,b)
        checks.append({'check':name,'intersection_mm3':overlap})
        assert overlap<.01,(name,overlap)
    tf=L.roll_socket_frame(P.ROOT_ROLL_Y)
    for i,(name,probe) in enumerate(S.socket_keepouts()[1:]): check(f'roll {name} {i}',part,tf*probe)
    for shift in (0,5,15,25,50): check(f'roll insertion {shift} mm',part,tf*Pos(0,0,shift)*S._parametric_case())
    heads=Rot(Y=fork_angle())*mirror(L.pitch_fork_frame()*S.horn_head_envelopes(),Plane.XY)
    for kind,items in [('pitch horn head/washer',heads),('roll ear head',tf*S.ear_head_envelopes())]:
        for i,head in enumerate(items.solids()): check(f'{kind} {i}',part,head)
    forks=Rot(Y=fork_angle())*mirror(L.pitch_fork_frame()*(L.fork('drive')+L.fork('idler')),Plane.XY)
    # Restrict to the pitch fork span: the unchanged B socket can project into
    # this rotated Z band farther outboard, but is not part of either pad.
    inner=P.ROOT_PITCH_Y+P.SOCKET_IDLER_FACE-P.SOCKET_PAD_T
    outer=P.ROOT_PITCH_Y+P.SOCKET_DRIVE_FACE+P.SOCKET_PAD_T
    region=Rot(Y=fork_angle())*S._box(-30,30,inner,outer,-P.SOCKET_PLATE_R-1,P.SOCKET_PLATE_R)
    record['horn_pad_changed_volume_mm3']=audit.volume((part-forks)&region)+audit.volume((forks-part)&region)
    assert record['horn_pad_changed_volume_mm3']<.01
    for pose,angles in [('quadruped',(-30,-20,-10,0,10,20,30)),('upright',(0,))]:
        body=B.poses()[pose];limb=body['rear']
        location=A.segment_frame(limb.root,limb.bend,0)*Rot(Z=-90)
        root=A.body_location(body)*pelvis.module(False)
        pitch_tf=A.body_location(body)*pelvis.pitch_socket(False)
        obstacles={'root module':root,'pitch case':pitch_tf*S.socket_reference()}
        check(f'{pose} thigh at rest',location*part,
              A.segment_frame(limb.root,limb.bend,P.ROOT_ROLL_Y)*L.upper_link(P.BODY_THIGH_MM,True))
        for angle in angles:
            moved=A.joint_transform(A.joint_data(pose)['rear'],'pitch',pitch=angle)*location*part
            for name,obstacle in obstacles.items(): check(f'{pose} pitch {angle:+g} / {name}',moved,obstacle)
    record['checks']=checks
    record['limitations']=['Discrete right-side samples only; no complete travel interval or gait established.',
        'Other installed hardware, complete cable routing, loaded strength and sliced layers remain unverified.',
        'The wider, heavier wedge is a first construction, not an optimized production replacement.',
        'Fork undersides and hole roofs may require accessible supports.']
    record['source_sha256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
        for p in (Path(__file__),Path(L.__file__),Path(P.__file__),Path(S.__file__),Path(B.__file__))}
    record['artifact_sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
        for p in (OUT/'angled-fork.step',OUT/'angled-fork.stl')}
    (OUT/'angled-fork.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({k:v for k,v in record.items() if k not in ('checks','source_sha256','artifact_sha256')},indent=2))
    print(f'PASS {len(checks)} intersection checks; exact horn pads; valid solid and watertight STL')


if __name__=='__main__': main()
