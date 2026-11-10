# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Pocket-limited 20.8 mm links and signed placement regression checks."""
import unittest
from koala_hardware import assembly as A, body_plan as B
from koala_hardware.bend_limits import SIGNED_BEND_LIMITS, FIRST_BLOCKED_SAMPLES, REVIEW_POSES, nominal_angle
from koala_hardware.bend_clearance import local_geometry, local_sample


class BendLimitTests(unittest.TestCase):
    def test_endpoints_clear_and_contact_beyond_them_is_detected(self):
        for key,bounds in SIGNED_BEND_LIMITS.items():
            geometry=local_geometry(key)
            for angle in bounds:
                row=local_sample(key,angle,geometry)
                self.assertLessEqual(max(row['overlap_mm3'].values()),.01,(key,row))
            for angle in FIRST_BLOCKED_SAMPLES[key]:
                row=local_sample(key,angle,geometry)
                self.assertGreater(row['overlap_mm3']['printed_cup'],.01,(key,row))

    def test_missing_vendor_file_is_not_reported_as_a_second_case_model(self):
        from unittest.mock import patch
        from koala_hardware import servo_iface as S
        with patch.object(S,'case_model',return_value=None):
            names=[name for name,_ in local_geometry('front')[2]]
        self.assertIn('fallback_case',names)
        self.assertNotIn('vendor_case',names)

    def test_actual_front_folds_negative_and_nominal_poses_remain_inside_limits(self):
        for pose in B.poses().values():
            self.assertLess(nominal_angle(pose['front']),0)
            for key in ('front','rear'):
                value=nominal_angle(pose[key]);lo,hi=SIGNED_BEND_LIMITS[key]
                self.assertLess(lo,value);self.assertLess(value,hi)

    def test_endpoint_pose_rotates_entire_lower_packages_and_mirrors_both_sides(self):
        original={n:s for n,s,_,_,_ in A.nominal_details('walking')}
        for name in REVIEW_POSES:
            items={n:s for n,s,_,_,_ in A.bend_review_details(name)}
            self.assertEqual(set(items),set(original))
            for n in ('torso_frame','front_upper_arm_right','rear_thigh_right'):
                self.assertAlmostEqual(items[n].volume,original[n].volume)
                self.assertAlmostEqual((items[n].center()-original[n].center()).length,0)
            for prefix in ('front_forearm','rear_shank','front_contact_pad','rear_contact_pad'):
                a,b=(items[prefix+'_'+hand].center() for hand in ('right','left'))
                self.assertAlmostEqual(a.X,b.X);self.assertAlmostEqual(a.Y,-b.Y);self.assertAlmostEqual(a.Z,b.Z)
                self.assertGreater((items[prefix+'_right'].center()-original[prefix+'_right'].center()).length,1)

if __name__=='__main__':unittest.main()
