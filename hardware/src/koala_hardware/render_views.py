# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Multi-view render of one part for the "does this design look stupid?" gate
(owner, 2026-09-19): iso, front, side and top, shaded, no bed or colouring.

    uv run python -m koala_hardware.render_views torso_frame            # a production part (all_builders name)
    uv run python -m koala_hardware.render_views thigh_flat --option    # an option builder in links

Writes docs/design/parts/<name>-views.png. Look at it before running the build
chain, and say in the revision log whether it passed the question.
"""
import sys,pathlib,tempfile
import numpy as np,trimesh,matplotlib
matplotlib.use('Agg');import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from .parts import all_builders,links as L
from .meshing import export_mesh

ROOT=pathlib.Path(__file__).resolve().parents[3]


def views_png(name,mesh,out):
    light=np.array([0.4,0.3,0.86]);light/=np.linalg.norm(light)
    def rot(axis,deg):return trimesh.transformations.rotation_matrix(np.radians(deg),axis)[:3,:3]
    frames=[('iso',rot([0,0,1],-35)@rot([1,0,0],0)),('side (along Y)',np.eye(3)),('end (along X)',rot([0,0,1],90)),('top (along Z)',rot([1,0,0],-90))]
    fig,axes=plt.subplots(2,2,figsize=(12,10))
    for ax,(label,Rm) in zip(axes.flat,frames):
        v=mesh.vertices@Rm.T;n=mesh.face_normals@Rm.T;tri=v[mesh.faces]
        if label=='iso':
            tilt=rot([1,0,0],-55);v=v@tilt.T;n=n@tilt.T;tri=v[mesh.faces]
        # view along +Y (screen: X right, Z up); draw far faces first, front-facing only
        facing=n[:,1]<0;order=np.argsort(-tri[:,:,1].mean(axis=1))
        shade=np.clip(0.35+0.65*np.abs(n@light),0,1)
        cols=np.stack([shade*0.55,shade*0.68,shade*0.9,np.ones_like(shade)],axis=1)
        idx=[i for i in order if facing[i]]
        ax.add_collection(PolyCollection(tri[idx][:,:,[0,2]],facecolors=cols[idx],edgecolors='none'))
        ax.set_aspect('equal');ax.autoscale();ax.set_title(f'{name} — {label}');ax.set_xlabel('mm');ax.grid(alpha=0.25)
    fig.suptitle(f'{name}: does this design look stupid? Judge before building on it.',fontsize=12)
    plt.tight_layout(rect=(0,0,1,0.96));plt.savefig(out,dpi=80);plt.close(fig)


def main():
    name=sys.argv[1];option='--option' in sys.argv
    builders={b().get('name'):b for b in ([getattr(L,f'option_{name}')] if option else all_builders())} if option else {b().get('name'):b for b in all_builders()}
    spec=builders[name]() if not option else getattr(L,f'option_{name}')()
    with tempfile.TemporaryDirectory() as td:
        mesh=export_mesh(spec['part'],pathlib.Path(td)/'p.stl')
    out=ROOT/'docs/design/parts'/f'{name}-views.png';out.parent.mkdir(parents=True,exist_ok=True)
    views_png(name,mesh,out);print('wrote',out.relative_to(ROOT))


if __name__=='__main__':main()
