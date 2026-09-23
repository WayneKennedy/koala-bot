"""MuJoCo MJCF of the four-foot walking build (DEC-62), from the CAD's solids and kinematic frames.

    uv run python -m koala_hardware.mjcf              # sim/koala_walking.xml + .json + meshes/*.stl
    uv run python -m koala_hardware.mjcf --crude      # sim/koala_walking_crude.xml: capsule visuals, same inertia
    uv run python -m koala_hardware.mjcf OUT.xml      # elsewhere (meshes/ beside it)

Bodies are the CAD's rigid groups (assembly.nominal_details): every print of a group plus the servo
case(s) its socket frames place, unioned and exported as one visual STL per body in that body's
joint frame. Inertia is computed per solid from the BREP and summed per body: prints at an effective
density (the slicer's filament volume where a docs/design/*/slices.json record matches the current
STL hash, exactly as the BOM does; else solid PETG/TPU, an upper bound), each servo as a
SERVO_MASS box of the case dimensions at its socket. Omitted: fasteners, horn/ear screw heads,
the unbought neck-servo envelopes, battery, electronics, head and cables. Contacts are the four
sphere feet and a torso box for fall detection. Joint ranges are the viewer's shared-slider
clearance bounds (no per-joint search exists), and the actuator is Open Duck's BAM fit of the
7.4 V STS3215 until the 12 V unit is identified (wk-robotics docs/status.md, "A sim model of
koala-bot's four-foot build"). Nothing here is verified against hardware. Loading the output needs
MuJoCo, which is not a dependency of this package: mjcf_check.py runs from any venv that has it.
"""
import hashlib, json, sys, tempfile
from pathlib import Path
import numpy as np
from build123d import Box, Pos, Plane, Align, CenterOf, Compound, mirror, export_stl
from OCP.BRepTools import BRepTools
from koala_hardware import assembly as A, body_plan as B, params as P
from koala_hardware.export import DENSITY                       # g/cm3 PETG 1.27, TPU 1.2 (provisional)
from koala_hardware.meshing import export_mesh
from koala_hardware.parts import configuration_specs, links, torso

ROOT = Path(__file__).resolve().parents[2]
SLICE_RECORDS = [ROOT.parent / 'docs/design' / d / 'slices.json' for d in ('walking', 'manufacturing', 'front-redesign')]
MM = 1e-3
SERVO_G = P.SERVO_MASS                                          # 55 g [SPEC], params.py
SERVO_CASE = (P.SOCKET_CASE_X, P.SOCKET_CASE_Y, P.SOCKET_CASE_L)  # 34.9 x 24.7 x 45.23 mm, socket frame (servo_iface.py)
MESH_TOL = (0.2, 0.6)                                            # export_stl linear mm, angular rad: visual only
# Shared-control clearance bounds in the walking pose (degrees, relative to the pose),
# docs/design/walking/viewer-endpoints.json "initial_pose_bounds.walking". These are
# sampled CAD clearances for ONE shared slider driving all limbs, not servo limits.
RANGE = {'pitch': (-43.5, 107.5), 'roll': (-16.0, 29.25), 'bend': (-61.25, 89.25)}
# Placeholder actuator: Open Duck's BAM fit of the 7.4 V STS3215
# (Open_Duck_Playground/.../open_duck_mini_v2.xml:45-49). 12 V fit is plan step 1.
SERVO_CLASS = dict(damping=0.56, frictionloss=0.068, armature=0.027, kp=13.37, force=3.23)
# nominal_details name (hand suffix stripped) -> BOM export name (export.py variants)
EXPORT_NAME = {'pelvis_socket': 'root_socket', 'shoulder_socket': 'root_socket', 'rear_carrier': 'hip_carrier',
               'rear_thigh': 'thigh', 'rear_shank': 'foot_shank', 'rear_contact_pad': 'front_contact_pad',
               'front_carrier': 'shoulder_carrier', 'front_upper_arm': 'upper_arm', 'front_forearm': 'forearm'}
HANDED = {'root_socket', 'hip_carrier', 'thigh', 'foot_shank', 'shoulder_carrier', 'upper_arm', 'forearm', 'shoulder_mount'}
JOINT_NAMES = {'rear': {'pitch': 'hip_pitch', 'roll': 'hip_roll', 'bend': 'knee'},
               'front': {'pitch': 'shoulder_pitch', 'roll': 'shoulder_roll', 'bend': 'elbow'}}


