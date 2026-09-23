"""Load a koala MJCF in MuJoCo and report what the CAD package cannot: masses, CoM against the
support polygon, a zero-control stand, and an oblique render.

Standalone on purpose: needs only mujoco and numpy (and PIL for --render), none of which this
package depends on, so run it from any venv that has MuJoCo, e.g. the family's Open Duck one:

    MUJOCO_GL=egl python hardware/src/koala_hardware/mjcf_check.py hardware/sim/koala_walking.xml [--render out.png] [--seconds 3]

Exit status is non-zero if the model does not load, the CoM projection leaves the foot polygon,
or the torso falls (height drops > 30 mm or the IMU up-vector tilts > 15 deg) during the stand.
"""
import sys
import numpy as np
import mujoco


def point_in_polygon(p, poly):
    """Ray-crossing test, poly as ordered (x, y) rows."""
    inside = False
    n = len(poly)
    for i in range(n):
        (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % n]
        if (y1 > p[1]) != (y2 > p[1]) and p[0] < (x2 - x1) * (p[1] - y1) / (y2 - y1) + x1:
            inside = not inside
    return inside


def main(path, render=None, seconds=3.0):
    m = mujoco.MjModel.from_xml_path(path)
    d = mujoco.MjData(m)
    mujoco.mj_resetDataKeyframe(m, d, 0)
    mujoco.mj_forward(m, d)
    print(f'{path}: {m.nbody - 1} bodies, {m.njnt} joints, {m.nu} actuators, {m.nmesh} meshes, {m.ngeom} geoms')
    total = 0.0
    for b in range(1, m.nbody):
        name = mujoco.mj_id2name(m, mujoco.mjtObj.mjOBJ_BODY, b)
        print(f'  {name:22s} {m.body_mass[b]*1000:7.1f} g  principal inertia {np.round(m.body_inertia[b]*1e7, 2)} g cm2')
        total += m.body_mass[b]
    com = d.subtree_com[1].copy()                                    # torso subtree = the whole robot
    feet = [d.site_xpos[mujoco.mj_name2id(m, mujoco.mjtObj.mjOBJ_SITE, f'{s}_foot')][:2]
            for s in ('rear_right', 'front_right', 'front_left', 'rear_left')]   # ordered round the polygon
    inside = point_in_polygon(com[:2], feet)
    print(f'total {total*1000:.1f} g | CoM world x {com[0]:.4f} y {com[1]:.4f} z {com[2]:.4f} m | '
          f'feet xy {np.round(np.array(feet), 3).tolist()} | CoM inside support polygon: {inside}')
    z0 = d.qpos[2]
    ok = inside
    steps = int(seconds / m.opt.timestep)
    for i in range(steps):
        mujoco.mj_step(m, d)
    adr = m.sensor_adr[mujoco.mj_name2id(m, mujoco.mjtObj.mjOBJ_SENSOR, 'upvector')]
    up = d.sensordata[adr:adr + 3]
    tilt = np.degrees(np.arccos(np.clip(up[2], -1, 1)))
    drop = (z0 - d.qpos[2]) * 1000
    qmax = np.degrees(np.abs(d.qpos[7:])).max()
    stood = drop < 30 and tilt < 15
    print(f'stand {seconds:g} s at zero control: torso height {z0:.4f} -> {d.qpos[2]:.4f} m (drop {drop:.1f} mm), '
          f'IMU tilt {tilt:.1f} deg, max |joint| {qmax:.1f} deg, contacts {d.ncon}: {"STANDS" if stood else "FELL"}')
    ok = ok and stood
    if render:
        from PIL import Image
        cam = mujoco.MjvCamera()
        cam.type = mujoco.mjtCamera.mjCAMERA_FREE
        cam.lookat[:] = [com[0], 0, 0.10]
        cam.distance, cam.azimuth, cam.elevation = 0.6, 150, -18
        opt = mujoco.MjvOption()
        opt.geomgroup[:] = 0
        opt.geomgroup[0] = opt.geomgroup[1] = 1                         # floor/feet and visual meshes; hide the torso box (group 3)
        with mujoco.Renderer(m, 720, 960) as r:
            r.update_scene(d, cam, opt)
            Image.fromarray(r.render()).save(render)
        print('rendered', render)
    return ok


if __name__ == '__main__':
    args = sys.argv[1:]
    render = args[args.index('--render') + 1] if '--render' in args else None
    seconds = float(args[args.index('--seconds') + 1]) if '--seconds' in args else 3.0
    sys.exit(0 if main(args[0], render, seconds) else 1)
