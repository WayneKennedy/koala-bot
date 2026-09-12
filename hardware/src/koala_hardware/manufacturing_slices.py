# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Local manufacturing slices; never connects to or starts a printer.

Uses the shared printer profile in the sibling 3d-printing repository plus
Koala-specific settings. G-code is review-only until material/fit validation.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import argparse, hashlib, json, re, subprocess
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

ROOT=Path(__file__).resolve().parents[2]
DOC=ROOT.parent/'docs/design/manufacturing'
BUILD=ROOT/'build/manufacturing'


def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def paths(path):
    """Extract deposited XY segments by layer/type from relative-extrusion G-code."""
    layers={};x=y=z=0.;kind='';relative=True;previous_e=0.
    for line in path.read_text().splitlines():
        if line.startswith(';TYPE:'):kind=line[6:]
        if line.startswith('M82'):relative=False
        if line.startswith('M83'):relative=True
        if line.startswith('G92 E'):previous_e=float(line.split('E')[1].split()[0])
        if not line.startswith(('G0 ','G1 ')):continue
        v={k:float(a) for k,a in re.findall(r'([XYZE])([-+\d.]+)',line.split(';')[0])}
        nx,ny,nz=v.get('X',x),v.get('Y',y),v.get('Z',z)
        de=v.get('E',0) if relative else v.get('E',previous_e)-previous_e
        if de>0 and (nx!=x or ny!=y):
            layers.setdefault(round(nz,3),[]).append(((x,y),(nx,ny),kind))
        x,y,z=nx,ny,nz
        if 'E' in v:previous_e=v['E']
    return layers


def render(path,out,name):
    layers=paths(path)
    model=lambda k:'Support' not in k and k not in ('Skirt/Brim','Skirt','Brim')
    zs=sorted(z for z,segs in layers.items() if any(model(k) for a,b,k in segs))
    support_zs=sorted(z for z,segs in layers.items() if any('Support' in k for a,b,k in segs))
    assert len(zs)>3,name
    indices=sorted(set([0,int((len(zs)-1)*.2),int((len(zs)-1)*.55),int((len(zs)-1)*.85)]))
    fig,axes=plt.subplots(1,4,figsize=(15,4),layout='constrained')
    for ax,i in zip(axes,indices):
        z=zs[i];seg=[(a,b,k) for a,b,k in layers[z] if 'Support' not in k]
        sz=min(support_zs,key=lambda h:abs(h-z)) if support_zs else None
        if sz is not None and abs(sz-z)<=.25:
            seg += [(a,b,k) for a,b,k in layers[sz] if 'Support' in k]
        else:sz=None
        ax.add_collection(LineCollection([(a,b) for a,b,k in seg],
            colors=['#dc8a35' if 'Support' in k else '#347d8d' for a,b,k in seg],linewidths=.45))
        ax.autoscale();ax.set_aspect('equal');ax.set_title(f'Part Z = {z:g} mm'+(f'\nSupport Z = {sz:g} mm' if sz is not None else ''));ax.axis('off')
    fig.suptitle(name+' — deposited paths (orange = support); geometry review, unprinted')
    fig.savefig(out,dpi=130);plt.close(fig)
    return len(zs)


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--profile',type=Path,default=ROOT.parent.parent/'3d-printing/reference/ender5s1_petg_koala.ini')
    args=ap.parse_args();profile=args.profile.resolve();assert profile.is_file(),profile
    BUILD.mkdir(parents=True,exist_ok=True);DOC.mkdir(parents=True,exist_ok=True)
    version=subprocess.check_output(['prusa-slicer','--help'],text=True).splitlines()[0]
    files=sorted((ROOT/'build/stl').glob('*.stl'))
    previous_path=DOC/'slices.json'
    previous=json.loads(previous_path.read_text()) if previous_path.exists() else {}
    reusable={r['name']:r for r in previous.get('parts',[])} if previous.get('shared_profile_sha256')==sha(profile) and previous.get('slicer')==version else {}
    def run(stl):
        material='TPU' if stl.stem=='front_contact_pad' else 'PETG'
        overrides=ROOT/'print'/f'manufacturing-{material.lower()}.ini'
        dest=BUILD/(stl.stem+'.gcode');log=BUILD/(stl.stem+'.log')
        old=reusable.get(stl.stem)
        if old and old['stl_sha256']==sha(stl) and old['overrides_sha256']==sha(overrides) and dest.exists() and old['gcode_sha256']==sha(dest):
            return old
        command=['prusa-slicer','--load',str(profile),'--load',str(overrides),'--threads','2',
                 '--export-gcode','--output',str(dest),str(stl)]
        result=subprocess.run(command,text=True,capture_output=True)
        log.write_text(result.stdout+result.stderr)
        assert result.returncode==0 and dest.exists(),(stl.stem,log.read_text())
        g=dest.read_text()
        volume=re.search(r'; filament used \[cm3\] = ([\d.]+)',g)
        timing=re.search(r'; estimated printing time \(normal mode\) = (.+)',g)
        assert volume and timing,stl
        return {'name':stl.stem,'material':material,'printable':'assumed','stl_sha256':sha(stl),
                'overrides_sha256':sha(overrides),'gcode_sha256':sha(dest),
                'filament_cm3':float(volume[1]),'print_time':timing[1],
                'warnings':[l for l in log.read_text().splitlines() if 'warn' in l.lower() or 'error' in l.lower()]}
    with ThreadPoolExecutor(max_workers=2) as pool:
        records=list(pool.map(run,files))
    for r in records:
        if previous.get('layer_plot_version')!=2 or 'layers' not in r or not (DOC/(r['name']+'-layers.png')).exists():
            r['layers']=render(BUILD/(r['name']+'.gcode'),DOC/(r['name']+'-layers.png'),r['name'])
        print(r['name'],r['material'],r['layers'],'layers',r['print_time'],flush=True)
    result={'slicer':version,'layer_plot_version':2,'shared_profile':str(profile),'shared_profile_sha256':sha(profile),
            'scope':'Local slices and layer-path review. Nothing printed. TPU settings are provisional, not a validated material profile.',
            'parts':records}
    (DOC/'slices.json').write_text(json.dumps(result,indent=2)+'\n')
    (ROOT/'build/slice-cache.json').write_text(json.dumps({r['name']:{'sha256':r['stl_sha256'],'cm3':r['filament_cm3'],'time':r['print_time'],'material':r['material']} for r in records},indent=2)+'\n')


if __name__=='__main__':main()
