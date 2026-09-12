# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Regression checks for structural decomposition and the measured interface."""
import unittest
from build123d import Pos
from koala_hardware import params as P,servo_iface as S
from koala_hardware.parts import all_builders,links as L
from koala_hardware.audit import volume


class IntegratedCADTests(unittest.TestCase):
    def test_saddle_export_has_no_tangent_nonmanifold_edges(self):
        import tempfile
        from pathlib import Path
        import trimesh
        from build123d import export_stl
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/'saddle.stl'
            export_stl(S.saddle(),path)
            mesh=trimesh.load(path,force='mesh')
            self.assertTrue(mesh.is_watertight)
            self.assertGreater(mesh.volume,0)

    def test_rounded_forearm_exports_closed_without_collapsed_faces(self):
        import tempfile
        import numpy as np
        import trimesh
        from pathlib import Path
        from koala_hardware.meshing import export_mesh
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/'forearm.stl'
            export_mesh(L.build_forearm()['orientation']*L.build_forearm()['part'],path)
            mesh=trimesh.load(path,force='mesh')
            self.assertTrue(mesh.is_watertight)
            self.assertGreater(mesh.volume,0)
            self.assertTrue(np.all(np.diff(np.sort(mesh.faces,axis=1),axis=1)!=0))
            # The flat forearm is exported on its broad back, not standing on
            # the fork tips; this is the actual manufacturing requirement.
            from koala_hardware.printability import metrics
            self.assertGreater(metrics(mesh)['bed_area'],900)
            self.assertLess(mesh.extents[2],25)

    def test_socket_slots_match_the_asymmetric_so101_template(self):
        from koala_hardware.so101_templates import socket_template
        from build123d import GeomType
        # Read the actual planar recess faces, independently of the builder.
        def slots(part,x):
            out={}
            for face in part.faces():
                if face.geom_type!=GeomType.PLANE:continue
                c=face.center()
                if abs(abs(c.X)-x)<1e-5 and abs(face.normal_at().X)>.99:
                    bb=face.bounding_box()
                    out['drive' if c.X>0 else 'idler']=(bb.size.Y,bb.min.Z)
            return out
        expected=slots(socket_template(),17.4)
        self.assertEqual(set(expected),{'drive','idler'})
        actual=slots(S.saddle(),P.SOCKET_CASE_X/2)
        for side in expected:
            for a,b in zip(actual[side],expected[side]):self.assertAlmostEqual(a,b,places=5)
        self.assertLess(actual['drive'][0],actual['idler'][0])

    def test_four_carriers_share_two_print_variants_and_flat_backs(self):
        from koala_hardware import assembly as A,body_plan as B
        d=L.build_root_carrier()
        self.assertEqual(d['qty']*(2 if d['handed'] else 1),4)
        self.assertAlmostEqual(L.rear_axis_y(),P.BODY_SHOULDER_WIDTH_MM/2)
        for pose,body in B.poses().items():
            shapes={n:s for n,s,*_ in A.scene_details(pose=pose)}
            self.assertNotIn('reference_head_envelope',shapes)
            for key in ('front','rear'):
                limb=body[key]
                from build123d import Rot
                tf=A.segment_frame(limb.root,limb.bend,0)*Rot(Z=-90)
                part=tf.inverse()*shapes[key+'_carrier_right']
                self.assertLess(volume(part-d['part'])+volume(d['part']-part),.01)
        import tempfile
        from pathlib import Path
        from koala_hardware.meshing import export_mesh
        from koala_hardware.printability import metrics
        with tempfile.TemporaryDirectory() as td:
            mesh=export_mesh(d['orientation']*d['part'],Path(td)/'carrier.stl')
            self.assertTrue(mesh.is_watertight)
            self.assertGreater(metrics(mesh)['bed_area'],1900)

    def test_main_limb_prints_are_connected(self):
        for length in (70,85):
            self.assertTrue(L.upper_link(length).is_valid)
            self.assertEqual(len(L.upper_link(length).solids()),1)
        for length,front in ((100,True),(90,False)):
            self.assertTrue(L.lower_link(length,front).is_valid)
            self.assertEqual(len(L.lower_link(length,front).solids()),1)

    def test_fastening_schedule_covers_twelve_joints_and_two_motors(self):
        from collections import Counter
        total=Counter();names=[]
        for builder in all_builders():
            d=builder()
            if d['name'].startswith('coupon'):continue
            qty=d['qty']*(2 if d.get('handed') else 1)
            total.update({k:v*qty for k,v in d['fasteners'].items()});names.append(d['name'])
        self.assertEqual(total['M2x5 self-tapper into servo ear'],48)
        self.assertEqual(total['M3x6 supplied horn-square pan screw (bottoming to verify)'],96)
        self.assertEqual(total['M3x8 motor-face screw (depth to verify)'],12)
        self.assertFalse(any('cheek' in n or 'crossbar' in n for n in names))
        self.assertFalse(any('seam' in k or 'M3x50' in k for k in total))

    def test_two_ankle_drives_and_front_feet_ground_contact(self):
        from koala_hardware import assembly as A
        for pose in ('quadruped','upright'):
            scene={n:s for n,s,c in A.build_scene(pose=pose)}
            self.assertEqual(sum(n.startswith('rear_motor_') for n in scene),2)
            self.assertFalse(any(n.startswith('front_'+k+'_') for n in scene
                                 for k in ('motor','shaft','hub','wheel')))
            for side in ('left','right'):
                self.assertAlmostEqual(scene['rear_wheel_'+side].bounding_box().min.Z,0,places=5)
                foot_z=scene['front_contact_pad_'+side].bounding_box().min.Z
                if pose=='quadruped':self.assertAlmostEqual(foot_z,0,places=5)
                else:self.assertGreater(foot_z,0)
            for n,solid in scene.items():
                self.assertGreaterEqual(solid.bounding_box().min.Z,-1e-5,n)

    def test_independent_root_modules_allow_bench_and_frame_driver_access(self):
        from build123d import Cylinder,Align,Plane,mirror
        from koala_hardware.parts import pelvis
        from koala_hardware.audit import clear
        for front in (False,True):
            module=pelvis.module(front);tf=pelvis.pitch_socket(front)
            clear(module,mirror(module,Plane.XZ),'separate root modules')
            for name,probe in S.socket_keepouts()[1:]:
                clear(module,tf*probe,'bench module '+name)
            for shift in (0,5,15,25,50):
                clear(module,tf*Pos(0,0,shift)*S._parametric_case(),'open-end insertion')
            z0=-P.ROOT_MOUNT_Z-P.FRAME_PLATE_T if front else P.ROOT_REAR_MOUNT_Z
            for x,y in P.ROOT_FRAME_HOLES:
                if y<0:continue
                za,zb=(z0+P.FRAME_PLATE_T,z0+P.FRAME_PLATE_T+40) if front else (z0-40,z0)
                probe=Pos(x,y,za)*Cylinder(3,zb-za,align=(Align.CENTER,Align.CENTER,Align.MIN))
                clear(pelvis.solid(front),probe,'installed frame head driver')
                clear(tf*S.socket_reference(),probe,'frame driver / installed servo')

    def test_corrected_flat_horn_faces_clear_measured_centres(self):
        reference=S.socket_reference()
        for side in ('drive','idler'):
            fork=S.plate_location(side)*S.clevis_plate(side)
            self.assertLess(volume(fork&reference),.01)
        self.assertAlmostEqual(P.SOCKET_DRIVE_FACE-P.SOCKET_IDLER_FACE,36.4)
        self.assertAlmostEqual(S.ear_face('drive')-S.ear_face('idler'),31.8)
        self.assertAlmostEqual(6-P.SOCKET_PLATE_T-P.HORN_IDLER_WASHER_T,2.0)


if __name__=='__main__':unittest.main()
