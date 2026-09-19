# DEC-49/50 manufacturing evidence

All current STL variants have successful local slices and **`printable = assumed`**.
No physical print, fit, load test or validated TPU profile is claimed.
[Per-part orientation and support-removal review](../../part-design-review.md).

[Slice records](slices.json) identify each STL by SHA-256, its material, settings
hash, model-layer count, estimated filament/time and G-code hash. For each
part, `<part-name>-layers.png` shows four deposited-path sections: blue is the
part and orange is the nearest support layer (its separate Z is labelled). These PNGs open directly in iPad Files.

The shared printer profile is read from `../3d-printing/reference/`; it is not
copied into Koala. Project-specific overrides live in `hardware/print/`.
PETG uses snug supports **from the bed only** (`support_material_buildplate_only = 1`, the
house rule; plate 1 on 2026-09-19 was sliced without it and its M2 ear holes came out
blocked) and a brim; `manufacturing-petg-tree.ini` is the organic-support variant for the
v2 thigh and shank, one part per job. The TPU contact pad uses no
support; its taper avoids a flat cavity roof. TPU temperatures/feed remain
provisional until matched to the actual spool. G-code is a local review artefact
in `hardware/build/manufacturing/`, not a job submitted to the printer.

Regenerate locally from the repository root (requires PrusaSlicer):

```sh
uv run --directory hardware python -m koala_hardware.export
uv run --directory hardware python -m koala_hardware.manufacturing_slices
```

Supply `--profile /path/to/shared.ini` if the sibling checkout is elsewhere.
Re-export the BOM after slicing to include hash-matched estimates. Successful
slicing establishes an achievable toolpath, not reliable adhesion, clean
support removal, mechanical fit or strength in a physical print.
