# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Build revision-paired Python / FCStd deliverables with native feature histories.

Run with hardware/freecad-run -m koala_hardware.freecad_build. Each immutable
source snapshot is stored once; every part/assembly revision has its own replay
script beside its document. `--check` verifies hashes and fresh recomputation.
"""
import argparse
import hashlib
import importlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

import FreeCAD as App
from .cad import Compound, Plane, mirror
from .freecad_document import History, make_document, validate_document
from .parts import all_builders
from .part_versions import OPTION_BUILDERS

ROOT=Path(__file__).resolve().parents[2]
DEFAULT=ROOT/'freecad'


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def reference_inputs(repo,out):
    """External STEP inputs only; never recursively import our frozen archive."""
    for rel in subprocess.check_output(['git','ls-files','*.step','*.stp'],cwd=repo,text=True).splitlines():
        path=repo/rel
        if path.is_relative_to(DEFAULT) or path.is_relative_to(out):continue
        yield rel,path


def source_files():
    package=Path(__file__).resolve().parent
    return {str(p.relative_to(package.parent)):p for p in sorted(package.rglob('*.py'))}


def snapshot(out):
    files=source_files()
    digest=hashlib.sha256()
    for name,path in files.items():digest.update(name.encode()+b'\0'+path.read_bytes()+b'\0')
    revision=digest.hexdigest()
    folder=out/'sources'/revision
    for name,path in files.items():
        target=folder/name
        if target.exists():
            if target.read_bytes()!=path.read_bytes():raise ValueError('Immutable source snapshot was modified: '+str(target))
        else:target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(path,target)
    return revision


def specs():
    for builder in list(all_builders())+OPTION_BUILDERS:
        spec=builder()
        yield builder,spec


def replay_text(meta,source_revision):
    return f'''# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Rebuild this exact revision in FreeCAD; canonical Python dependencies are
in the immutable sources/{source_revision}/koala_hardware snapshot.
Run with hardware/freecad-run PATH or execute in FreeCAD's Python console:
    p = r"<absolute path to this file>"
    exec(compile(open(p).read(), p, "exec"), {{"__name__": "__main__", "__file__": p}})
The script creates a new document. It never closes an existing GUI document.
"""
from pathlib import Path
import sys

SOURCE_REVISION = {source_revision!r}
MODEL = {meta!r}

if __name__ == "__main__":
    here = Path(__file__).resolve()
    root = next(p for p in here.parents if (p / "sources" / SOURCE_REVISION).is_dir())
    # FreeCAD's interpreter persists between runs: load the archived revision,
    # not another revision's cached Python modules. Existing documents remain open.
    for name in list(sys.modules):
        if name == "koala_hardware" or name.startswith("koala_hardware."):
            del sys.modules[name]
    sys.path.insert(0, str(root / "sources" / SOURCE_REVISION))
    from koala_hardware.freecad_build import replay
    replay(here, MODEL, SOURCE_REVISION)
