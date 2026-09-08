# SPDX-License-Identifier: CERN-OHL-S-2.0
"""DEC-34 sampled solid intersections, socket access and full-depth hole probes.

Nominal geometry only. No continuous-collision, thermal or structural claim.
Run: uv run python -m koala_hardware.audit
"""
import itertools
from build123d import Align, Cylinder, Plane, Pos, Rot, mirror
from . import assembly as A, params as P, servo_iface as S, validation
from .parts import all_builders, links as L, pelvis, e_tray


def volume_overlap(a, b):
    aa, bb = a.bounding_box(), b.bounding_box()
    if any(getattr(aa.max, k) <= getattr(bb.min, k)+1e-6 or
           getattr(bb.max, k) <= getattr(aa.min, k)+1e-6 for k in 'XYZ'):
        return 0.0
    return sum(s.volume for s in (a & b).solids())


def require_clear(a, b, label, limit=.01):
    v = volume_overlap(a, b)
    if v > limit:
        raise AssertionError(f'{label}: {v:.3f} mm³ overlap')


def check_socket():
    case, cradle, collar = S.socket_reference(), S.cradle(), S.collar()
    # The pocket is a zero-clearance press fit and the vendored case model is
    # good to ~0.3 mm (vendor/st3215/README.md), so case-to-pocket contact may
    # register as a sliver of overlap. 50 mm³ is ~0.1 mm over the two 18.5 x
    # 13.5 pads; a pocket 0.5 mm too narrow would show ~250 mm³ and still fail.
    for a,b,label,limit in [(case,cradle,'case/cradle',50.),(case,collar,'case/collar',50.),
                            (cradle,collar,'cradle/collar',.01)]:
        require_clear(a,b,label,limit)
    for name,tool in S.socket_keepouts()[1:]:
        for n,p in [('cradle',cradle),('collar',collar)]:
            require_clear(tool,p,name+'/'+n)
    # Full-depth lug shafts; shoulders must not silently become blind bores.
    x=P.SOCKET_CASE_X/2
    for y in (-P.SOCKET_LUG_Y,P.SOCKET_LUG_Y):
        for z,lo,hi in [(P.SOCKET_LUG_BACK_Z,-x-20,-x),
                        (P.SOCKET_LUG_DRIVE_Z,x,x+20)]:
            probe=S._x_hole(lo,hi,y,z,P.SOCKET_M2_CLEAR-.02)
            for p in (cradle,collar):require_clear(probe,p,'M2 shaft',.001)
    for side in ('drive','idler'):
        plate=L.registered_fork(side)
        tf=L.AXIS*S.plate_location(side)
        for a,b in itertools.product((-P.SERVO_DRIVE_SQ/2,P.SERVO_DRIVE_SQ/2),repeat=2):
            probe=tf*Pos(a,b,-10)*Cylinder((P.CLEAR_HOLE_M3-.02)/2,25,
                align=(Align.CENTER,Align.CENTER,Align.MIN))
            require_clear(plate,probe,'full-depth '+side+' horn shaft',.001)
        for angle in range(-90,91,10):
            posed=Rot(X=angle)*plate
            for n,p in [('case',case),('cradle',cradle),('collar',collar)]:
                require_clear(posed,L.AXIS*p,f'rig {side} {angle}/{n}')
    crossbar = L._register(L._crossbar(),
        [(y,P.SOCKET_BRIDGE_Z) for y in (-P.SOCKET_BRIDGE_BOLT_Y,P.SOCKET_BRIDGE_BOLT_Y)])
    for angle in range(-90,91,10):
        for n,p in [('case',case),('cradle',cradle),('collar',collar)]:
            require_clear(Rot(X=angle)*crossbar,L.AXIS*p,f'rig bridge {angle}/{n}')
    print('PASS shared socket, driver/cable corridors, four M2 and eight horn bores, rig sweep',flush=True)


