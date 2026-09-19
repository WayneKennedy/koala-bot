# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Print-orientation screen for one exported STL: bed contact, >45° overhang and
a support-volume estimate (overhang area × drop to the part or bed) for a set of
candidate orientations, with faces coloured in a two-view PNG.

    uv run --with rtree python -m koala_hardware.orientation_study thigh_right
    uv run --with rtree python -m koala_hardware.orientation_study --thigh-options   # the 2026-09-19 option prints

It is a screen for choosing what to slice, not a slice: it ignores bridging,
support style and perimeters. Run `export` first; reads build/stl/<name>.stl and
writes docs/design/rear-leg/<name>-orientation-study.png.
"""
import sys, pathlib
import numpy as np, trimesh, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
ROOT=pathlib.Path(__file__).resolve().parents[2]
OPTIONS='--thigh-options' in sys.argv
NAME='thigh_right' if OPTIONS else (sys.argv[1] if len(sys.argv)>1 else 'thigh_right')
m0=trimesh.load(ROOT/'build/stl'/f'{NAME}.stl')
def rot(axis,deg): return trimesh.transformations.rotation_matrix(np.radians(deg),axis)
cands=[('A  declared: thin cheek down',np.eye(4)),
       ('B  flipped: thick cheek + socket wall down',rot([0,1,0],180)),
       ('C  standing on the knee socket',rot([1,0,0],90)),
       ('D  flipped, fork end raised 20',rot([1,0,0],20)@rot([0,1,0],180)),
       ('E  flipped, socket end raised 20',rot([1,0,0],-20)@rot([0,1,0],180))]
if OPTIONS:
    # The 2026-09-19 print-form options, each in its declared print orientation (spec['orientation']).
    import tempfile
    from .parts import links as L
    from .meshing import export_mesh
    builders=[('thigh v2 production (tapered, rounded), declared: cup-floor plane down',L.build_thigh),
              ('Option 1 frame, standing on the knee socket (LEFT leg)',L.option_thigh_frame),
              ('Option 2 body, lying on the cup-floor plane (RIGHT leg)',L.option_thigh_split_body),
              ('Option 2 cheek piece, on its outer face (RIGHT leg)',L.option_thigh_split_cheek),
              ('Option 3 one piece, tapered, on the cup-floor plane (owner 2026-09-19)',L.option_thigh_flat),
              ('shank v2 production (flush, rounded), declared: outer face down',L.build_shank),
              ('shank_flush study (unrounded, inset now 0)',L.option_shank_flush)]
    _tmp=tempfile.mkdtemp();cands=[]
    for i,(label,b) in enumerate(builders):
        s=b();cands.append((label,export_mesh(s['orientation']*s['part'],pathlib.Path(_tmp)/f'{i}.stl')))
def score(m):
    n=m.face_normals; area=m.area_faces; c=m.triangles_center
    bed=(n[:,2]<-0.999)&(c[:,2]<0.3); over=(n[:,2]<-np.cos(np.radians(45)))&~bed
    o=c[over]-[0,0,0.05]; d=np.tile([0,0,-1.0],(len(o),1))
    hits,ri,_=m.ray.intersects_location(o,d,multiple_hits=False)
    h=o[:,2].copy()
    for loc,i in zip(hits,ri): h[i]=min(h[i],o[i,2]-loc[2])
    return bed,over,area[bed].sum(),area[over].sum(),(area[over]*h).sum()/1000
fig,axes=plt.subplots(len(cands),2,figsize=(12,4*len(cands)))
print(f"{'orientation':46s} {'bed mm2':>8s} {'overhang mm2':>13s} {'support cm3':>12s} {'height':>7s}")
for r,(name,T) in enumerate(cands):
    if OPTIONS:m=T.copy()
    else:m=m0.copy(); m.apply_transform(T)
    m.apply_translation(-m.bounds[0])
    bed,over,ab,ao,vs=score(m); ext=m.bounds[1]-m.bounds[0]
    print(f"{name:58s} {ab:8.0f} {ao:13.0f} {vs:12.1f} {ext[2]:7.1f}  volume {m.volume/1000:5.1f} cm3")
    n=m.face_normals; tri=m.triangles
    for col,(u,v,label) in enumerate([(0,2,'view along the knee axis'),(1,2,'view along the length')]):
        ax=axes[r,col]; vdir=np.array([0,-1,0]) if col==0 else np.array([-1,0,0])
        facing=(n@vdir)>0; order=np.argsort(tri[:,:,1 if col==0 else 0].mean(axis=1))
        polys=tri[:,:,[u,v]]; cols=np.where(over,'#d33',np.where(bed,'#2a2','#9ab'))
        idx=[i for i in order if facing[i]]
        ax.add_collection(PolyCollection(polys[idx],facecolors=cols[idx],edgecolors='none'))
        oi=np.where(over)[0]; ax.add_collection(PolyCollection(polys[oi],facecolors='#d33',edgecolors='none',alpha=0.6))
        ax.set_aspect('equal'); ax.autoscale(); ax.axhline(0,color='k',lw=0.8); ax.grid(alpha=0.3)
        ax.set_title(f'{name} — {label}',fontsize=10); ax.set_xlabel('mm')
    axes[r,0].text(0.02,0.96,f'height {ext[2]:.0f} mm · bed {ab:.0f} mm² (green) · overhang {ao:.0f} mm² (red) · support ≈ {vs:.0f} cm³',transform=axes[r,0].transAxes,fontsize=9,va='top')
fig.suptitle(('Thigh print-form options in their declared print orientations' if OPTIONS else f'{NAME} — print-orientation study')+'\nred = faces steeper than 45° overhang; support volume = overhang area × drop to part or bed (not a slice)',fontsize=11)
plt.tight_layout(rect=(0,0,1,0.97)); out=ROOT.parent/'docs/design/rear-leg/thigh-options/print-orientations.png' if OPTIONS else ROOT.parent/'docs/design/rear-leg'/f'{NAME.split("_")[0]}-orientation-study.png'
plt.savefig(out,dpi=80); print('wrote',out.relative_to(ROOT.parent))
