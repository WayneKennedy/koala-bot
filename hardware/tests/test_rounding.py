# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Rounding must accumulate on the current solid, including after group failure."""
from math import pi
import warnings
import unittest
from unittest.mock import patch

from koala_hardware.cad import Box, Part, Solid
from koala_hardware import params as P, servo_iface as S
from koala_hardware.parts import links as L
from koala_hardware.meshing import closed_shape_mesh


class RoundingTests(unittest.TestCase):
    def test_rejected_group_keeps_both_successful_corner_rounds(self):
        original_fillet=Part.fillet
        successes=[]

        def split_group(part,radius,edges):
            if len(edges)>1:
                raise ValueError('exercise the individual-edge fallback')
            result=original_fillet(part,radius,edges)
            successes.append(result)
            return result

        block=Box(20,20,20)
        with patch.object(Part,'fillet',split_group),patch.object(Solid,'fillet',split_group):
            rounded=L.round_convex_edges(block,2,
                exclude=lambda c:abs(c.Z)>1e-5 or c.X*c.Y<0)
        # Two opposite vertical corners, each removing a square minus a quarter-circle.
        self.assertEqual(len(successes),2)
        self.assertAlmostEqual(rounded.volume,8000-2*20*4*(1-pi/4),places=5)
        self.assertTrue(rounded.is_valid)
        self.assertEqual(len(rounded.solids()),1)

    def test_unroundable_edges_are_reported(self):
        with self.assertWarnsRegex(RuntimeWarning,r'12 edge\(s\) left sharp at R25'):
            rounded=L.round_convex_edges(Box(20,20,20),25)
        self.assertAlmostEqual(rounded.volume,8000,places=5)

    def test_protected_corner_material_survives_rounding(self):
        block=Box(20,20,20)
        protect=S._box(8,11,8,11,-11,11)
        with warnings.catch_warnings():
            warnings.simplefilter('ignore',RuntimeWarning)
            rounded=L.round_convex_edges(block,4,protect=protect)
        self.assertLess(((block&protect)-rounded).volume,.001)
        self.assertLess(rounded.volume,block.volume-100)
        self.assertTrue(rounded.is_valid)

    def test_r3_outer_fork_rims_preserve_original_bearing_material(self):
        from koala_hardware.rounding import horn_material
        from koala_hardware.parts import front as F
        from koala_hardware.cad import GeomType
        original=L.fork('drive',family=False)+L.fork('idler',family=False)
        part=F.forearm()
        self.assertLess(((original&horn_material())-part).volume,.001)
        # The two circular outer nose rims have toroidal R3 rolling surfaces.
        rims=[f for f in part.fc.Faces if type(f.Surface).__name__=='Toroid'
              and abs(f.Surface.MinorRadius-3)<1e-6]
        self.assertGreaterEqual(len(rims),2)

    def test_r3_thigh_native_history_matches_geometry_used_by_checks(self):
        import FreeCAD as App
        from koala_hardware.freecad_document import make_document
        part=L.upper_link(P.BODY_THIGH_MM,True)
        doc,final=make_document('R3ThighRegression',part)
        try:
            self.assertAlmostEqual(final.Shape.Volume,part.volume,delta=.01)
            self.assertTrue(any(o.TypeId=='Part::Fillet' and any(abs(e[1]-3)<1e-8 for e in o.Edges)
                                for o in doc.Objects))
        finally:App.closeDocument(doc.Name)


if __name__=='__main__':unittest.main()
