# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Rebuild this exact revision in FreeCAD; canonical Python dependencies are
in the immutable sources/44ed687d14e1a9e410c6bef1f9b3ff46079a8fb87fed5ec9a0d3ea60ec658c98/koala_hardware snapshot.
Run with hardware/freecad-run PATH or execute in FreeCAD's Python console:
    p = r"<absolute path to this file>"
    exec(compile(open(p).read(), p, "exec"), {"__name__": "__main__", "__file__": p})
The script creates a new document. It never closes an existing GUI document.
"""
from pathlib import Path
import sys

SOURCE_REVISION = '44ed687d14e1a9e410c6bef1f9b3ff46079a8fb87fed5ec9a0d3ea60ec658c98'
MODEL = {'kind': 'assembly', 'name': 'koala-walking', 'pose': 'walking'}

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
