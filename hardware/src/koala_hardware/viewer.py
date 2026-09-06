# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Local 3D viewer for the lower-body assembly and the printed parts.

    uv run python -m koala_hardware.viewer            # build, serve, open
    uv run python -m koala_hardware.viewer --build    # regenerate data only
    uv run python -m koala_hardware.viewer --port N   # default 8017

Writes build/viewer/scene.json next to the checked-in viewer.html, so any
harness can refresh the geometry and just reload the browser tab. The viewer
is an eyeball check on proportion and packaging; the build-time gates in
printability.py and validation.py are what actually pass or fail a part.
"""
import argparse
import base64
import http.server
import json
import pathlib
import shutil
import tempfile
import webbrowser

import numpy as np
import trimesh
from build123d import export_stl

from . import assembly
from . import params as P
from .parts import all_builders

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
    export_stl(solid, str(path))
    return trimesh.load(path, force="mesh")


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


def _assembly_items(tmp: pathlib.Path) -> list[dict]:
    items = []
    for i, (name, solid, colour) in enumerate(assembly.build_scene()):
        ghost = name.startswith("keepout")
        bought = name.split("_right")[0].split("_left")[0] in (
            "motor", "shaft", "hub", "wheel")
        items.append(_item(name, _mesh(solid, tmp, i), colour,
                           ghost=ghost,
                           kind="keep-out" if ghost
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
                           qty=spec.get("qty", 2 if spec.get("handed") else 1)))
        x += w + PART_GAP
        row_h = max(row_h, d)
    return items


def build() -> pathlib.Path:
    OUT.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        tmp = pathlib.Path(td)
        scene = {
            "assembly": _assembly_items(tmp),
            "parts": _part_items(tmp),
            "meta": {
                "ground_z": assembly.GROUND_Z,
                "wheel_z": assembly.WHEEL_Z,
                "roll_z": assembly.ROLL_Z,
                "pitch_z": assembly.PITCH_Z,
                "grid": GRID_STEP,
                "bed": [P.BED_X, P.BED_Y],
                "track": 2 * P.TRACK_HALF,
                "stance": -assembly.GROUND_Z,
                "hip_axes": P.HIP_PITCH_DROP,
            },
        }
    data = OUT / "scene.json"
    data.write_text(json.dumps(scene))
    shutil.copy(HTML, OUT / "index.html")
    tris = sum(i["tris"] for g in ("assembly", "parts") for i in scene[g])
    print(f"wrote {data.relative_to(ROOT)}  "
          f"{len(scene['assembly'])} assembly + {len(scene['parts'])} parts, "
          f"{tris:,} triangles, {data.stat().st_size / 1e6:.1f} MB")
    return data


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
