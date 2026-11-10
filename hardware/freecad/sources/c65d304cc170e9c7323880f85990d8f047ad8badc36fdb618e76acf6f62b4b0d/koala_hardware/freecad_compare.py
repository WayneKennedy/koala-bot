# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Compare migrated solids with the captured pre-migration BREP baseline.

Boolean differences alone can report an entire solid when coincident curved
faces confuse the kernel. Report them alongside volume, bounds and two-sided
surface samples. Samples do not prove continuous surface equivalence.
"""
import argparse
import hashlib
import json
from pathlib import Path
import FreeCAD as App
import Part
from .parts import all_builders
from .part_versions import OPTION_BUILDERS


def skin_distance(a,b):
    maximum=0.;count=0;seen=set()
    fractions=(.5,) if len(a.Faces)>300 else (.2,.5,.8)
    for face in a.Faces:
        u0,u1,v0,v1=face.ParameterRange
        points=[] if len(a.Faces)>300 else [v.Point for v in face.Vertexes]
        points += [face.valueAt(u0+(u1-u0)*u,v0+(v1-v0)*v)
                   for u in fractions for v in fractions]
        for point in points:
            key=tuple(round(x,7) for x in point)
            if key in seen:continue
            seen.add(key)
            vertex=Part.Vertex(point)
            # Ignore UV samples outside a trimmed face (holes and trimmed arcs).
            if face.distToShape(vertex)[0]>1e-6:continue
            count+=1;maximum=max(maximum,vertex.distToShape(b)[0])
    return {'samples':count,'max_distance_mm':maximum}


def compare(a,b):
    bounds=('XMin','XMax','YMin','YMax','ZMin','ZMax')
    return {'old_volume_mm3':a.Volume,'native_volume_mm3':b.Volume,
            'volume_delta_mm3':b.Volume-a.Volume,
            'removed_boolean_mm3':a.cut(b).Volume,'added_boolean_mm3':b.cut(a).Volume,
            'old_solids':len(a.Solids),'native_solids':len(b.Solids),
            'valid':b.isValid(),
            'max_bounds_delta_mm':max(abs(getattr(a.optimalBoundingBox(),k)-getattr(b.optimalBoundingBox(),k)) for k in bounds),
            'old_to_native':skin_distance(a,b),'native_to_old':skin_distance(b,a)}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--only',help='Compare only this design and retain other report entries')
    parser.add_argument('--legacy-commit',required=True,help='Git commit from which the baseline was captured')
    args=parser.parse_args()
    old=json.loads((args.baseline/'parts.json').read_text())
    report={'freecad_version':'.'.join(App.Version()[:3]),'occt_version':Part.OCC_VERSION,
            'legacy_git_commit':args.legacy_commit,
            'scope':'Current designs and five versioned study designs, native right-hand frames. Surface samples are not a continuous proof.',
            'parts':{}}
    if args.only and args.output.exists():report=json.loads(args.output.read_text())
    for builder in list(all_builders())+OPTION_BUILDERS:
        spec=builder()
        if args.only and spec['name']!=args.only:continue
        path=args.baseline/(spec['name']+'.brep')
        previous=Part.Shape();previous.read(str(path))
        result=compare(previous,spec['part'].fc)
        result.update(old_version=old[spec['name']]['version'],native_version=spec.get('version',1),
                      baseline_sha256=hashlib.sha256(path.read_bytes()).hexdigest())
        report['parts'][spec['name']]=result
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(report,indent=2)+'\n')
        print(spec['name'],max(result['old_to_native']['max_distance_mm'],result['native_to_old']['max_distance_mm']),flush=True)

if __name__=='__main__':main()
