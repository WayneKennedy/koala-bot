# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Koala's small algebraic modelling vocabulary, implemented by FreeCAD.

Shapes are evaluated with FreeCAD's Part kernel and retain an operation DAG.
`freecad_document.History` replays that DAG as native FreeCAD primitives, sketches,
extrusions, lofts, booleans, fillets, mirrors and placement links. No build123d
or OCP runtime is used. The vocabulary preserves the established part datums.
"""
from enum import Enum, auto
import math
from pathlib import Path
import FreeCAD as App
import Part as FC


class Align(Enum):
    MIN = auto()
    CENTER = auto()
    MAX = auto()
    NONE = auto()


class GeomType(Enum):
    LINE = auto()
    CIRCLE = auto()
    ELLIPSE = auto()
    BSPLINE = auto()
    BEZIER = auto()
    PLANE = auto()
    CYLINDER = auto()
    CONE = auto()
    SPHERE = auto()
    TORUS = auto()
    EXTRUSION = auto()
    OTHER = auto()


class CenterOf(Enum):
    MASS = auto()
    GEOMETRY = auto()
    BOUNDING_BOX = auto()


class Vector:
    def __init__(self, *args):
        if len(args) == 1:
            a = args[0]
            self.fc = App.Vector(a.fc if isinstance(a, Vector) else a) if isinstance(a, (Vector, App.Vector)) else App.Vector(*a)
        else:
            self.fc = App.Vector(*args)
    X = property(lambda s: s.fc.x)
    Y = property(lambda s: s.fc.y)
    Z = property(lambda s: s.fc.z)
    x, y, z = X, Y, Z
    length = property(lambda s: s.fc.Length)
    def __iter__(self): return iter((self.X, self.Y, self.Z))
    def __getitem__(self, i): return tuple(self)[i]
    def __add__(self, b): return Vector(self.fc + Vector(b).fc)
    def __sub__(self, b): return Vector(self.fc - Vector(b).fc)
    def __mul__(self, b): return Vector(self.fc * b)
    __rmul__ = __mul__
    def __truediv__(self, b): return self * (1/b)
    def __neg__(self): return self * -1
    def dot(self, b): return self.fc.dot(Vector(b).fc)
    def cross(self, b): return Vector(self.fc.cross(Vector(b).fc))
    def normalized(self): return self/self.length
    def __repr__(self): return f'Vector{tuple(self)}'


class Axis:
    def __init__(self, origin=(0,0,0), direction=(0,0,1)):
        self.origin, self.direction = Vector(origin), Vector(direction).normalized()
Axis.X, Axis.Y, Axis.Z = Axis(direction=(1,0,0)), Axis(direction=(0,1,0)), Axis()


class Location:
    def __init__(self, position=(0,0,0), axis=None, angle=None, _placement=None):
        if _placement is not None:
            self.fc = _placement
        elif angle is not None:
            self.fc = App.Placement(Vector(position).fc, App.Rotation(Vector(axis).fc, angle))
        else:
            self.fc = App.Placement(Vector(position).fc, App.Rotation())
    position = property(lambda s: Vector(s.fc.Base))
    def inverse(self): return Location(_placement=self.fc.inverse())
    def __mul__(self, other):
        if isinstance(other, Location): return Location(_placement=self.fc.multiply(other.fc))
        if isinstance(other, Plane): return self*other.location
        if isinstance(other, (list, tuple)): return [self*x for x in other]
        shape = other.fc.copy()
        shape.Placement = self.fc.multiply(shape.Placement)
        return Part(shape, ('Placement', other, self.fc), label=other.label)
    def matrix(self):
        m=self.fc.toMatrix()
        return [[m.A[r*4+c] for c in range(4)] for r in range(4)]


def Pos(*args, **kwargs):
    return Location(args[0] if len(args)==1 else args or (kwargs.get('X',0),kwargs.get('Y',0),kwargs.get('Z',0)))


def Rot(*args, X=0, Y=0, Z=0):
    if args:
        values=args[0] if len(args)==1 and isinstance(args[0],(tuple,list)) else args
        X,Y,Z=tuple(values)+(0,)*(3-len(values))
    # Original datums use intrinsic XYZ: Rx * Ry * Rz.
    r=App.Rotation(App.Vector(1,0,0),X).multiply(App.Rotation(App.Vector(0,1,0),Y)).multiply(App.Rotation(App.Vector(0,0,1),Z))
    return Location(_placement=App.Placement(App.Vector(),r))


class Plane:
    def __init__(self, origin=(0,0,0), x_dir=None, z_dir=(0,0,1)):
        z=Vector(z_dir).normalized()
        if x_dir is None:
            x_dir=(1,0,0) if abs(z.X)<.99 else (0,1,0)
        x=Vector(x_dir).normalized(); y=z.cross(x).normalized(); x=y.cross(z)
        self.origin,self.z_dir=Vector(origin),z
        self.location=Location(_placement=App.Placement(Vector(origin).fc,App.Rotation(x.fc,y.fc,z.fc,'ZXY')))
    def __mul__(self, other): return self.location*other
    def offset(self, distance): return Plane(self.origin+self.z_dir*distance, self.location.fc.Rotation.multVec(App.Vector(1,0,0)), self.z_dir)
Plane.XY=Plane()
Plane.XZ=Plane(x_dir=(1,0,0),z_dir=(0,-1,0))
Plane.YZ=Plane(x_dir=(0,1,0),z_dir=(1,0,0))


class Bounds:
    def __init__(self, bb):
        self.min=Vector(bb.XMin,bb.YMin,bb.ZMin)
        self.max=Vector(bb.XMax,bb.YMax,bb.ZMax)
        self.size=self.max-self.min
    def center(self): return (self.min+self.max)/2


class ShapeList(list):
    def filter_by(self, criterion):
        if isinstance(criterion, Axis):
            return ShapeList(e for e in self if e.geom_type==GeomType.LINE and abs((e.position_at(1)-e.position_at(0)).normalized().dot(criterion.direction))>1-1e-7)
        return ShapeList(e for e in self if e.geom_type==criterion)
    def sort_by(self, axis): return ShapeList(sorted(self,key=lambda e:e.center().dot(axis.direction)))


class Part:
    def __init__(self, shape=None, recipe=None, label=''):
        self.fc=shape if shape is not None else FC.Shape()
        self.recipe=recipe
        self.label=label
        self.parent=None
        self.children=[]
    volume=property(lambda s: 0.0 if s.fc.isNull() else abs(s.fc.Volume))
    area=property(lambda s: 0.0 if s.fc.isNull() else s.fc.Area)
    length=property(lambda s: s.fc.Length)
    is_valid=property(lambda s: not s.fc.isNull() and s.fc.isValid())
    X=property(lambda s:s.fc.Point.x)
    Y=property(lambda s:s.fc.Point.y)
    Z=property(lambda s:s.fc.Point.z)
    def __bool__(self): return not self.fc.isNull()
    def __hash__(self): return self.fc.hashCode()
    def __eq__(self,b): return isinstance(b,Part) and self.fc.isSame(b.fc)
    def _binary(self,b,kind):
        if not self: return b if kind=='Fuse' else Part()
        if not b: return self if kind!='Common' else Part()
        try:
            raw={'Fuse':self.fc.fuse,'Cut':self.fc.cut,'Common':self.fc.common}[kind](b.fc)
            shape=raw.removeSplitter() if raw.Solids else raw
            return Part(shape,(kind,self,b))
        except Exception as e: raise ValueError(f'{kind}: {e}') from e
    def __add__(self,b): return self._binary(b,'Fuse')
    def __radd__(self,b): return self if b==0 else NotImplemented
    def __sub__(self,b): return self._binary(b,'Cut')
    def __and__(self,b): return self._binary(b,'Common')
    def _subshapes(self,kind):
        out=ShapeList()
        for i,raw in enumerate(getattr(self.fc,kind)):
            if kind=='Edges' and raw.Degenerated:continue
            p=Part(raw,('Subshape',self,{'Edges':'Edge','Faces':'Face','Vertexes':'Vertex','Solids':'Solid'}[kind]+str(i+1)))
            p.parent=self; out.append(p)
        return out
    def edges(self): return self._subshapes('Edges')
    def faces(self): return self._subshapes('Faces')
    def vertices(self): return self._subshapes('Vertexes')
    def solids(self): return self._subshapes('Solids') if self else ShapeList()
    def bounding_box(self, optimal=True): return Bounds(self.fc.optimalBoundingBox() if optimal else self.fc.BoundBox)
    def center(self, kind=CenterOf.GEOMETRY):
        if kind==CenterOf.BOUNDING_BOX:return self.bounding_box().center()
        if self.fc.ShapeType=='Vertex':return Vector(self.fc.Point)
        if kind==CenterOf.MASS and self.fc.ShapeType!='Compound':return Vector(self.fc.CenterOfMass)
        if self.fc.ShapeType=='Edge':return self.position_at(.5)
        if self.fc.ShapeType=='Face':
            u0,u1,v0,v1=self.fc.ParameterRange
            return Vector(self.fc.valueAt((u0+u1)/2,(v0+v1)/2))
        if self.fc.ShapeType=='Compound':
            solids=self.fc.Solids
            return Vector(sum((s.CenterOfMass*s.Volume for s in solids),App.Vector())/sum(s.Volume for s in solids))
        return Vector(self.fc.CenterOfMass)
    def position_at(self,t):
        return Vector(self.fc.valueAt(self.fc.FirstParameter+t*(self.fc.LastParameter-self.fc.FirstParameter)))
    def normal_at(self,point=None):
        if point is None:
            a,b,c,d=self.fc.ParameterRange; u,v=(a+b)/2,(c+d)/2
        else:u,v=self.fc.Surface.parameter(Vector(point).fc)
        return Vector(self.fc.normalAt(u,v))
    def is_inside(self,point): return self.fc.isInside(Vector(point).fc,1e-6,True)
    def distance_to(self,other): return self.fc.distToShape(other.fc)[0]
    def moved(self,loc): return loc*self
    def fillet(self,radius,edges):
        try:
            raw=self.fc.makeFillet(radius,[e.fc for e in edges])
            if not raw.isValid(): raise ValueError('invalid fillet')
            ids=[next(i for i,x in enumerate(self.fc.Edges,1) if x.isSame(e.fc)) for e in edges]
            return Part(raw,('Fillet',self,ids,radius))
        except Exception as e: raise ValueError(f'fillet R{radius}: {e}') from e
    def fillet_2d(self,radius,vertices):
        # Planar straight-sided profiles: exact tangent line/arc construction.
        points=[e.Vertexes[0].Point for e in self.fc.OuterWire.OrderedEdges]
        # OrderedVertexes respects edge orientation (Edges does not).
        points=[v.Point for v in self.fc.OuterWire.OrderedVertexes]
        selected=[v.fc.Point for v in vertices]
        corners=[]
        for i,p in enumerate(points):
            if not any((p-v).Length<1e-7 for v in selected):
                corners.append((p,p,None));continue
            a=(points[i-1]-p).normalize();b=(points[(i+1)%len(points)]-p).normalize()
            half=a.getAngle(b)/2
            t=radius/math.tan(half)
            centre=p+(a+b).normalize()*(radius/math.sin(half))
            middle=centre+(p-centre).normalize()*radius
            corners.append((p+a*t,p+b*t,middle))
        edges=[]
        for i,(start,end,middle) in enumerate(corners):
            previous=corners[i-1][1]
            edges.append(FC.makeLine(previous,start))
            if middle is not None:edges.append(FC.Arc(start,middle,end).toShape())
        raw=FC.Face(FC.Wire(edges))
        return Part(raw,('Profile',))
    def clean(self): return Part(self.fc.removeSplitter(),self.recipe)
    def clean_mesh(self): self.fc=self.fc.cleaned()
    @property
    def matrix_of_inertia(self):
        if self.fc.ShapeType!='Compound':
            m=self.fc.MatrixOfInertia
            return [[m.A[r*4+c] for c in range(3)] for r in range(3)]
        centre=self.center(CenterOf.MASS)
        result=[[0. for c in range(3)] for r in range(3)]
        for solid in self.fc.Solids:
            delta=Vector(solid.CenterOfMass)-centre;m=solid.MatrixOfInertia
            for r in range(3):
                for c in range(3):
                    result[r][c]+=m.A[r*4+c]+solid.Volume*((delta.dot(delta) if r==c else 0)-delta[r]*delta[c])
        return result
    @property
    def geom_type(self):
        try: raw=getattr(self.fc,'Curve',None) if self.fc.ShapeType=='Edge' else getattr(self.fc,'Surface',None)
        except TypeError: return GeomType.OTHER
        name=type(raw).__name__.upper().replace('SURFACE','')
        if name in ('LINE','LINESEGMENT'):return GeomType.LINE
        if name=='TOROID':return GeomType.TORUS
        if name=='OFEXTRUSION':return GeomType.EXTRUSION
        if 'BSPLINE' in name:return GeomType.BSPLINE
        if 'BEZIER' in name:return GeomType.BEZIER
        return GeomType.__members__.get(name,GeomType.OTHER)
Solid=Part


def _aligned(shape, align):
    if align is None:return shape
    if not isinstance(align,tuple):align=(align,)*3
    b=shape.BoundBox;lo=(b.XMin,b.YMin,b.ZMin);hi=(b.XMax,b.YMax,b.ZMax)
    shift=[-a if k==Align.MIN else -b if k==Align.MAX else -(a+b)/2 if k==Align.CENTER else 0 for a,b,k in zip(lo,hi,align)]
    shape.translate(App.Vector(*(shift+[0]*(3-len(shift)))))
    return shape


def _primitive(kind,shape,properties,align):
    shape=_aligned(shape,align)
    return Part(shape,(kind,properties,shape.Placement))


def Box(length,width,height,align=(Align.CENTER,)*3):
    return _primitive('Box',FC.makeBox(length,width,height),dict(Length=length,Width=width,Height=height),align)

def Cylinder(radius,height,align=(Align.CENTER,)*3):
    return _primitive('Cylinder',FC.makeCylinder(radius,height),dict(Radius=radius,Height=height),align)

def Cone(radius1,radius2,height,align=(Align.CENTER,)*3):
    return _primitive('Cone',FC.makeCone(radius1,radius2,height),dict(Radius1=radius1,Radius2=radius2,Height=height),align)

def Sphere(radius,align=(Align.CENTER,)*3):
    return _primitive('Sphere',FC.makeSphere(radius),dict(Radius=radius,Angle1=-90.,Angle2=90.,Angle3=360.),align)

def Vertex(*args): return Part(FC.Vertex(Vector(*args).fc),('Vertex',tuple(Vector(*args))))

def Polygon(*points,align=None,rotation=0):
    if len(points)==1:points=points[0]
    vs=[App.Vector(*p) for p in points]
    shape=FC.Face(FC.makePolygon(vs+[vs[0]]))
    shape=_aligned(shape,align)
    if rotation:shape.rotate(App.Vector(),App.Vector(0,0,1),rotation)
    return Part(shape,('Profile',))

def Rectangle(width,height):return Polygon((-width/2,-height/2),(width/2,-height/2),(width/2,height/2),(-width/2,height/2))

def RectangleRounded(width,height,radius):
    face=Rectangle(width,height)
    return face.fillet_2d(radius,face.vertices())

def Circle(radius):return Part(FC.Face(FC.Wire([FC.makeCircle(radius)])),('Profile',))

def RegularPolygon(radius,side_count,rotation=0):
    return Polygon(*[(radius*math.cos(math.radians(rotation)+2*math.pi*i/side_count),radius*math.sin(math.radians(rotation)+2*math.pi*i/side_count)) for i in range(side_count)])

def extrude(profile,amount,both=False):
    normal=profile.faces()[0].normal_at().fc
    base=profile.fc.copy()
    if both:base.translate(normal*(-amount))
    shape=base.extrude(normal*amount*(2 if both else 1))
    return Part(shape,('Extrusion',profile,tuple(normal),amount,both))

def loft(sections,ruled=False):
    if len(sections)==2 and all(s.fc.ShapeType!='Vertex' for s in sections):
        a,b=sections
        delta=b.fc.CenterOfMass-a.fc.CenterOfMass
        if delta.Length>1e-8 and len(a.fc.Edges)==len(b.fc.Edges) and len(a.fc.Vertexes)==len(b.fc.Vertexes) and abs(a.area-b.area)<1e-7 and all(any((v.Point+delta-w.Point).Length<1e-7 for w in b.fc.Vertexes) for v in a.fc.Vertexes):
            normal=delta/delta.Length
            return Part(a.fc.extrude(delta),('Extrusion',a,tuple(normal),delta.Length,False))
    ruled = ruled or (len(sections)==2 and all(s.fc.ShapeType!='Vertex' and all(e.geom_type==GeomType.LINE for e in s.edges()) for s in sections))
    wires=[s.fc if s.fc.ShapeType=='Vertex' else s.fc.Wires[0] for s in sections]
    return Part(FC.makeLoft(wires,True,ruled).removeSplitter(),('Loft',sections,ruled))

def fillet(edges,radius):
    edges=list(edges)
    if not edges:raise ValueError('No edges selected for fillet')
    return edges[0].parent.fillet(radius,edges)

def mirror(shape,about=Plane.XZ):
    raw=shape.fc.copy(); raw=raw.mirror(about.origin.fc,about.z_dir.fc)
    return Part(raw,('Mirroring',shape,tuple(about.origin),tuple(about.z_dir)))

def Compound(children):
    result=Part(FC.makeCompound([s.fc for s in children]),('Compound',list(children)))
    result.children=list(children)
    return result

def section(shape,section_by=Plane.XY):
    face=section_by*Rectangle(10000,10000)
    return Part(shape.fc.section(face.fc))

def import_step(path):
    # Import with labels for the optional supplier case and licensed references.
    import Import
    doc=App.newDocument('ReferenceImport')
    try:
        Import.insert(str(path),doc.Name)
        objects=[o for o in doc.Objects if hasattr(o,'Shape') and not o.Shape.isNull() and o.Shape.Solids and not o.OutList]
        children=[]
        for o in objects:
            shape=o.Shape.copy()
            shape.Placement=o.getGlobalPlacement().multiply(o.Placement.inverse()).multiply(shape.Placement)
            children.append(Part(shape,('Reference',str(path),o.Label),o.Label))
        return Compound(children)
    finally:App.closeDocument(doc.Name)

def export_step(shape,path):
    doc=App.newDocument('StepExport')
    try:
        objects=[]
        for item in shape.children or [shape]:
            obj=doc.addObject('Part::Feature','Export');obj.Label=item.label or 'Solid';obj.Shape=item.fc;objects.append(obj)
        import Import
        Import.export(objects,str(path))
    finally:App.closeDocument(doc.Name)

def export_brep(shape,path):shape.fc.exportBrep(str(path))

def export_stl(shape,path,tolerance=.001,angular_tolerance=.1,**kwargs):
    import MeshPart
    mesh=MeshPart.meshFromShape(Shape=shape.fc,LinearDeflection=tolerance,AngularDeflection=angular_tolerance,Relative=False)
    mesh.write(str(path))


def Text(txt,font_size,font='DejaVu Sans'):
    from .engraving import GLYPHS
    if txt not in GLYPHS:
        raise ValueError(f'No canonical engraving profile for {txt!r}; add an explicit font-derived profile')
    edges=[]
    for kind,*values in GLYPHS[txt]:
        if kind=='L':edges.append(FC.makeLine(*(App.Vector(*p)*font_size for p in values)))
        else:
            curve=FC.BezierCurve();curve.setPoles([App.Vector(*p)*font_size for p in values[0]])
            edges.append(curve.toShape())
    wires=[FC.Wire(group) for group in FC.sortEdges(edges)]
    return Part(FC.makeFace(wires,'Part::FaceMakerBullseye'),('Profile',))
