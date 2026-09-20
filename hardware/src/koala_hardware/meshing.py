# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Tessellate BREP solids without collapsed pole triangles."""
import numpy as np
import trimesh
from build123d import export_stl


def export_mesh(solid,path,**kwargs):
    export_stl(solid,str(path),**kwargs)
    raw=trimesh.load(path,force='mesh',process=False)
    mesh=trimesh.load(path,force='mesh')
    # OCC may give coincident planar vertices coordinates differing only by
    # roundoff (e.g. Z=1.95e-14 versus 2.13e-14). Trimesh's ordinary vertex
    # merge already handles these during validation. Persist that same mesh
    # when it merged non-identical coordinates, so slicers receive the closed
    # topology we checked instead of having to repair numerical cracks.
    merged_roundoff=len(np.unique(raw.vertices,axis=0))!=len(mesh.vertices)
    # OCC can emit a zero-area triangle at a sphere pole. After coincident
    # vertices merge it repeats an index. Remove only these collapsed faces;
    # never fill holes, join separate shells or hide failed watertightness.
    keep=np.all(np.diff(np.sort(mesh.faces,axis=1),axis=1)!=0,axis=1)
    if not np.all(keep):
        mesh.update_faces(keep)
        mesh.remove_unreferenced_vertices()
    if not mesh.is_watertight or mesh.volume<=0:
        raise ValueError(f'{path}: STL is not a closed positive-volume mesh')
    if merged_roundoff or not np.all(keep):
        mesh.export(str(path),file_type='stl')
    return mesh