def export_name(item):
    """nominal_details item name -> (BOM export name incl. hand, material)."""
    hand = ''
    for suffix in ('_right', '_left'):
        if item.endswith(suffix):
            item, hand = item[:-len(suffix)], suffix
    if item.startswith('tray_spacer'):
        item = 'tray_spacer'
    base = EXPORT_NAME.get(item, item)
    return base + (hand if base in HANDED else ''), ('TPU' if 'contact_pad' in base else 'PETG')


def slicer_masses(names):
    """{export name: record} where the current STL (built exactly as export.py builds it) hashes to a slice record."""
    records = {}
    for path in SLICE_RECORDS:
        if path.exists():
            for r in json.loads(path.read_text())['parts']:
                records.setdefault(r['stl_sha256'], (r, f'{path.parent.name}/{path.name}'))
    found = {}
    with tempfile.TemporaryDirectory() as tmp:
        for spec in configuration_specs('walking'):
            if spec['name'] not in {n.removesuffix('_right').removesuffix('_left') for n in names}:
                continue
            oriented = spec['orientation'] * spec['part']
            variants = ([(f"{spec['name']}_right", oriented), (f"{spec['name']}_left", mirror(oriented, Plane.XZ))]
                        if spec.get('handed') else [(spec['name'], oriented)])
            for name, solid in variants:
                if name not in names:
                    continue
                solid = Pos(0, 0, -solid.bounding_box().min.Z) * solid
                f = Path(tmp) / f'{name}.stl'
                export_mesh(solid, f)
                hit = records.get(hashlib.sha256(f.read_bytes()).hexdigest())
                if hit:
                    r, src = hit
                    found[name] = {'cm3': r['filament_cm3'], 'source': src, 'sha256': r['stl_sha256'][:12]}
    return found


def props(shape):
    """Volume (mm3), centroid (mm) and volume-inertia about the centroid (mm5) of a BREP shape."""
    v = shape.volume
    c = np.array(tuple(shape.center(CenterOf.MASS)))
    return v, c, np.array(shape.matrix_of_inertia)              # OCC GProp: already about the centroid


def servo_boxes(pose_name):
    """{reference servo item name: box solid, world mm} for all twelve limb servos."""
    box = Box(*SERVO_CASE, align=(Align.CENTER, Align.CENTER, Align.MIN))
    out = {}
    for name, _owner, frame in A.socket_frames(pose_name):
        right = frame * box
        out[name] = right
        out[name.replace('_right', '_left')] = mirror(right, Plane.XZ)
    return out


def collect(pose_name='walking'):
    """Per MJCF body: its solids (world mm), each with a mass-model role, plus the body's joint origin."""
    jd = A.joint_data(pose_name)
    pose = B.poses()[pose_name]
    hip = np.array([pose['rear'].root.x, 0.0, pose['rear'].root.z])
    bodies = {'torso': {'origin': hip, 'parent': None, 'joint': None, 'items': []}}
    group_of = {'fixed': 'torso', 'rear_fixed': 'torso', 'front_fixed': 'torso'}
    for key in ('rear', 'front'):
        d = jd[key]
        for side, sname in ((1, 'right'), (-1, 'left')):
            prev = 'torso'
            for stage, part in zip(d['order'], ('carrier', 'upper', 'lower')):
                body = f'{key}_{sname}_{part}'
                centre = np.array(d[stage]) * [1, side, 1]
                axis = side * np.array(d['roll_axis']) if stage == 'roll' else np.array([0., 1., 0.])  # mirrored roll: same axis, opposite sign
                bodies[body] = {'origin': centre, 'parent': prev, 'items': [], 'side': side, 'key': key,
                                'joint': {'name': f'{key}_{sname}_{JOINT_NAMES[key][stage]}', 'axis': axis, 'range': RANGE[stage]}}
                group_of[(f'{key}_{stage}', side)] = body
                prev = body
    boxes = servo_boxes(pose_name)
    for name, shape, _colour, group, side in A.nominal_details(pose_name):
        body = group_of.get(group) or group_of[(group, side)]
        if name.startswith('reference_'):
            if name in boxes:
                bodies[body]['items'].append({'name': name, 'role': 'servo', 'visual': shape, 'mass_shape': boxes[name]})
            continue                                              # screw heads, fixings, neck envelopes: omitted
        bodies[body]['items'].append({'name': name, 'role': 'print', 'visual': shape, 'mass_shape': shape})
    for key in ('rear', 'front'):
        limb = pose[key]
        y = P.BODY_SHOULDER_WIDTH_MM / 2 if key == 'front' else links.rear_axis_y()
        for side, sname in ((1, 'right'), (-1, 'left')):
            bodies[f'{key}_{sname}_lower']['foot'] = np.array([limb.axle.x, side * y, limb.axle.z])
    return bodies


