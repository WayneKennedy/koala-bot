# SPDX-License-Identifier: CERN-OHL-S-2.0
"""DEC-43 rear-wheel / fixed-front-foot body master shared with the structural assembly.

Lengths are distances between parallel pitch axes, not between tyre centres.
Generates dimensioned SVGs, joint coordinates and review STEP assemblies.
This is a kinematic master, not an export of fabrication-ready parts.
"""
from dataclasses import dataclass, asdict
from math import atan2, cos, sin, sqrt, hypot, acos, degrees, radians, pi
from pathlib import Path
import json
from . import params as P


@dataclass(frozen=True)
class Point:
    x: float
    z: float

    def distance(self, other):
        return hypot(self.x-other.x, self.z-other.z)


@dataclass(frozen=True)
class Limb:
    root: Point
    bend: Point
    axle: Point  # terminal centre: rear axle or fixed front ball centre
    upper: float
    lower: float
    flexion: float


def solve(root, axle, upper, lower, branch):
    """Planar two-link IK; + branch puts a rear knee towards the nose."""
    dx,dz=axle.x-root.x,axle.z-root.z
    d=hypot(dx,dz)
    if not abs(upper-lower)<d<upper+lower:
        raise ValueError(f'Unreachable or singular limb: {d:g} for {upper:g}/{lower:g}')
    q=(upper*upper-lower*lower+d*d)/(2*d)
    h=sqrt(max(0,upper*upper-q*q))
    bend=Point(root.x+q*dx/d-branch*h*dz/d,
               root.z+q*dz/d+branch*h*dx/d)
    flexion=180-degrees(acos((upper*upper+lower*lower-d*d)/(2*upper*lower)))
    return Limb(root,bend,axle,upper,lower,flexion)


def poses():
    hip=Point(0,P.BODY_QUAD_HIP_HEIGHT_MM)
    dz=P.BODY_QUAD_SHOULDER_HEIGHT_MM-hip.z
    shoulder=Point(sqrt(P.BODY_TORSO_LENGTH_MM**2-dz**2),hip.z+dz)
    # 55 mm behind the hip retains the requested 260 mm contact spacing.
    rear=Point(-P.BODY_QUAD_REAR_OFFSET_MM,P.WHEEL_DIA/2)
    front=Point(rear.x+P.BODY_WHEELBASE_TARGET_MM,P.BODY_FRONT_FOOT_RADIUS_MM)
    upright_hip=Point(0,P.BODY_STANDING_HEIGHT_MM-P.BODY_TORSO_LENGTH_MM
                        -P.BODY_NECK_LENGTH_MM-P.BODY_HEAD_HEIGHT_MM)
    upright_shoulder=Point(0,upright_hip.z+P.BODY_TORSO_LENGTH_MM)
    out={}
    for name,h,s,r,f in [('quadruped',hip,shoulder,rear,front),
                         ('upright',upright_hip,upright_shoulder,
                          Point(0,P.WHEEL_DIA/2),Point(P.BODY_UPRIGHT_WRIST_X_MM,
                          upright_shoulder.z+P.BODY_UPRIGHT_WRIST_RISE_MM))]:
        theta=atan2(s.z-h.z,s.x-h.x)
        neck=Point(s.x+P.BODY_NECK_LENGTH_MM*cos(theta),
                   s.z+P.BODY_NECK_LENGTH_MM*sin(theta))
        out[name]={'rear':solve(h,r,P.BODY_THIGH_MM,P.BODY_SHANK_MM,1),
                   'front':solve(s,f,P.BODY_UPPER_ARM_MM,P.BODY_FOREARM_MM+P.BODY_HAND_MM,-1),
                   'neck':neck,'body_angle':degrees(theta)}
    return out


def motor_intervals():
    # Same purchased direct-drive stack as DEC-34; mirrors about the midline.
    face=P.BODY_TRACK_TARGET_MM/2-P.WHEEL_W/2-P.HUB_STACK
    return [(-face,-face+P.MOTOR_BODY_LEN),(face-P.MOTOR_BODY_LEN,face)]


