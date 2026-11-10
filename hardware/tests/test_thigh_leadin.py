# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Thick thigh lead-ins must not recreate the rejected thin-neck prototype."""
import unittest
import FreeCAD as App
import Part as FC
from koala_hardware.parts import links as L
from koala_hardware import params as P


class ThighLeadInTests(unittest.TestCase):
    def test_both_necks_keep_a_broad_web_beyond_the_holes(self):
        part=L.rear_thigh_rounded(P.BODY_THIGH_MM)
        # Centre and +/-4 mm rays screen an 8 mm wide structural strip.
        # The earlier removal-only prototype fell below 3 mm here.
        for x in (-4,0,4):
            for tick in range(85):
                z=10.51+tick*.25
                ray=FC.makeLine(App.Vector(x,-50,z),App.Vector(x,50,z))
                segments=part.fc.common(ray).Edges
                self.assertEqual(len(segments),2,(x,z))
                self.assertGreaterEqual(min(e.Length for e in segments),5.5,(x,z))

    def test_leadins_extend_across_the_lower_screw_row(self):
        part=L.rear_thigh_rounded(P.BODY_THIGH_MM)
        # Between the two lower screws: stock now covers the old outer face.
        z=P.SERVO_DRIVE_SQ/2
        for y in (-P.SOCKET_DRIVE_FACE-P.SOCKET_PAD_T-.5,
                  -P.SOCKET_IDLER_FACE+P.SOCKET_PAD_T+.5):
            self.assertTrue(part.fc.isInside(App.Vector(0,y,z),1e-6,True))


if __name__=='__main__':unittest.main()
