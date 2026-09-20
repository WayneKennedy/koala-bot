// SPDX-License-Identifier: CERN-OHL-S-2.0
// Run with node tests/test_viewer_joint_order.cjs (no npm dependencies).
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const source=path.join(__dirname,'../src/koala_hardware'),vendor=path.join(__dirname,'../vendor/viewer');
const context=vm.createContext({console,atob,postMessage:()=>{},assert,Buffer});
context.importScripts=(...names)=>{
  for(const name of names)vm.runInContext(fs.readFileSync(path.join(vendor,name),'utf8'),context);
};
vm.runInContext(fs.readFileSync(path.join(source,'mechanical_limits.js'),'utf8'),context);
const html=fs.readFileSync(path.join(source,'viewer.html'),'utf8');
vm.runInContext(html.slice(html.indexOf('function pivotRotation('),html.indexOf('function applyPose(')),context);

vm.runInContext(`
const datum={pitch:[0,0,0],roll:[0,0,0],bend:[0,0,2],roll_axis:[0,0,1]};
joints={front:{...datum,order:['roll','pitch','bend']},rear:{...datum,order:['pitch','roll','bend']}};
const item=(joint,side=1)=>({joint,side});
const near=(actual,expected)=>assert.ok(actual.every((n,i)=>Math.abs(n-expected[i])<1e-9),actual+' != '+expected);
const q={pitch:90,roll:90,knee:90};
// These expected positions come from quarter-turns of (1,0,0), with an elbow at Z=2.
for(const [group,expected] of [
  ['front_roll',[0,1,0]],['front_pitch',[0,0,-1]],['front_bend',[0,1,2]],
  ['rear_pitch',[0,0,-1]],['rear_roll',[0,1,0]],['rear_bend',[1,-2,0]],
])for(const side of [1,-1]) {
  const it=item(group,side),position=new THREE.Vector3(1,0,0);
  const want=expected.map((v,i)=>i===1?v*side:v);
  near(position.clone().applyMatrix4(transform(it,q)).toArray(),want);
  near(position.clone().applyMatrix4(poseTransform(it,joints,q)).toArray(),want);
}
const deps=(a,b)=>JSON.stringify(dependencies(item(a),item(b)));
assert.equal(deps('front_roll','front_pitch'),'["pitch"]');
assert.equal(deps('front_roll','front_bend'),'["pitch","knee"]');
assert.equal(deps('rear_pitch','rear_roll'),'["roll"]');
assert.equal(deps('front_roll','rear_pitch'),'["pitch","roll"]');
assert.equal(JSON.stringify(dependencies(item('front_roll'),item('front_roll',-1))),'["roll"]');
assert.equal(JSON.stringify(dependencies({side:0},item('front_pitch'))),'["pitch","roll"]');
assert.equal(deps('front_pitch','front_pitch'),'[]');
delete joints.front.order; // Historical scenes keep their original pitch-first hierarchy.
near(new THREE.Vector3(1,0,0).applyMatrix4(transform(item('front_roll'),q)).toArray(),[0,1,0]);
near(new THREE.Vector3(1,0,0).applyMatrix4(poseTransform(item('front_roll'),joints,q)).toArray(),[0,1,0]);
joints.front.order=['roll','pitch','bend'];

// A cached shoulder collision must be invalidated by pitch even though roll is first.
const g=new THREE.BoxGeometry(2,2,2).translate(5,0,0);
const packed={pos:Buffer.from(g.attributes.position.array.buffer).toString('base64'),
              idx:Buffer.from(new Uint32Array(g.index.array).buffer).toString('base64')};
init({joints,items:[{...packed,...item('front_roll'),name:'carrier'},
                   {...packed,...item('front_pitch'),name:'arm'}]});
assert.ok(blocked({pitch:0,roll:0,knee:0}));
assert.equal(blocked({pitch:90,roll:0,knee:0}),null);
assert.ok(blocked({pitch:0,roll:45,knee:0}));
`,context);
console.log('PASS front/rear joint order, mirrored viewer/worker transforms, historical scenes and collision cache');
