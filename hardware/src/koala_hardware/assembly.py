# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Lower-body geometry. Angles are CAD inspection poses, not control limits."""
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
ROLL_Z = -P.HIP_ROLL_DROP
PITCH_Z = ROLL_Z - P.HIP_PITCH_DROP
WHEEL_Z = PITCH_Z - P.THIGH_DROP
GROUND_Z = WHEEL_Z - P.WHEEL_DIA / 2


def leg_parts():
    """One right leg in roll-local frame, with kinematic group labels."""
    pitch = Pos(P.HIP_PITCH_X, 0, -P.HIP_PITCH_DROP)
    knee = pitch * Pos(0, 0, -P.THIGH_DROP)
    items = []
    for b in (hip_link.build_drive, hip_link.build_idler,
              hip_link.build_saddle, hip_link.build_cap):
        s = b()
        items.append((s["name"], s["part"], "#d9a48f", "roll"))
    for b in (thigh.build_outer, thigh.build_inner):
        s = b()
        items.append((s["name"], pitch * s["part"], "#c98fd9", "pitch"))
    for i, spacer in enumerate(thigh.placed_spacers()):
        items.append((f"thigh_spacer_{i+1}", pitch * spacer, "#8fd9c9", "pitch"))
    def cyl(r, h):
        return Cylinder(r, h, align=(Align.CENTER, Align.CENTER, Align.MIN))
    face = thigh.MOTOR_FACE_Y
    items += [
        ("motor", knee * Pos(0, face, 0) * Rot(X=90) *
         cyl(P.MOTOR_DIA / 2, P.MOTOR_BODY_LEN), "#777777", "pitch"),
        ("shaft", knee * Pos(0, face, 0) * Rot(X=-90) *
         cyl(P.MOTOR_SHAFT_DIA / 2, P.MOTOR_SHAFT_LEN), "#aaaaaa", "pitch"),
        ("hub", knee * Pos(0, face + P.HUB_STACK - P.HUB_T, 0) * Rot(X=-90) *
         cyl(P.HUB_DIA / 2, P.HUB_T), "#bbbbbb", "pitch"),
        ("wheel", knee * Pos(0, face + P.HUB_STACK, 0) * Rot(X=-90) *
         cyl(P.WHEEL_DIA / 2, P.WHEEL_W), "#555555", "pitch"),
        ("reference_roll_servo", S.on_axis(Rot(Y=90)) * S.servo_reference(),
         "#e8d44d", "fixed"),
        ("reference_pitch_servo", pitch * Pos(0, P.HIP_PITCH_Y, 0) *
         S.on_axis(Rot(X=-90)) * S.servo_reference(), "#e8d44d", "roll"),
    ]
    return items


def build_scene(roll=0.0, pitch=0.0):
    """Symmetric local roll (positive = splay), common fore/aft pitch."""
    items = [("pelvis", pelvis.build()["part"], "#8fb4d9"),
             ("e_tray", Pos(0, 0, P.TRAY_GAP) * e_tray.build()["part"], "#b4d98f")]
    local = leg_parts()
    pitch_tf = (Pos(P.HIP_PITCH_X, 0, -P.HIP_PITCH_DROP) * Rot(Y=pitch) *
                Pos(-P.HIP_PITCH_X, 0, P.HIP_PITCH_DROP))
    for side in (1, -1):
        for name, solid, colour, group in local:
            if group == "pitch":
                solid = pitch_tf * solid
            if group != "fixed":
                solid = Rot(X=roll) * solid
            if side == -1:
                solid = mirror(solid, Plane.XZ)
            items.append((name + ("_right" if side == 1 else "_left"),
                          Pos(0, side * P.HIP_ROLL_Y, ROLL_Z) * solid, colour))
    return items


def main():
    tmp = ROOT / "build" / "_asm"
    tmp.mkdir(parents=True, exist_ok=True)
    meshes = []
    for i, (_name, solid, colour) in enumerate(build_scene()):
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