def check_mounting():
    """Tray bores must traverse the final deck/root solid, not only PLATE mm."""
    for x,y in P.V2_TRAY_HOLES:
        shaft=Pos(x,y,-100)*Cylinder((P.CLEAR_HOLE_M3-.02)/2,120,
            align=(Align.CENTER,Align.CENTER,Align.MIN))
        require_clear(shaft,pelvis.solid(),'full-depth pelvis tray bore',.001)
        require_clear(shaft,Pos(0,0,P.TRAY_GAP)*e_tray.solid(),'full-depth tray bore',.001)
        driver=Pos(x,y,-100)*Cylinder(3,100-P.V2_DECK_SIZE[2],
            align=(Align.CENTER,Align.CENTER,Align.MIN))
        require_clear(driver,pelvis.solid(),'tray underside driver path')
    for core in (L.thigh_core(),L.shank_core()):
        parts=[core,L.registered_fork('drive'),L.registered_fork('idler')]
        for y in (-P.SOCKET_BRIDGE_BOLT_Y,P.SOCKET_BRIDGE_BOLT_Y):
            shaft=S._x_hole(L.B0-P.SOCKET_PLATE_T-1,L.B1+P.SOCKET_PLATE_T+1,
                            y,P.SOCKET_BRIDGE_Z,P.CLEAR_HOLE_M3-.02)
            for p in parts:require_clear(shaft,p,'full crossbar shaft',.001)
    for z in P.V2_MOTOR_BOLTS_Z:
        shaft=S._x_hole(L.B0-P.V2_MOTOR_PLATE_T-1,L.B1+P.V2_MOTOR_PLATE_T+1,
                        0,z,P.CLEAR_HOLE_M3-.02)
        for p in (L.shank_core(),L.motor_plate(True),L.motor_plate(False)):
            require_clear(shaft,p,'full motor seam shaft',.001)
    for z in (-P.SOCKET_BRIDGE_BOLT_Y,P.SOCKET_BRIDGE_BOLT_Y):
        shaft=S._x_hole(L.B0-P.SOCKET_PLATE_T-1,P.V2_PITCH_REAR_X+1,
                        P.V2_PITCH_Y,z,P.CLEAR_HOLE_M3-.02)
        for p in (L.hip_socket(),L.build_hip_bridge()['part'],
                  Rot(X=-90)*L.registered_fork('drive'),Rot(X=-90)*L.registered_fork('idler')):
            require_clear(shaft,p,'full hip carrier shaft',.001)
    print('PASS tray through-bores/tool paths and complete crossbar/motor/carrier shafts',flush=True)


def horn_heads():
    """Proud M3 cap heads at BOTH horns of roll, pitch and knee."""
    output=[]
    thigh=A.PITCH_FRAME*Rot(X=90-P.V2_HIP_NOMINAL)
    knee=thigh*Pos(0,0,P.V2_THIGH)*Rot(X=P.V2_KNEE_NOMINAL)
    for joint,tf,group in [('roll',Rot(X=-90),'roll'),('pitch',thigh,'pitch'),('knee',knee,'knee')]:
        for side in ('drive','idler'):
            plate=tf*L.AXIS*S.plate_location(side)
            for i,(a,b) in enumerate(itertools.product((-P.SERVO_DRIVE_SQ/2,P.SERVO_DRIVE_SQ/2),repeat=2)):
                head=plate*Pos(a,b,-P.CAP_M3_H)*Cylinder(P.CAP_M3_DIA/2,P.CAP_M3_H,
                    align=(Align.CENTER,Align.CENTER,Align.MIN))
                output.append((f'head_{joint}_{side}_{i}',head,'',group))
    return output


def other_heads():
    """Carrier, motor and M2 lug heads/nuts, separate from mating shafts."""
    out=[]
    def add(name,tf,x0,x1,y,z,d,group):
        out.append(('head_'+name,tf*S._x_hole(x0,x1,y,z,d),'',group))
    thigh=A.PITCH_FRAME*Rot(X=90-P.V2_HIP_NOMINAL)
    knee=thigh*Pos(0,0,P.V2_THIGH)*Rot(X=P.V2_KNEE_NOMINAL)
    for joint,tf,group in [('pitch',thigh,'pitch'),('knee',knee,'knee')]:
        for i,y in enumerate((-P.SOCKET_BRIDGE_BOLT_Y,P.SOCKET_BRIDGE_BOLT_Y)):
            x=L.B1+P.SOCKET_PLATE_T+P.V2_WASHER_H
            add(f'{joint}_bridge_{i}',tf,x,x+P.CAP_M3_H,y,P.SOCKET_BRIDGE_Z,P.CAP_M3_DIA,group)
            x=L.B0-P.SOCKET_PLATE_T-P.V2_WASHER_H
            add(f'{joint}_nut_{i}',tf,x-P.V2_NUT_H,x,y,P.SOCKET_BRIDGE_Z,P.V2_NUT_DIA,group)
    for i,z in enumerate((-P.SOCKET_BRIDGE_BOLT_Y,P.SOCKET_BRIDGE_BOLT_Y)):
        add(f'carrier_{i}',Pos(),P.V2_PITCH_REAR_X-P.CAP_M3_H,P.V2_PITCH_REAR_X,
            P.V2_PITCH_Y,z,P.CAP_M3_DIA,'roll')
        x=L.B0-P.SOCKET_PLATE_T-P.V2_WASHER_H
        add(f'carrier_nut_{i}',Pos(),x-P.V2_NUT_H,x,P.V2_PITCH_Y,z,P.V2_NUT_DIA,'roll')
    from math import sin,cos,radians
    for i in range(P.MOTOR_FACE_SCREWS):
        a=radians(i*60+30);x=P.V2_MOTOR_FACE+P.V2_MOTOR_PLATE_T
        add(f'motor_face_{i}',knee,x,x+P.CAP_M3_H,
            P.MOTOR_BCD/2*cos(a),P.V2_SHANK+P.MOTOR_BCD/2*sin(a),P.CAP_M3_DIA,'knee')
    for i,z in enumerate(P.V2_MOTOR_BOLTS_Z):
        x=L.B1+P.V2_MOTOR_PLATE_T+P.V2_WASHER_H
        add(f'motor_seam_{i}',knee,x,x+P.CAP_M3_H,0,z,P.CAP_M3_DIA,'knee')
        x=L.B0-P.V2_MOTOR_PLATE_T-P.V2_WASHER_H
        add(f'motor_nut_{i}',knee,x-P.V2_NUT_H,x,0,z,P.V2_NUT_DIA,'knee')
    for joint,tf,group in [('roll',Rot(X=180)*L.AXIS,'fixed'),
                            ('pitch',A.PITCH_FRAME*L.AXIS,'roll'),
                            ('knee',thigh*Pos(0,0,P.V2_THIGH)*L.AXIS,'pitch')]:
        for i,y in enumerate((-P.SOCKET_LUG_Y,P.SOCKET_LUG_Y)):
            x=P.SOCKET_CASE_X/2+P.SOCKET_M2_SEAT
            add(f'{joint}_lug_drive_{i}',tf,x,x+P.SOCKET_M2_HEAD_H,y,
                P.SOCKET_LUG_DRIVE_Z,P.SOCKET_M2_HEAD,group)
            add(f'{joint}_lug_idler_{i}',tf,-x-P.SOCKET_M2_HEAD_H,-x,y,
                P.SOCKET_LUG_BACK_Z,P.SOCKET_M2_HEAD,group)
    return out


