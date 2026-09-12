"""Physical consistency of the adopted conceptual dimensions."""
import unittest
from unittest.mock import patch
from koala_hardware import body_plan as B, params as P


class BodyPlanTests(unittest.TestCase):
    def test_drawing_shoulder_height_is_unreachable(self):
        with self.assertRaises(ValueError):
            B.solve(B.Point(0,240),B.Point(0,40),70,75,-1)

    def test_120_track_collides_with_bought_motors(self):
        with patch.object(P,'BODY_TRACK_TARGET_MM',120):
            a,b=B.motor_intervals()
            self.assertAlmostEqual(a[1]-b[0],64)
            with self.assertRaises(AssertionError): B.check()

    def test_adopted_poses_close(self):
        data=B.check()
        self.assertEqual(data['drive_motor_count'],2)
        self.assertAlmostEqual(data['motor_end_gap_mm'],36)
        q,u=data['poses']['quadruped'],data['poses']['upright']
        self.assertAlmostEqual(q['front'].axle.x-q['rear'].axle.x,260)
        self.assertEqual(q['rear'].axle.z,40)
        self.assertEqual(q['front'].axle.z,P.BODY_FRONT_FOOT_RADIUS_MM)
        self.assertEqual(q['front'].lower,100)
        self.assertAlmostEqual(u['rear'].root.z,190)
        self.assertAlmostEqual(u['front'].root.z,340)
        self.assertAlmostEqual(u['neck'].z+75,450)
        self.assertGreater(u['front'].axle.z-40,0)
        # Keep straight-leg singularities away from both nominated stances.
        for pose in (q,u):
            for key in ('front','rear'):
                self.assertGreater(pose[key].flexion,20)
                self.assertLess(pose[key].flexion,140)



if __name__=='__main__':unittest.main()
