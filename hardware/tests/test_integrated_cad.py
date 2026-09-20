# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Regression checks for structural decomposition and the measured interface."""
import unittest
from build123d import Pos
from koala_hardware import params as P,servo_iface as S
from koala_hardware.parts import all_builders,links as L,front as F,shoulder_mount
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
            spec=F.build_forearm()
            export_mesh(spec['orientation']*spec['part'],path)
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

    def test_carriers_match_their_builders_and_have_flat_backs(self):
        from koala_hardware import assembly as A,body_plan as B
        builders={'front':F.build_carrier(),'rear':L.build_hip_carrier()}
        for d in builders.values():
            self.assertEqual(d['qty']*(2 if d['handed'] else 1),2)
        self.assertAlmostEqual(L.rear_axis_y(),P.ROOT_ROLL_Y)
        for pose,body in B.poses().items():
            shapes={n:s for n,s,*_ in A.scene_details(pose=pose)}
            self.assertNotIn('reference_head_envelope',shapes)
            for key in ('front','rear'):
                limb=body[key];d=builders[key]
                from build123d import Rot
                tf=(A.body_location(body)*shoulder_mount.carrier_frame() if key=='front'
                    else A.segment_frame(limb.root,limb.bend,0)*Rot(Z=-90))
                part=tf.inverse()*shapes[key+'_carrier_right']
                self.assertLess(volume(part-d['part'])+volume(d['part']-part),.01)
        import tempfile
        from pathlib import Path
        from koala_hardware.meshing import export_mesh
        from koala_hardware.printability import metrics
        with tempfile.TemporaryDirectory() as td:
            for key,d in builders.items():
                mesh=export_mesh(d['orientation']*d['part'],Path(td)/f'{key}.stl')
                self.assertTrue(mesh.is_watertight)
                self.assertGreater(metrics(mesh)['bed_area'],1900)

    def test_hip_carrier_and_thigh_clear_the_root_and_each_other_at_rest(self):
        from koala_hardware import assembly as A
        from koala_hardware.audit import overlap
        for pose in ('quadruped','upright'):
            d={n:p for n,p,c,g,s in A.scene_details(pose=pose)}
            for a,b in (('rear_carrier_right','reference_rear_pitch_servo_right'),('rear_carrier_right','pelvis_socket_right'),
                        ('rear_thigh_right','rear_carrier_right'),('rear_thigh_right','reference_rear_roll_servo_right'),
                        ('reference_rear_roll_servo_right','pelvis_socket_right')):
                self.assertLess(overlap(d[a],d[b]),.01,f'{pose}: {a} vs {b}')

    def test_hip_carrier_refinement_preserves_horn_pads_and_servo_access(self):
        from build123d import Plane,mirror
        from koala_hardware.audit import clear
        part=L.carrier(False)
        forks=mirror(L.pitch_fork_frame()*(L.fork('drive')+L.fork('idler')),Plane.XY)
        # A bevel following tangent edges can silently cut into a screw pad.
        # Compare the complete horn region, including its web and recesses.
        region=S._box(-30,30,-10,100,-P.SOCKET_PLATE_R-1,P.SOCKET_PLATE_R)
        self.assertLess(volume((part-forks)&region)+volume((forks-part)&region),.01)
        heads=mirror(L.pitch_fork_frame()*S.horn_head_envelopes(),Plane.XY)
        for head in heads.solids(): clear(part,head,'hip pitch horn head/washer')
        tf=L.roll_socket_frame(P.ROOT_ROLL_Y)
        for name,probe in S.socket_keepouts()[1:]:
            clear(part,tf*probe,'hip roll '+name)
        for shift in (0,5,15,25,50):
            clear(part,tf*Pos(0,0,shift)*S._parametric_case(),'hip roll insertion')
        for head in (tf*S.ear_head_envelopes()).solids():
            clear(part,head,'hip roll ear head')

    def test_main_limb_prints_are_connected(self):
        for part in (F.upper_arm(),F.forearm(),F.carrier(),L.upper_link(85,True),L.lower_link(90)):
            self.assertTrue(part.is_valid)
            self.assertEqual(len(part.solids()),1)

    def test_rear_links_keep_complete_horn_pads_and_driver_paths(self):
        from build123d import Rot,Cylinder,Align
        from koala_hardware.audit import clear
        for part,tf,core in ((L.upper_link(85,True),Rot(Z=-90),S._box(-6,6,-40,40,-12,P.SOCKET_PLATE_R)),
                             (L.lower_link(90),Pos(),S._box(-40,40,-6,6,-12,P.SOCKET_PLATE_R))):
            expected=tf*(L.fork('drive')+L.fork('idler'))
            # Retain every original pad seat and web: the arms' core (inner 12 of the
            # 16 mm width) must be complete. The v2 rounding pass (2026-09-19) may
            # round the arms' outer corners R2; the outer return fillets may add
            # material. The independent head/driver checks below still apply.
            self.assertLess(volume((expected-part)&core),.01)
            for head in (tf*S.horn_head_envelopes()).solids():clear(part,head,'rear horn head/washer')
            for side in ('drive','idler'):
                frame=tf*L.AXIS*S.plate_location(side)
                for x in (-4.95,4.95):
                    for y in (-4.95,4.95):
                        clear(part,frame*Pos(x,y,4)*Cylinder(3.19,35,align=(Align.CENTER,Align.CENTER,Align.MIN)),
                              'rear horn driver through stepped fork')

    def test_rear_thigh_roll_and_knee_folding_clear_the_adjacent_joint(self):
        from build123d import Rot
        from koala_hardware.audit import clear
        from unittest.mock import patch
        thigh=L.upper_link(85,True);shank=L.lower_link(90)
        tf=Pos(-P.ROOT_ROLL_Y,0,0)*Rot(Z=-90)
        with patch.object(S,'case_model',return_value=None):fallback=S.socket_reference.__wrapped__()
        for angle in (-30,-15,0,15,30):
            clear(Rot(Y=angle)*thigh,tf*L.carrier(False),'thigh swing / carrier')
            clear(Rot(Y=angle)*thigh,tf*L.roll_socket_frame(P.ROOT_ROLL_Y)*S.socket_reference(),'thigh swing / B case')
            clear(Rot(Y=angle)*thigh,tf*L.roll_socket_frame(P.ROOT_ROLL_Y)*fallback,'thigh swing / measured B case')
        for angle in (0,60,90,120):
            lower=Pos(0,0,85)*Rot(X=angle)*shank
            clear(lower,thigh,'folded knee / thigh')
            clear(lower,L.knee_socket_frame(85,True)*S.socket_reference(),'folded knee / C case')

    def test_motor_shank_keeps_insertion_and_all_six_fixing_approaches(self):
        from koala_hardware.audit import check_motor_insertion
        check_motor_insertion()

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
        from build123d import Plane,mirror
        from koala_hardware.parts import pelvis
        from koala_hardware.audit import clear,check_frame
        for module in (pelvis.module(False),shoulder_mount.module()):
            clear(module,mirror(module,Plane.XZ),'separate root modules')
        check_frame()

    def test_root_driver_audit_rejects_restoring_the_obstructing_torso_flange(self):
        from unittest.mock import patch
        from koala_hardware.parts import torso
        from koala_hardware.audit import check_frame
        # Restore precisely the horizontal flange that hid the original driver
        # obstruction. Module-only checks pass this geometry; the audit must fail.
        restored=torso.solid()+S._box(-46,20,-P.TORSO_HALF_WIDTH,P.TORSO_HALF_WIDTH,torso.LOW,torso.LOW+5)
        with patch.object(torso,'solid',return_value=restored):
            with self.assertRaisesRegex(AssertionError,r'rear .* torso driver'):
                check_frame()

    def test_torso_dorsal_rails_clear_front_carrier_roll(self):
        from koala_hardware import assembly as A
        from koala_hardware.audit import clear
        for pose in ('quadruped','upright'):
            shapes={n:s for n,s,*_ in A.nominal_details(pose)}
            joint=A.joint_data(pose)['front']
            for angle in (-15,15):
                carrier=A.joint_transform(joint,'roll',roll=angle)*shapes['front_carrier_right']
                clear(shapes['torso_frame'],carrier,f'{pose} shoulder rail / carrier at roll {angle}')

    def test_front_joint_lengths_contact_reach_and_socket_recess(self):
        from build123d import Vector,GeomType
        from OCP.BRepAdaptor import BRepAdaptor_Surface
        from koala_hardware import assembly as A,body_plan as B
        from koala_hardware.parts import torso
        for pose,body in B.poses().items():
            origins={name:(tf*Pos(0,0,P.SOCKET_AXIS_Z)).position for name,_,tf in A.socket_frames(pose)}
            elbow=origins['reference_front_elbow_servo_right']
            self.assertAlmostEqual((elbow-origins['reference_front_pitch_servo_right']).length,70)
            shapes={n:s for n,s,*_ in A.scene_details(pose=pose)}
            pad=shapes['front_contact_pad_right']
            spheres=[f for f in pad.faces() if f.geom_type==GeomType.SPHERE]
            self.assertTrue(spheres)
            contact=Vector(BRepAdaptor_Surface(spheres[0].wrapped).Sphere().Location().Coord())
            self.assertAlmostEqual((contact-elbow).length,100)
            roll_body=(A.body_location(body).inverse()*Pos(*origins['reference_front_roll_servo_right'])).position
            self.assertAlmostEqual(roll_body.Z,150)
        lip=(shoulder_mount.socket_frame()*Pos(0,0,P.SOCKET_DEPTH)).position
        self.assertAlmostEqual(torso.solid().bounding_box().max.Y-lip.Y,10,delta=1e-5)
        self.assertGreater(torso.solid().bounding_box().max.Z,P.BODY_TORSO_LENGTH_MM)

    def test_redesigned_parts_do_not_inherit_physical_print_provenance(self):
        specs={f()['name']:f() for f in all_builders()}
        for name in ('shoulder_carrier','upper_arm','forearm','shoulder_mount','torso_frame','thigh'):
            self.assertEqual(specs[name]['printable'],'unknown',name)
        self.assertEqual(specs['root_socket']['version'],1)
        self.assertEqual(specs['root_socket']['printable'],'proven')
        self.assertEqual(specs['front_contact_pad']['version'],1)

    def test_corrected_flat_horn_faces_clear_measured_centres(self):
        reference=S.socket_reference()
        for side in ('drive','idler'):
            fork=S.plate_location(side)*S.clevis_plate(side)
            self.assertLess(volume(fork&reference),.01)
        self.assertAlmostEqual(P.SOCKET_DRIVE_FACE-P.SOCKET_IDLER_FACE,36.4)
        self.assertAlmostEqual(S.ear_face('drive')-S.ear_face('idler'),31.8)
        self.assertAlmostEqual(6-P.SOCKET_PLATE_T-P.HORN_IDLER_WASHER_T,2.0)


if __name__=='__main__':unittest.main()
