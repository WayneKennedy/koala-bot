# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Joint semantics must survive a change in torso attitude (DEC-41)."""
import unittest
from math import radians, sin
from build123d import Pos, Vector
from koala_hardware import assembly as A, body_plan as B, params as P


class JointAxisTests(unittest.TestCase):
    def test_roll_abducts_the_thigh_in_both_body_poses(self):
        for pose, body in B.poses().items():
            for key, joint in A.joint_data(pose).items():
                with self.subTest(pose=pose, limb=key):
                    limb=body[key]
                    axis=Vector(joint['roll_axis'])
                    thigh=Vector(limb.bend.x-limb.root.x,0,limb.bend.z-limb.root.z)
                    self.assertAlmostEqual(axis.length,1)
                    self.assertAlmostEqual(axis.dot(thigh),0)
                    self.assertAlmostEqual(axis.Y,0)
                    # Saved poses must retain a primarily fore/aft axis, not yaw.
                    self.assertGreater(axis.X,.7)
                    moved=(A.pivot(joint['roll'],axis,5)*Pos(*joint['bend'])).position
                    self.assertAlmostEqual(moved.Y-joint['bend'][1],limb.upper*sin(radians(5)))

    def test_physical_servo_axes_match_the_kinematics(self):
        for pose in B.poses():
            joints=A.joint_data(pose)
            for reference,owner,frame in A.socket_frames(pose):
                key=reference.split('_')[1];joint=joints[key]
                origin=(frame*Pos(0,0,P.SOCKET_AXIS_Z)).position
                output=(frame*Pos(1,0,P.SOCKET_AXIS_Z)).position-origin
                if '_roll_' in reference:
                    self.assertIn('carrier',owner)
                    self.assertAlmostEqual(abs(output.dot(Vector(joint['roll_axis']))),1)
                    self.assertLess((origin-Vector(joint['roll'])).length,1e-8)
                elif '_pitch_' in reference:
                    self.assertIn(owner,('pelvis_socket_right','shoulder_socket_right'))
                    self.assertAlmostEqual(abs(output.Y),1)
                    self.assertLess((origin-Vector(joint['pitch'])).length,1e-8)

    def test_pitch_is_parent_of_roll(self):
        # A pure roll command must leave its case/carrier fixed. Pitch must
        # carry that case and the upper link together. This checks actual CAD.
        for pose in B.poses():
            nominal={n:s for n,s,*_ in A.scene_details(pose=pose)}
            rolled={n:s for n,s,*_ in A.scene_details(roll=5,pose=pose)}
            pitched={n:s for n,s,*_ in A.scene_details(pitch=5,pose=pose)}
            for key in ('rear','front'):
                for side in ('right','left'):
                    n=f'{key}_carrier_{side}'
                    self.assertLess((nominal[n].center()-rolled[n].center()).length,1e-7)
                    self.assertGreater((nominal[n].center()-pitched[n].center()).length,.1)
                    n=f'reference_{key}_pitch_servo_{side}'
                    self.assertLess((nominal[n].center()-pitched[n].center()).length,1e-7)

    def test_socket_contact_allowance_follows_a_perturbed_pose(self):
        from koala_hardware.audit import fit_pairs,volume
        q=(-5,5,5)
        shapes={n:s for n,s,*_ in A.scene_details(*q,pose='upright',asymmetric=True)}
        for pair,zone in fit_pairs('upright',q,asymmetric=True).items():
            a,b=pair;hit=shapes[a]&shapes[b]
            self.assertLessEqual(volume(hit),50)
            self.assertLess(volume(hit-zone),.01)


if __name__=='__main__':unittest.main()
