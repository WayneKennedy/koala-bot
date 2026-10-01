# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Original stepped front lower link in the collision review's 120 degree pose.

Run: hardware/freecad-run docs/design/flat-link-removal/original_elbow_120.py
Uses frozen benchmark sources; no production or open GUI documents are edited.
"""
from pathlib import Path
import hashlib
import json
import sys

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[2]
SOURCE='3c52315ce49d97f40a771f66ae916768eb8f4695231bf536658e58c5a67ac477'
for name in list(sys.modules):
    if name=='koala_hardware' or name.startswith('koala_hardware.'):
        del sys.modules[name]
sys.path.insert(0,str(REPO/'hardware/freecad/sources'/SOURCE))
import FreeCAD as App
from koala_hardware.parts import front as F
from koala_hardware import params as P
from koala_hardware.cad import Pos,Rot,Compound
from koala_hardware.freecad_document import make_document
from koala_hardware.freecad_build import save_checked


def main():
    upper=F.upper_arm()
    lower=F.forearm()
    rows=[]
    for angle in (110,115,120):
        moving=Pos(0,0,P.BODY_UPPER_ARM_MM)*Rot(X=angle)*lower
        hit=upper.fc.common(moving.fc)
        rows.append(dict(angle_deg=angle,overlap_mm3=hit.Volume,
                         minimum_separation_mm=upper.fc.distToShape(moving.fc)[0]))
    upper.label='Original upper arm v2'
    moving.label='Original stepped forearm v2 — 120 deg'
    scene=Compound(children=[upper,moving])
    doc,final=make_document('OriginalElbow120',scene,dict(
        Status='Benchmark geometry, 120 degree front elbow inspection pose',
        SourceBenchmark=SOURCE,ElbowAngleDeg=120,LowerLinkReachMm=100))
    save_checked(doc,final,HERE/'original_elbow_120.FCStd')
    if not App.GuiUp:App.closeDocument(doc.Name)
    report=dict(benchmark_commit='9e6ded8',source_snapshot=SOURCE,
                generator_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                lower_link='forearm v2, 100 mm',upper_link='upper_arm v2, 70 mm',
                transform='Translate Z=70 mm * Rotate X=angle; same as collision review',
                scope='Plastic lower link vs printed upper-arm cup only; exact static poses, not a full travel or loaded validation.',
                samples=rows)
    (HERE/'original-elbow-clearance.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2),flush=True)

if __name__=='__main__':main()
