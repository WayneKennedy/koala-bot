# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Document blocked paired-root ear screws and the upstream split-socket reference.

Study only: no production geometry, BOM or viewer changes. Derived upstream
STEP/STL assets retain Apache-2.0 licensing; source shapes are not resized.
"""
from pathlib import Path
import hashlib,json,tempfile,shutil
from build123d import import_step,export_step,Plane,mirror,Pos
from . import params as P,servo_iface as S
from .parts import pelvis
from .audit import overlap
from .meshing import export_mesh

ROOT=Path(__file__).resolve().parents[2]
SOURCES={'Under_arm_SO101':'677a1a57efeddc439d97ebdc309b1c2853cfcb83f14c7d695c312fcf13a89713',
         'Motor_holder_SO101_Wrist':'e58d86502535a5a4936677e9d934f1bda9417e83f7480f475061728c146739c4'}


def write(out):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    originals={}
    for name,sha in SOURCES.items():
        path=ROOT/'vendor/so-arm100/SO101'/f'{name}.step'
        assert hashlib.sha256(path.read_bytes()).hexdigest()==sha,name
        originals[name]=import_step(path)
    # Keep the complete wrist socket and a short connection stub; no resizing.
    cradle=originals['Under_arm_SO101'] & S._box(-100,-24.85,-100,100,-100,100)
    holder=originals['Motor_holder_SO101_Wrist']
    result={'upstream_commit':'eecbe3e0a9ebb23e25ad7b2759b03884c6660903',
            'source_sha256':SOURCES,'under_arm_crop_native_X_max_mm':-24.85,
            'reference_frame':'original upstream coordinates; both source files already share placement',
            'derived_geometry_license':'Apache-2.0','templates':{},
            'pitch_centres_mm':2*P.ROOT_PITCH_Y,
            'minimum_saddle_gap_mm':2*(P.ROOT_PITCH_Y-P.SOCKET_CASE_X/2-P.SOCKET_CLEAR-P.SOCKET_WALL),
            'driver_probe_diameter_mm':P.SOCKET_M2_HEAD,'driver_probe_length_mm':40,
            'blocked_inboard_ear_screws':[]}
    for name,part in [('under_socket_source',cradle),('wrist_holder_source',holder)]:
        assert part.is_valid and len(part.solids())==1
        if name=='wrist_holder_source':
            # The complete holder is unchanged: retain original STEP bytes.
            shutil.copyfile(ROOT/'vendor/so-arm100/SO101/Motor_holder_SO101_Wrist.step',out/f'{name}.step')
        else:
            export_step(part,out/f'{name}.step')
        mesh=export_mesh(part,out/f'{name}.stl')
        restored=import_step(out/f'{name}.step')
        error=abs(restored.volume-part.volume)/part.volume
        assert restored.is_valid and len(restored.solids())==1 and error<1e-5
        assert max(abs(a-b) for a,b in zip(restored.bounding_box().size,part.bounding_box().size))<1e-5
        result['templates'][name]={'volume_mm3':part.volume,'size_mm':list(part.bounding_box().size),
                                  'watertight_STL':mesh.is_watertight,'STEP_reimport_relative_volume_error':error}
    for front in (False,True):
        tf=pelvis.pitch_socket(front);mount=pelvis.solid(front)
        opposite=mirror(tf*S.socket_reference(),Plane.XZ)
        for side in ('right','left'):
            for y in (-P.SOCKET_LUG_Y,P.SOCKET_LUG_Y):
                start=S.ear_face('idler')-P.SOCKET_M2_SEAT
                probe=tf*S._x_hole(start-40,start,y,P.SOCKET_LUG_BACK_Z,P.SOCKET_M2_HEAD)
                sibling=opposite
                if side=='left':probe=mirror(probe,Plane.XZ);sibling=mirror(sibling,Plane.XZ)
                hit=overlap(probe,sibling);plastic=overlap(probe,mount)
                assert hit>0 and plastic>0
                result['blocked_inboard_ear_screws'].append({'root':'shoulder' if front else 'hip',
                    'side':side,'ear_lateral_mm':y,'opposite_servo_overlap_mm3':round(hit,4),
                    'crossmember_overlap_mm3':round(plastic,4)})
    result['limits']='40 mm straight-driver access screen on paired fixed roots; no offset tool, installation trajectory, revised mount or physical assembly acceptance.'
    result['upstream_cradle_holder_overlap_mm3']=overlap(cradle,holder)
    (out/'root-access-study.json').write_text(json.dumps(result,indent=2)+'\n')
    with tempfile.TemporaryDirectory() as td:
        td=Path(td)
        def panel(ax,items,title):
            meshes=[]
            for i,(part,colour) in enumerate(items):
                mesh=export_mesh(part,td/f'{i}.stl');meshes.append(mesh)
                ax.add_collection3d(Poly3DCollection(mesh.triangles,facecolors=colour,edgecolors=None,linewidths=0,shade=True))
            import numpy as np
            lo=np.min([m.bounds[0] for m in meshes],axis=0);hi=np.max([m.bounds[1] for m in meshes],axis=0)
            c=(lo+hi)/2;r=max(hi-lo)*.6
            ax.set_xlim(c[0]-r,c[0]+r);ax.set_ylim(c[1]-r,c[1]+r);ax.set_zlim(c[2]-r,c[2]+r)
            ax.set_box_aspect((1,1,1));ax.view_init(elev=28,azim=-20);ax.set_axis_off();ax.set_title(title,fontsize=11)
        fig=plt.figure(figsize=(13,6),layout='constrained')
        panel(fig.add_subplot(1,2,1,projection='3d'),[(cradle,'#71aeb3'),(holder,'#deac79')],
              'SO-101 wrist socket + holder\nOriginal source placement')
        panel(fig.add_subplot(1,2,2,projection='3d'),[(cradle,'#71aeb3'),(Pos(-40,0,0)*holder,'#deac79')],
              'Separated for inspection\nBlue: cradle · tan: removable holder')
        fig.suptitle('SO-101 two-piece socket construction reference',fontsize=16)
        fig.supxlabel('Exact source surfaces. Separation illustrates the components, not a checked insertion path. Root-mount adaptation still required.',fontsize=10)
        fig.savefig(out/'split-socket-reference.png',dpi=160);plt.close(fig)
    print('PASS two source extracts; all eight inboard screw approaches blocked by sibling servo; study:',out)


if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',default='../docs/design/so101')
    write(ap.parse_args().output)
