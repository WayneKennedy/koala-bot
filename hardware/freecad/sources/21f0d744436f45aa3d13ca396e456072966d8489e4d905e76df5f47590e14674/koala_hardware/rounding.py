# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Exterior edge fillets, including circular fork rims, with material guards.

Interface guards describe bearing/contact material, not whole horn regions.
Radii of bores, structural roots and mating profiles are independent of style.
"""
import warnings
import Part as FC
from .cad import GeomType, Cylinder, Align, Pos
from . import params as P, servo_iface as S

REPORTS=[]


def horn_material():
    """Flat Ø20 contact face and Ø6 screw-bearing columns through the 3.5 mm web.

    The outer 2.8 mm counterbore lip may open into an exterior fillet, as on
    SO-101; the web beneath each screw remains intact. Native link frame.
    """
    def cyl(r,h):return Cylinder(r,h,align=(Align.CENTER,Align.CENTER,Align.MIN))
    face=cyl(P.SOCKET_HORN_DIA/2,.15)
    for x in (-P.SERVO_DRIVE_SQ/2,P.SERVO_DRIVE_SQ/2):
        for y in (-P.SERVO_DRIVE_SQ/2,P.SERVO_DRIVE_SQ/2):
            face+=Pos(x,y,0)*cyl(3,P.SOCKET_PLATE_T)
    axis=Pos(0,0,-P.SOCKET_AXIS_Z)
    return axis*S.plate_location('drive')*face+axis*S.plate_location('idler')*face


def exterior(part,radius=None,exclude=lambda p:False,select=lambda e:True,
             protect=None,native_inputs=True,label='exterior',grouped=False,verify_each=False):
    """Accumulate fillets on convex line/arc boundaries; never round hole rims.

    Reselect surviving portions geometrically after every successful operation.
    Failed groups split, preserving earlier successes. Report every surviving
    rejected edge for the design review; a kernel rejection is not approval of
    a sharp edge. Native recomputation and meshing must agree with the candidate.
    """
    from .freecad_document import recomputed_part
    from .meshing import closed_shape_mesh
    radius=P.FAMILY_EDGE_RADIUS if radius is None else radius
    if native_inputs:part=recomputed_part(part)
    before=part
    chosen=[];blocked=[]
    for e in part.edges():
        p=e.position_at(.5)
        if exclude(p) or not select(e):continue
        if e.geom_type not in (GeomType.LINE,GeomType.CIRCLE):continue
        # Small circles are screw/counterbore rims or existing tangent blends.
        if e.geom_type==GeomType.CIRCLE and e.fc.Curve.Radius<5:continue
        faces=[f for f in part.faces() if any(x.fc.isSame(e.fc) for x in f.edges())]
        if len(faces)!=2:continue
        n1,n2=[f.normal_at(p) for f in faces]
        if abs(n1.dot(n2))>.95 or part.is_inside(p+(n1+n2)*.1):continue
        # Reject a local corner cut before asking OCCT to build it. Besides
        # saving work, this avoids its crash on inner horn/neck arc junctions.
        offsets=[(.05,.5),(.5,.05),(.1,.1),(1.,1.)]
        hits=False
        if protect is not None:
            for a,b in offsets:
                q=p-n1*a-n2*b
                if (radius-a)**2+(radius-b)**2>radius**2 and part.is_inside(q) and protect.is_inside(q):
                    hits=True;break
        if hits:
            blocked.append({'centre_mm':list(p),'reason':f'local R{radius:g} corner intersects bearing/contact material'})
        else:chosen.append(e.fc.copy())

    def reselect(group):
        result=[]
        for e in part.edges():
            if e.geom_type not in (GeomType.LINE,GeomType.CIRCLE):continue
            points=[FC.Vertex(e.position_at(t).fc) for t in (.1,.5,.9)]
            if any(all(p.distToShape(old)[0]<1e-5 for p in points) for old in group):result.append(e)
        return result

    protected=before.fc.common(protect.fc) if protect is not None else None
    # OCCT follows tangent chains. Most parts need sequential long boundaries;
    # the thigh needs its frame corners solved together.
    todo=[chosen] if grouped else [[e] for e in sorted(chosen,key=lambda e:e.Length)]
    failed=[];accepted=0
    while todo:
        group=todo.pop();edges=reselect(group)
        if not edges:continue
        try:
            rounded=part.fillet(radius,edges)
            if verify_each:rounded=recomputed_part(rounded)
            if len(rounded.solids())!=len(part.solids()):raise ValueError('solid count changed')
            if protected is not None and protected.cut(rounded.fc).Volume>.001:
                raise ValueError('would remove protected bearing/contact material')
            if not closed_shape_mesh(rounded):raise ValueError('mesh is not closed')
            part=rounded;accepted+=len(edges)
        except ValueError as exc:
            if len(group)>1:todo.extend([group[len(group)//2:],group[:len(group)//2]])
            else:failed.append((group[0],str(exc)))
    evaluated=recomputed_part(part)
    delta=evaluated.volume-part.volume
    if native_inputs and abs(delta)>.01:raise ValueError('Native fillets differ from checked geometry')
    # Direct-input exceptions avoid an OCCT crash on reconstructed operands.
    # Their native tree is authoritative, with the same material/mesh guards;
    # record its numerical corner difference rather than checking another shape.
    if evaluated.volume>before.volume+.01:raise ValueError('Exterior rounding added volume')
    old,new=before.bounding_box(),evaluated.bounding_box()
    if any(a>b+1e-5 for a,b in zip(new.max,old.max)) or any(a<b-1e-5 for a,b in zip(new.min,old.min)):
        raise ValueError('Exterior rounding expanded the part envelope')
    if not closed_shape_mesh(evaluated):raise ValueError('Native fillet mesh is not closed')
    loss=protected.cut(evaluated.fc).Volume if protected is not None else 0.
    if loss>.001:raise ValueError('Native fillets remove protected interface material')
    rejected=[{'centre_mm':list(e.center()),'reason':reason}
              for old,reason in failed for e in reselect([old])]
    REPORTS.append(dict(label=label,radius_mm=radius,candidates=len(chosen),accepted_edges=accepted,
                        rejected=rejected+blocked,protected_loss_mm3=loss,direct_native_volume_delta_mm3=delta))
    if rejected:warnings.warn(f'{label}: {len(rejected)} R{radius:g} edges require exception review',RuntimeWarning)
    return evaluated