def check():
    data=poses()
    for name,pose in data.items():
        for key in ('rear','front'):
            limb=pose[key]
            assert abs(limb.root.distance(limb.bend)-limb.upper)<1e-8
            assert abs(limb.bend.distance(limb.axle)-limb.lower)<1e-8
            assert 0<limb.flexion<150
        assert abs(pose['rear'].root.distance(pose['front'].root)-P.BODY_TORSO_LENGTH_MM)<1e-8
        assert abs(pose['front'].root.distance(pose['neck'])-P.BODY_NECK_LENGTH_MM)<1e-8
        assert abs(pose['rear'].axle.z-P.WHEEL_DIA/2)<1e-8
    q=data['quadruped']; u=data['upright']
    assert abs(q['front'].axle.z-P.BODY_FRONT_FOOT_RADIUS_MM)<1e-8
    assert abs(q['front'].axle.x-q['rear'].axle.x-P.BODY_WHEELBASE_TARGET_MM)<1e-8
    assert abs(u['neck'].z+P.BODY_HEAD_HEIGHT_MM-P.BODY_STANDING_HEIGHT_MM)<1e-8
    # In quadruped the nominal body axis projects inside the contact rectangle.
    assert q['rear'].axle.x < q['rear'].root.x < q['front'].root.x < q['front'].axle.x
    intervals=motor_intervals()
    gap=intervals[1][0]-intervals[0][1]
    assert gap>=P.BODY_MOTOR_GAP_MIN_MM
    assert u['front'].axle.z>P.BODY_FRONT_FOOT_RADIUS_MM
    return {'drive_motor_count':P.BODY_DRIVE_MOTOR_COUNT,
            'front_foot_radius_mm':P.BODY_FRONT_FOOT_RADIUS_MM,
            'motor_end_gap_mm':gap,'poses':data}


