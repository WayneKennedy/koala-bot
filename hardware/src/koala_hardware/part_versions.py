# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Per-part version ledger: `part-versions.json` pairs every printed design's
declared `version` with a geometric fingerprint of its current solid.

    uv run python -m koala_hardware.part_versions            # check: exit 1 and say what to do
    uv run python -m koala_hardware.part_versions --update   # record the current versions and fingerprints

Rule (AGENTS.md): when a part's geometry changes, bump `version` in its spec and
run `--update`, with a one-line `note` of what changed and why. A geometry
change without a bump fails `tests/test_part_versions.py`. A `proven` tag and
every test-log entry name the version that was printed; a bump resets the
part to `unknown` unless the change is recorded as cosmetic there.
"""
import json,sys,datetime,pathlib
from . import params as P
from .parts import all_builders, links as L

ROOT=pathlib.Path(__file__).resolve().parents[2]
MANIFEST=ROOT/'part-versions.json'
OPTION_BUILDERS=[L.option_thigh_frame,L.option_thigh_split_body,L.option_thigh_split_cheek,L.option_thigh_flat,L.option_shank_flush]


def fingerprint(part):
    bb=part.bounding_box()   # extents, not bounds: a rigid shift of a part's frame is not a design change
    return {'volume_mm3':round(part.volume,2),
            'extents':[round(v,1) for v in (bb.max.X-bb.min.X,bb.max.Y-bb.min.Y,bb.max.Z-bb.min.Z)],   # 0.1 mm: rigid-shift float noise is not a change
            'faces':len(part.faces()),'edges':len(part.edges())}


def current():
    out={}
    for b in list(all_builders())+OPTION_BUILDERS:
        s=b();out[s['name']]={'version':int(s.get('version',1)),'fingerprint':fingerprint(s['part'])}
    return out


def load():
    saved=json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}
    for entry in saved.values():   # 2026-09-19 schema change: absolute bounds -> placement-invariant extents
        fp=entry.get('fingerprint',{})
        if 'bbox' in fp:
            b=fp.pop('bbox');fp['extents']=[round(b[3]-b[0],1),round(b[4]-b[1],1),round(b[5]-b[2],1)]
            fp.update({'volume_mm3':fp.pop('volume_mm3'),'extents':fp.pop('extents'),'faces':fp.pop('faces'),'edges':fp.pop('edges')})
        elif 'extents' in fp:fp['extents']=[round(v,1) for v in fp['extents']]
    return saved


def same(a,b):
    """Fingerprints agree within tolerance: volume 0.5 mm3, extents 0.15 mm (one rounding step of float noise), face and edge counts exact."""
    return (abs(a['volume_mm3']-b['volume_mm3'])<=0.5 and all(abs(x-y)<=0.15 for x,y in zip(a["extents"],b["extents"]))
            and a['faces']==b['faces'] and a['edges']==b['edges'])


def check(now=None,saved=None):
    """Return a list of problems (empty when the ledger matches the code)."""
    now=now or current();saved=saved or load();problems=[]
    for name,c in now.items():
        s=saved.get(name)
        if s is None:problems.append(f'{name}: not in part-versions.json — run --update (new part starts at v{c["version"]})');continue
        if c['version']<s['version']:problems.append(f'{name}: code says v{c["version"]} but the ledger has v{s["version"]}: versions never go down')
        elif c['version']==s['version'] and not same(c['fingerprint'],s['fingerprint']):
            problems.append(f'{name}: geometry changed at v{c["version"]} — bump `version` in its spec and run --update with a note')
        elif c['version']>s['version']:problems.append(f'{name}: bumped to v{c["version"]} in code — run --update with a note')
    for name in saved:
        if name not in now:problems.append(f'{name}: in the ledger but no builder produces it')
    return problems


def update(note=''):
    saved=load();now=current();today=datetime.date.today().isoformat()
    for name,c in now.items():
        s=saved.get(name,{})
        if s.get('version')!=c['version'] or not s or not same(s['fingerprint'],c['fingerprint']):
            hist=s.get('history',[])
            if s and s.get('version')==c['version'] and not same(s['fingerprint'],c['fingerprint']):
                raise SystemExit(f'{name}: geometry changed without a version bump; bump it first')
            hist.append({'version':c['version'],'date':today,'note':note or ('initial ledger' if not s else '')})
            saved[name]={'version':c['version'],'since':today,'fingerprint':c['fingerprint'],'history':hist}
    for name in [n for n in saved if n not in now]:del saved[name]
    MANIFEST.write_text(json.dumps(dict(sorted(saved.items())),indent=1)+'\n')
    print('part-versions.json:',len(saved),'parts')


if __name__=='__main__':
    if '--update' in sys.argv:
        i=sys.argv.index('--update');update(sys.argv[i+1] if len(sys.argv)>i+1 else '')
    else:
        p=check()
        for line in p:print(line)
        print('part versions OK' if not p else f'{len(p)} problem(s)');sys.exit(1 if p else 0)