def is_hardware(name):
    return name in ('motor','shaft','hub','wheel') or name.startswith(('reference','head_'))


def posed_local(local, roll, hip, knee):
    tf=A.motion(roll,hip,knee)
    root=Pos(P.V2_ROLL_X,P.V2_ROLL_Y,A.ROLL_Z)
    return [(n,root*tf[g]*p,c,g) for n,p,c,g in local]


def main():
    validation.check_layout()
    for builder in all_builders():
        d=builder();p=d['part']
        assert p.is_valid and (d.get('multi_body') or len(p.solids())==1),d['name']
        assert all(0<v<=200.001 for v in (d['orientation']*p).bounding_box().size),d['name']
    # Deck must include matching handed roots; otherwise a right-only audit
    # would miss the left collar occupying a differently oriented cradle.
    assert sum(p.volume for p in (pelvis.solid()-mirror(pelvis.solid(),Plane.XZ)).solids()) < .001, 'pelvis handed symmetry'
    check_socket()
    check_mounting()
    local=A.leg_parts()+horn_heads()+other_heads()
    failures=[]
    deck=('pelvis',pelvis.solid(),'','fixed')
    # Check unchanged within-group pairs once; moving pairs at every sampled pose.
    seen_static=set()
    rolls=sorted(set((0.,*P.V2_ROLL_RANGE)))
    hips=sorted(set((P.V2_HIP_NOMINAL,*P.V2_HIP_RANGE)))
    knees=sorted(set((P.V2_KNEE_NOMINAL,*P.V2_KNEE_RANGE)))
    for roll,hip,knee in itertools.product(rolls,hips,knees):
        items=[deck]+posed_local(local,roll,hip,knee)
        for (n,a,_,ga),(m,b,_,gb) in itertools.combinations(items,2):
            if is_hardware(n) and is_hardware(m):continue
            if ga==gb:
                pair=(n,m)
                if pair in seen_static:continue
                seen_static.add(pair)
            v=volume_overlap(a,b)
            if v>.01:failures.append((roll,hip,knee,n,m,round(v,3)))
        print(f'checked roll {roll:+g}, hip {hip:+g}, knee {knee:g}',flush=True)
    # Opposing legs: independent hip and knee positions at worst inward roll.
    shapes=[i for i in A.leg_parts() if not i[0].startswith('reference')]
    poses=list(itertools.product(hips,knees))
    right_cache={q:posed_local(shapes,P.V2_ROLL_RANGE[0],*q) for q in poses}
    for r,l in itertools.product(poses,repeat=2):
        right=right_cache[r]
        left=[(n,mirror(s,Plane.XZ),c,g) for n,s,c,g in right_cache[l]]
        for n,a,_,_ in right:
            for m,b,_,_ in left:
                v=volume_overlap(a,b)
                if v>.01:failures.append(('opposing',r,l,n,m,round(v,3)))
    print(f'checked {len(poses)**2} independent opposing-leg poses',flush=True)
    if failures:
        for f in failures:print('FAIL',f)
        raise SystemExit(f'{len(failures)} nominal intersections; do not print structural parts')
    print('PASS 27 local poses with horn heads and 81 opposing-leg poses; nominal samples only',flush=True)


if __name__=='__main__':main()
