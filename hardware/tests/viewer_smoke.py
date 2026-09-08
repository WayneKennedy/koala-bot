# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Optional live viewer smoke check.

Start viewer, then: uv run --with playwright python tests/viewer_smoke.py
PLAYWRIGHT_CHROMIUM may point at an existing Chromium binary.
"""
import os
from playwright.sync_api import sync_playwright
from koala_hardware.assembly import build_scene


with sync_playwright() as p:
    browser = p.chromium.launch(
        executable_path=os.environ.get("PLAYWRIGHT_CHROMIUM"),
        headless=True,
        args=["--no-sandbox", "--disable-dev-shm-usage", "--use-gl=angle",
              "--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
    page = browser.new_page(viewport={"width": 1440, "height": 1000})
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto("http://127.0.0.1:8017/")
    page.wait_for_selector("#loading", state="detached", timeout=60000)
    page.wait_for_function("renderer.info.render.triangles > 0")
    assert not page.evaluate("renderer.getContext().isContextLost()")
    assert page.locator(".row").count() == len(build_scene())
    page.screenshot(path="build/viewer/assembly-check.png")
    page.locator("#pitch").fill("20")
    page.locator("#roll").fill("-5")
    assert page.locator("#pitch-value").inner_text() == "20°"
    page.locator("#knee").fill("60")
    # Verify viewer pivots and mirroring against CAD, not just a moving slider.
    cad = {n: s for n, s, _ in build_scene(roll=-5, pitch=20, knee=60)}
    for name in ("shank_core_right", "shank_core_left",
                 "hip_pitch_cradle_left", "reference_roll_servo_right", "reference_knee_servo_left"):
        bounds = page.evaluate("""name => {
          const m = meshes.find(m => m.userData.name === name);
          m.updateMatrixWorld(true);
          const b = new THREE.Box3(), v = new THREE.Vector3();
          const positions = m.geometry.getAttribute("position");
          for (let i = 0; i < positions.count; i++)
            b.expandByPoint(v.fromBufferAttribute(positions, i).applyMatrix4(m.matrixWorld));
          return [...b.min.toArray(), ...b.max.toArray()];
        }""", name)
        bb = cad[name].bounding_box()
        expected = [*bb.min, *bb.max]
        assert max(abs(a-b) for a, b in zip(bounds, expected)) < .1, (name, bounds, expected)
    page.screenshot(path="build/viewer/posed-check.png")
    page.locator("#tab-parts").click()
    assert page.locator("#pose").is_hidden()
    page.get_by_role("button", name="thigh_core", exact=False).click()
    assert "tapered support" in page.locator("#detail").inner_text()
    assert page.evaluate("meshes.filter(m=>m.visible).length") == 1
    page.get_by_role("button", name="thigh_core", exact=False).click()
    page.screenshot(path="build/viewer/parts-check.png")
    page.locator("#tab-assembly").click()
    page.locator("#neutral").click()
    assert page.locator("#pitch-value").inner_text() == "15°"
    assert not errors, errors
    browser.close()
    print("PASS rendered geometry, CAD/viewer pose parity, part orientation notes, solo and reset")
