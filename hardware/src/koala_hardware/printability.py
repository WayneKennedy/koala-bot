# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Support-free printability analysis (DEC-24).

A part is judged in its declared print orientation:
  bed_area      - area of faces lying on the build plate (adhesion / stability)
  overhang_area - area of down-facing faces steeper than the self-support
                  limit, excluding the bed itself (these need support)

Overhang convention: `angle` is measured from straight-down, so a horizontal
ceiling = 0 deg and a vertical wall = 90 deg. FDM self-supports above ~45 deg.
"""
import numpy as np
import trimesh

SELF_SUPPORT_DEG = 45.0
BED_TOL = 0.05          # mm - face counts as "on the bed"
MIN_BED_AREA = 300.0    # mm^2 - below this the part stands on pinpoints
MAX_OVERHANG_AREA = 800.0  # mm^2 - above this it needs real support

# Candidate orientations: the six principal "up" directions. Rotation about Z
# never changes overhang, so it is not searched.
CANDIDATES = {
    "as-modelled": np.eye(4),
    "X+180": trimesh.transformations.rotation_matrix(np.pi, [1, 0, 0]),
    "X+90": trimesh.transformations.rotation_matrix(np.pi / 2, [1, 0, 0]),
    "X-90": trimesh.transformations.rotation_matrix(-np.pi / 2, [1, 0, 0]),
    "Y+90": trimesh.transformations.rotation_matrix(np.pi / 2, [0, 1, 0]),
    "Y-90": trimesh.transformations.rotation_matrix(-np.pi / 2, [0, 1, 0]),
}


def metrics(mesh: trimesh.Trimesh) -> dict:
    n = mesh.face_normals
    a = mesh.area_faces
    face_min_z = mesh.triangles[:, :, 2].min(axis=1)
    z_min = mesh.bounds[0][2]

    on_bed = (face_min_z <= z_min + BED_TOL) & (n[:, 2] < -0.9)
    limit = -np.cos(np.radians(SELF_SUPPORT_DEG))   # nz below this => overhang
    overhang = (n[:, 2] < limit) & ~on_bed

    size = mesh.bounds[1] - mesh.bounds[0]
    return {
        "bed_area": float(a[on_bed].sum()),
        "overhang_area": float(a[overhang].sum()),
        "size": tuple(float(v) for v in size),
        "height": float(size[2]),
    }


def check(mesh: trimesh.Trimesh) -> tuple[bool, str, dict]:
    """Returns (ok, one-line verdict, metrics) for the mesh as oriented."""
    m = metrics(mesh)
    problems = []
    if m["bed_area"] < MIN_BED_AREA:
        problems.append(f"bed contact only {m['bed_area']:.0f} mm2")
    if m["overhang_area"] > MAX_OVERHANG_AREA:
        problems.append(f"overhang {m['overhang_area']:.0f} mm2")
    verdict = "; ".join(problems) if problems else "support-free"
    return (not problems), verdict, m


def best_orientations(mesh: trimesh.Trimesh, top: int = 3) -> list[tuple]:
    """Rank the principal orientations: least overhang, then most bed area."""
    scored = []
    for name, T in CANDIDATES.items():
        m = metrics(mesh.copy().apply_transform(T))
        scored.append((name, m["overhang_area"], m["bed_area"]))
    scored.sort(key=lambda r: (round(r[1]), -r[2]))
    return scored[:top]
