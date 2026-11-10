# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Rebuild this exact revision in FreeCAD; canonical Python dependencies are
in the immutable sources/4b63c47db7e3590dd09bcc79fb98eb584f9a2e695e4738f2d99379e83c384ac1/koala_hardware snapshot.
Run with hardware/freecad-run PATH or execute in FreeCAD's Python console:
    p = r"<absolute path to this file>"
    exec(compile(open(p).read(), p, "exec"), {"__name__": "__main__", "__file__": p})
The script creates a new document. It never closes an existing GUI document.
"""
from pathlib import Path
import sys

SOURCE_REVISION = '4b63c47db7e3590dd09bcc79fb98eb584f9a2e695e4738f2d99379e83c384ac1'
MODEL = {'kind': 'part', 'name': 'forearm_left', 'builder': 'koala_hardware.parts.front:build_forearm', 'hand': 'left', 'version': 5}

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
