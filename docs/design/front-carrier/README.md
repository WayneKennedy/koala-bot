# Front carrier — flat-back study

2026-09-10. **Historical candidate snapshot, now superseded by DEC-49/50 production CAD.**
The common flat-back approach is implemented without the historical bevel in
`root_carrier_left/right`, two of each hand at front and rear; current status and exports are linked from
the [part review](../../part-design-review.md).

[Comparison PNG](comparison.png) · [Candidate STEP](flat-back-candidate.step) ·
[Candidate STL](flat-back-candidate.stl) ·
[Current print orientation STL](current-print-orientation.stl) ·
[Measured results and clearance scope](study.json).

The candidate fills the 8.115 mm bridge-to-socket step to provide a shared
flat back. Its head-facing chamfer preserves clearance at the six sampled
pose/pitch combinations. Joint interfaces and centres are unchanged. Bed
contact is 1,797 mm² versus 575 mm²; print height is 50.5 mm versus 88.1 mm.
The current and candidate STLs use their respective print orientations.
Place the minimum Z face on the bed; no packed plate or sliced file is supplied.

This is a valid single solid with a watertight mesh, not a successful print.
Six added-material collision checks do not establish full joint travel,
tool access or strength. Resolve the revised enclosing socket and inspect
layers before integrating the candidate into production CAD.

The study images and measurements are retained unchanged. Use the production
exporter for the revised parts; the superseded candidate builder is retired.

Koala-derived study geometry: CERN-OHL-S-2.0, as the production source.