def svg(name,pose):
    """True-scale side view; a second front elevation makes the track explicit."""
    bits=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="-340 -510 790 580" width="1580" height="1160">',
          '<style>text{font-family:Arial,sans-serif;fill:#253d48;font-size:8px}.small{font-size:6.5px}.bone{fill:none;stroke:#16867c;stroke-width:5;stroke-linecap:round}.shell{fill:#dce8e7;stroke:#829a99;stroke-width:1;stroke-dasharray:4 3}.wheel{fill:#e1e5e8;stroke:#3c515e;stroke-width:2}.guide{fill:none;stroke:#8b9da3;stroke-width:.6}.dot{fill:#f4b769;stroke:#273f49;stroke-width:1.2}</style>',
          '<rect x="-340" y="-510" width="790" height="580" fill="#f7faf9"/>']
    def txt(x,y,s,small=False):bits.append(f'<text x="{x}" y="{y}" class="{"small" if small else ""}">{s}</text>')
    def path(a,b,cls='bone'):bits.append(f'<path class="{cls}" d="M{-a.x},{-a.z} L{-b.x},{-b.z}"/>')
    def dot(p):bits.append(f'<circle class="dot" cx="{-p.x}" cy="{-p.z}" r="4"/>')
    def dimension(x,z0,z1,label):
        bits.append(f'<path class="guide" d="M{x},{-z0} V{-z1} M{x-3},{-z0} h6 M{x-3},{-z1} h6"/>');txt(x+5,-(z0+z1)/2,label,True)
    txt(-320,-487,f'KOALA V1 · REAR WHEELS + FRONT FEET · DEC-49/50 · {name.upper()}')
    txt(-320,-474,'Dimensionally closed layout · mm · Front ← · circles: joints / terminal centres · orange lines: roll axes',True)
    txt(-320,-461,'Head outline is sizing intent only; position/mount undecided. Structural CAD omits it; loaded motion unverified.',True)
    hip,shoulder=pose['rear'].root,pose['front'].root
    # Torso envelope aligned with its 150 mm shoulder/hip axis.
    theta=pose['body_angle'];t=radians(theta)
    centre=(P.BODY_TORSO_LENGTH_MM-P.BODY_RUMP_LENGTH_MM)/2
    mid=Point(hip.x+centre*cos(t),hip.z+centre*sin(t))
    torso_radius=(P.BODY_TORSO_LENGTH_MM+P.BODY_RUMP_LENGTH_MM)/2
    bits.append(f'<ellipse class="shell" cx="{-mid.x}" cy="{-mid.z}" rx="{torso_radius}" ry="45" transform="rotate({theta} {-mid.x} {-mid.z})"/>')
    # Head envelope: neck endpoint is rear/base; includes ears within 75 mm height.
    neck=pose['neck']
    u,v=-neck.x,-neck.z;w,h=P.BODY_HEAD_LENGTH_MM,P.BODY_HEAD_HEIGHT_MM
    bits.append(f'<path class="shell" d="M{u},{v} Q{u},{v-h} {u-w/2},{v-h} Q{u-w},{v-h} {u-w},{v-h/2} Q{u-w},{v} {u},{v} Z"/>')
    path(hip,shoulder);path(shoulder,neck);dot(neck)
    txt(-mid.x+18,-mid.z-12,'Torso 150',True)
    for key,limb in ((k,pose[k]) for k in ('rear','front')):
        path(limb.root,limb.bend);path(limb.bend,limb.axle)
        for p in (limb.root,limb.bend,limb.axle):dot(p)
        dx=(limb.bend.x-limb.root.x)/limb.upper
        dz=(limb.bend.z-limb.root.z)/limb.upper
        a=Point(limb.root.x-18*dz,limb.root.z+18*dx)
        b=Point(limb.root.x+18*dz,limb.root.z-18*dx)
        bits.append(f'<path d="M{-a.x},{-a.z} L{-b.x},{-b.z}" stroke="#d47920" stroke-width="2"/>')
        p=limb.axle;radius=P.WHEEL_DIA/2 if key=='rear' else P.BODY_FRONT_FOOT_RADIUS_MM
        bits.append(f'<circle class="wheel" cx="{-p.x}" cy="{-p.z}" r="{radius}"/>');dot(p)
        for a,b,n in ((limb.root,limb.bend,limb.upper),(limb.bend,limb.axle,limb.lower)):
            txt(-(a.x+b.x)/2-19,-(a.z+b.z)/2,'100 (75+25)' if key=='front' and n==limb.lower else f'{n:g}',True)
        txt(-p.x-36,-p.z+(55 if key=='rear' else 32),'Ankle drive' if key=='rear' else 'TPU contact pad',True)
    path(Point(-130,0),Point(310,0),'guide')
    for h in range(0,451,50):
        path(Point(320,h),Point(315,h),'guide');txt(-312,-h+2,str(h),True)
    dimension(112,0,hip.z,f'Hip {hip.z:g}')
    dimension(-290,0,shoulder.z,f'Shoulder {shoulder.z:g}')
    if name=='upright':dimension(156,0,450,'450 overall')
    else:
        txt(-215,42,'Front foot–rear wheel centres: 260',True)
        txt(-215,53,'Head-top envelope: 237.7 · approximate nose–rump length: 340',True)
    txt(210,-498,'FRONT / TRACK',True)
    bits.append(f'<path class="guide" d="M285,{-hip.z} V{-shoulder.z} V{-neck.z}"/>')
    bits.append(f'<rect class="shell" x="{285-P.BODY_HEAD_WIDTH_MM/2}" y="{-neck.z-P.BODY_HEAD_HEIGHT_MM}" width="{P.BODY_HEAD_WIDTH_MM}" height="{P.BODY_HEAD_HEIGHT_MM}" rx="20"/>')
    for key,roots in [('rear',rear_axis_y()),('front',P.BODY_SHOULDER_WIDTH_MM/2)]:
        l=pose[key]
        for side in (-1,1):
            x0=285+side*roots;x1=285+side*P.BODY_TRACK_TARGET_MM/2 if key=='rear' else x0
            bits.append(f'<path class="bone" d="M{x0},{-l.root.z} V{-l.bend.z} V{-l.axle.z} H{x1}"/>')
            for p in (l.root,l.bend,l.axle):
                bits.append(f'<circle class="dot" cx="{x0}" cy="{-p.z}" r="3"/>')
            if key=='rear':
                bits.append(f'<rect class="wheel" x="{x1-5}" y="{-l.axle.z-40}" width="10" height="80" rx="4"/>')
            else:
                bits.append(f'<circle class="wheel" cx="{x1}" cy="{-l.axle.z}" r="{P.BODY_FRONT_FOOT_RADIUS_MM}"/>')
    lo=285-P.BODY_TRACK_TARGET_MM/2; hi=285+P.BODY_TRACK_TARGET_MM/2
    bits.append(f'<path class="guide" d="M{lo},0 H{hi} M{lo},10 v15 M{hi},10 v15 M{lo},20 H{hi}"/>')
    txt(242,35,f'{P.BODY_TRACK_TARGET_MM:g} wheel-centre track',True)
    txt(190,-487,f'Roll centres: {P.BODY_SHOULDER_WIDTH_MM:g} shoulder · {2*rear_axis_y():g} hip',True)
    txt(190,-476,f'Pitch servo centres: {2*P.ROOT_PITCH_Y:g} · pitch → roll → knee/elbow',True)
    txt(195,-465,'Rear: Ø80 drives ×2 · Front: Ø32 fixed feet',True)
    txt(195,-454,f'Opposed motor end gap: {check()["motor_end_gap_mm"]:g}',True)
    txt(-320,65,'Engineering master only: no actuator torque, collision-free transition or physical fit acceptance is implied.',True)
    bits.append('</svg>');return '\n'.join(bits)


