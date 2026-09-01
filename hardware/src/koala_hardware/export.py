# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Build everything: STL + 4-view PNG render per part + DEC-23 fit check.

Usage:  uv run python -m koala_hardware.export [name-filter]
Outputs: build/stl/*.stl, build/renders/*.png, build/manifest.txt
The build FAILS (exit 1) if any part exceeds the print bed in its declared
print orientation (DEC-09 / DEC-23).
"""
import sys
import pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import trimesh
from build123d import export_stl
from . import params as P
from . import printability as PR
from .parts import all_builders

ROOT = pathlib.Path(__file__).resolve().parents[2]
STL = ROOT / "build" / "stl"
REN = ROOT / "build" / "renders"


def render(mesh: trimesh.Trimesh, path: pathlib.Path, title: str):
    fig = plt.figure(figsize=(10, 8))
    views = [(30, -60, "iso"), (0, -90, "side"), (0, 0, "front"), (90, -90, "top")]
    for i, (elev, azim, label) in enumerate(views, 1):
        ax = fig.add_subplot(2, 2, i, projection="3d")
        tris = mesh.vertices[mesh.faces]
        pc = Poly3DCollection(tris, alpha=1.0, facecolor="#8fb4d9",
                              edgecolor="#2a4a6a", linewidth=0.15)
        ax.add_collection3d(pc)
        lo, hi = mesh.bounds
        c, r = (lo + hi) / 2, max(hi - lo) / 2 * 1.1
        ax.set_xlim(c[0] - r, c[0] + r)
        ax.set_ylim(c[1] - r, c[1] + r)
        ax.set_zlim(c[2] - r, c[2] + r)
        ax.set_title(label, fontsize=9)
        ax.view_init(elev=elev, azim=azim)
        ax.set_axis_off()
    fig.suptitle(title)
    fig.tight_layout()
    fig.savefig(path, dpi=90)
    plt.close(fig)


def prune(current: set[str]) -> list[str]:
    """Delete outputs for parts that no longer exist under that name.

    A renamed part otherwise leaves its old STL sitting beside the new one,
    and a stale file slices just as happily as a current one.
    """
    keep = current | {"assembly"}
    removed = []
    for folder, ext in ((STL, ".stl"), (REN, ".png")):
        for f in folder.glob(f"*{ext}"):
            if f.stem not in keep:
                f.unlink()
                removed.append(f.name)
    return removed


def main():
    name_filter = sys.argv[1] if len(sys.argv) > 1 else ""
    STL.mkdir(parents=True, exist_ok=True)
    REN.mkdir(parents=True, exist_ok=True)
    failures, lines = [], []

    built = []
    for builder in all_builders():
        spec = builder()
        built.append(spec["name"])
        if name_filter and name_filter not in spec["name"]:
            continue
        name, part = spec["name"], spec["part"]
        oriented = spec["orientation"] * part
        bb = oriented.bounding_box()
        size = (bb.size.X, bb.size.Y, bb.size.Z)
        fits = size[0] <= P.BED_X and size[1] <= P.BED_Y and size[2] <= P.BED_Z
        stl_path = STL / f"{name}.stl"
        export_stl(oriented, str(stl_path))
        mesh = trimesh.load(stl_path)
        render(mesh, REN / f"{name}.png", name)
        printable, verdict, m = PR.check(mesh)
        ok = fits and printable
        status = "OK  " if ok else "FAIL"
        line = (f"[{status}] {name:22s} {size[0]:6.1f} x {size[1]:6.1f} x "
                f"{size[2]:6.1f} mm  {mesh.volume / 1000:6.1f} cm3  "
                f"bed {m['bed_area']:7.0f}  overhang {m['overhang_area']:7.0f}"
                f"  {'' if fits else 'EXCEEDS BED; '}{verdict}")
        print(line)
        if not printable:
            alts = ", ".join(f"{n}(oh {o:.0f}, bed {b:.0f})"
                             for n, o, b in PR.best_orientations(mesh))
            print(f"         better orientations: {alts}")
            line += f"\n    better orientations: {alts}"
        lines.append(line + "\n    " + spec["notes"])
        if not ok:
            failures.append(name)

    orphans = prune(set(built))
    if orphans:
        print(f"\npruned stale output for renamed/removed parts: "
              f"{', '.join(sorted(orphans))}")

    (ROOT / "build" / "manifest.txt").write_text("\n".join(lines) + "\n")
    if failures:
        print(f"\nFAILURES (DEC-09 bed fit / DEC-24 support-free): {failures}")
        sys.exit(1)


if __name__ == "__main__":
    main()
