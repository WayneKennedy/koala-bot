# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Analytical limits and force-moment checks for the knee redesign study."""
import unittest
from math import sqrt

from koala_hardware import leg_sizing as S, params as P


class LegSizingTests(unittest.TestCase):
    def test_straight_and_right_angle_chain(self):
        p = S.forward(0, 0, thigh=100, shank=80)
        self.assertAlmostEqual(p.axle_x, 0)
        self.assertAlmostEqual(p.axle_z, -180)
        p = S.forward(90, 90, thigh=100, shank=80)
        self.assertAlmostEqual(p.knee_x, 100)
        self.assertAlmostEqual(p.knee_z, 0)
        self.assertAlmostEqual(p.axle_x, 100)
        self.assertAlmostEqual(p.axle_z, -80)

    def test_centered_crouch_keeps_axle_under_hip(self):
        p = S.forward(45, 90, thigh=100, shank=100)
        self.assertAlmostEqual(p.axle_x, 0)
        self.assertAlmostEqual(p.axle_z, -100 * sqrt(2))

    def test_force_moment_includes_wheel_radius(self):
        p = S.forward(0, 0, thigh=100, shank=100)
        self.assertAlmostEqual(S.knee_moment_nm(p, 20), 0)
        self.assertAlmostEqual(S.knee_moment_nm(p, 20, 10),
                               -(100 + P.WHEEL_DIA / 2) * 10 / 1000)
        p = S.forward(0, 90, thigh=100, shank=100)
        self.assertAlmostEqual(S.knee_moment_nm(p, 20), 2)
        self.assertAlmostEqual(S.knee_moment_nm(p, 40), 4)

    def test_neutral_motor_gap_independent_of_hip_datum(self):
        reach = P.MOTOR_BODY_LEN + P.HUB_STACK + P.WHEEL_W / 2
        for half in (40, 70):
            self.assertAlmostEqual(S.motor_gap_mm(240, half, 225, 0),
                                   240 - 2 * reach)

    def test_track_threshold_and_roll_penalty(self):
        track = S.minimum_track_mm(60, 225, 10, gap=2)
        self.assertAlmostEqual(S.motor_gap_mm(track, 60, 225, 10), 2)
        self.assertGreater(track, S.minimum_track_mm(60, 225, 5, gap=2))
        self.assertLess(S.motor_gap_mm(track - 1, 60, 225, 10), 2)

    def test_invalid_geometry(self):
        with self.assertRaises(ValueError):
            S.forward(0, 0, thigh=0)
        for angle in (-1, 90):
            with self.assertRaises(ValueError):
                S.minimum_track_mm(60, 225, angle)


if __name__ == "__main__":
    unittest.main()
