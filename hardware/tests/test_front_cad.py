# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Manufacturing and local movement checks for the roll-first front limbs."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from build123d import Pos, Rot, Cylinder, Align, Plane, mirror

from koala_hardware import params as P, servo_iface as S
from koala_hardware.audit import clear, volume
from koala_hardware.meshing import export_mesh
from koala_hardware.parts import front as F, links as L, pelvis, shoulder_mount as SM, neck_space, torso
from koala_hardware.printability import metrics


class FrontCADTests(unittest.TestCase):
    def test_all_three_prints_are_connected_closed_and_have_real_bed_faces(self):
        minimum_bed={'shoulder_carrier':2000,'upper_arm':900,'forearm':1400}
        maximum_height={'shoulder_carrier':51,'upper_arm':49.1,'forearm':21}
        with tempfile.TemporaryDirectory() as td:
            for build in F.BUILDERS:
                d=build();part=d['part']
                self.assertTrue(part.is_valid,d['name'])
                self.assertEqual(len(part.solids()),1,d['name'])
                mesh=export_mesh(d['orientation']*part,Path(td)/(d['name']+'.stl'))
                self.assertTrue(mesh.is_watertight,d['name'])
                self.assertGreater(metrics(mesh)['bed_area'],minimum_bed[d['name']])
                self.assertLess(mesh.extents[2],maximum_height[d['name']])
                self.assertLess(max(mesh.extents[:2]),200)
                self.assertEqual(d['version'],3 if d['name']=='shoulder_carrier' else 2)
                self.assertEqual(d['printable'],'unknown')

    def test_viewer_tessellation_of_the_installed_carrier_remains_closed(self):
        from koala_hardware import assembly as A,body_plan,viewer
        from OCP.BRepTools import BRepTools
        carrier=A.body_location(body_plan.poses()['quadruped'])*SM.carrier_frame()*F.carrier()
        # Earlier manufacturing exports cache a finer mesh on the same OCC
        # faces. Start cold so the viewer cannot accidentally inherit it.
        BRepTools.Clean_s(carrier.wrapped)
        with tempfile.TemporaryDirectory() as td:
            mesh=viewer._mesh(carrier,Path(td),0)
        self.assertTrue(mesh.is_watertight)
        self.assertGreater(mesh.volume,0)

    def test_cups_keep_insertion_cables_and_all_four_ear_driver_paths(self):
        for part,tf in ((F.carrier(),F.pitch_socket_frame()),
                        (F.upper_arm(),F.elbow_socket_frame())):
            for name,probe in S.socket_keepouts()[1:]:
                clear(part,tf*probe,'front bench '+name)
            for offset in (0,5,15,25,50):
                clear(part,tf*Pos(0,0,offset)*S._parametric_case(),'front cup insertion')
            for head in (tf*S.ear_head_envelopes()).solids():
                clear(part,head,'front seated ear screw')

    def test_horn_interfaces_and_straight_square_driver_paths_are_complete(self):
        core=S._box(-40,40,-6,6,-12,P.SOCKET_PLATE_R)
        expected=L.fork('drive')+L.fork('idler')
        for part,pads in ((F.carrier(),mirror(expected,Plane.XY)),
                          (F.upper_arm(),expected),(F.forearm(),expected)):
            self.assertLess(volume((pads&core)-part),.01)
            for head in S.horn_head_envelopes().solids():
                clear(part,head,'front horn head and washer')
            for side in ('drive','idler'):
                tf=L.AXIS*S.plate_location(side)
                for x in (-4.95,4.95):
                    for y in (-4.95,4.95):
                        probe=tf*Pos(x,y,4)*Cylinder(3.19,35,
                            align=(Align.CENTER,Align.CENTER,Align.MIN))
                        clear(part,probe,'front straight horn driver')

    def test_local_roll_pitch_and_elbow_ranges_clear_with_both_case_envelopes(self):
        with patch.object(S,'case_model',return_value=None):
            fallback=S.socket_reference.__wrapped__()
        carrier=F.carrier();upper=F.upper_arm();forearm=F.forearm()
        root=F.roll_socket_frame()*pelvis.root_socket()
        for case in (S.socket_reference(),fallback):
            a=F.roll_socket_frame()*case
            b=F.pitch_socket_frame()*case
            c=F.elbow_socket_frame()*case
            for angle in range(-30,61,15):
                moving=Rot(X=angle)*carrier
                clear(moving,a,'front local roll / A')
                clear(moving,root,'front local roll / A module')
            for angle in range(-90,91,15):
                moving=F.pitch_link_frame()*Rot(X=angle)*upper
                for obstacle,label in ((carrier,'carrier'),(a,'A'),(b,'B'),(root,'A module')):
                    clear(moving,obstacle,'front local pitch / '+label)
            for angle in range(0,121,15):
                moving=Pos(0,0,P.BODY_UPPER_ARM_MM)*Rot(X=angle)*forearm
                clear(moving,upper,'front local elbow / upper arm')
                clear(moving,c,'front local elbow / C')

    def test_parallel_pitch_elbow_axes_retain_lengths_and_existing_pad(self):
        self.assertEqual(P.BODY_UPPER_ARM_MM,70)
        self.assertEqual(P.BODY_FOREARM_MM+P.BODY_HAND_MM,100)
        # Pocket frame's +X is the elbow shaft, parallel to the upper fork X.
        p=F.elbow_socket_frame()*Pos(1,0,0)
        origin=F.elbow_socket_frame().position
        delta=p.position-origin
        self.assertAlmostEqual(delta.X,1)
        self.assertAlmostEqual(delta.Y,0)
        self.assertAlmostEqual(delta.Z,0)
        terminal=S._box(-15,15,-15,15,P.FRONT_PAD_START,110)
        old=L.lower_link(100,True)&terminal
        new=F.forearm()&terminal
        self.assertLess(volume(old-new)+volume(new-old),.01)

    def test_root_roll_clears_the_complete_driven_package_with_real_margin(self):
        from koala_hardware import assembly as A,body_plan
        with patch.object(S,'case_model',return_value=None):fallback=S.socket_reference.__wrapped__()
        for pose in ('quadruped','upright'):
            body=A.body_location(body_plan.poses()[pose]);d=A.joint_data(pose)['front']
            root=body*SM.socket_frame()
            obstacles={'A module':body*SM.module(),'cassette':body*SM.solid(),
                       'A imported case':root*S.socket_reference(),'A caliper case':root*fallback,
                       'A ear screws':root*S.ear_head_envelopes(),'root fixings':body*SM.root_fixings()}
            moving=[(n,p) for n,p,_,g,side in A.nominal_details(pose)
                    if side==1 and g.startswith('front_') and not g.endswith('fixed')]
            for angle in (-30,-15,0,15,30):
                tf=A.joint_transform(d,'roll',roll=angle)
                for name,part in moving:
                    shifted=tf*part
                    for other,obstacle in obstacles.items():
                        clear(shifted,obstacle,f'{pose} roll {angle}: {name} / {other}')
                    if abs(angle)==30 and name in ('front_upper_arm_right','reference_front_pitch_horn_heads_right'):
                        # The earlier 35 mm spacing cleared the empty carrier,
                        # but the driven fork hit A after about eight degrees.
                        self.assertGreater(shifted.distance_to(obstacles['A caliper case']),1.5)

    def test_shoulder_recess_and_front_width_close_against_the_actual_modules(self):
        self.assertAlmostEqual(P.TORSO_HALF_WIDTH-SM.module().bounding_box().max.Y,10,places=5)
        b=SM.carrier_frame()*F.pitch_socket_frame()*Pos(0,0,P.SOCKET_AXIS_Z)
        self.assertAlmostEqual(2*b.position.Y,P.BODY_SHOULDER_WIDTH_MM)
        self.assertAlmostEqual(b.position.Z,P.BODY_TORSO_LENGTH_MM)
        clear(SM.module(),SM.solid(),'shoulder module/cassette')
        clear(SM.module(),mirror(SM.module(),Plane.XZ),'opposite recessed modules')

    def test_three_small_neck_servos_keep_packaging_and_cartridge_driver_space(self):
        obstacles={'torso':torso.solid()}
        for name,part in (('module',SM.module()),('cassette',SM.solid()),
                          ('A servo',SM.socket_frame()*S.socket_reference())):
            for side in (1,-1):
                obstacles[name+str(side)]=part if side==1 else mirror(part,Plane.XZ)
        self.assertEqual(len(neck_space.case_envelopes()),3)
        self.assertEqual(neck_space.clearance_interferences(obstacles),[])
        self.assertEqual(neck_space.CAP_Z,P.TORSO_SHOULDER_TOP)
        # The installed case/ear allocations also participate in the tool check.
        obstacles.update({n:s for n,s,_ in neck_space.reference_items()})
        drivers=neck_space.driver_envelopes()
        self.assertEqual(len(drivers),4)
        for name,probe in drivers.items():
            for other,part in obstacles.items():clear(probe,part,name+' / '+other)

    def test_front_viewer_exempts_only_each_servos_actual_driven_fork(self):
        import trimesh
        from koala_hardware import assembly as A, viewer
        details=[d for d in A.nominal_details('quadruped') if 'front_' in d[0]]
        frames=[f for f in A.socket_frames('quadruped') if '_front_' in f[0]]
        with patch.object(viewer,'all_builders',return_value=F.BUILDERS), \
             patch.object(viewer,'_mesh',return_value=trimesh.creation.box()):
            items={d['name']:d for d in viewer._assembly_items(Path('/tmp'),details=details,frames=frames)}
        for joint,driven in (('roll','carrier'),('pitch','upper_arm'),('elbow','forearm')):
            for side in ('right','left'):
                name=f'reference_front_{joint}_servo_{side}'
                self.assertEqual(items[name]['contactPartner'],f'front_{driven}_{side}')
                self.assertEqual(items[f'front_{driven}_{side}']['version'],3 if driven=='carrier' else 2)


if __name__=='__main__':unittest.main()
