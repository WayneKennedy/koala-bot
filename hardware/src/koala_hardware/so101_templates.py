# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Extract unchanged SO-101 socket/fork reference geometry; not production parts.

Derived STEP/STL assets retain upstream Apache-2.0 licensing. Crop planes
only isolate features; they are not proposed structural seams in a robot.
"""
from pathlib import Path
from functools import lru_cache
import hashlib
import json
import numpy as np
from build123d import import_step, export_step, Pos, Rot, Plane, GeomType
from . import servo_iface as S, printability as PR
from .meshing import export_mesh

ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/'vendor/so-arm100/SO101/Upper_arm_SO101.step'
SOURCE_SHA='efa19a6dd2ccb459248500c76629cfa840630e7e15d9e146394d31da1525dd61'
UPSTREAM_COMMIT='eecbe3e0a9ebb23e25ad7b2759b03884c6660903'
# Native STEP landmarks, measured from planar/cylindrical faces.
SOCKET_SIDE_CENTRE=-47.4849891178812
SOCKET_AXIS_MID=-.9   # midway between widest inner walls -18.3 and +16.5
SOCKET_FLOOR=4.8
HORN_X=65.0849891178812
HORN_Y=12.0
SOCKET_CUT_X=-28.0
FORK_CUT_X=10.0


@lru_cache
def source():
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==SOURCE_SHA,'SO-101 source changed; remeasure datums'
    return import_step(SOURCE)


def socket_template():
    """X output axis, Y case width, Z Bottom→Top; floor contact at Z=0.

    Retains upstream dimensions and all enclosing walls, reliefs and holes.
    It is NOT the current koala pocket: see measured differences in the report.
    """
    part=source() & S._box(-100,SOCKET_CUT_X,-100,100,-100,100)
    tf=Plane(origin=(-SOCKET_AXIS_MID,-SOCKET_SIDE_CENTRE,-SOCKET_FLOOR),
             x_dir=(0,1,0),z_dir=(1,0,0)).location
    return tf*part


def fork_template():
    """X output axis, Z towards link root; horn centre origin, inner faces ±18.2."""
    part=source() & S._box(FORK_CUT_X,100,-100,100,-100,100)
    tf=Plane(origin=(0,-HORN_Y,HORN_X),x_dir=(0,0,-1),z_dir=(1,0,0)).location
    return tf*part


def show(ax,mesh,title,heat=False):
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    mesh=mesh.copy();mesh.apply_translation(-mesh.bounds[0])
    colours=np.tile(np.array([.48,.72,.70,1]),(len(mesh.faces),1))
    if heat:
        down=(mesh.face_normals[:,2]<-np.cos(np.pi/4)) & (mesh.triangles[:,:,2].max(axis=1)>.05)
        colours[down]=[.90,.38,.24,1]
    poly=Poly3DCollection(mesh.triangles,facecolors=colours,linewidths=0,shade=True,edgecolors=None)
    ax.add_collection3d(poly)
    size=mesh.extents;centre=size/2;r=max(size)*.55
    ax.set_xlim(centre[0]-r,centre[0]+r);ax.set_ylim(centre[1]-r,centre[1]+r);ax.set_zlim(centre[2]-r,centre[2]+r)
    ax.set_box_aspect((1,1,1));ax.view_init(elev=32,azim=-55);ax.set_axis_off();ax.set_title(title,fontsize=10,pad=0)


def slot_measurements(part,plane_x):
    """Measure the actual planar recess faces in the normalized socket frame."""
    slots={}
    for face in part.faces():
        if face.geom_type!=GeomType.PLANE:continue
        c=face.center()
        if abs(abs(c.X)-plane_x)<1e-5 and abs(face.normal_at().X)>.99:
            bb=face.bounding_box()
            slots['drive' if c.X>0 else 'idler']={
                'plane_x_mm':c.X,'width_mm':bb.size.Y,
                'start_z_mm':bb.min.Z,'end_z_mm':bb.max.Z}
    assert set(slots)=={'drive','idler'}
    return slots


def write_slot_views(out):
    """Wall elevations of the current unequal slots, with pinned-source evidence."""
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle,Circle
    from . import params as P
    source_slots=slot_measurements(socket_template(),17.4)
    current=slot_measurements(S.saddle(),P.SOCKET_CASE_X/2)
    fig,axes=plt.subplots(1,2,figsize=(11,6),layout='constrained')
    for ax,side in zip(axes,('drive','idler')):
        d=current[side];w=d['width_mm'];z=d['start_z_mm']
        for key in ('width_mm','start_z_mm'):
            assert abs(d[key]-source_slots[side][key])<1e-5
        half=P.SOCKET_CASE_Y/2+2
        ax.add_patch(Rectangle((-half,-P.SOCKET_SHELF),2*half,P.SOCKET_DEPTH+P.SOCKET_SHELF,
                               facecolor='#8fb4d9',edgecolor='#284754'))
        ax.add_patch(Rectangle((-w/2,z),w,P.SOCKET_DEPTH-z,facecolor='white',edgecolor='#284754'))
        hole_z=P.SOCKET_LUG_DRIVE_Z if side=='drive' else P.SOCKET_LUG_BACK_Z
        for y in (-P.SOCKET_LUG_Y,P.SOCKET_LUG_Y):
            ax.add_patch(Circle((y,hole_z),P.SOCKET_M2_CLEAR/2,facecolor='white',edgecolor='#284754'))
        ax.axhline(0,color='#73848d',linestyle='--',linewidth=.8)
        ax.annotate('',xy=(-w/2,21),xytext=(w/2,21),arrowprops=dict(arrowstyle='<->'))
        ax.text(0,22,f'{w:g} mm slot',ha='center',fontsize=13)
        ax.text(0,z+(P.SOCKET_DEPTH-z)/2,'Recess to widest\ncase plane',ha='center',va='center',fontsize=10)
        ax.set_title(f'{side.upper()} face\nSlot begins {z:g} mm above floor',fontsize=14)
        ax.set_xlim(-19,19);ax.set_ylim(-7,26);ax.set_aspect('equal')
        ax.set_xlabel('Case width Y (mm)');ax.set_ylabel('Height from servo Bottom Z (mm)')
    fig.suptitle('DEC-50 · Different drive / idler socket profiles',fontsize=18)
    fig.supxlabel('Pocket-facing wall elevations; through-bores shown, outer counterbores omitted.\n'
                  'Slot widths/starts match pinned SO-101 Upper arm. Koala retains 34.9 × 24.7 mm pocket and 17 mm capture.\n'
                  'The continuous seat below the idler slot supports its low ear screws. Fit/load acceptance remains physical.',fontsize=10)
    for ext in ('png','svg'):fig.savefig(out/f'socket-slot-comparison.{ext}',dpi=160)
    plt.close(fig)
    (out/'socket-slots.json').write_text(json.dumps({'source':str(SOURCE.relative_to(ROOT.parent)),
        'sha256':SOURCE_SHA,'source_slots':source_slots,'koala_slots':current,
        'case_envelope_note':'Drive raised plane in supplied case STEP reaches Z=25.5444; fallback covers to 25.55. No new caliper measurement.'},indent=2)+'\n')
    return source_slots


def write(out):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import tempfile
    from .parts import all_builders, links as L
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    source_slots=write_slot_views(out)
    with tempfile.TemporaryDirectory() as td:
        td=Path(td)
        items={'upper_socket_source':socket_template(),'upper_fork_source':fork_template()}
        data={'source':str(SOURCE.relative_to(ROOT.parent)),'source_sha256':SOURCE_SHA,
              'upstream_commit':UPSTREAM_COMMIT,'derived_assets_license':'Apache-2.0',
              'source_crop_planes_X_mm':{'socket_max':SOCKET_CUT_X,'fork_min':FORK_CUT_X},
              'socket_datum_source_xyz':[SOCKET_SIDE_CENTRE,SOCKET_FLOOR,SOCKET_AXIS_MID],
              'fork_datum_source_xyz':[HORN_X,HORN_Y,0],
              'templates':{},'current_parts':[]}
        for name,part in items.items():
            assert part.is_valid and len(part.solids())==1,name
            export_step(part,out/(name+'.step'))
            mesh=export_mesh(part,out/(name+'.stl'))
            restored=import_step(out/(name+'.step'))
            relative_error=abs(restored.volume-part.volume)/part.volume
            assert restored.is_valid and len(restored.solids())==1,name
            # STEP round-trip integration noise is ~5e-8 relative here.
            assert relative_error<1e-6,(name,relative_error)
            assert max(abs(a-b) for a,b in zip(restored.bounding_box().size,part.bounding_box().size))<1e-5
            data['templates'][name]={'size_mm':list(part.bounding_box().size),'volume_mm3':part.volume,
                'valid_single_solid':True,'watertight_STL':mesh.is_watertight,
                'STEP_reimport_relative_volume_error':relative_error}
        # Same print-bed convention in every panel: Z is up.
        # Upstream's native Y=0 is the continuous flat bed face.
        upstream=export_mesh(Rot(X=90)*source(),td/'whole.stl')
        socket=export_mesh(socket_template(),td/'socket.stl')
        forks=export_mesh(Rot(X=-90)*fork_template(),td/'fork.stl')
        current_socket=export_mesh(S.saddle(),td/'current-socket.stl')
        current_fork=export_mesh(Rot(Y=90)*L.clevis(),td/'current-fork.stl')
        data['upstream_print_orientation']={'native_build_direction':'+Y',**PR.metrics(upstream)}
        data['upstream_features']={'main_outer_fillet_radius_mm':5,'local_end_radius_mm':2,
            'fork_tip_radius_mm':12,'horn_contact_span_mm':36.4,'fork_outer_span_mm':63.4,
            'pocket_widest_planes_source_Z_mm':[-18.3,16.5], 'pocket_across_axis_mm':34.8,
            'pocket_side_planes_source_X_mm':[-59.8849891178812,-35.0849891178812],
            'pocket_width_mm':24.8,'floor_thickness_mm':4.8,'highest_wall_above_floor_mm':19.7,
            'ear_planes_source_Z_mm':[-16.4,15.4],'normalized_socket_slots':source_slots}
        fig=plt.figure(figsize=(16,10),layout='constrained')
        panels=[(upstream,'SO-101 upper arm\nFlat back on bed · both axes horizontal'),
                (socket,'Extracted enclosed socket\nOriginal walls, reliefs and screw seats'),
                (forks,'Extracted fork + root web\nOriginal broad roots and rounded outline'),
                (current_socket,'DEC-49/50 koala socket\nEnclosing Side returns; measured ear seats'),
                (current_fork,'DEC-49/50 koala fork\nTapered rounded roots; local supports'),
                (export_mesh(Rot(X=90)*L.upper_link(85),td/'thigh.stl'),'DEC-49/50 85 mm thigh\nOrthogonal axes; tapered transition')]
        for i,(mesh,title) in enumerate(panels,1):show(fig.add_subplot(2,3,i,projection='3d'),mesh,title,True)
        fig.suptitle('SO-101 construction reference versus current koala parts',fontsize=17)
        fig.supxlabel('Each panel independently scaled. Orange: downward surface screen, not a support or strength verdict. Print evidence is recorded separately; nothing physically printed.',fontsize=10)
        fig.savefig(out/'template-comparison.png',dpi=150);plt.close(fig)
        # Complete structural review inventory, including coupons in JSON.
        structural=[]
        for builder in all_builders():
            d=builder();mesh=export_mesh(d['orientation']*d['part'],td/(d['name']+'.stl'))
            m=PR.metrics(mesh)
            row={'name':d['name'],'qty':d.get('qty',1)*(2 if d.get('handed') else 1),
                 'declared_orientation_metrics':m,'principal_orientation_screen':PR.best_orientations(mesh),
                 'notes':d.get('notes',''),'printable':d.get('printable','unknown'),'material':d.get('material','PETG')}
            data['current_parts'].append(row)
            if not d['name'].startswith('coupon'):structural.append((mesh,d['name'],m))
        fig=plt.figure(figsize=(15,16),layout='constrained')
        for i,(mesh,name,m) in enumerate(structural,1):
            show(fig.add_subplot(4,3,i,projection='3d'),mesh,
                 f'{name}\n{m["size"][0]:.0f} × {m["size"][1]:.0f} mm bed footprint; {m["overhang_area"]:.0f} mm² flagged',True)
        fig.suptitle('DEC-49/50 parts — assumed printable in declared orientations',fontsize=17)
        fig.supxlabel('Orange: downward surface screen. Sizes use declared orientation; views independently scaled. See part review for structural and aesthetic findings.',fontsize=10)
        fig.savefig(out/'current-parts-review.png',dpi=150);plt.close(fig)
        (out/'template-study.json').write_text(json.dumps(data,indent=2)+'\n')
    print('PASS pinned source, two valid connected STEP templates, closed meshes and current part inventory:',out)


if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',default='../docs/design/so101')
    write(ap.parse_args().output)
