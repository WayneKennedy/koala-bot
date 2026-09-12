# SPDX-License-Identifier: CERN-OHL-S-2.0
"""DEC-42 local knee envelope study; not structural CAD or a gait validation.

Native X is lateral/output axis, Y is fore/aft in the thigh frame, Z points
from knee toward a straight lower leg. Positive fold angles move away from
positive-Y motor offsets. No drive carrier, foot or complete robot is solved.
"""
import json
from pathlib import Path
from build123d import Pos,Rot
from . import params as P,servo_iface as S
from .parts import links as L
from .audit import overlap


def study():
    servo=L.AXIS*S.socket_reference()
    thigh=Pos(0,0,-P.BODY_THIGH_MM)*L.upper_link(P.BODY_THIGH_MM)
    shank=L.clevis()+S._box(-8,8,-8,8,18,P.BODY_SHANK_MM)
    angles=(0,30,60,90,120)
    face=L.motor_face(False);rows=[]
    for offset in (0,25,30,35,40,45):
        motor=S._x_hole(face-P.MOTOR_BODY_LEN,face,offset,0,P.MOTOR_DIA)
        wheel=S._x_hole(face+P.HUB_STACK,face+P.HUB_STACK+P.WHEEL_W,offset,0,P.WHEEL_DIA)
        rows.append({'offset_mm':offset,
            'motor_servo_overlap_mm3':round(overlap(motor,servo),3),
            'motor_thigh_overlap_mm3':round(overlap(motor,thigh),3),
            'motor_servo_distance_mm':round(motor.distance_to(servo),3),
            'wheel_thigh_overlap_mm3':round(overlap(wheel,thigh),3),
            'shank_motor_overlap_mm3':[round(overlap(Rot(X=a)*shank,motor),3) for a in angles]})
    outboard=P.SOCKET_DRIVE_FACE+P.SOCKET_PAD_T
    coaxial_track=2*(L.rear_axis_y()+outboard+3+P.MOTOR_BODY_LEN+P.HUB_STACK+P.WHEEL_W/2)
    return {'reference':'imported case + measured horns' if S.case_model() is not None else 'parametric case + measured horns',
        'native_frame':'X lateral, Y fore/aft in thigh frame, Z down straight shank',
        'fold_angles_deg':angles,'offset_sweep':rows,
        'shank_servo_overlap_mm3':[round(overlap(Rot(X=a)*shank,servo),3) for a in angles],
        'shank_thigh_overlap_mm3':[round(overlap(Rot(X=a)*shank,thigh),3) for a in angles],
        'existing_track_mm':P.BODY_TRACK_TARGET_MM,
        'existing_knee_centre_spacing_mm':2*L.rear_axis_y(),
        'outboard_coaxial_stack_track_mm':round(coaxial_track,1),
        'coaxial_stack_assumed_clearance_mm':3,
        'limits':'Local nominal envelope study only. Shank is retained clevis + 16 mm beam, not final foot geometry. No motor mounts, hardware heads, wiring, full-robot collisions, continuous sweep, strength or loaded poses.'}


