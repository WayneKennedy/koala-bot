# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Create inspectable, recomputable native FreeCAD feature histories.

The construction tree uses the Part workbench (including Sketcher profiles),
which supports the existing intersected solids and multi-solid coupons. It is
not a PartDesign Body; use Part features when extending it interactively.
"""
import math
import FreeCAD as App
import Part
import Sketcher


def _sketch(doc, shape):
    """Editable, fully constrained planar profile, including arcs and text curves."""
    face=shape.Faces[0]
    normal=face.normalAt(*[sum(face.ParameterRange[i:i+2])/2 for i in (0,2)])
    origin=face.Vertexes[0].Point if face.Vertexes else face.CenterOfMass
    placement=App.Placement(origin,App.Rotation(App.Vector(0,0,1),normal))
    local=shape.copy();local.Placement=placement.inverse().multiply(local.Placement)
    obj=doc.addObject('Sketcher::SketchObject','Profile')
    obj.Placement=placement
    for edge in local.Edges:
        if edge.Degenerated:continue
        curve=edge.Curve
        if isinstance(curve,Part.Line):geometry=Part.LineSegment(edge.Vertexes[0].Point,edge.Vertexes[-1].Point)
        elif isinstance(curve,Part.Circle):
            geometry=curve if edge.isClosed() else Part.ArcOfCircle(curve,edge.FirstParameter,edge.LastParameter)
        elif isinstance(curve,Part.Ellipse):
            geometry=curve if edge.isClosed() else Part.ArcOfEllipse(curve,edge.FirstParameter,edge.LastParameter)
        else:
            geometry=curve.toBSpline() if isinstance(curve,Part.BezierCurve) else curve.copy()
            geometry.segment(edge.FirstParameter,edge.LastParameter)
        index=obj.addGeometry(geometry,False)
        obj.addConstraint(Sketcher.Constraint('Block',index))
    return obj


def _edge_signature(e):
    return (e.Length,e.CenterOfMass,sorted((tuple(v.Point) for v in e.Vertexes)))


def _matching_edges(expected, actual, indices):
    """Select by geometry after recompute, never assume stable edge numbering."""
    result=[]
    for index in indices:
        e=expected.Edges[index-1]
        matches=[i for i,a in enumerate(actual.Edges,1)
                 if abs(e.Length-a.Length)<1e-5 and (e.CenterOfMass-a.CenterOfMass).Length<1e-5
                 and len(e.Vertexes)==len(a.Vertexes)
                 and all(any((v.Point-w.Point).Length<1e-5 for w in a.Vertexes) for v in e.Vertexes)]
        if len(matches)!=1:raise ValueError(f'Fillet edge match is not unique: {matches}; length={e.Length}, centre={e.CenterOfMass}; nearest={sorted([(abs(e.Length-a.Length)+(e.CenterOfMass-a.CenterOfMass).Length, a.Length, tuple(a.CenterOfMass)) for a in actual.Edges])[:3]}')
        result.append(matches[0])
    return result


class History:
    def __init__(self,doc):self.doc=doc;self.cache={}
    def add(self,shape):
        key=id(shape)
        if key in self.cache:return self.cache[key]
        recipe=shape.recipe
        if recipe is None:raise ValueError('Generated solid has no native feature history')
        kind=recipe[0];d=self.doc
        if kind in ('Box','Cylinder','Cone','Sphere'):
            obj=d.addObject('Part::'+kind,kind)
            for name,value in recipe[1].items():setattr(obj,name,float(value))
            obj.Placement=recipe[2]
        elif kind=='Profile':obj=_sketch(d,shape.fc)
        elif kind=='Vertex':
            obj=d.addObject('PartDesign::Point','LoftVertex')
            obj.Placement.Base=App.Vector(*recipe[1])
        elif kind in ('Fuse','Cut','Common'):
            a,b=self.add(recipe[1]),self.add(recipe[2])
            obj=d.addObject('Part::'+kind,kind);obj.Base=a;obj.Tool=b;obj.Refine=True
        elif kind=='Placement':
            source=self.add(recipe[1]);obj=d.addObject('App::Link','Placed')
            obj.setLink(source);obj.LinkTransform=True;obj.LinkPlacement=recipe[2]
        elif kind=='Mirroring':
            source=self.add(recipe[1])
            if source.TypeId=='App::Link':
                placed=d.addObject('Part::Compound','MirrorInput');placed.Links=[source];source=placed
            obj=d.addObject('Part::Mirroring','Mirrored')
            obj.Source=source;obj.Base=App.Vector(*recipe[2]);obj.Normal=App.Vector(*recipe[3])
        elif kind=='Extrusion':
            source=self.add(recipe[1]);obj=d.addObject('Part::Extrusion','Extrusion')
            obj.Base=source;obj.DirMode='Custom';obj.Dir=App.Vector(*recipe[2])
            obj.LengthFwd=recipe[3];obj.LengthRev=recipe[3] if recipe[4] else 0
            obj.Solid=True
        elif kind=='Loft':
            sections=[self.add(s) for s in recipe[1]]
            obj=d.addObject('Part::Loft','Loft');obj.Sections=sections;obj.Solid=True;obj.Ruled=recipe[2]
        elif kind=='Fillet':
            source=self.add(recipe[1]);d.recompute()
            indices=_matching_edges(recipe[1].fc,source.Shape,recipe[2])
            obj=d.addObject('Part::Fillet','Fillet');obj.Base=source
            obj.Edges=[(i,recipe[3],recipe[3]) for i in indices]
        elif kind=='Compound':
            children=[self.add(s) for s in recipe[1]]
            obj=d.addObject('Part::Compound','Components');obj.Links=children
        elif kind=='Subshape':
            source=self.add(recipe[1]);obj=d.addObject('App::Link','Selected')
            obj.setLink(source,recipe[2]);obj.LinkTransform=True
        elif kind=='Reference':
            # External supplier geometry has no recoverable authoring tree.
            obj=d.addObject('Part::Feature','SupplierReference');obj.Shape=shape.fc
            obj.addProperty('App::PropertyString','SourceFile','Provenance');obj.SourceFile=recipe[1]
        else:raise ValueError(f'Unsupported feature: {kind}')
        if shape.label:obj.Label=shape.label
        self.cache[key]=obj
        return obj


def validate_document(doc, final, expected=None, solids=1):
    doc.recompute()
    bad=[]
    for obj in doc.Objects:
        if not obj.isValid() or 'Invalid' in obj.State:bad.append(f'{obj.Name}: {obj.getStatusString()}')
        if obj.TypeId=='Sketcher::SketchObject':
            if obj.DoF:bad.append(f'{obj.Name}: {obj.DoF} unconstrained DoF')
            for key in ('RedundantConstraints','ConflictingConstraints','MalformedConstraints','PartiallyRedundantConstraints'):
                if getattr(obj,key):bad.append(f'{obj.Name}: {key}')
    s=final.Shape
    if s.isNull() or not s.isValid() or len(s.Solids)!=solids:bad.append('Final shape: invalid or wrong solid count')
    if expected is not None and not s.isNull():
        # Volume difference is supplemented by two-sided sampled skin distances in
        # the migration report. Here catch failed/reoriented feature recreation.
        delta=abs(s.Volume-expected.Volume)
        if delta>max(.01,abs(expected.Volume)*1e-7):bad.append(f'Feature tree volume differs by {delta} mm3')
        for key in ('XMin','XMax','YMin','YMax','ZMin','ZMax'):
            if abs(getattr(s.optimalBoundingBox(False),key)-getattr(expected.optimalBoundingBox(False),key))>1e-5:bad.append('Feature tree bounds differ: '+key)
    if bad:raise ValueError('\n'.join(bad))


def make_document(name,shape,metadata=None):
    doc=App.newDocument(name)
    try:
        final=History(doc).add(shape)
        final.Label=name
        for key,value in (metadata or {}).items():
            final.addProperty('App::PropertyString',key,'Koala')
            setattr(final,key,str(value));final.setEditorMode(key,1)
        validate_document(doc,final,shape.fc,len(shape.solids()))
        for obj in doc.Objects:obj.Visibility=False
        final.Visibility=True
        if App.GuiUp:
            import FreeCADGui as Gui
            final.ViewObject.ShapeColor=(.56,.71,.85)
            Gui.activeDocument().activeView().viewAxonometric();Gui.activeDocument().activeView().fitAll()
        return doc,final
    except BaseException:
        App.closeDocument(doc.Name);raise


def recomputed_part(part):
    """Evaluate a recipe through native features before downstream CAD checks.

    OCCT fillet corner solutions can differ after upstream sketch/boolean
    reconstruction despite near-identical input volumes. The native tree is
    authoritative: return its evaluated solid with the same editable recipe.
    Never substitute an imported/baked feature in the released history.
    """
    from .cad import Part as CADPart
    previous=App.ActiveDocument
    doc=App.newDocument('NativeEvaluation')
    try:
        final=History(doc).add(part)
        validate_document(doc,final,solids=len(part.solids()))
        return CADPart(final.Shape.copy(),part.recipe,part.label)
    finally:
        App.closeDocument(doc.Name)
        if previous:App.setActiveDocument(previous.Name)