def rear_axis_y():
    return P.BODY_SHOULDER_WIDTH_MM/2


def cad_items(name,pose):
    """Review solids for the actual joint centres and bought-wheel/motor envelopes."""
    from build123d import Cylinder, Box, Sphere, Plane, Pos, Align
    out=[]
    def rod(a,b,y,label,r=5):
        length=a.distance(b)
        loc=Plane(origin=(a.x,y,a.z),z_dir=(b.x-a.x,0,b.z-a.z)).location
        out.append((label,loc*Cylinder(r,length,align=(Align.CENTER,Align.CENTER,Align.MIN))))
    def axial(p,y,length,r,label):
        loc=Plane(origin=(p.x,y,p.z),z_dir=(0,1,0)).location
        out.append((label,loc*Cylinder(r,length,align=(Align.CENTER,Align.CENTER,Align.MIN))))
    for side in (-1,1):
        for key,y in [('rear',rear_axis_y()),('front',P.BODY_SHOULDER_WIDTH_MM/2)]:
            l=pose[key];y*=side
            rod(l.root,l.bend,y,f'{key}_upper_{side}');rod(l.bend,l.axle,y,f'{key}_lower_{side}')
            for i,p in enumerate((l.root,l.bend,l.axle)):
                out.append((f'{key}_axis_{i}_{side}',Pos(p.x,y,p.z)*Sphere(7)))
            if key=='front':
                out.append((f'front_foot_{side}',Pos(l.axle.x,y,l.axle.z)*Sphere(P.BODY_FRONT_FOOT_RADIUS_MM)))
                continue
            wy=side*P.BODY_TRACK_TARGET_MM/2
            axial(l.axle,wy-P.WHEEL_W/2,P.WHEEL_W,P.WHEEL_DIA/2,f'{key}_wheel_{side}')
            axial(l.axle,min(y,wy),abs(wy-y),3,f'{key}_axle_{side}')
        lo,hi=motor_intervals()[0 if side==-1 else 1]
        for key in ('rear',):
            axial(pose[key].axle,lo,hi-lo,P.MOTOR_DIA/2,f'{key}_motor_{side}')
    rod(pose['rear'].root,pose['front'].root,0,'torso_axis',8)
    rod(pose['front'].root,pose['neck'],0,'neck_axis',5)
    n=pose['neck']
    out.append(('head_envelope',Pos(n.x,-P.BODY_HEAD_WIDTH_MM/2,n.z)*Box(P.BODY_HEAD_LENGTH_MM,P.BODY_HEAD_WIDTH_MM,P.BODY_HEAD_HEIGHT_MM,align=(Align.MIN,Align.MIN,Align.MIN))))
    return out


def write(output, with_cad=False):
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    result=check()
    def serial(v):
        if hasattr(v,'__dataclass_fields__'):return asdict(v)
        raise TypeError(type(v))
    (output/'body-plan.json').write_text(json.dumps(result,default=serial,indent=2))
    for name,pose in result['poses'].items():
        (output/f'body-{name}.svg').write_text(svg(name,pose))
        if with_cad:
            from build123d import Compound, export_step
            solids=[]
            for label,solid in cad_items(name,pose):solid.label=label;solids.append(solid)
            export_step(Compound(children=solids),str(output/f'body-{name}.step'))
    print(f'PASS exact link lengths, torso/neck closure, floor contacts, wheelbase and {result["motor_end_gap_mm"]:g} mm motor gap')


def render_pngs(output):
    """Optional browser rasterization for iPad Files; preserves the SVG scale."""
    import os
    from playwright.sync_api import sync_playwright
    output=Path(output).resolve()
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True,
            executable_path=os.environ.get('PLAYWRIGHT_CHROMIUM'),args=['--no-sandbox'])
        page=browser.new_page(viewport={'width':1580,'height':1160},device_scale_factor=2)
        for name in ('quadruped','upright'):
            page.goto((output/f'body-{name}.svg').as_uri())
            page.locator('svg').screenshot(path=str(output/f'body-{name}.png'))
        browser.close()


if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',default='build/body-plan');ap.add_argument('--cad',action='store_true')
    ap.add_argument('--png',action='store_true',help='render PNGs with optional Playwright/Chromium')
    args=ap.parse_args();write(args.output,args.cad)
    if args.png:render_pngs(args.output)