'''


def construct(meta,archive=None):
    kind=meta['kind']
    if kind=='part':
        module,name=meta['builder'].split(':');s=getattr(importlib.import_module(module),name)()
        shape=s['part']
        if meta.get('hand')=='left':shape=mirror(shape,Plane.XZ)
        return make_document(meta['name'],shape,{
            'PartVersion':s.get('version',1),'Material':s.get('material','PETG'),
            'Printability':s.get('printable','unknown'),'DesignNotes':s.get('notes',''),
            'SourceBuilder':meta['builder'],'Hand':meta.get('hand','none'),
            'SourceOfTruth':'Python; carry GUI edits back into the generator before rebuilding'})
    if kind=='assembly':
        from .assembly import nominal_details, bend_review_details
        d=App.newDocument(meta['name']);history=History(d);items=[]
        groups={}
        details=bend_review_details(meta['bend_review']) if meta.get('bend_review') else nominal_details(meta['pose'])
        for name,shape,colour,joint,side in details:
            obj=history.add(shape);obj.Label=name
            obj.addProperty('App::PropertyString','JointGroup','Koala');obj.JointGroup=joint
            obj.addProperty('App::PropertyString','Role','Koala');obj.Role='reference' if name.startswith('reference') else 'component'
            group_name='References' if name.startswith('reference') else 'PrintedAndDriveParts'
            if group_name not in groups:groups[group_name]=d.addObject('App::DocumentObjectGroup',group_name)
            groups[group_name].addObject(obj)
            if App.GuiUp:obj.ViewObject.ShapeColor=tuple(int(colour[i:i+2],16)/255 for i in (1,3,5))
            items.append((obj,shape))
        result=d.addObject('Part::Compound','Assembly');result.Links=[o for o,s in items]
        if meta.get('bend_review'):
            from .bend_limits import REVIEW_POSES
            result.addProperty('App::PropertyString','InspectionStatus','Koala')
            result.InspectionStatus='Suspended bend endpoint pose; hips/shoulders fixed. Unprinted; not a grounded or loaded stance.'
            result.addProperty('App::PropertyString','SignedBendDegrees','Koala')
            result.SignedBendDegrees=json.dumps(REVIEW_POSES[meta['bend_review']])
        validate_document(d,result,solids=sum(len(s.solids()) for o,s in items))
        for o in d.Objects:o.Visibility=False
        for o,s in items:o.Visibility=True
        for g in groups.values():g.Visibility=True
        result.Visibility=False
        d.recompute()
        return d,result
    if kind=='study':
        module,name=meta['builder'].split(':');shape=getattr(importlib.import_module(module),name)(**meta.get('arguments',{}))
        return make_document(meta['name'],shape,{'Status':'Historical design study; not a production part'})
    if kind=='reference':
        from .cad import import_step
        path=Path(meta['source'])
        if meta.get('archived_source'):
            if archive is None:
                archive=next((p for p in Path(__file__).resolve().parents if (p/'sources').is_dir()),DEFAULT)
            path=archive/meta['archived_source']
        elif not path.is_absolute():
            # Source snapshots are nested; locate the repository, not a sibling repo.
            repo=next(p for p in Path(__file__).resolve().parents if (p/'AGENTS.md').exists())
            path=repo/path
        if sha(path)!=meta['source_sha256']:raise ValueError('Reference source changed: '+str(path))
        shape=import_step(path)
        return make_document(meta['name'],shape,{'Status':'Frozen STEP reference; original authoring history unavailable','SourcePath':meta['source'],'SourceSHA256':meta['source_sha256']})
    raise ValueError('Unknown model kind: '+kind)


def save_checked(doc,final,target):
    """Stage, reopen, recompute and validate before publishing a document."""
    target.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.freecad-',dir=target.parent) as td:
        staged=Path(td)/target.name
        final_name=final.Name
        expected=final.Shape.copy();solids=len(expected.Solids)
        doc.saveAs(str(staged))
        from .freecad_view_state import write_view_state
        write_view_state(staged,expected)
        readback=Path(td)/('readback-'+target.name)
        shutil.copyfile(staged,readback)
        restored=App.openDocument(str(readback),True)
        try:
            for obj in restored.Objects:obj.touch()
            validate_document(restored,restored.getObject(final_name),expected,solids)
        finally:App.closeDocument(restored.Name)
        shutil.copyfile(staged,target)
    return final_name


def replay(script,meta,revision):
    archive=next(p for p in Path(script).resolve().parents if (p/'sources'/revision).is_dir())
    doc,final=construct(meta,archive)
    # Replays deliberately keep their new document unsaved in the GUI. The
    # original release and any human edits to it are never overwritten.
    doc.Label=meta['name']+' — Python replay'
    if App.GuiUp:
        import FreeCADGui as Gui
        Gui.activeDocument().activeView().viewAxonometric();Gui.activeDocument().activeView().fitAll()
        print('Rebuilt in a new unsaved document. Archive through freecad_build after updating Python.')
    else:
        target=Path(script).with_suffix('.rebuilt.FCStd')
        save_checked(doc,final,target);App.closeDocument(doc.Name)
        print('Rebuilt',target)


def check(out):
    index=json.loads((out/'manifest.json').read_text())
    for path,digest in index['source_files'].items():
        if sha(out/path)!=digest:raise ValueError('Source hash mismatch: '+path)
    for item in index['models']:
        for kind in ('python','fcstd'):
            if sha(out/item[kind])!=item[kind+'_sha256']:raise ValueError('Revision modified: '+item[kind])
        doc=App.openDocument(str(out/item['fcstd']),True)
        try:
            final=doc.getObject(item['final_object']);expected=final.Shape.copy()
            for obj in doc.Objects:obj.touch()
            validate_document(doc,final,expected,item['solids'])
        finally:App.closeDocument(doc.Name)
        print('verified',item['fcstd'],flush=True)


def build(out,only=None,include_references=True):
    from .part_versions import check as check_versions
    problems=check_versions()
    if problems:raise ValueError('Part version check failed: '+ '; '.join(problems))
    out.mkdir(parents=True,exist_ok=True)
    revision=snapshot(out);models=[]
    for builder,spec in specs():
        for hand in ('right','left') if spec.get('handed') else ('none',):
            name=spec['name']+('_'+hand if hand!='none' else '')
            models.append((f'parts/{spec["name"]}/v{spec.get("version",1)}/{revision[:16]}/{name}',
                           {'kind':'part','name':name,'builder':builder.__module__+':'+builder.__name__,'hand':hand,'version':spec.get('version',1)}))
    for pose in ('walking','quadruped','upright'):
        name='koala-'+pose
        models.append((f'assemblies/{revision[:16]}/{name}',{'kind':'assembly','name':name,'pose':pose}))
    from .bend_limits import REVIEW_POSES
    for review in REVIEW_POSES:
        name='koala-walking-'+review
        models.append((f'assemblies/{revision[:16]}/{name}',
                       {'kind':'assembly','name':name,'pose':'walking','bend_review':review}))
    for name,builder in (('angled-fork','koala_hardware.carrier_fork_study:candidate'),('pitch-mount-face','koala_hardware.pitch_socket_tilt_study:mount_face')):
        models.append((f'studies/{revision[:16]}/{name}',{'kind':'study','name':name,'builder':builder}))
    for pose in ('walking','quadruped','upright'):
        name='body-'+pose
        models.append((f'studies/{revision[:16]}/{name}',{'kind':'study','name':name,
                       'builder':'koala_hardware.freecad_studies:body_master','arguments':{'pose':pose}}))
    for variant in ('current','options','flat'):
        for pose in ('quadruped','upright'):
            name=f'rear-leg-{variant}-{pose}'
            models.append((f'studies/{revision[:16]}/{name}',{'kind':'study','name':name,
                           'builder':'koala_hardware.freecad_studies:rear_leg','arguments':{'pose':pose,'variant':variant}}))
    name='pitch-socket-45'
    models.append((f'studies/{revision[:16]}/{name}',{'kind':'study','name':name,
                   'builder':'koala_hardware.freecad_studies:pitch_socket_45'}))
    if include_references:
        repo=ROOT.parent
        for rel,path in reference_inputs(repo,out):
            digest=sha(path);name=rel.removesuffix(path.suffix).replace('/','__')
            archived=f'reference-sources/{digest}/{path.name}'
            target=out/archived
            if target.exists():
                if sha(target)!=digest:raise ValueError('Archived STEP modified: '+str(target))
            else:
                target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(path,target)
            models.append((f'references/{digest[:16]}/{name}',{'kind':'reference','name':path.stem,'source':rel,'source_sha256':digest,'archived_source':archived}))
    manifest_path=out/'manifest.json'
    index=json.loads(manifest_path.read_text()) if manifest_path.exists() else {'schema':1,'models':[],'source_files':{}}
    index['source_files'].update({str(p.relative_to(out)):sha(p) for p in (out/'reference-sources').rglob('*') if p.is_file()})
    for stem,meta in models:
        if only and only not in stem:continue
        py=out/(stem+'.py');fcstd=out/(stem+'.FCStd')
        old=next((i for i in index['models'] if i['python']==str(py.relative_to(out))),None)
        if old:
            if sha(py)!=old['python_sha256'] or sha(fcstd)!=old['fcstd_sha256']:raise ValueError('Existing revision modified; preserve GUI edits and sync Python first: '+str(fcstd))
            print('kept',stem,flush=True);continue
        if py.exists() or fcstd.exists():raise ValueError('Unindexed revision exists: '+stem)
        print('building',stem,flush=True)
        doc,final=construct(meta,out)
        try:
            final_name=save_checked(doc,final,fcstd)
            py.write_text(replay_text(meta,revision))
            entry={**meta,'source_revision':revision,'python':str(py.relative_to(out)),'fcstd':str(fcstd.relative_to(out)),
                   'python_sha256':sha(py),'fcstd_sha256':sha(fcstd),'final_object':final_name,
                   'solids':len(final.Shape.Solids),'volume_mm3':final.Shape.Volume,'objects':len(doc.Objects),
                   'freecad_version':'.'.join(App.Version()[:3])}
            index['models'].append(entry)
        finally:App.closeDocument(doc.Name)
        index['source_files'].update({str(p.relative_to(out)):sha(p) for p in (out/'sources'/revision).rglob('*.py')})
        staged=manifest_path.with_suffix('.tmp');staged.write_text(json.dumps(index,indent=2)+'\n');staged.replace(manifest_path)
    print('Archived',len(index['models']),'documents in',out,flush=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=DEFAULT)
    parser.add_argument('--only',help='Filter path substring for development')
    parser.add_argument('--no-references',action='store_true')
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    if args.check:check(args.output.resolve())
    else:build(args.output.resolve(),args.only,not args.no_references)

if __name__=='__main__':main()