def diagram(result):
    # Dimensioned 2D projections; the side view intentionally overlaps items
    # which occupy different lateral planes. Not a depiction of assembled prints.
    if any(abs(a-b)>1e-6 for a,b in ((P.MOTOR_DIA,37),(P.MOTOR_BODY_LEN,69),(P.SOCKET_DRIVE_FACE+P.SOCKET_PAD_T,25.7),(P.SOCKET_IDLER_FACE-P.SOCKET_PAD_T,-23.3),(P.HUB_STACK,18),(P.HUB_T,9.5),(P.WHEEL_W,10),(P.WHEEL_DIA,80),(2*L.rear_axis_y(),149.2))):
        raise ValueError('Update the dimensioned SVG template for changed hardware')
    parts=['''<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="810" viewBox="0 0 1400 810">
<style>text{font-family:Arial,sans-serif;fill:#203c4b;font-size:19px}.small{font-size:16px}.label{font-size:10px}.dim{stroke:#203c4b;fill:none;stroke-width:1}</style>
<rect width="1400" height="810" fill="#f6f9fa"/>
<text x="40" y="44" font-size="26">Knee drive packaging — DEC-42 envelope study</text>
<text x="40" y="76">37D body: Ø37 × 69 mm · Knee clevis: 49 mm across · Wheel: Ø80 mm</text>
<text x="40" y="120">A. Offset direct drive — side projection</text>
<text x="745" y="120">B. Coaxial outboard stack — axial section</text>
<text class="small" x="40" y="152">Wheel and motor share an axis; knee axis is separate.</text>
<text class="small" x="745" y="152">Servo and motor cannot occupy the same axial space.</text>
<g transform="translate(310,390) scale(2.5)">
<rect x="-8" y="-85" width="16" height="50" fill="#a6bfd2"/>
<rect x="-12.35" y="-35.115" width="24.7" height="45.23" fill="#efd277" stroke="#867128"/>
<circle cx="40" cy="0" r="40" fill="#a8bac5" fill-opacity=".16" stroke="#546b78" stroke-dasharray="3 2"/>
<circle cx="40" cy="0" r="18.5" fill="#e6a28a" fill-opacity=".85" stroke="#af5e42"/>
<circle cx="40" cy="0" r="2" fill="#203c4b"/>
''']
    for a in (0,60,90,120):
        colour='#bd3b3b' if a==120 else '#389c8a'
        parts.append(f'<g transform="rotate({a})"><path d="M0,18 V90" stroke="{colour}" opacity=".3" stroke-width="16"/><circle r="10.4" fill="none" stroke="#389c8a"/></g>')
    parts.append('''<circle r="2" fill="#203c4b"/>
<path class="dim" d="M0,-49 V-60 M40,-49 V-60 M0,-56 H40"/>
<text class="label" x="3" y="-63">40 mm</text>
<text class="label" x="-55" y="-75">Thigh</text>
</g>
<text class="small" x="40" y="662">Gold: knee servo · Orange: drive motor · Dashed: tyre</text>
<text class="small" x="40" y="689">Green: lower leg at 0°, 60°, 90°; red 120° hits servo.</text>
<text class="small" x="40" y="716">Fold shown away from motor; front/aft choice is still open.</text>
<g transform="translate(855,390) scale(2.5)">
<rect x="-23.3" y="-25" width="49" height="50" fill="#a6bfd2" stroke="#526e84"/>
<rect x="28.7" y="-18.5" width="69" height="37" fill="#e6a28a" stroke="#af5e42"/>
<rect x="97.7" y="-3" width="21" height="6" fill="#788e9b"/>
<rect x="106.2" y="-12.7" width="9.5" height="25.4" fill="#acbdc6"/>
<rect x="115.7" y="-40" width="10" height="80" fill="#627582"/>
<path class="dim" d="M-23.3,-31 V-53 M25.7,-31 V-53 M-23.3,-48 H25.7 M28.7,-25 V-53 M97.7,-25 V-53 M28.7,-48 H97.7"/>
<text class="label" x="-9" y="-57">49 mm</text><text class="label" x="48" y="-57">69 mm</text>
<path class="dim" d="M0,46 V62 M120.7,46 V62 M0,57 H120.7"/>
<text class="label" x="21" y="73">120.7 mm to wheel centre</text>
</g>
<text class="small" x="745" y="630">3 mm joint/motor gap; retained hub/tyre stack.</text>
''')
    parts.append(f'<text x="745" y="664">Resulting track: {result["outboard_coaxial_stack_track_mm"]:g} mm (current: {P.BODY_TRACK_TARGET_MM:g})</text>')
    parts.append('''<text class="small" x="745" y="695">Conditional on current 149.2 mm knee spacing.</text>
<text class="small" x="40" y="768">Local clearance evidence only. Motor carrier, foot, screws, cables, whole-body poses and strength are NOT validated.</text>
</svg>''')
    return '\n'.join(parts)


def main():
    out=Path(__file__).resolve().parents[3]/'docs/design'
    result=study()
    (out/'knee-packaging.json').write_text(json.dumps(result,indent=2)+'\n')
    (out/'knee-packaging.svg').write_text(diagram(result))
    print(json.dumps(result,indent=2),flush=True)


if __name__=='__main__':main()
