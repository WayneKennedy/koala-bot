# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Guard declared print versions against unrecorded geometry changes.

    uv run python -m koala_hardware.part_versions
    uv run python -m koala_hardware.part_versions --update "what changed and why"

Fingerprints include each face's position relative to the part bounds, so moving
holes within an unchanged outer envelope is a design change; translating the
whole part is not. Rotation changes the declared part/print frame and is not
normalised. The descriptors are a tolerance-based change detector, not a proof
of B-rep equivalence: positions/perimeters within 0.005 mm and face areas within
0.005 mm² can compare equal.

Legacy fingerprints cannot establish that internal features are unchanged.
Migrate them explicitly with --migrate-baseline PATH, supplying a JSON object
{"source_revision": "<full git commit>", "parts": current()} generated using
this fingerprint implementation against that historical, unmodified CAD source.
Migration records that baseline, never the current working geometry; run the
normal version check/update afterwards. Do not generate the baseline from edits
being approved. Geometry changes still require version bumps (AGENTS.md).
"""
import argparse
import datetime
import json
import os
import pathlib
import tempfile

from build123d import CenterOf
from .parts import all_builders, links as L

ROOT = pathlib.Path(__file__).resolve().parents[2]
MANIFEST = ROOT / 'part-versions.json'
FINGERPRINT_SCHEMA = 2
OPTION_BUILDERS = [L.option_thigh_frame, L.option_thigh_split_body,
                   L.option_thigh_split_cheek, L.option_thigh_flat, L.option_shank_flush]


def fingerprint(part):
    """Deterministic face descriptors in the part's translation-free frame."""
    bb = part.bounding_box()
    origin = bb.min
    descriptors = []
    for face in part.faces():
        fb = face.bounding_box()
        points = (face.center(CenterOf.MASS) - origin,
                  fb.min - origin, fb.max - origin)
        descriptors.append([face.geom_type.name, round(face.area, 4),
                            *[round(v, 4) for point in points for v in point],
                            round(sum(edge.length for edge in face.edges()), 4)])
    return {
        'schema': FINGERPRINT_SCHEMA,
        'volume_mm3': round(part.volume, 2),
        'extents': [round(v, 1) for v in bb.size],
        'faces': len(part.faces()),
        'edges': len(part.edges()),
        'face_geometry': sorted(descriptors),
    }


def current():
    out = {}
    for builder in list(all_builders()) + OPTION_BUILDERS:
        spec = builder()
        out[spec['name']] = {'version': int(spec.get('version', 1)),
                             'fingerprint': fingerprint(spec['part'])}
    return out


def load():
    return json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}


def _legacy_same(a, b):
    """Only for checking an explicitly supplied historical migration baseline."""
    def extents(fp):
        if 'extents' in fp:
            return fp['extents']
        box = fp['bbox']
        return [box[i + 3] - box[i] for i in range(3)]

    return (abs(a['volume_mm3'] - b['volume_mm3']) <= 0.5
            and all(abs(x - y) <= 0.15 for x, y in zip(extents(a), extents(b)))
            and a['faces'] == b['faces'] and a['edges'] == b['edges'])


def _has_geometry(fp):
    return (fp.get('schema') == FINGERPRINT_SCHEMA
            and len(fp.get('face_geometry', [])) == fp.get('faces'))


def same(a, b):
    """Compare unordered face geometry with tolerances, independent of edge order.

    The old aggregate checks remain a fast screen. Matching face descriptors
    rather than hashing rounded values avoids false changes at rounding borders
    and changes to the kernel's face enumeration order.
    """
    if not (_has_geometry(a) and _has_geometry(b) and _legacy_same(a, b)):
        return False
    remaining = list(b['face_geometry'])
    for face in a['face_geometry']:
        for index, candidate in enumerate(remaining):
            if (face[0] == candidate[0] and len(face) == len(candidate)
                    and all(abs(x - y) <= 0.005
                            for x, y in zip(face[1:], candidate[1:]))):
                del remaining[index]
                break
        else:
            return False
    return not remaining


