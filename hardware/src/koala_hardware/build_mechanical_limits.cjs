// SPDX-License-Identifier: CERN-OHL-S-2.0
// Warm the exact same worker engine off-line so the static viewer opens promptly.
const fs=require('fs'),vm=require('vm'),path=require('path'),crypto=require('crypto');
const base=process.argv[2];
const raw=fs.readFileSync(path.join(base,'scene.json'));
const scene=JSON.parse(raw),result={scene_sha256:crypto.createHash('sha256').update(raw).digest('hex'),engine_sha256:crypto.createHash('sha256').update(fs.readFileSync(path.join(base,'mechanical_limits.js'))).digest('hex'),poses:{}};
const savedPath=path.join(base,'mechanical-limits.json');
const saved=fs.existsSync(savedPath)?JSON.parse(fs.readFileSync(savedPath)):{};
for(const pose of Object.keys(scene.poses)){
  const poseHash=crypto.createHash('sha256').update(JSON.stringify({items:scene.poses[pose],joints:scene.meta.joints[pose]})).digest('hex');
  const seed=saved.engine_sha256===result.engine_sha256 && saved.poses?.[pose]?.pose_sha256===poseHash?saved.poses[pose].cache:[];
  const context=vm.createContext({console,atob,performance,postMessage:()=>{}});
  context.importScripts=(...names)=>{for(const name of names)vm.runInContext(fs.readFileSync(path.join(base,name),'utf8'),context);};
  vm.runInContext(fs.readFileSync(path.join(base,'mechanical_limits.js'),'utf8'),context);
  context.DATA={items:scene.poses[pose],joints:scene.meta.joints[pose],cache:seed};
  const start=performance.now();
  const record=JSON.parse(vm.runInContext("init(DATA);const limits=bounds({pitch:0,roll:0,knee:0});JSON.stringify({limits,cache:[...cache]})",context));
  if(record.limits.error)throw new Error(pose+': '+JSON.stringify(record.limits));
  record.pose_sha256=poseHash;
  result.poses[pose]=record;
  console.log(pose,JSON.stringify(record.limits.bounds),Math.round((performance.now()-start)/1000)+'s',record.cache.length+' cached pair states');
}
fs.writeFileSync(path.join(base,'mechanical-limits.json'),JSON.stringify(result));
