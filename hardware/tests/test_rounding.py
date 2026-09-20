# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Rounding must accumulate on the current solid, including after group failure."""
from math import pi
import unittest
from unittest.mock import patch

from build123d import Box, Part, Solid
from koala_hardware import params as P
from koala_hardware.parts import links as L


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

    def test_production_thigh_keeps_every_successful_rounding_group(self):
        # Warm up the structural root fillets: record only the outer rounding pass.
        base=L.rear_thigh_flat(P.BODY_THIGH_MM)
        original_fillet=Part.fillet
        successes=[]

        def record(part,radius,edges):
            result=original_fillet(part,radius,edges)
            # Convex rounding must not restore material removed in an earlier group.
            self.assertLess((result-part).volume,.01)
            successes.append(result)
            return result

        with patch.object(Part,'fillet',record),patch.object(Solid,'fillet',record):
            rounded=L.rear_thigh_rounded.__wrapped__(P.BODY_THIGH_MM)
        self.assertGreater(len(successes),2,'exercise the production split-group fallback')
        for intermediate in successes:
            self.assertLess((rounded-intermediate).volume,.01)
        self.assertLess(rounded.volume,base.volume)
        self.assertTrue(rounded.is_valid)
        self.assertEqual(len(rounded.solids()),1)


if __name__=='__main__':unittest.main()
