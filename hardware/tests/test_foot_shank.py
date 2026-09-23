# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Interchangeability, assembly and manufacturing checks for DEC-62."""
from collections import Counter
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from build123d import Pos, Rot, Cylinder, Align
from koala_hardware import assembly as A, body_plan as B, params as P, servo_iface as S
from koala_hardware.audit import clear, volume
from koala_hardware.meshing import export_mesh
from koala_hardware.parts import foot_shank as FS, front as F, links as L, configuration_specs
from koala_hardware.printability import metrics


class FootShankTests(unittest.TestCase):
    def test_one_solid_with_closed_mesh_broad_bed_and_new_version(self):
        d=FS.build();part=d['part']
        self.assertTrue(part.is_valid)
        self.assertEqual(len(part.solids()),1)
        self.assertEqual(d['version'],1)
        self.assertEqual(d['printable'],'unknown')
        with tempfile.TemporaryDirectory() as td:
            mesh=export_mesh(d['orientation']*part,Path(td)/'foot.stl')
        self.assertTrue(mesh.is_watertight)
        self.assertGreater(metrics(mesh)['bed_area'],1000)
        self.assertLess(max(mesh.extents[:2]),200)
        self.assertLess(mesh.extents[2],21)

    def test_interchangeable_knee_seats_holes_heads_and_driver_access(self):
        part=FS.solid()
        core=S._box(-40,40,-6,6,-12,P.SOCKET_PLATE_R)
        expected=(L.fork('drive')+L.fork('idler'))&core
        self.assertLess(volume(expected-part)+volume((part&core)-expected),.01)
        for head in S.horn_head_envelopes().solids():clear(part,head,'footed knee head')
        for side in ('drive','idler'):
            frame=L.AXIS*S.plate_location(side)
            for x in (-4.95,4.95):
                for y in (-4.95,4.95):
                    clear(part,frame*Pos(x,y,4)*Cylinder(3.19,35,
                          align=(Align.CENTER,Align.CENTER,Align.MIN)),'footed knee driver')

    def test_identical_pad_key_and_nut_access_without_drive_bracket(self):
        shift=FS.pad_location();part=part_at_front=shift.inverse()*FS.solid()
        region=S._box(-15,15,-15,15,80,110)
        original=F.forearm()&region
        self.assertLess(volume((part_at_front&region)-original)+volume(original-part_at_front),.01)
        clear(part,L.front_pad(),'existing TPU pad/key')
        clear(part,A.pad_fixing(),'existing pad head and nut')
        clear(part,S._box(0,25,-2.8,2.8,P.FRONT_PAD_NUT_Z+.1,P.FRONT_PAD_NUT_Z+2.5),'nut side insertion')
        # The full 37D ring cannot silently survive under a new part name.
        self.assertLess(FS.solid().volume,L.lower_link(P.BODY_SHANK_MM).volume)

    def test_local_knee_sweep_with_pad_and_both_case_models(self):
        with patch.object(S,'case_model',return_value=None):fallback=S.socket_reference.__wrapped__()
        thigh=L.upper_link(P.BODY_THIGH_MM,True)
        package=FS.solid()+FS.pad_location()*L.front_pad()
        for angle in range(0,121,10):
            lower=Pos(0,0,P.BODY_THIGH_MM)*Rot(X=angle)*package
            clear(lower,thigh,f'footed knee {angle} / thigh')
            for case in (S.socket_reference(),fallback):
                clear(lower,L.knee_socket_frame(P.BODY_THIGH_MM,True)*case,f'footed knee {angle} / case')

    def test_four_grounded_feet_no_drive_hardware_and_shared_upper_chassis(self):
        pose=B.check()['poses']['walking']
        self.assertEqual(pose['rear'].lower,90)
        self.assertGreater(pose['rear'].flexion,20)
        scene={n:s for n,s,c in A.build_scene(pose='walking')}
        wheel={n:s for n,s,c in A.build_scene(pose='quadruped')}
        self.assertFalse(any('_'+kind+'_' in n for n in scene for kind in ('motor','shaft','hub','wheel')))
        for side in ('right','left'):
            for limb in ('rear','front'):
                self.assertAlmostEqual(scene[f'{limb}_contact_pad_{side}'].bounding_box().min.Z,0,places=5)
        for name,part in scene.items():self.assertGreaterEqual(part.bounding_box().min.Z,-1e-5,name)
        for name in ('torso_frame','pelvis_socket_right','front_forearm_right'):
            self.assertLess(volume(scene[name]-wheel[name])+volume(wheel[name]-scene[name]),.01)

    def test_each_build_counts_only_its_fitted_shanks_and_pad_fixings(self):
        for config,prints,pads,motor_screws in [('walking',28,4,0),('wheeled',26,2,12)]:
            counts={};hardware=Counter()
            for d in configuration_specs(config):
                if d['name'].startswith('coupon'):continue
                qty=d['qty']*(2 if d.get('handed') else 1)
                counts[d['name']]=qty
                hardware.update({k:v*qty for k,v in d['fasteners'].items()})
            self.assertEqual(sum(counts.values()),prints)
            self.assertEqual(counts['front_contact_pad'],pads)
            self.assertEqual(hardware['M3x20 TPU-pad screw'],pads)
            self.assertEqual(hardware['M3x8 motor-face screw (depth to verify)'],motor_screws)
            self.assertEqual(hardware['M3x6 supplied horn-square pan screw (bottoming to verify)'],96)
            self.assertEqual('foot_shank' in counts,config=='walking')
            self.assertEqual('shank' in counts,config=='wheeled')


if __name__=='__main__':unittest.main()
