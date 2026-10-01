# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Rejected removal-only trials, not released print revisions.

Run from repo root: hardware/freecad-run docs/design/flat-link-removal/removal_study.py
Uses the immutable conversion benchmark; writes paired native study documents,
multiview PNGs and geometric strength-screen metrics alongside this script.
No production geometry or existing GUI documents are changed.
"""
from pathlib import Path
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
SOURCE = '3c52315ce49d97f40a771f66ae916768eb8f4695231bf536658e58c5a67ac477'
for name in list(sys.modules):
    if name == 'koala_hardware' or name.startswith('koala_hardware.'):
        del sys.modules[name]
sys.path.insert(0, str(REPO/'hardware/freecad/sources'/SOURCE))
import FreeCAD as App
from koala_hardware.parts import front as F
from koala_hardware import params as P, servo_iface as S
from koala_hardware.cad import Rot
from koala_hardware.meshing import export_mesh
from koala_hardware.printability import metrics
from koala_hardware.render_views import views_png
from koala_hardware.freecad_document import make_document
from koala_hardware.freecad_build import save_checked


def stem_section(shape, z):
    thickness = .1
    section = (shape & S._box(-40,40,-30,30,z-thickness/2,z+thickness/2)).fc
    assert len(section.Solids)==1
    section=section.Solids[0]
    area = section.Volume/thickness
    inertia = section.MatrixOfInertia
    ix = inertia.A11/thickness-area*thickness**2/12
    iy = inertia.A22/thickness-area*thickness**2/12
    bb = section.BoundBox
    cy = section.CenterOfMass.y
    cx = section.CenterOfMass.x
    return dict(area_mm2=area, Ix_mm4=ix, Iy_mm4=iy,
                Zx_mm3=ix/max(bb.YMax-cy,cy-bb.YMin),
                Zy_mm3=iy/max(bb.XMax-cx,cx-bb.XMin))


def main():
    rows=[]
    for length in (90,100):
        baseline=F.forearm(length)
        before=stem_section(baseline,length-20)
        for depth in (16.,):
            trial=baseline & S._box(-40,40,-depth/2,depth/2,-20,120)
            after=stem_section(trial,length-20)
            added=(trial-baseline).volume
            assert added<1e-5 and trial.is_valid and len(trial.solids())==1
            name=f'removal_trial_L{length}_D{int(depth)}'
            doc,final=make_document(name,trial,dict(
                Status='REJECTED STUDY: trims horn recess rims; weaker stem sections',
                SourceBenchmark=SOURCE, SourceScript=Path(__file__).name))
            save_checked(doc,final,HERE/f'{name}.FCStd')
            if not App.GuiUp: App.closeDocument(doc.Name)
            mesh=export_mesh(Rot(X=90)*trial,REPO/'hardware/build'/f'{name}.stl')
            # Signed clearance to a 6.4 mm head recess at Y=+/-4.95.
            # Negative means the recess opens through the new outside plane.
            recess_margin=depth/2-(P.SERVO_DRIVE_SQ/2+P.SOCKET_HEAD_CLEAR/2)
            rows.append(dict(name=name, length_mm=length, depth_mm=depth,
                baseline_volume_mm3=baseline.volume, volume_mm3=trial.volume,
                added_volume_mm3=added, removed_volume_mm3=(baseline-trial).volume,
                head_recess_to_cut_plane_mm=recess_margin,
                section_z_mm=length-20, baseline_section=before, trial_section=after,
                section_ratios={k:after[k]/before[k] for k in before},
                print_screen=metrics(mesh), mesh_watertight=bool(mesh.is_watertight),
                status='REJECTED: not a strength-validated or released part'))
            if depth==16:
                # Native frame for inspection, print orientation only for metrics.
                display_mesh=export_mesh(trial,REPO/'hardware/build'/f'{name}-native.stl')
                views_png(name,display_mesh,HERE/f'{name}-views.png')
    report=dict(benchmark_commit='9e6ded8',source_snapshot=SOURCE,
        generator_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        scope='Geometric section comparison only. Solid homogeneous beam section ratios '
              'are not FFF part strength, a material model, FEA, or a safety factor. '
              'No load test or printed material calibration has been performed.', trials=rows)
    (HERE/'strength-screen.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2),flush=True)

if __name__=='__main__':main()
