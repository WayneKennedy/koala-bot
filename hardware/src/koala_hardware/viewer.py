# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Local 3D viewer for the lower-body assembly and the printed parts.

    uv run python -m koala_hardware.viewer            # build, serve, open
    uv run python -m koala_hardware.viewer --build    # regenerate data only
    uv run python -m koala_hardware.viewer --port N   # default 8017

Writes build/viewer/scene.json next to the checked-in viewer.html, so any
harness can refresh the geometry and just reload the browser tab. The viewer
is an inspection aid. Build/audit checks have limited scope; no combination
of these establishes hardware fit, continuous clearance or printed strength.
"""
import argparse
import base64
import http.server
import json
import math
import pathlib
import shutil
import tempfile
import webbrowser
import subprocess

import numpy as np
import trimesh
from build123d import export_stl, Plane, mirror

from . import assembly
from . import params as P, servo_iface as S
from .parts import all_builders
from .printability import metrics
from . import body_plan
from .meshing import export_mesh

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "build" / "viewer"
HTML = pathlib.Path(__file__).parent / "viewer.html"

PART_COLOURS = ["#8fb4d9", "#d9d08f", "#d9a48f", "#c98fd9", "#8fd9c9",
                "#b4d98f", "#d98f9e", "#8f9ed9", "#d9c48f", "#9ed98f"]
GRID_STEP = 20.0     # mm, viewer floor grid
PART_GAP = 15.0      # mm between parts in the layout
LAYOUT_W = 430.0     # mm; wrap width, chosen to read as a grid rather
                     # than the one-per-row column a 200 mm bed forces


def _mesh(solid, tmp: pathlib.Path, i: int) -> trimesh.Trimesh:
    path = tmp / f"{i}.stl"
    return export_mesh(solid, path, tolerance=.08, angular_tolerance=.25)


def _item(name: str, mesh: trimesh.Trimesh, colour: str, **extra) -> dict:
    v = np.asarray(mesh.vertices, dtype=np.float32)
    f = np.asarray(mesh.faces, dtype=np.uint32)
    lo, hi = mesh.bounds
    return {
        "name": name,
        "colour": colour,
        "tris": int(len(f)),
        "size": [round(float(x), 1) for x in (hi - lo)],
        "pos": base64.b64encode(v.tobytes()).decode(),
        "idx": base64.b64encode(f.tobytes()).decode(),
        **extra,
    }


def _assembly_items(tmp: pathlib.Path, pose="quadruped") -> list[dict]:
    items = []
    specs={d['name']:d for d in (f() for f in all_builders())}
    cores={}
    # Use the conservative caliper case for collision search, avoiding cosmetic
    # details in the imported STEP. Visual geometry remains the supplied STEP.
    from unittest.mock import patch
    with patch.object(S,'case_model',return_value=None):
        collision_case=S.socket_reference.__wrapped__()
    # Only for the servo's OWN coaxial fork: the circular horns, boss and
    # centre head sit in rotationally invariant, audited contact/relief zones.
    # Test the full conservative case here; retain all hardware for other pairs.
    clipped=S._parametric_case()
    for ref,mount,tf in assembly.socket_frames(pose):
        key=ref.split('_')[1]
        joint=ref.split('_')[2]
        partner=key+'_'+({'pitch':'carrier','roll':'upper_arm' if key=='front' else 'thigh','elbow':'forearm','knee':'shank'}[joint])
        for side in ('right','left'):
            core=tf*clipped
            if side=='left':core=mirror(core,Plane.XZ)
            matrix=np.eye(4)
            for r in range(3):
                for c in range(4):matrix[r,c]=tf.wrapped.Transformation().Value(r+1,c+1)
            if side=='left':matrix=np.diag([1,-1,1,1])@matrix
            cores[ref.replace('_right','_'+side)]=(partner+'_'+side,core,tf*collision_case if side=='right' else mirror(tf*collision_case,Plane.XZ),matrix.T.flatten().tolist())
    for i, (name, solid, colour, group, side) in enumerate(assembly.scene_details(pose=pose)):
        ghost = name.startswith("reference")
        bought = any("_"+s+"_" in name for s in ("motor", "shaft", "hub", "wheel"))
        tag=name.removesuffix('_right').removesuffix('_left')
        tag={'rear_carrier':'root_carrier','front_carrier':'root_carrier',
             'front_contact_pad':'front_contact_pad','rear_thigh':'thigh',
             'rear_shank':'shank','front_upper_arm':'upper_arm','front_forearm':'forearm'}.get(tag,tag)
        if tag.startswith('tray_spacer_'):tag='tray_spacer'
        spec=specs.get(tag,{})
        extra={}
        if name in cores:
            partner,core,collision,case_frame=cores[name]
            extra={'contactFrame':case_frame,'contactBoxes':S.case_boxes(),
                   'contactPartner':partner,'contactCore':_item(name,_mesh(core,tmp,2000+i),colour),
                   'collisionMesh':_item(name,_mesh(collision,tmp,3000+i),colour)}
        items.append(_item(name, _mesh(solid, tmp, i), colour,
                           printable=spec.get('printable') if not (ghost or bought) else None,
                           material=spec.get('material'),notes=spec.get('notes',''),**extra,
                           ghost=ghost,
                           side=side, joint=group,
                           kind="reference" if ghost
                           else "bought" if bought else "printed"))
    return items


def _part_items(tmp: pathlib.Path) -> list[dict]:
    """Every printed part in its declared print orientation, laid out in rows.

    This is a size and shape comparison, not a plate: the 200 mm bed square is
    drawn alongside purely as a scale reference (DEC-09)."""
    specs = []
    for i, builder in enumerate(all_builders()):
        spec = builder()
        mesh = _mesh(spec["orientation"] * spec["part"], tmp, 1000 + i)
        mesh.apply_translation(-mesh.bounds[0])          # sit on the bed
        specs.append((spec, mesh))

    items, x, y, row_h = [], PART_GAP, PART_GAP, 0.0
    for n, (spec, mesh) in enumerate(specs):
        w, d = mesh.extents[0], mesh.extents[1]
        if x + w > LAYOUT_W and x > PART_GAP:
            x, y, row_h = PART_GAP, y + row_h + PART_GAP, 0.0
        mesh.apply_translation([x, y, 0])
        kind = "coupon" if spec["name"].startswith("coupon") else "printed"
        items.append(_item(spec["name"], mesh, PART_COLOURS[n % len(PART_COLOURS)],
                           ghost=False, kind=kind,
                           notes=spec.get("notes", ""),
                           printable=spec.get("printable","unknown"), material=spec.get("material","PETG"),
                           print_metrics=metrics(mesh),
                           qty=spec.get("qty", 1) * (2 if spec.get("handed") else 1)))
        x += w + PART_GAP
        row_h = max(row_h, d)
    return items


def build() -> pathlib.Path:
    OUT.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        tmp = pathlib.Path(td)
        poses={name:_assembly_items(tmp,name) for name in body_plan.poses()}
        scene={"poses":poses,
               "parts":_part_items(tmp),"meta":{
                   "ground_z":0,"grid":GRID_STEP,"bed":[P.BED_X,P.BED_Y],
                   "track":P.BODY_TRACK_TARGET_MM,"stance":P.BODY_STANDING_HEIGHT_MM,
                   "hip_axes":2*__import__('koala_hardware.parts.links',fromlist=['rear_axis_y']).rear_axis_y(),
                   "joints":{name:assembly.joint_data(name) for name in poses},
                   "status":"DEC-49/50: common flat-back carriers, unequal drive/idler socket slots; head placement undecided and omitted. Printable: assumed; physical prints, fit and loads unproven. Slider ranges are sampled CAD clearances, not calibrated servo limits."}}
    data = OUT / "scene.json"
    data.write_text(json.dumps(scene))
    shutil.copy(HTML, OUT / "index.html")
    shutil.copy(HTML.with_name('mechanical_limits.js'),OUT/'mechanical_limits.js')
    for source in (ROOT/'vendor/viewer').iterdir():
        if source.is_file():shutil.copy(source,OUT/source.name)
    # Drawings come from the same body master as the structural assembly.
    for pose in body_plan.poses():
        source=ROOT.parent/'docs/design'/f'body-{pose}.svg'
        if source.exists():shutil.copy(source,OUT/source.name)
    write_backdrops(OUT)
    subprocess.run(["node",str(HTML.with_name("build_mechanical_limits.cjs")),str(OUT)],check=True)
    tris = sum(i['tris'] for items in [*scene['poses'].values(),scene['parts']] for i in items)
    print(f"wrote {data.relative_to(ROOT)}  "
          f"{len(poses['quadruped'])} assembly per pose + {len(scene['parts'])} parts, "
          f"{tris:,} triangles, {data.stat().st_size / 1e6:.1f} MB")
    return data


def write_backdrops(out):
    """Plain, metrically aligned side skeleton; no labels stretched into 3D."""
    for name in ('layout-150.svg','layout-200.svg'):
        (out/name).unlink(missing_ok=True)
    variants=[]
    for name,pose in body_plan.poses().items():
        bounds=(-305,-270,430,300) if name=='quadruped' else (-175,-475,285,505)
        bits=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{2*bounds[2]}" height="{2*bounds[3]}" viewBox="{" ".join(map(str,bounds))}">']
        for key in ('rear','front'):
            l=pose[key]
            points=' '.join(f'{-p.x},{-p.z}' for p in (l.root,l.bend,l.axle))
            bits.append(f'<polyline points="{points}" fill="none" stroke="#73aea4" stroke-width="2" stroke-dasharray="4 3"/>')
            radius=P.WHEEL_DIA/2 if key=='rear' else P.BODY_FRONT_FOOT_RADIUS_MM
            bits.append(f'<circle cx="{-l.axle.x}" cy="{-l.axle.z}" r="{radius}" fill="none" stroke="#73aea4"/>')
        h,s=pose['rear'].root,pose['front'].root
        bits.append(f'<path d="M{-h.x},{-h.z} L{-s.x},{-s.z}" stroke="#73aea4" stroke-width="3"/>')
        bits.append('</svg>')
        file=f'backdrop-{name}.svg';(out/file).write_text(''.join(bits))
        variants.append({'pose':name,'file':file,'bounds':bounds})
    (out/'layout-reference.json').write_text(json.dumps({'variants':variants}))


def serve(port: int, open_browser: bool) -> None:
    handler = lambda *a, **k: http.server.SimpleHTTPRequestHandler(
        *a, directory=str(OUT), **k)
    url = f"http://localhost:{port}/"
    with http.server.ThreadingHTTPServer(("127.0.0.1", port), handler) as httpd:
        print(f"serving {url}  (ctrl-c to stop)")
        if open_browser:
            webbrowser.open(url)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nstopped")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--build", action="store_true",
                    help="regenerate scene.json and exit, do not serve")
    ap.add_argument("--serve", action="store_true",
                    help="serve the existing scene.json without rebuilding")
    ap.add_argument("--port", type=int, default=8017)
    ap.add_argument("--no-open", action="store_true")
    args = ap.parse_args()

    if not args.serve:
        build()
    if not args.build:
        serve(args.port, not args.no_open)


if __name__ == "__main__":
    main()