def check(now=None, saved=None):
    """Return problems without silently upgrading a legacy fingerprint."""
    now = current() if now is None else now
    saved = load() if saved is None else saved
    problems = []
    for name, entry in now.items():
        old = saved.get(name)
        if old is None:
            problems.append(f'{name}: not in part-versions.json — run --update (new part starts at v{entry["version"]})')
            continue
        if entry['version'] < old['version']:
            problems.append(f'{name}: code says v{entry["version"]} but the ledger has v{old["version"]}: versions never go down')
        elif not _has_geometry(old['fingerprint']):
            problems.append(f'{name}: legacy fingerprint — migrate an unchanged historical baseline with --migrate-baseline before updating')
        elif entry['version'] == old['version'] and not same(entry['fingerprint'], old['fingerprint']):
            problems.append(f'{name}: geometry changed at v{entry["version"]} — bump `version` in its spec and run --update with a note')
        elif entry['version'] > old['version']:
            problems.append(f'{name}: bumped to v{entry["version"]} in code — run --update with a note')
    for name in saved:
        if name not in now:
            problems.append(f'{name}: in the ledger but no builder produces it')
    return problems


def _write(saved):
    """Replace the ledger only after every entry has passed validation."""
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', dir=MANIFEST.parent,
                                         prefix='.part-versions-', delete=False) as stream:
            temporary = pathlib.Path(stream.name)
            stream.write(json.dumps(dict(sorted(saved.items())), indent=1) + '\n')
        os.replace(temporary, MANIFEST)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    print('part-versions.json:', len(saved), 'parts')


def migrate_baseline(path):
    """Upgrade a ledger using explicitly identified, pre-edit CAD geometry."""
    saved = load()
    snapshot = json.loads(pathlib.Path(path).read_text())
    revision = snapshot.get('source_revision', '')
    baseline = snapshot.get('parts', {})
    if len(revision) != 40 or any(c not in '0123456789abcdef' for c in revision):
        raise SystemExit('baseline must identify its full source_revision git commit')
    if set(baseline) != set(saved):
        raise SystemExit('baseline parts must exactly match the existing ledger')
    for name, old in saved.items():
        source = baseline[name]
        if (source['version'] != old['version']
                or not _has_geometry(source['fingerprint'])
                or not _legacy_same(source['fingerprint'], old['fingerprint'])
                or (_has_geometry(old['fingerprint'])
                    and not same(source['fingerprint'], old['fingerprint']))):
            raise SystemExit(f'{name}: historical baseline does not match the recorded version/geometry')
    for name, old in saved.items():
        if not _has_geometry(old['fingerprint']):
            old['fingerprint'] = baseline[name]['fingerprint']
            old.setdefault('fingerprint_migrations', []).append({
                'schema': FINGERPRINT_SCHEMA,
                'date': datetime.date.today().isoformat(),
                'source_revision': revision,
            })
    _write(saved)


def update(note=''):
    saved = load()
    now = current()
    # Prevalidate everything before modifying history or opening the output file.
    for name, entry in now.items():
        old = saved.get(name)
        if old is None:
            continue
        if entry['version'] < old['version']:
            raise SystemExit(f'{name}: v{entry["version"]} is below recorded v{old["version"]}; versions never go down')
        if not _has_geometry(old['fingerprint']):
            raise SystemExit(f'{name}: legacy fingerprint; use --migrate-baseline from unmodified historical CAD first')
        if entry['version'] == old['version'] and not same(old['fingerprint'], entry['fingerprint']):
            raise SystemExit(f'{name}: geometry changed without a version bump; bump it first')
    changed = [name for name, entry in now.items()
               if name not in saved or entry['version'] != saved[name]['version']]
    if (changed or set(saved) - set(now)) and not note.strip():
        raise SystemExit('--update requires a note explaining what changed and why')
    today = datetime.date.today().isoformat()
    for name in changed:
        entry = now[name]
        old = saved.get(name, {})
        history = list(old.get('history', []))
        history.append({'version': entry['version'], 'date': today, 'note': note.strip()})
        saved[name] = {**old, 'version': entry['version'], 'since': today,
                       'fingerprint': entry['fingerprint'], 'history': history}
    for name in set(saved) - set(now):
        del saved[name]
    _write(saved)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group()
    action.add_argument('--update', metavar='NOTE')
    action.add_argument('--migrate-baseline', type=pathlib.Path, metavar='PATH')
    args = parser.parse_args()
    if args.update is not None:
        update(args.update)
    elif args.migrate_baseline is not None:
        migrate_baseline(args.migrate_baseline)
    else:
        problems = check()
        for line in problems:
            print(line)
        print('part versions OK' if not problems else f'{len(problems)} problem(s)')
        raise SystemExit(1 if problems else 0)
