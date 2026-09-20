# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Check and capture the current production rear viewer, leaving studies untouched."""
import hashlib
import json
import os
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/design/rear-leg'
LIVE=ROOT/'hardware/build/viewer/rear-leg'

with sync_playwright() as p:
    browser=p.chromium.launch(executable_path=os.environ.get('PLAYWRIGHT_CHROMIUM'),headless=True,
        args=['--no-sandbox','--disable-dev-shm-usage','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
    page=browser.new_page(viewport={'width':1600,'height':1100});errors=[];poses=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto(os.environ.get('VIEWER_URL','http://127.0.0.1:8020/rear-leg/'))
    page.wait_for_selector('#loading',state='detached',timeout=60000)
    page.wait_for_function('renderer.info.render.triangles>0')
    assert page.locator('#reference-controls').is_hidden()
    for pose in ('quadruped','upright'):
        page.locator('#body-pose').select_option(pose)
        page.wait_for_function('!limitState.pending',timeout=300000)
        assert not page.evaluate('limitState.error||null')
        parts=page.evaluate('Object.fromEntries(DATA.poses[poseName].filter(i=>i.kind==="printed").map(i=>[i.name,{version:i.version,printable:i.printable}]))')
        for side in ('right','left'):
            assert parts['rear_thigh_'+side]=={'version':3,'printable':'unknown'}
            assert parts['rear_shank_'+side]=={'version':2,'printable':'assumed'}
            assert parts['pelvis_socket_'+side]=={'version':1,'printable':'proven'}
        assert parts['torso_frame']['version']==5
        assert 'proposed_torso_face' not in parts
        assert page.evaluate('limitState.angular_reserve_degrees')==2
        poses.append({'pose':pose,'bounds':page.evaluate('limitState.bounds'),'parts':parts})
        page.locator('[data-view="iso"]').click()
        page.screenshot(path=str(OUT/f'rear-leg-{pose}.png'))
        if pose=='quadruped':
            before=page.evaluate('meshes.find(m=>m.userData.name==="rear_thigh_right").matrix.toArray()')
            assert float(page.locator('#roll').get_attribute('max'))>=30
            page.locator('#roll').fill('30')
            page.wait_for_function('!limitState.pending',timeout=300000)
            assert not page.evaluate('limitState.error||null')
            assert float(page.locator('#roll').input_value())==30
            after=page.evaluate('meshes.find(m=>m.userData.name==="rear_thigh_right").matrix.toArray()')
            assert before!=after
            page.screenshot(path=str(OUT/'rear-leg-roll-30.png'))
            page.locator('#neutral').click()
            page.wait_for_function('!limitState.pending',timeout=300000)
    page.locator('#tab-parts').click()
    page.get_by_role('button',name='thigh',exact=False).click()
    assert page.evaluate('meshes.filter(m=>m.visible).length')==1
    assert 'thigh v3' in page.locator('#detail').inner_text()
    assert 'printable: unknown' in page.locator('#hud').inner_text()
    page.screenshot(path=str(OUT/'rear-leg-thigh-v3.png'))
    assert not page.evaluate('renderer.getContext().isContextLost()')
    assert not errors,errors
    result={'tailnet_url':'https://blake.tail13a0c0.ts.net:8443/rear-leg/',
            'scene_sha256':hashlib.sha256((LIVE/'scene.json').read_bytes()).hexdigest(),
            'page_errors':errors,'checks':['both pose caches load','2 degree reserve','production versions and printability',
            'actual torso present','30 degree rear roll changes pose matrix','thigh v3 selection and notes','backdrop controls hidden'],
            'poses':poses}
    (OUT/'browser.json').write_text(json.dumps(result,indent=2)+'\n')
    browser.close()
    print('PASS production rear viewer, versions, both poses, roll, current screenshots and part selection')
