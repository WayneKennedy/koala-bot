# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Actual axes and parent order for rear hips and roll-first shoulders."""
import unittest
from math import radians, sin
from build123d import Pos, Vector
from koala_hardware import assembly as A, body_plan as B, params as P


class JointAxisTests(unittest.TestCase):
    def test_roll_abducts_the_thigh_in_both_body_poses(self):
        for pose, body in B.poses().items():
            joint=A.joint_data(pose)['rear'];limb=body['rear']
            axis=Vector(joint['roll_axis'])
            thigh=Vector(limb.bend.x-limb.root.x,0,limb.bend.z-limb.root.z)
            self.assertAlmostEqual(axis.length,1)
            self.assertAlmostEqual(axis.dot(thigh),0)
            self.assertAlmostEqual(axis.Y,0)
            self.assertGreater(axis.X,.7)
            moved=(A.pivot(joint['roll'],axis,5)*Pos(*joint['bend'])).position
            self.assertAlmostEqual(moved.Y-joint['bend'][1],limb.upper*sin(radians(5)))

    def test_front_roll_is_fixed_to_the_spine_before_pitch(self):
        for pose,body in B.poses().items():
            joints=A.joint_data(pose);front=joints['front']
            self.assertEqual(list(front['order']),['roll','pitch','bend'])
            self.assertEqual(list(joints['rear']['order']),['pitch','roll','bend'])
            tf=A.body_location(body)
            spine=(tf*Pos(0,0,1)).position-tf.position
            axis=Vector(front['roll_axis'])
            self.assertAlmostEqual(abs(axis.dot(spine)),1)
            origin=(tf*Pos(0,P.SHOULDER_A_Y,150)).position
            self.assertLess((origin-Vector(front['roll'])).length,1e-8)
            self.assertAlmostEqual((Vector(front['pitch'])-origin).length,40)

    def test_physical_servo_axes_match_the_kinematics(self):
        for pose in B.poses():
            joints=A.joint_data(pose)
            for reference,owner,frame in A.socket_frames(pose):
                key=reference.split('_')[1];joint=joints[key]
                origin=(frame*Pos(0,0,P.SOCKET_AXIS_Z)).position
                output=(frame*Pos(1,0,P.SOCKET_AXIS_Z)).position-origin
                if '_roll_' in reference:
                    self.assertEqual(owner,'shoulder_socket_right' if key=='front' else 'rear_carrier_right')
                    self.assertAlmostEqual(abs(output.dot(Vector(joint['roll_axis']))),1)
                    self.assertLess((origin-Vector(joint['roll'])).length,1e-8)
                elif '_pitch_' in reference:
                    self.assertEqual(owner,'front_carrier_right' if key=='front' else 'pelvis_socket_right')
                    self.assertAlmostEqual(abs(output.Y),1)
                    self.assertLess((origin-Vector(joint['pitch'])).length,1e-8)
                elif '_knee_' in reference or '_elbow_' in reference:
                    self.assertAlmostEqual(abs(output.Y),1)
                    self.assertLess((origin-Vector(joint['bend'])).length,1e-8)

    def test_actual_carriers_follow_each_limbs_first_axis(self):
        for pose in B.poses():
            nominal={n:s for n,s,*_ in A.scene_details(pose=pose)}
            rolled={n:s for n,s,*_ in A.scene_details(roll=5,pose=pose)}
            pitched={n:s for n,s,*_ in A.scene_details(pitch=5,pose=pose)}
            for key in ('rear','front'):
                for side in ('right','left'):
                    n=f'{key}_carrier_{side}'
                    upstream,downstream=(rolled,pitched) if key=='front' else (pitched,rolled)
                    self.assertLess((nominal[n].center()-downstream[n].center()).length,1e-7)
                    self.assertGreater((nominal[n].center()-upstream[n].center()).length,.1)
                    primary='roll' if key=='front' else 'pitch'
                    n=f'reference_{key}_{primary}_servo_{side}'
                    self.assertLess((nominal[n].center()-upstream[n].center()).length,1e-7)

    def test_audit_cache_tracks_front_pitch_after_roll(self):
        from unittest.mock import patch
        from build123d import Box,Compound
        from koala_hardware.audit import check_scene
        # A fork's bounding box contains a clear window. Moving the next stage
        # into either cheek must invalidate the cached no-contact result.
        carrier=Compound(children=[Pos(-3,0,0)*Box(2,4,4),Pos(3,0,0)*Box(2,4,4)])
        def scene(roll=0,pitch=0,knee=0,**kwargs):
            return [('carrier',carrier,'','front_roll',1),
                    ('arm',Pos(3 if pitch else 0,0,0)*Box(1,1,1),'','front_pitch',1)]
        joints={'front':{'order':['roll','pitch','bend']}}
        with patch.object(A,'scene_details',side_effect=scene),patch.object(A,'joint_data',return_value=joints),\
             patch('koala_hardware.audit.fit_pairs',return_value={}):
            cache=set()
            self.assertEqual(check_scene('test',(0,0,0),cache),1)
            with self.assertRaisesRegex(AssertionError,'carrier.*arm'):
                check_scene('test',(0,5,0),cache)

    def test_socket_contact_allowance_follows_a_perturbed_pose(self):
        from koala_hardware.audit import fit_pairs,volume
        q=(-5,5,5)
        shapes={n:s for n,s,*_ in A.scene_details(*q,pose='upright',asymmetric=True)}
        for pair,zone in fit_pairs('upright',q,asymmetric=True).items():
            a,b=pair;hit=shapes[a]&shapes[b]
            self.assertLessEqual(volume(hit),50)
            self.assertLess(volume(hit-zone),.01)


if __name__=='__main__':unittest.main()