def mass_model(bodies):
    """Fill each item's mass_g and each body's mass, com (world mm) and inertia about it (kg m2). Returns the per-print table."""
    prints = {it['name']: export_name(it['name']) for b in bodies.values() for it in b['items'] if it['role'] == 'print'}
    sliced = slicer_masses({e for e, _ in prints.values()})
    table = {}
    for b in bodies.values():
        total = 0.0; first = np.zeros(3); inertia = []
        for it in b['items']:
            v, c, ic = props(it['mass_shape'])                    # mm3, mm, mm5
            assert v > 0, it['name']
            if it['role'] == 'servo':
                m, src = SERVO_G, 'servo box'
            else:
                e, material = prints[it['name']]
                if e in sliced:
                    m, src = sliced[e]['cm3'] * DENSITY[material], f"slicer {sliced[e]['source']}"
                else:
                    m, src = DENSITY[material] * v / 1000, f'solid {material}'
                table[e] = {'mass_g': m, 'solid_g': DENSITY[material] * v / 1000, 'source': src, 'material': material}
            rho = m / v                                           # g/mm3, uniform over the solid
            it.update(mass_g=m, density_g_cm3=rho * 1000, source=src)
            total += m; first += m * c; inertia.append((m, c, rho * ic))  # g mm2
        com = first / total
        i = sum(ic + m * ((d := c - com) @ d * np.eye(3) - np.outer(d, d)) for m, c, ic in inertia)
        b.update(mass_g=total, com=com, inertia=i * 1e-3 * MM**2)  # g mm2 -> kg m2
    return table


def union(items, key='visual'):
    u = None
    for it in items:
        for s in it[key].solids():
            u = s if u is None else u + s
    return u


def write_mesh(bodies, name, path):
    b = bodies[name]
    try:
        shape = union(b['items']); kind = 'union'
    except Exception as e:                                         # boolean failure: ship the shells unfused
        shape = Compound(children=[s for it in b['items'] for s in it['visual'].solids()]); kind = f'compound ({e})'
    shape = Pos(*(-b['origin'])) * shape
    BRepTools.Clean_s(shape.wrapped)                               # drop any finer cached triangulation
    export_stl(shape, str(path), tolerance=MESH_TOL[0], angular_tolerance=MESH_TOL[1])
    return kind, path.stat().st_size


def v3(p): return ' '.join(f'{x*MM:.6f}' for x in p)
def ax(a): return ' '.join(f'{x:.6f}' for x in a)


def inertial(b):
    i = b['inertia']
    return (f'<inertial pos="{v3(b["com"] - b["origin"])}" mass="{b["mass_g"]*1e-3:.5f}" '
            f'fullinertia="{i[0,0]:.3e} {i[1,1]:.3e} {i[2,2]:.3e} {i[0,1]:.3e} {i[0,2]:.3e} {i[1,2]:.3e}"/>')


