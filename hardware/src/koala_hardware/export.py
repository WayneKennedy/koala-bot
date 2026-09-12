# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Build current STEP/STL parts, four-view PNGs and the generated chassis BOM.

Usage:  uv run python -m koala_hardware.export [name-filter]
Outputs: build/stl/*.stl, build/renders/*.png, build/manifest.txt
The build FAILS (exit 1) if any part exceeds the print bed in its declared
print orientation, has an undeclared support need, or violates a critical assembly datum.
DEC-39 allows explicitly declared supports; surface screens remain advisory.
"""
import hashlib
from collections import Counter
import json
import sys
import pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import trimesh
from build123d import export_stl, export_step, mirror, Plane, Pos
from . import params as P
from . import printability as PR
from . import validation
from .meshing import export_mesh
from .parts import all_builders

ROOT = pathlib.Path(__file__).resolve().parents[2]
STL = ROOT / "build" / "stl"
REN = ROOT / "build" / "renders"
STEP = ROOT / "build" / "step"


def render(mesh: trimesh.Trimesh, path: pathlib.Path, title: str):
    fig = plt.figure(figsize=(10, 8))
    views = [(30, -60, "iso"), (0, -90, "side"), (0, 0, "front"), (90, -90, "top")]
    for i, (elev, azim, label) in enumerate(views, 1):
        ax = fig.add_subplot(2, 2, i, projection="3d")
        tris = mesh.vertices[mesh.faces]
        pc = Poly3DCollection(tris, alpha=1.0, facecolor="#8fb4d9",
                              edgecolor="#2a4a6a", linewidth=0.15)
        ax.add_collection3d(pc)
        lo, hi = mesh.bounds
        c, r = (lo + hi) / 2, max(hi - lo) / 2 * 1.1
        ax.set_xlim(c[0] - r, c[0] + r)
        ax.set_ylim(c[1] - r, c[1] + r)
        ax.set_zlim(c[2] - r, c[2] + r)
        ax.set_title(label, fontsize=9)
        ax.view_init(elev=elev, azim=azim)
        ax.set_axis_off()
    fig.suptitle(title)
    fig.tight_layout()
    fig.savefig(path, dpi=90)
    plt.close(fig)


def prune(current: set[str]) -> list[str]:
    """Delete outputs for parts that no longer exist under that name.

    A renamed part otherwise leaves its old STL sitting beside the new one,
    and a stale file slices just as happily as a current one.
    """
    keep = current | {"koala-quadruped", "koala-upright"}
    removed = []
    for folder, ext in ((STL, ".stl"), (REN, ".png"), (STEP, ".step")):
        for f in folder.glob(f"*{ext}"):
            if f.stem not in keep:
                f.unlink()
                removed.append(f.name)
    return removed


DENSITY = {"PETG": 1.27, "TPU": 1.2}  # g/cm3; TPU value provisional, matching review slice
BOM_BEGIN = "<!-- BEGIN GENERATED: printed parts -->"
BOM_END = "<!-- END GENERATED -->"


def _secs(t: str) -> int:
    """'3h 46m 5s' -> seconds."""
    total, num = 0, ""
    for ch in t:
        if ch.isdigit():
            num += ch
        elif ch in "hms" and num:
            total += int(num) * {"h": 3600, "m": 60, "s": 1}[ch]
            num = ""
    return total


def _hm(seconds: float) -> str:
    return f"{int(seconds // 3600)}h {int(seconds % 3600 // 60):02d}m"


def write_bom(bom: list[dict]) -> bool:
    """Rewrite the generated block in docs/bom.md. Returns False if the doc or
    its markers are missing (a filtered build simply skips this)."""
    doc = ROOT.parent / "docs" / "bom.md"
    if not doc.exists():
        return False
    text = doc.read_text()
    if BOM_BEGIN not in text or BOM_END not in text:
        return False

    cache_file = ROOT / "build" / "slice-cache.json"
    raw_sliced = (json.loads(cache_file.read_text()) if cache_file.exists() else {})
    # A name-only cache silently lies after geometry changes. Trust a slice
    # only when it records the exact STL bytes it measured.
    sliced = {}
    for name, result in raw_sliced.items():
        path = STL / f"{name}.stl"
        if path.exists() and result.get("sha256") == hashlib.sha256(
                path.read_bytes()).hexdigest():
            sliced[name] = result

    rows = ["| Part | Qty | Printable | Material | Size (mm) | Filament | Print time | Print notes |",
            "|------|-----|-----------|----------|-----------|----------|-----------|-------------|"]
    tot_vol = tot_qty = tot_secs = 0
    tot_solid = 0.0
    tot_mass = tot_solid_mass = 0.0
    for r in sorted(bom, key=lambda r: (r["name"].startswith("coupon"),
                                        r["name"])):
        sx, sy, sz = r["size"]
        density = DENSITY[r.get("material","PETG")]
        note = [] if r["ok"] else ["**FAILS CHECK**"]
        # Tall on a small footprint: worth a brim regardless of adhesion luck.
        if r["bed_area"] < PR.MIN_BED_AREA:
            note.append("small contact area; brim / grouped placement")
        elif r["bed_area"] < 1500 and r["size"][2] > 50:
            note.append("brim (tall, small footprint)")
        if r["overhang"] > 0:
            note.append(f"{r['overhang']:.0f} mm2 flagged overhang; inspect slice")

        s = sliced.get(r["name"])
        if s:
            fil = f"{s['cm3'] * density * r['qty']:.0f} g"
            tim = s["time"]
        else:
            fil = f"~{r['vol'] * density * r['qty']:.0f} g (solid max)"
            tim = "-"
        rows.append(f"| `{r['name']}` | {r['qty']} | {r.get('printable', 'unknown')} | {r.get('material', 'PETG')} | {sx:.0f} x {sy:.0f} x "
                    f"{sz:.0f} | {fil} | {tim} | "
                    f"{'; '.join(note) if note else 'clean'} |")
        if not r["name"].startswith("coupon"):
            tot_qty += r["qty"]
            tot_solid += r["vol"] * r["qty"]
            tot_solid_mass += r["vol"] * density * r["qty"]
            if s:
                tot_vol += s["cm3"] * r["qty"]
                tot_mass += s["cm3"] * density * r["qty"]
                tot_secs += _secs(s["time"]) * r["qty"]
    structural_names = {r["name"] for r in bom
                        if not r["name"].startswith("coupon")}
    all_structural_sliced = structural_names <= sliced.keys()
    if all_structural_sliced:
        total_filament = f"{tot_mass:.0f} g"
        total_time = _hm(tot_secs)
    else:
        total_filament = f"~{tot_solid_mass:.0f} g (solid max)"
        total_time = "-"
    rows.append(f"| **Structural total** | **{tot_qty}** | | | | "
                f"**{total_filament}** | **{total_time}** | |")

    hardware = Counter()
    for r in bom:
        if not r['name'].startswith('coupon'):
            hardware.update({key: count*r['qty'] for key, count in r.get('fasteners', {}).items()})
    rows += ['', '**Four-limb chassis fastening schedule, derived from the same builders.** '
             'Candidate lengths require rig checks; excludes coupon hardware, '
             'head/neck mechanisms and supplier-specific wheel/hub fixings.', '',
             '| Fastener / interface hardware | Qty |', '|---|---:|']
    rows += [f'| {key} | {count} |' for key,count in sorted(hardware.items())]

    if sliced:
        preamble = (f"Figures with a matching STL hash are **slicer estimates** using "
                    f"the recorded PETG/TPU review settings "
                    f"(`docs/design/manufacturing/slices.json`); changed or unsliced "
                    f"parts fall back to a labelled solid-geometry upper "
                    f"bound. All structural parts printed solid would be "
                    f"{tot_solid_mass:.0f} g.")
    else:
        preamble = ("No current hash-matched slice results, so filament is the "
                    "**solid-geometry upper bound**, not a print setting. "
                    "Run `koala_hardware.slice_remote` for "
                    "measured figures.")

    block = (f"{BOM_BEGIN}\n\n*Generated by `koala_hardware.export` - do not "
             f"hand-edit. Coupons are excluded from the total.*\n\n"
             f"{preamble}\n\n" + "\n".join(rows) + f"\n\n{BOM_END}")
    start = text.index(BOM_BEGIN)
    end = text.index(BOM_END) + len(BOM_END)
    doc.write_text(text[:start] + block + text[end:])
    return True


def main():
    name_filter = sys.argv[1] if len(sys.argv) > 1 else ""
    layout = validation.check_layout()
    print(f"[OK  ] assembly layout: {', '.join(layout)}")
    STL.mkdir(parents=True, exist_ok=True)
    REN.mkdir(parents=True, exist_ok=True)
    STEP.mkdir(parents=True, exist_ok=True)
    failures, lines = [], []

    built, bom = [], []
    for builder in all_builders():
        spec = builder()
        assert spec["part"].is_valid, spec["name"]
        solid_count = len(spec["part"].solids())
        if solid_count != 1 and not spec.get("multi_body", False):
            raise ValueError(
                f"{spec['name']} contains {solid_count} disconnected solids")
        handed = spec.get("handed", False)
        qty = spec.get("qty", 1)
        oriented = spec["orientation"] * spec["part"]
        # A handed part needs a real mirrored STL, not "remember to flip it in
        # the slicer". Mirroring about a vertical plane preserves Z, so the
        # print orientation and its metrics carry over unchanged.
        variants = ([(f"{spec['name']}_right", oriented),
                     (f"{spec['name']}_left", mirror(oriented, Plane.XZ))]
                    if handed else [(spec["name"], oriented)])
        built += [n for n, _ in variants]
        if name_filter and name_filter not in spec["name"]:
            continue

        for name, solid in variants:
            solid = Pos(0, 0, -solid.bounding_box().min.Z) * solid
            bb = solid.bounding_box()
            size = (bb.size.X, bb.size.Y, bb.size.Z)
            fits = (size[0] <= P.BED_X and size[1] <= P.BED_Y
                    and size[2] <= P.BED_Z)
            stl_path = STL / f"{name}.stl"
            mesh = export_mesh(solid, stl_path)
            export_step(solid, str(STEP / f"{name}.step"))
            if not mesh.is_watertight or mesh.volume <= 0:
                raise ValueError(f"{name}: STL is not a closed positive-volume mesh")
            render(mesh, REN / f"{name}.png", name)
            printable, verdict, m = PR.check(mesh)
            # DEC-39 permits explicitly declared local supports / brim. Report the
            # surface screen, but do not force artificial structural seams.
            supported = spec.get("supports", False)
            ok = fits and (printable or supported)
            if not printable and supported:
                verdict += "; declared supports/brim — inspect slice"
            status = "OK  " if ok else "FAIL"
            line = (f"[{status}] {name:22s} printable={spec.get('printable', 'unknown')} {spec.get('material','PETG')}  {size[0]:6.1f} x {size[1]:6.1f} x "
                    f"{size[2]:6.1f} mm  {mesh.volume / 1000:6.1f} cm3  "
                    f"bed {m['bed_area']:7.0f}  overhang "
                    f"{m['overhang_area']:7.0f}"
                    f"  {'' if fits else 'EXCEEDS BED; '}{verdict}")
            print(line)
            if not printable and not supported:
                alts = ", ".join(f"{n}(oh {o:.0f}, bed {b:.0f})"
                                 for n, o, b in PR.best_orientations(mesh))
                print(f"         better orientations: {alts}")
                line += f"\n    better orientations: {alts}"
            lines.append(line + "\n    " + spec["notes"])
            bom.append({"name": name, "qty": qty, "size": size,
                        "vol": mesh.volume / 1000, "ok": ok,
                        "printable": spec.get("printable","unknown"),
                        "material": spec.get("material","PETG"),
                        "overhang": m["overhang_area"],
                        "bed_area": m["bed_area"],
                        "fasteners": spec.get("fasteners", {})})
            if not ok:
                failures.append(name)

    orphans = prune(set(built))
    if orphans:
        print(f"\npruned stale output for renamed/removed parts: "
              f"{', '.join(sorted(orphans))}")

    if not name_filter and write_bom(bom):
        print("updated docs/bom.md (printed parts)")

    (ROOT / "build" / "manifest.txt").write_text("\n".join(lines) + "\n")
    if failures:
        print(f"\nFAILURES (bed fit / surface geometry screen): {failures}")
        sys.exit(1)


if __name__ == "__main__":
    main()
