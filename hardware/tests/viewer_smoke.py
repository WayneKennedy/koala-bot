# SPDX-License-Identifier: CERN-OHL-S-2.0
"""DEC-49/50 browser/CAD parity, print tags and geometry-derived travel bounds."""
import os
from pathlib import Path
from playwright.sync_api import sync_playwright
from koala_hardware.assembly import build_scene

with sync_playwright() as p:
    browser=p.chromium.launch(executable_path=os.environ.get('PLAYWRIGHT_CHROMIUM'),headless=True,
        args=['--no-sandbox','--disable-dev-shm-usage','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
    page=browser.new_page(viewport={'width':1600,'height':1100});errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto(os.environ.get('VIEWER_URL','http://127.0.0.1:8020/'))
    page.wait_for_selector('#loading',state='detached',timeout=60000)
    page.wait_for_function('renderer.info.render.triangles>0')
    page.wait_for_function('referenceMesh!==null')
    saw_bound_change=False
    for pose in ('quadruped','upright'):
        page.locator('#body-pose').select_option(pose)
        page.wait_for_function('referenceMesh.material.map.image.src.endsWith("backdrop-"+poseName+".svg")')
        page.wait_for_function('!limitState.pending',timeout=180000)
        assert not page.evaluate('limitState.error||null')
        initial=page.evaluate('limitState.bounds')
        assert any(v['max']>5 or v['min']< -5 for v in initial.values())
        assert all(page.evaluate('DATA.poses[poseName].filter(i=>i.kind==="printed").map(i=>i.printable==="assumed")'))
        assert page.locator('.row').count()==len(build_scene(pose=pose))
        assert '2 powered wheels' in page.locator('#hud').inner_text()
        page.locator('[data-view="side"]').click()
        assert page.evaluate('camera.isOrthographicCamera && referenceMesh.visible')
        assert page.evaluate('''() => {
          const d=DATA.meta.joints[poseName].rear.pitch;
          const a=new THREE.Vector3(...d).project(camera);
          const b=new THREE.Vector3(d[0],-400,d[2]).project(camera);
          return Math.abs(a.x-b.x)<1e-9 && Math.abs(a.y-b.y)<1e-9;
        }''')
        page.screenshot(path=f'build/viewer/{pose}-side-check.png')
        page.locator('[data-view="iso"]').click()
        page.screenshot(path=f'build/viewer/{pose}-check.png')
        last_request=page.evaluate('limitState.id')
        for axis,value in [('pitch',2),('roll',-2),('knee',2)]:
            page.locator('#'+axis).fill(str(value))
            page.wait_for_function('!limitState.pending',timeout=180000)
            assert not page.evaluate('limitState.error||null')
            assert float(page.locator('#'+axis).input_value())==value
            request=page.evaluate('limitState.id')
            assert request>last_request, 'no new clearance result for slider change'
            last_request=request
        changed=page.evaluate('limitState.bounds')
        # A purely local case/fork stop can legitimately remain unchanged
        # after small upstream movements; verify every search completed and
        # at least one tested configuration changes the coupled bounds.
        saw_bound_change |= changed!=initial
        cad={n:s for n,s,c in build_scene(roll=-2,pitch=2,knee=2,pose=pose)}
        for name in ('rear_shank_right','rear_shank_left','front_forearm_left','front_carrier_right','reference_front_elbow_servo_left'):
            bounds=page.evaluate('''name => {
              const m=meshes.find(m=>m.userData.name===name);m.updateMatrixWorld(true);
              const b=new THREE.Box3(),v=new THREE.Vector3(),p=m.geometry.getAttribute('position');
              for(let i=0;i<p.count;i++)b.expandByPoint(v.fromBufferAttribute(p,i).applyMatrix4(m.matrixWorld));
              return [...b.min.toArray(),...b.max.toArray()];
            }''',name)
            bb=cad[name].bounding_box();expected=[*bb.min,*bb.max]
            assert max(abs(a-b) for a,b in zip(bounds,expected))<.2,(pose,name,bounds,expected)
        page.locator('#neutral').click()
        page.wait_for_function('!limitState.pending',timeout=180000)
        assert page.locator('#pitch-value').inner_text()=='0°'
    assert saw_bound_change, 'coupled bounds did not respond to any tested configuration'
    page.locator('#tab-parts').click()
    assert page.locator('#pose').is_hidden()
    page.get_by_role('button',name='thigh',exact=False).click()
    assert page.evaluate('meshes.filter(m=>m.visible).length')==1
    assert 'One 85 mm link' in page.locator('#detail').inner_text()
    assert 'printable: assumed' in page.locator('#hud').inner_text()
    page.screenshot(path='build/viewer/integrated-thigh-check.png')
    page.get_by_role('button',name='front_contact_pad',exact=False).click()
    assert 'TPU' in page.locator('#hud').inner_text()
    page.screenshot(path='build/viewer/tpu-pad-check.png')
    assert not page.evaluate('renderer.getContext().isContextLost()')
    assert not errors,errors
    browser.close()
    print('PASS both body poses, backdrop alignment, mirrored CAD/browser motion, parts and reset')
