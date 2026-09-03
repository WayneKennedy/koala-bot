# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Assembly sanity render: lower body posed at neutral, with servo keep-out
ghosts. Eyeball check for proportion and collision - not an export artefact.

Usage: uv run python -m koala_hardware.assembly  -> build/renders/assembly.png
"""
import pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import trimesh
from build123d import Pos, Rot, Cylinder, Align, mirror, Plane, export_stl
from . import params as P
from . import servo_iface as S
from .parts import pelvis, hip_bracket, hip_link, thigh, e_tray

ROOT = pathlib.Path(__file__).resolve().parents[2]

ROLL_Z = -P.HIP_ROLL_DROP
PITCH_Z = ROLL_Z - P.HIP_PITCH_DROP
WHEEL_Z = PITCH_Z - P.THIGH_DROP
GROUND_Z = WHEEL_Z - P.WHEEL_DIA / 2


def build_scene():
    items = [(pelvis.build()["part"], "#8fb4d9"),
             (Pos(0, 0, P.TRAY_GAP) * e_tray.build()["part"], "#b4d98f")]

    br = hip_bracket.build()["part"]
    hl = hip_link.build()["part"]
    tu = thigh.build_upper()["part"]
    mc = thigh.build_clamp()["part"]
    wheel = Rot(X=90) * Cylinder(P.WHEEL_DIA / 2, P.WHEEL_W,
                                 align=(Align.CENTER, Align.CENTER, Align.CENTER))

    for side in (1, -1):
        def s(solid):
            return solid if side == 1 else mirror(solid, Plane.XZ)

        y = side * P.HIP_ROLL_Y
        items += [
            (Pos(0, y, ROLL_Z) * s(br), "#d9d08f"),
            (Pos(0, y, ROLL_Z) * s(hl), "#d9a48f"),
            (Pos(0, y, PITCH_Z) * s(tu), "#c98fd9"),
            (Pos(0, y, WHEEL_Z) * s(mc), "#8fd9c9"),
            (Pos(0, side * P.TRACK_HALF, WHEEL_Z) * wheel, "#555555"),
            # servo keep-out ghosts. The pitch servo lies AFT and OUTBOARD
            # (params: sliding along its own axis is free), not stacked under
            # the roll joint - that is what collapses the hip to 26 mm.
            (Pos(0, y, ROLL_Z) * s(S.on_axis(Rot(Y=90)) * S.servo_envelope(0)),
             "#e8d44d"),
            (Pos(0, y, ROLL_Z) * s(Pos(0, P.HIP_PITCH_Y, -P.HIP_PITCH_DROP)
             * S.on_axis(Rot(X=-90)) * S.servo_envelope(0)), "#e8d44d"),
        ]
    return items


def main():
    tmp = ROOT / "build" / "_asm"
    tmp.mkdir(parents=True, exist_ok=True)
    meshes = []
    for i, (solid, colour) in enumerate(build_scene()):
        p = tmp / f"{i}.stl"
        export_stl(solid, str(p))
        meshes.append((trimesh.load(p), colour))

    fig = plt.figure(figsize=(14, 6))
    views = [(20, -55, "iso"), (0, -90, "side profile"), (0, 0, "front")]
    bounds = np.array([m.bounds for m, _ in meshes])
    lo, hi = bounds[:, 0].min(axis=0), bounds[:, 1].max(axis=0)
    c, r = (lo + hi) / 2, max(hi - lo) / 2 * 1.05
    for i, (elev, azim, label) in enumerate(views, 1):
        ax = fig.add_subplot(1, 3, i, projection="3d")
        for m, colour in meshes:
            ax.add_collection3d(Poly3DCollection(
                m.vertices[m.faces], alpha=0.95, facecolor=colour,
                edgecolor="#333333", linewidth=0.1))
        ax.set_xlim(c[0] - r, c[0] + r)
        ax.set_ylim(c[1] - r, c[1] + r)
        ax.set_zlim(c[2] - r, c[2] + r)
        ax.view_init(elev=elev, azim=azim)
        ax.set_title(label, fontsize=10)
        ax.set_axis_off()
    fig.suptitle(f"koala-bot lower body v1 - wheel axis {WHEEL_Z:.0f} mm, "
                 f"ground {GROUND_Z:.0f} mm below the pelvis deck")
    fig.tight_layout()
    out = ROOT / "build" / "renders" / "assembly.png"
    fig.savefig(out, dpi=100)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
