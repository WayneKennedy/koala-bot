# SPDX-License-Identifier: CERN-OHL-S-2.0
"""The exported STL must retain the topology checked by the mesh validator."""
import tempfile
import unittest
from pathlib import Path

import numpy as np
import trimesh
from koala_hardware.meshing import export_mesh
from koala_hardware.parts.front import build_forearm


class MeshExportTests(unittest.TestCase):
    def test_forearm_roundoff_is_normalized_in_the_written_stl(self):
        spec=build_forearm()
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/'forearm.stl'
            checked=export_mesh(spec['orientation']*spec['part'],path)
            raw=trimesh.load(path,force='mesh',process=False)
            # Exact coordinate welding, with no rounded coordinate tolerance:
            # this is what exposed the inconsistent OCC planar vertices.
            vertices,inverse=np.unique(raw.vertices,axis=0,return_inverse=True)
            exact=trimesh.Trimesh(vertices=vertices,faces=inverse[raw.faces],process=False)
            self.assertTrue(exact.is_watertight)
            self.assertGreater(exact.volume,0)
            self.assertAlmostEqual(exact.volume,checked.volume,places=6)


if __name__=='__main__':unittest.main()
