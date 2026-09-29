# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Native document histories must recompute and retain human-editable features."""
import tempfile
import unittest
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
import FreeCAD as App
from koala_hardware.parts import e_tray
from koala_hardware.freecad_build import save_checked
from koala_hardware.freecad_document import make_document, validate_document


class FreeCADTests(unittest.TestCase):
    def test_native_cylinder_edit_changes_the_saved_spacer(self):
        spec=e_tray.build_spacer()
        doc,final=make_document('NativeHistoryTest',spec['part'])
        try:
            self.assertEqual(final.TypeId,'Part::Cut')
            old=final.Shape.Volume
            outer=final.Base
            self.assertEqual(outer.TypeId,'Part::Cylinder')
            outer.Radius=4
            doc.recompute()
            self.assertGreater(final.Shape.Volume,old)
            validate_document(doc,final)
            with tempfile.TemporaryDirectory() as td:
                path=Path(td)/'spacer.FCStd'
                save_checked(doc,final,path)
                self.assertTrue(path.exists())
                self.assertEqual(doc.Name,'NativeHistoryTest') # readback must not close the original
                with zipfile.ZipFile(path) as archive:
                    view=ET.fromstring(archive.read('GuiDocument.xml'))
                visible=[o.get('name') for o in view.findall('./ViewProviderData/ViewProvider')
                         if o.find('./Properties/Property/Bool').get('value')=='true']
                self.assertIn(final.Name,visible)
                self.assertNotIn(outer.Name,visible)
        finally:App.closeDocument(doc.Name)

    def test_step_import_excludes_origin_planes(self):
        from koala_hardware.cad import Box,export_step,import_step
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/'box.step'
            export_step(Box(2,3,4),path)
            imported=import_step(path)
            self.assertEqual(len(imported.fc.Solids),1)
            self.assertAlmostEqual(imported.volume,24)
            self.assertLess(imported.fc.BoundBox.DiagonalLength,6)

    def test_mirror_of_rotated_translated_link_keeps_its_frame(self):
        from koala_hardware.cad import Box,Pos,Rot,Plane,mirror
        part=mirror(Pos(3,7,11)*Rot(Y=33)*Box(2,3,4),Plane.XY)
        doc,final=make_document('MirrorFrameTest',part)
        try:
            self.assertAlmostEqual(final.Shape.Solids[0].CenterOfMass.z,-11)
            self.assertEqual(final.TypeId,'Part::Mirroring')
        finally:App.closeDocument(doc.Name)

    def test_engraving_is_native_fully_constrained_sketch_geometry(self):
        from koala_hardware.cad import Text,extrude
        shape=extrude(Text('3.4',font_size=5),amount=.6)
        doc,final=make_document('TextHistoryTest',shape)
        try:
            sketches=[o for o in doc.Objects if o.TypeId=='Sketcher::SketchObject']
            self.assertEqual(len(sketches),1)
            self.assertEqual(sketches[0].DoF,0)
            self.assertEqual(final.TypeId,'Part::Extrusion')
        finally:App.closeDocument(doc.Name)

if __name__=='__main__':unittest.main()
