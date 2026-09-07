# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Repeatable nominal-geometry checks, not certification or continuous CCD.

Run: uv run python -m koala_hardware.audit
"""
import itertools
from build123d import Align, Cylinder, Plane, Pos, Rot, mirror
from . import assembly as A, params as P
from .parts import hip_link as H, thigh as T, all_builders, pelvis


def volume_overlap(a, b):
    aa, bb = a.bounding_box(), b.bounding_box()
    if any(getattr(aa.max, k) <= getattr(bb.min, k) + 1e-6 or
           getattr(bb.max, k) <= getattr(aa.min, k) + 1e-6 for k in "XYZ"):
        return 0.0
    return sum(s.volume for s in (a & b).solids())


def screw_heads():
    """Proud M3 cap head envelopes; no invented thread engagement."""
    head = Cylinder(P.CAP_M3_DIA / 2, P.CAP_M3_H,
                    align=(Align.CENTER, Align.CENTER, Align.MIN))
    items = []
    sq = P.SERVO_DRIVE_SQ / 2
    for a, b in itertools.product((-sq, sq), repeat=2):
        items += [
            ("head_roll_drive", Pos(H.DRIVE_X + H.T, a, b) * Rot(Y=90) * head, "", "roll"),
            ("head_roll_idler", Pos(H.IDLER_X - H.T, a, b) * Rot(Y=-90) * head, "", "roll"),
            ("head_pitch_drive", Pos(P.HIP_PITCH_X + a, T.DRIVE_Y + T.T,
             -P.HIP_PITCH_DROP + b) * Rot(X=-90) * head, "", "pitch"),
            ("head_pitch_idler", Pos(P.HIP_PITCH_X + a, T.IDLER_Y - T.T,
             -P.HIP_PITCH_DROP + b) * Rot(X=90) * head, "", "pitch"),
        ]
    for y, z in H.BOLTS:
        items.append(("head_carrier", Pos(H.DRIVE_X + H.T, y, z) *
                      Rot(Y=90) * head, "", "roll"))
        # Conservative cylindrical nut envelope, 6.4 mm across corners.
        nut = Cylinder(3.2, 3, align=(Align.CENTER, Align.CENTER, Align.MIN))
        items.append(("nut_carrier", Pos(H.IDLER_X - H.T, y, z) *
                      Rot(Y=-90) * nut, "", "roll"))
    for x in H.POST_X:
        items.append(("head_cap", Pos(x, P.HIP_PITCH_Y, H.TOP_Z + 4) * head, "", "roll"))
    return items


def posed(items, roll, pitch, side=1):
    pt = (Pos(P.HIP_PITCH_X, 0, -P.HIP_PITCH_DROP) * Rot(Y=pitch) *
          Pos(-P.HIP_PITCH_X, 0, P.HIP_PITCH_DROP))
    out = []
    for name, solid, _, group in items:
        if group == "pitch":
            solid = pt * solid
        if group != "fixed":
            solid = Rot(X=roll) * solid
        if side == -1:
            solid = mirror(solid, Plane.XZ)
        out.append((name, Pos(0, side * P.HIP_ROLL_Y, A.ROLL_Z) * solid))
    return out


def is_print(name):
    return name.startswith(("hip_", "thigh_")) or name == "pelvis"


def main():
    for builder in all_builders():
        s = builder()
        assert s["part"].is_valid, s["name"]
        assert s.get("multi_body") or len(s["part"].solids()) == 1, s["name"]
        size = (s["orientation"] * s["part"]).bounding_box().size
        assert all(0 < v <= 200.001 for v in size), (s["name"], size)
    # Probe the ENTIRE roll/thigh horn plate, not merely nominal cutter depth.
    for builder, transform in [
        (H.build_drive, Pos(H.DRIVE_X, 0, 0) * Plane.YZ.location),
        (H.build_idler, Pos(H.IDLER_X-H.T, 0, 0) * Plane.YZ.location),
        (T.build_outer, Pos(0, T.DRIVE_Y+T.T, 0) * Plane.XZ.location),
        (T.build_inner, Pos(0, T.IDLER_Y, 0) * Plane.XZ.location),
    ]:
        solid = builder()["part"]
        for a, b in itertools.product((-P.SERVO_DRIVE_SQ/2, P.SERVO_DRIVE_SQ/2), repeat=2):
            probe = transform * Pos(a, b) * H.hole(P.SERVO_DRIVE_SCREW/2-.02, 5)
            assert volume_overlap(solid, probe) < .001, builder.__name__
    print("PASS topology, bed bounds, and 16 full-depth horn-hole probes", flush=True)
    local = A.leg_parts() + screw_heads()
    deck = ("pelvis", pelvis.build()["part"])
    failures = []
    rolls = [P.ROLL_TEST_DEG * f for f in (-1, -.5, 0, .5, 1)]
    pitches = [P.PITCH_TEST_DEG * f for f in (-1, -.5, 0, .5, 1)]
    poses = list(itertools.product(rolls, pitches))
    min_gap = float("inf")
    for roll, pitch in poses:
        items = [deck] + posed(local, roll, pitch)
        for (a, p), (b, q) in itertools.combinations(items, 2):
            if not (is_print(a) or is_print(b)):
                continue
            v = volume_overlap(p, q)
            if v > .01:
                failures.append((roll, pitch, a, b, round(v, 3)))
        if roll == 0:
            for (a, p), (b, q) in itertools.product(items, repeat=2):
                if a.startswith("hip_") and b.startswith("thigh_"):
                    min_gap = min(min_gap, p.distance_to(q))
        print(f"checked local roll {roll:+} pitch {pitch:+}", flush=True)
    # Both inward motors, including unequal pitch. Other opposing-leg shapes
    # are screened too, rather than assuming mirrored neutral proves clearance.
    cross = [i for i in local if not i[0].startswith(("head_", "nut_"))]
    for rp, lp in itertools.product((-P.PITCH_TEST_DEG, 0, P.PITCH_TEST_DEG), repeat=2):
        right = posed(cross, -P.ROLL_TEST_DEG, rp, 1)
        left = posed(cross, -P.ROLL_TEST_DEG, lp, -1)
        for (a, p), (b, q) in itertools.product(right, left):
            v = volume_overlap(p, q)
            if v > .01:
                failures.append(("cross", rp, lp, a, b, round(v, 3)))
    if min_gap < 2.0:
        failures.append(("hip/thigh sampled gap below 2 mm", min_gap))
    if failures:
        for fail in failures:
            print("FAIL", fail)
        raise SystemExit(1)
    print("PASS 25 local poses incl. nominal cap heads; 9 opposing-leg poses.")
    print(f"Minimum sampled printed hip/thigh gap: {min_gap:.2f} mm")
    print("NOT checked: continuous motion, measured idler/cables, thread engagement, "
          "tool approach, complete fasteners, sliced layers, loads or creep.")


if __name__ == "__main__":
    main()
