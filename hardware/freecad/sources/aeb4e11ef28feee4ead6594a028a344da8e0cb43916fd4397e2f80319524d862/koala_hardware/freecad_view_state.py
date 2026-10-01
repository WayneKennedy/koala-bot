# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Persist visibility and an isometric camera from headless FreeCAD builds.

FreeCAD's GUI ignores document-side Visibility on first open when GuiDocument.xml
is absent. Emit its native XML view-state schema; geometry remains untouched.
Only standard properties are written, so no custom view provider is required.
"""
import math
from pathlib import Path
import zipfile
import xml.etree.ElementTree as ET
import FreeCAD as App


def write_view_state(path,shape):
    path=Path(path)
    with zipfile.ZipFile(path) as archive:
        contents={name:archive.read(name) for name in archive.namelist()}
    data=ET.fromstring(contents['Document.xml'])
    objects=data.findall('./ObjectData/Object')
    root=ET.Element('Document',SchemaVersion='1',HasExpansion='1')
    ET.SubElement(root,'Expand')
    providers=ET.SubElement(root,'ViewProviderData',Count=str(len(objects)))
    for obj in objects:
        visible='false'
        for prop in obj.findall('./Properties/Property'):
            if prop.get('name')=='Visibility':visible=prop.find('Bool').get('value')
        view=ET.SubElement(providers,'ViewProvider',name=obj.get('name'),expanded='0')
        props=ET.SubElement(view,'Properties',Count='1',TransientCount='0')
        prop=ET.SubElement(props,'Property',name='Visibility',type='App::PropertyBool',status='1')
        ET.SubElement(prop,'Bool',value=visible)
    box=shape.optimalBoundingBox()
    radius=math.sqrt(box.XLength**2+box.YLength**2+box.ZLength**2)/2
    if not math.isfinite(radius) or radius<=0 or radius>1e6:raise ValueError('Cannot frame an empty or unbounded shape')
    centre=box.Center
    rotation=App.Rotation(App.Vector(.74290609,.30772209,.59447283),math.degrees(1.2171158))
    position=centre+rotation.multVec(App.Vector(0,0,3*radius))
    settings=('OrthographicCamera {\n viewportMapping ADJUST_CAMERA\n'
              f' position {position.x} {position.y} {position.z}\n'
              ' orientation 0.74290609 0.30772209 0.59447283 1.2171158\n'
              f' nearDistance 0.01\n farDistance {10*radius}\n aspectRatio 1\n'
              f' focalDistance {3*radius}\n height {2.3*radius}\n}}\n')
    ET.SubElement(root,'Camera',settings=settings)
    contents['GuiDocument.xml']=ET.tostring(root,encoding='utf-8',xml_declaration=True)
    temporary=path.with_suffix('.view-state.tmp')
    with zipfile.ZipFile(temporary,'w',compression=zipfile.ZIP_DEFLATED) as archive:
        for name,content in contents.items():archive.writestr(name,content)
    temporary.replace(path)
