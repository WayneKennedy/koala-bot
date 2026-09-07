# SPDX-License-Identifier: CERN-OHL-S-2.0
import unittest
import trimesh
from koala_hardware.printability import metrics


class BedContactTests(unittest.TestCase):
    def test_one_vertex_on_bed_is_not_a_bed_face(self):
        mesh = trimesh.Trimesh(vertices=[[0, 0, 0], [0, 10, 1], [10, 0, 1]],
                               faces=[[0, 1, 2]], process=False)
        result = metrics(mesh)
        self.assertEqual(result["bed_area"], 0)
        self.assertGreater(result["overhang_area"], 50)

    def test_flat_bottom_is_bed_contact(self):
        result = metrics(trimesh.creation.box(extents=[10, 20, 5]))
        self.assertAlmostEqual(result["bed_area"], 200)
        self.assertEqual(result["overhang_area"], 0)


if __name__ == "__main__":
    unittest.main()
