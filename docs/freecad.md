# Native FreeCAD CAD — DEC-63

Python is the source of truth. FreeCAD documents are generated, inspectable
collaboration artefacts; carry GUI changes back into Python before releasing a
revision. [Decision](decisions.md) · [current geometry](cad-integrated-design.md) ·
[version/printability rules](part-design-review.md).

Conversion benchmark: Git `9e6ded8`, before the flat-depth lower-link
change. Superseded STEP exports under `docs/design/` are removed from the working
tree and retained in Git history; their links now open converted FCStd references.
Vendor originals and frozen `reference-sources/` inputs remain required for
reproducible Python replays. Simulation meshes remain runtime assets. Future
STEP exports under `docs/design/` are local, ignored derivatives.

Current lower-link revision and maximum-bend assemblies:
[20.8 mm footed links](design/flat-links/README.md).

## Build and open

From `hardware/`, with FreeCAD installed:

```sh
# FreeCAD supplies its own Python, Part, Sketcher, NumPy and Matplotlib.
# Install this pure-Python dependency into the directory the launcher exposes:
uv pip install --target build/freecad-python --no-deps 'trimesh==5.1.0'
./freecad-run -m koala_hardware.freecad_build
./freecad-run -m koala_hardware.freecad_build --check
./freecad-run -m unittest discover -s tests
```

`freecad-run` uses `FREECAD_CMD`, an installed `FreeCADCmd`/`freecadcmd`, or the
`org.freecad.FreeCAD` Flatpak. It propagates failures as a nonzero process exit.
The workstation build uses FreeCAD 1.1.3 / OCCT 7.8.1. Other versions must pass
the same checks; kernel upgrades can change topology and corner blends.
The tested interpreter is Python 3.13.15 with NumPy 2.4.4, Matplotlib 3.9.4 and
Trimesh 5.1.0. FreeCAD supplies the first two libraries; the launcher adds Trimesh.
Flatpak cannot see files created in the host's `/tmp`; use paths under the
checkout when passing files from the host.
Viewer cache generation requires Node.js on the host (`NODE_CMD` can name its
absolute executable path). Local slicing requires host PrusaSlicer. The launcher
provides a short-lived authenticated helper connection for those two commands
when FreeCAD runs in Flatpak; it closes when the build exits.

Open an FCStd listed in [`hardware/freecad/manifest.json`](../hardware/freecad/manifest.json).
The walking, quadruped and upright assemblies have separately selectable named
components and a References group. They are inspection poses, not a constraint
solver or a validated movement trajectory. Part documents use native design
frames; STL exports retain their separately declared bed orientations. A `_left`
part is a mirrored design-frame counterpart; `export.py` mirrors **after** print
orientation, retaining the established manufacturing convention.

## Source and revision layout

- `hardware/src/koala_hardware/parts/`: current part recipes; `params.py` holds
  the shared dimensions. Existing modelling expressions now call `cad.py`, a
  small FreeCAD-native geometry vocabulary, with no build123d/OCP dependency.
- `hardware/freecad/parts/<design>/vN/<source-hash>/<handed-name>.py` and
  `.FCStd`: immutable revision pair. Geometry versions remain the physical-print
  versions in `part-versions.json`; the source hash also distinguishes tooling
  changes that leave geometry unchanged.
- `hardware/freecad/sources/<sha256>/koala_hardware/`: frozen Python dependency
  closure, shared by that revision's scripts. These are historical snapshots;
  edit the current source, never an archived snapshot. A replay does not depend
  on the current builders or an external sibling checkout.
- `hardware/freecad/assemblies/` and `studies/`: native assembly and retained
  study revisions, including three kinematic body masters, the current/options/
  flat rear-leg comparisons in both wheeled poses, and carrier/mount studies.
  These replay retained generators with this revision's parameters; older STEP
  exports remain frozen separately. The five versioned link studies are under
  `parts/` and remain alternatives, not production prints.
