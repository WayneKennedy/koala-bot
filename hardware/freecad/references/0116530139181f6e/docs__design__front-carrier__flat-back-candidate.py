# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Rebuild this exact revision in FreeCAD; canonical Python dependencies are
in the immutable sources/3c52315ce49d97f40a771f66ae916768eb8f4695231bf536658e58c5a67ac477/koala_hardware snapshot.
Run with hardware/freecad-run PATH or execute in FreeCAD's Python console:
    p = r"<absolute path to this file>"
    exec(compile(open(p).read(), p, "exec"), {"__name__": "__main__", "__file__": p})
The script creates a new document. It never closes an existing GUI document.
"""
from pathlib import Path
import sys

SOURCE_REVISION = '3c52315ce49d97f40a771f66ae916768eb8f4695231bf536658e58c5a67ac477'
MODEL = {'kind': 'reference', 'name': 'flat-back-candidate', 'source': 'docs/design/front-carrier/flat-back-candidate.step', 'source_sha256': '0116530139181f6e6ebccbbe3fa39074488339af1d921f57d504cba919b3be73', 'archived_source': 'reference-sources/0116530139181f6e6ebccbbe3fa39074488339af1d921f57d504cba919b3be73/flat-back-candidate.step'}

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
