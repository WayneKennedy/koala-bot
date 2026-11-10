# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Record the current rounded-family geometry and print-face screen.

Run after visual review. This measures geometry, not FFF strength or adhesion.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import tempfile
from .cad import GeomType
from .parts import all_builders
from .meshing import export_mesh
from .printability import metrics


def main(output):
    report={'scope':'Current production designs; coupons omitted. Native solid and closed-mesh checks, analytic cylindrical radii and declared print-face metrics. No physical validation.','parts':{}}
    with tempfile.TemporaryDirectory() as td:
        for builder in all_builders():
            spec=builder();name=spec['name'];part=spec['part']
            if name.startswith('coupon_'):continue
            mesh=export_mesh(spec['orientation']*part,Path(td)/(name+'.stl'))
            radii=Counter(round(f.fc.Surface.Radius,6) for f in part.faces() if f.geom_type==GeomType.CYLINDER)
            assert part.is_valid and len(part.solids())==1,name
            report['parts'][name]={'version':spec.get('version',1),'printability':spec['printable'],
                'valid':True,'solids':1,'volume_mm3':part.volume,'watertight_mesh':mesh.is_watertight,
                'cylindrical_face_radius_counts':dict(sorted(radii.items())),
                'print_face_screen':metrics(mesh)}
            print('PASS rounded-family',name,spec.get('version',1),flush=True)
    package=Path(__file__).resolve().parent
    report['source_sha256']={str(p.relative_to(package)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(package.rglob('*.py'))}
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(report,indent=2)+'\n')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=Path(__file__).resolve().parents[3]/'docs/design/rounded-family/geometry.json')
    main(parser.parse_args().output)
