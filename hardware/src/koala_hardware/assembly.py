# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Assembly sanity render: lower body (pelvis + hips + thighs + wheels +
tray + servo envelopes) posed at neutral. Eyeball check for proportion and
collision - not an export artefact.

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
from .parts import pelvis, hip_link, thigh, e_tray

ROOT = pathlib.Path(__file__).resolve().parents[2]

ROLL_AXIS_Z = -pelvis.ROLL_DROP
PITCH_AXIS_Z = ROLL_AXIS_Z - hip_link.PITCH_DROP
WHEEL_AXIS_Z = PITCH_AXIS_Z - P.THIGH_DROP


def build_scene():
    items = []  # (solid, colour)
    items.append((pelvis.build()["part"], "#8fb4d9"))
    items.append((Pos(0, 0, pelvis.BOSS_H) * e_tray.build()["part"], "#b4d98f"))

    hl = hip_link.build()["part"]
    th = thigh.build()["part"]
    wheel = Rot(X=90) * Cylinder(P.WHEEL_DIA / 2, P.WHEEL_W,
                                 align=(Align.CENTER, Align.CENTER, Align.CENTER))
    for side in (1, -1):
        hl_s = hl if side == 1 else mirror(hl, Plane.XZ)
        th_s = th if side == 1 else mirror(th, Plane.XZ)
        items.append((Pos(0, side * pelvis.ROLL_Y, ROLL_AXIS_Z) * hl_s, "#d9a48f"))
        items.append((Pos(0, side * pelvis.ROLL_Y, WHEEL_AXIS_Z) * th_s, "#c98fd9"))
        items.append((Pos(0, side * P.TRACK_HALF, WHEEL_AXIS_Z) * wheel, "#555555"))
        # servo envelopes (keep-out ghosts)
        items.append((pelvis.servo_tf(side) * S.servo_envelope(0), "#e8d44d"))
        items.append((Pos(0, side * pelvis.ROLL_Y, PITCH_AXIS_Z) *
                      Rot(X=-90 * side) * Rot(Z=-90) * S.servo_envelope(0), "#e8d44d"))
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
    fig.suptitle(f"koala-bot lower body v0 - wheel axis at {WHEEL_AXIS_Z:.0f} mm, "
                 f"ground at {WHEEL_AXIS_Z - P.WHEEL_DIA / 2:.0f} mm below pelvis top")
    fig.tight_layout()
    out = ROOT / "build" / "renders" / "assembly.png"
    fig.savefig(out, dpi=100)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
