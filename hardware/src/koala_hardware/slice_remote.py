# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Slice every exported STL on the print host and cache the real figures.

The maintainer's printer (DEC-14) is an Ender-5 S1 running Klipper, driven
headlessly: PrusaSlicer CLI on the Pi with a fixed profile, reachable over
Tailscale. This asks that pipeline what each part *actually* costs, rather
than estimating from solid volume.

    uv run python -m koala_hardware.slice_remote [host]

Writes build/slice-cache.json, which `export` folds into docs/bom.md. It is
optional: with no cache the BOM simply omits the measured columns, so the CAD
build never depends on the printer being reachable.
"""
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
STL = ROOT / "build" / "stl"
CACHE = ROOT / "build" / "slice-cache.json"
DEFAULT_HOST = "wkenn@printhub"
PROFILE = "~/slicer/ender5s1_petg.ini"

REMOTE = r'''
mkdir -p /tmp/koala-slice && cd /tmp/koala-slice
for f in *.stl; do
  [ -e "$f" ] || continue
  n="${f%.stl}"
  prusa-slicer --load PROFILE --export-gcode --output "/tmp/koala-slice/$n.gcode" \
      "/tmp/koala-slice/$f" >/dev/null 2>&1
  if [ -f "/tmp/koala-slice/$n.gcode" ]; then
    v=$(grep -am1 "filament used \[cm3\]" "/tmp/koala-slice/$n.gcode" | sed "s/.*= *//")
    t=$(grep -am1 "estimated printing time (normal mode)" "/tmp/koala-slice/$n.gcode" | sed "s/.*= *//")
    echo "$n|$v|$t"
  else
    echo "$n|FAILED|"
  fi
  rm -f "/tmp/koala-slice/$n.gcode"
done
'''.replace("PROFILE", PROFILE)


def main():
    host = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_HOST
    stls = sorted(STL.glob("*.stl"))
    if not stls:
        sys.exit("no STLs in build/stl - run the export first")

    print(f"copying {len(stls)} STLs to {host} ...")
    subprocess.run(["ssh", host, "mkdir -p /tmp/koala-slice && rm -f /tmp/koala-slice/*.stl"],
                   check=True)
    subprocess.run(["scp", "-q", *[str(p) for p in stls],
                    f"{host}:/tmp/koala-slice/"], check=True)

    print("slicing (PETG profile on the print host) ...")
    out = subprocess.run(["ssh", host, REMOTE], capture_output=True, text=True,
                         check=True).stdout

    data = {}
    for line in out.strip().splitlines():
        name, vol, time = (line.split("|") + ["", ""])[:3]
        if vol == "FAILED" or not vol:
            print(f"  {name}: SLICE FAILED")
            continue
        data[name] = {"cm3": float(vol), "time": time.strip()}
        print(f"  {name}: {float(vol):.1f} cm3, {time.strip()}")

    CACHE.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
    print(f"wrote {CACHE.relative_to(ROOT)} - rerun the export to fold it "
          f"into docs/bom.md")


if __name__ == "__main__":
    main()
