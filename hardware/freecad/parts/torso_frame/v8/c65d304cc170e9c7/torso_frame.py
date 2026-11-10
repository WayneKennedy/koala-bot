# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Rebuild this exact revision in FreeCAD; canonical Python dependencies are
in the immutable sources/c65d304cc170e9c7323880f85990d8f047ad8badc36fdb618e76acf6f62b4b0d/koala_hardware snapshot.
Run with hardware/freecad-run PATH or execute in FreeCAD's Python console:
    p = r"<absolute path to this file>"
    exec(compile(open(p).read(), p, "exec"), {"__name__": "__main__", "__file__": p})
The script creates a new document. It never closes an existing GUI document.
"""
from pathlib import Path
import sys

SOURCE_REVISION = 'c65d304cc170e9c7323880f85990d8f047ad8badc36fdb618e76acf6f62b4b0d'
MODEL = {'kind': 'part', 'name': 'torso_frame', 'builder': 'koala_hardware.parts.torso:build', 'hand': 'none', 'version': 8, 'status': 'Superseded review: local fillet bulge obstructed lateral cassette removal; corrected in v9.'}

if __name__ == "__main__":
    here = Path(__file__).resolve()
    root = next(p for p in here.parents if (p / "sources" / SOURCE_REVISION).is_dir())
    # FreeCAD's interpreter persists between runs: load the archived revision,
    # not another revision's cached Python modules. Existing documents remain open.
    for name in list(sys.modules):
        if name == "koala_hardware" or name.startswith("koala_hardware."):
            del sys.modules[name]
    sys.path.insert(0, str(root / "sources" / SOURCE_REVISION))
    from koala_hardware.freecad_build import replay
    replay(here, MODEL, SOURCE_REVISION)