- `hardware/freecad/references/`: the migration’s Git-tracked STEP assets, including historic
  exports and upstream templates, preserved as explicitly labelled imported
  references. Their original authoring histories cannot be recovered from STEP.
  Their Python scripts reproduce the import from `reference-sources/` and verify
  the frozen STEP hash. Original licensing/provenance follows the recorded source
  path in the repository. Current
  generators and the native part/assembly documents supply editable histories.
- `manifest.json`: pairing, source hashes, document hashes, versions, object/solid
  counts and runtime version. Builds reject modified archived files. Older
  revisions are retained; no automatic pruning of revision history.

The migration starts with current revisions and retained study generators. It
does not invent FCStd histories for earlier part versions absent from the
current source. Prior Python versions remain in Git; the migration baseline
records the exact commit used.

To replay an archived Python script, run `./freecad-run path/to/part.py`, or
use the `exec(compile(...))` invocation in its header in FreeCAD's console.
A GUI replay creates a **new unsaved document**, preserving existing open
models. Headless replay writes a separate `.rebuilt.FCStd`, which is ignored by
Git. Do not overwrite a release with a hand-edited GUI file. Inspect the changes,
update the current generator, bump the physical version for geometry changes,
and rebuild. No script automatically closes an existing GUI document.

## What is editable

The construction tree uses FreeCAD's **Part workbench**, with Sketcher profiles:
boxes, cylinders, cones, spheres, extrusions, lofts, boolean operations, fillets,
mirrors, compounds and placement links. It is a recomputable feature history,
not a fused STEP import and not a PartDesign Body. Primitive dimensions, extrusion
lengths, fillet radii and placements are editable through native properties.
Sketch profiles have explicit Block constraints: release the relevant constraint
before changing profile geometry. There is no claim that every dimension is
bound to a central spreadsheet or that arbitrary GUI edits preserve engineering
constraints. For PartDesign work, explicitly create a Body and a base feature.

`freecad_document.py` translates the retained construction graph into these
native objects and locates fillet edges by geometry rather than cached edge IDs.
Saved documents reopen and recompute without installing a custom Python feature
proxy. Readback validation checks object/sketch validity, zero sketch DoF,
conflicting/redundant constraints, solid counts, volume and bounds. Regression
tests also change a native cylinder radius and verify that the final saved
part recomputes.
Headless builds also save native view-state XML so files open with their final
parts visible and an isometric camera. This was verified in the installed GUI.

## Migration evidence and limits

[`hardware/freecad/migration/`](../hardware/freecad/migration/README.md) contains
the old ledger, compressed baseline solids and comparison report. The engine
changes from OCCT 7.9.3 (build123d) to FreeCAD's OCCT 7.8.1. Topology descriptors
are rebaselined explicitly as fingerprint schema 3; this is not blanket
permission to ignore future geometry changes.

The rounded **thigh v4** and **shoulder carrier v4** record small local
kernel-dependent corner-blend differences; both remain `unknown`/unprinted.
Their interfaces, link dimensions and declared print planes are retained.
Earlier v3 STL hashes/slices are historical evidence, not validation of v4.
The report supplies boolean differences, volumes, bounds and two-sided sampled
surface distances. Coincident curved-face boolean subtraction can fail even
when the skins agree; samples are supplementary evidence, not a proof of
continuous equality or loaded movement.

The browser viewer, meshes, STEP/STL export, MuJoCo generation and engineering
checks remain available through `freecad-run`. FreeCAD is the primary CAD
collaboration tool; the browser remains a secondary inspection tool. Regenerated
meshes acquire new hashes, so old slice records do not automatically validate
them even where geometry is unchanged.
Consequently the regenerated BOM and MuJoCo mass/inertia estimates currently
use the documented solid-density upper bounds until matching slices are recorded.

The workflow follows the sibling [wk-drones FreeCAD precedent](https://github.com/WayneKennedy/wk-drones/blob/main/AGENTS.md#cad-in-freecad).
Koala's implementation and required sources are checked in here; it does not
import that repository's helper. Native feature API background:
[FreeCAD Part scripting](https://github.com/FreeCAD/FreeCAD-documentation/blob/main/wiki/Part_scripting.md).
