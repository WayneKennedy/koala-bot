// A servo's exempt contact partner: one name, or several when the fork is split across prints.
const partnerOf=(a,b)=>Array.isArray(a.contactPartner)?a.contactPartner.includes(b.name):a.contactPartner===b.name;
/* SPDX-License-Identifier: CERN-OHL-S-2.0
 * Pose-dependent, grouped joint clearance search for the static viewer.
 * Surfaces are checked at 0.25 degree increments with a 2 degree reserve before the first hit.
 * Start from the current clear pose and stop at the FIRST obstruction.
 * This is finite-resolution CAD inspection, not a certified swept-volume test.
 */
importScripts('three-r128.min.js', 'three-mesh-bvh-0.5.23.js');
// One degree left 0.013/0.020 mm3 of imported-case contact at the rear pitch
// endpoints. Two degrees clears those independent solid-CAD checks (DEC-58).
const STEP = .25, MARGIN = 0, RESERVE = 2, CEILING = 180;
let items=[], pairs=[], joints={}, cache=new Map();
const reflect=new THREE.Matrix4().makeScale(1,-1,1);
function decode(s,T) { const b=atob(s), a=new Uint8Array(b.length); for(let i=0;i<b.length;i++)a[i]=b.charCodeAt(i);return new T(a.buffer); }
function geometry(it) {
  const g=new THREE.BufferGeometry();
  g.setAttribute('position',new THREE.BufferAttribute(decode(it.pos,Float32Array),3));
  g.setIndex(new THREE.BufferAttribute(decode(it.idx,Uint32Array),1));
  g.boundsTree=new MeshBVHLib.MeshBVH(g,{maxLeafTris:8});
  g.computeBoundingBox(); return g;
}
function pivot(p,a,angle) { return new THREE.Matrix4().makeTranslation(...p)
  .multiply(new THREE.Matrix4().makeRotationAxis(new THREE.Vector3(...a),angle*Math.PI/180))
  .multiply(new THREE.Matrix4().makeTranslation(...p.map(v=>-v))); }
const command=joint=>joint==='bend'?'knee':joint;
function chain(it) {
  if(!it.side)return {limb:null,stages:[]};
  const [limb,joint]=it.joint.split('_');
  if(joint==='fixed')return {limb,stages:[]};
  const order=joints[limb].order||['pitch','roll','bend'],stage=order.indexOf(joint);
  if(stage<0)throw new Error('Unknown joint group: '+it.joint);
  return {limb,stages:order.slice(0,stage+1)};
}
function dependencies(a,b) {
  const ac=a.chain||chain(a),bc=b.chain||chain(b);
  // Only a shared rigid prefix on the same limb/hand cancels from relative motion.
  let common=0;
  if(a.side===b.side&&ac.limb===bc.limb)
    while(common<ac.stages.length&&ac.stages[common]===bc.stages[common])common++;
  const moving=new Set([...ac.stages.slice(common),...bc.stages.slice(common)].map(command));
  return ['pitch','roll','knee'].filter(k=>moving.has(k));
}
function transform(it,q) {
  const m=new THREE.Matrix4();if(!it.side)return m;
  const c=it.chain||chain(it),d=joints[c.limb];
  for(const stage of c.stages)
    m.multiply(pivot(d[stage],stage==='roll'?d.roll_axis:[0,1,0],q[command(stage)]));
  if(it.side<0)m.premultiply(reflect).multiply(reflect);
  return m;
}
function init(data) {
  joints=data.joints;cache=new Map(data.cache||[]);
  items=data.items.map((it,i)=>({...it,id:i,chain:chain(it),geometry:geometry(it.collisionMesh||it),core:it.contactCore?geometry(it.contactCore):null}));
  pairs=[];
  for(let i=0;i<items.length;i++)for(let j=i+1;j<items.length;j++){
    const a=items[i],b=items[j];
    const dependent=dependencies(a,b);
    // Every rigid configuration has already passed the BREP assembly audit.
    if(!dependent.length)continue;
    const ag=partnerOf(a,b)?a.core:a.geometry;
    const bg=partnerOf(b,a)?b.core:b.geometry;
    pairs.push({a,b,ag,bg,dependencies:dependent,id:pairs.length});
  }
}
function blocked(q) {
  const matrices=items.map(it=>transform(it,q));
  const boxes=items.map((it,i)=>it.geometry.boundingBox.clone().applyMatrix4(matrices[i]).expandByScalar(MARGIN));
  for(const p of pairs){
    const key=p.id+':'+p.dependencies.map(k=>q[k].toFixed(3)).join(',');
    if(cache.has(key)){const hit=cache.get(key);if(hit)return hit;continue;}
    let hit=null;
    if(!boxes[p.a.id].intersectsBox(boxes[p.b.id]))continue;
    {
      const owner=partnerOf(p.a,p.b)?p.a:partnerOf(p.b,p.a)?p.b:null;
      if(owner?.contactBoxes){
        const other=owner===p.a?p.b:p.a;
        const tf=matrices[other.id].clone().invert().multiply(matrices[owner.id])
          .multiply(new THREE.Matrix4().fromArray(owner.contactFrame));
        for(const [lo,hi] of owner.contactBoxes){
          const box=new THREE.Box3(new THREE.Vector3(...lo),new THREE.Vector3(...hi));
          if(other.geometry.boundsTree.intersectsBox(box,tf)){hit=[p.a.name,p.b.name];break;}
        }
      }else{
        const relative=matrices[p.b.id].clone().invert().multiply(matrices[p.a.id]);
        if(p.bg.boundsTree.bvhcast(p.ag.boundsTree,relative,{intersectsTriangles:(a,b)=>a.intersectsTriangle(b)}))hit=[p.a.name,p.b.name];
      }
    }
    cache.set(key,hit);if(hit)return hit;
  }
  if(cache.size>200000)cache.clear();
  return null;
}
function bounds(q) {
  const initial=blocked(q);if(initial)return {error:'Current pose intersects modelled geometry',pair:initial};
  const result={};
  for(const axis of ['pitch','roll','knee']){
    const limits=[],stops=[];
    for(const sign of [-1,1]){
      let last=q[axis],stop=null;
      for(let angle=q[axis]+sign*STEP;Math.abs(angle)<=CEILING+.0001;angle+=sign*STEP){
        const next={...q,[axis]:Math.round(angle*100)/100};
        stop=blocked(next);if(stop)break;last=next[axis];
      }
      // Angular reserve before the first detected obstruction.
      if(stop)last=q[axis]+sign*Math.max(0,Math.abs(last-q[axis])-RESERVE);
      limits.push(last);stops.push(stop);
    }
    result[axis]={min:limits[0],max:limits[1],stops};
    postMessage({progress:axis,result:result[axis]});
  }
  return {bounds:result,step:STEP,angular_reserve_degrees:RESERVE,search_ceiling:CEILING};
}
onmessage=e=>{
  const {id,type,...data}=e.data;
  try{
    if(type==='init')init(data);
    const result=bounds(data.angles);
    postMessage({id,...result});
  }catch(error){postMessage({id,error:String(error)});}
};