def build(out, crude=False, pose_name='walking'):
    out = Path(out); out.parent.mkdir(parents=True, exist_ok=True)
    pose = B.poses()[pose_name]
    bodies = collect(pose_name)
    table = mass_model(bodies)
    meshes = {}
    if not crude:
        (out.parent / 'meshes').mkdir(exist_ok=True)
        for name in bodies:
            meshes[name] = write_mesh(bodies, name, out.parent / 'meshes' / f'{name}.stl')
    sliced = sorted(e for e, r in table.items() if r['source'].startswith('slicer'))
    solid = sorted(e for e, r in table.items() if r['source'].startswith('solid'))
    total = sum(b['mass_g'] for b in bodies.values())
    com = sum(b['mass_g'] * b['com'] for b in bodies.values()) / total
    theta = pose['body_angle']
    L = []; w = L.append
    w(f'<mujoco model="koala_walking{"_crude" if crude else ""}">')
    w(f'  <!-- Generated by koala_hardware/mjcf.py from koala-bot CAD, {pose_name} pose (DEC-62). Do not hand-edit. -->')
    w('  <!-- visuals: ' + ('CRUDE capsules between joint centres, not the prints' if crude else
      f'one STL per body in meshes/ (mm, scaled), the body\'s prints unioned with its servo case(s) at the CAD socket frames; tolerance {MESH_TOL[0]} mm / {MESH_TOL[1]} rad') + ' -->')
    w(f'  <!-- inertia: per solid from the CAD BREP, summed per body. Prints at an effective density: slicer filament volume x PETG {DENSITY["PETG"]} / TPU {DENSITY["TPU"]} g/cm3 where the current STL hash matches a docs/design/*/slices.json record ({", ".join(sliced)}); otherwise SOLID density, an upper bound ({", ".join(solid)}). Each servo a {SERVO_G:g} g [SPEC] uniform box {SERVO_CASE[0]} x {SERVO_CASE[1]} x {SERVO_CASE[2]} mm at its socket. -->')
    w(f'  <!-- omitted mass: fasteners, horn/ear screw heads, neck servo envelopes (unbought), battery, electronics, head, cables. Total {total/1000:.3f} kg; CoM world {v3(com)} m in this pose. -->')
    w('  <!-- contacts: four sphere feet (contype 1) and a torso box (contype 2) for fall detection only; link meshes do not collide -->')
    w('  <!-- joint ranges: the viewer\'s shared-slider clearance bounds (viewer-endpoints.json), one slider per axis for all limbs; no per-joint search exists. NOT servo limits -->')
    w('  <!-- actuator: Open Duck 7.4 V BAM placeholder, NOT the 12 V unit -->')
    w('  <!-- CAD "right" is +Y (params.py body +Y right). With X forward / Z up that is the robot LEFT in a right-handed frame; names below follow the CAD. -->')
    w('  <compiler angle="degree" meshdir="meshes"/>')
    w('  <option timestep="0.002"/>')
    w('  <visual><global offwidth="1280" offheight="960"/></visual>')
    w('  <default>')
    w('    <default class="sts3215">')
    w(f'      <joint type="hinge" damping="{SERVO_CLASS["damping"]}" frictionloss="{SERVO_CLASS["frictionloss"]}" armature="{SERVO_CLASS["armature"]}" limited="true"/>')
    w(f'      <position kp="{SERVO_CLASS["kp"]}" forcerange="-{SERVO_CLASS["force"]} {SERVO_CLASS["force"]}"/>')
    w('    </default>')
    w('    <default class="visual"><geom contype="0" conaffinity="0" group="1" rgba="0.55 0.7 0.85 1"/></default>')
    w('    <default class="foot"><geom type="sphere" contype="1" conaffinity="1" condim="3" friction="0.8" rgba="0.3 0.3 0.3 1"/></default>')
    w('  </default>')
    if meshes:
        w('  <asset>')
        for name in bodies:
            w(f'    <mesh name="{name}" file="{name}.stl" scale="0.001 0.001 0.001"/>')
        w('  </asset>')
    w('  <worldbody>')
    w('    <light pos="0 0 2" dir="0 0 -1" directional="true"/>')
    w('    <geom name="floor" type="plane" size="0 0 0.05" contype="1" conaffinity="3" friction="0.8" rgba="0.9 0.9 0.9 1"/>')
    hip = bodies['torso']['origin']
    w(f'    <body name="torso" pos="{v3(hip)}">')
    w('      <freejoint name="floating_base"/>')
    w('      <site name="imu" pos="0.06 0 0.02"/>')
    w('      ' + inertial(bodies['torso']))
    bb = torso.solid().bounding_box()                             # torso_frame, body-native frame: X ventral depth, Y width, Z along the spine
    centre = np.array(tuple((A.body_location(pose) * Pos(*tuple(bb.center()))).position)) - hip
    w(f'      <geom name="torso_box" type="box" size="{v3([s / 2 for s in tuple(bb.size)])}" pos="{v3(centre)}" euler="0 {90-theta:.4f} 0" contype="2" conaffinity="2" group="3" rgba="0.6 0.6 0.7 0.3"/>')
    if not crude:
        w('      <geom class="visual" type="mesh" mesh="torso"/>')
    acts = []
    def emit(name, depth):
        b = bodies[name]; ind = '  ' * depth
        parent = bodies[b['parent']]
        w(f'{ind}<body name="{name}" pos="{v3(b["origin"] - parent["origin"])}">')
        j = b['joint']
        w(f'{ind}  <joint name="{j["name"]}" class="sts3215" axis="{ax(j["axis"])}" range="{j["range"][0]} {j["range"][1]}"/>')
        w(f'{ind}  ' + inertial(b))
        acts.append(j['name'])
        children = [n for n, c in bodies.items() if c['parent'] == name]
        if crude:
            end = bodies[children[0]]['origin'] if children else b['foot']
            r = {'carrier': 0.012, 'upper': 0.014, 'lower': 0.010}[name.rsplit('_', 1)[1]]
            w(f'{ind}  <geom class="visual" type="capsule" size="{r}" fromto="0 0 0 {v3(end - b["origin"])}"/>')
        else:
            w(f'{ind}  <geom class="visual" type="mesh" mesh="{name}"/>')
        if 'foot' in b:
            f = b['foot'] - b['origin']
            w(f'{ind}  <geom name="{name.rsplit("_", 1)[0]}_pad" class="foot" size="{P.BODY_FRONT_FOOT_RADIUS_MM*MM:.4f}" pos="{v3(f)}" mass="0"/>')
            w(f'{ind}  <site name="{name.rsplit("_", 1)[0]}_foot" pos="{v3(f)}"/>')
        for c in children:
            emit(c, depth + 1)
        w(f'{ind}</body>')
    for name, b in bodies.items():
        if b['parent'] == 'torso':
            emit(name, 3)
    w('    </body>')
    w('  </worldbody>')
    w('  <actuator>')
    for a in acts:
        w(f'    <position class="sts3215" name="{a}" joint="{a}" inheritrange="1"/>')
    w('  </actuator>')
    w('  <sensor>')
    w('    <gyro site="imu" name="gyro"/><accelerometer site="imu" name="accelerometer"/><framezaxis objtype="site" objname="imu" name="upvector"/>')
    for a in ('rear_right', 'rear_left', 'front_right', 'front_left'):
        w(f'    <framepos objtype="site" objname="{a}_foot" name="{a}_foot_pos"/>')
    w('  </sensor>')
    w('  <keyframe>')
    w(f'    <key name="home" qpos="{v3(hip)} 1 0 0 0 {" ".join("0"*12)}" ctrl="{" ".join("0"*12)}"/>')
    w('  </keyframe>')
    w('</mujoco>')
    out.write_text('\n'.join(L) + '\n')
    record = {
        'model': out.name, 'pose': pose_name, 'crude': crude, 'total_g': total, 'com_world_mm': com.tolist(),
        'prints_g': table, 'servo_g': SERVO_G, 'servo_box_mm': SERVO_CASE, 'density_g_cm3': DENSITY,
        'bodies': {n: {'mass_g': b['mass_g'], 'com_world_mm': b['com'].tolist(),
                       'items': {it['name']: {'mass_g': it['mass_g'], 'source': it['source']} for it in b['items']},
                       **({'mesh': {'kind': meshes[n][0], 'bytes': meshes[n][1]}} if meshes else {})} for n, b in bodies.items()},
        'joint_ranges_deg': RANGE, 'joint_ranges_source': 'docs/design/walking/viewer-endpoints.json initial_pose_bounds.walking (shared slider, not per joint)',
        'actuator': 'Open Duck 7.4 V BAM placeholder', 'omitted': 'fasteners, screw heads, neck envelopes, battery, electronics, head, cables'}
    out.with_suffix('.json').write_text(json.dumps(record, indent=1) + '\n')
    print(f'wrote {out} | total {total:.0f} g | CoM world mm {np.round(com, 1).tolist()}'
          + (f' | meshes {sum(m[1] for m in meshes.values())/1e6:.2f} MB' if meshes else ''))
    for e, r in sorted(table.items()):
        print(f'  {e:24s} {r["mass_g"]:6.1f} g  (solid {r["solid_g"]:6.1f} g)  {r["source"]}')
    for n, b in bodies.items():
        print(f'  body {n:20s} {b["mass_g"]:6.1f} g' + (f'  mesh {meshes[n][0]} {meshes[n][1]/1e3:.0f} kB' if meshes else ''))
    return bodies


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    crude = '--crude' in sys.argv
    build(args[0] if args else ROOT / 'sim' / ('koala_walking_crude.xml' if crude else 'koala_walking.xml'), crude=crude)
