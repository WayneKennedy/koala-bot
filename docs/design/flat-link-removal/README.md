# Flat-link removal study — rejected, unprinted (2026-10-01)

**Historical study:** the owner subsequently selected the 20.8 mm additive
profile with restricted bend travel. [Current revision](../flat-links/README.md).
The 16 mm removal-only trial remains rejected. The chronology below records
its evaluation before that selection.

The owner requested a **removal-only** change with printed strength retained.
At this stage the additive draft was withdrawn; production Python, ledger and
part renders were restored to benchmark `9e6ded8`. No upper-arm modification
or motion-limit change was made during this removal-only trial. The benchmark itself has no physical
strength validation for these links.

## Geometry and result

The benchmark has 20.8 mm-deep horn surrounds and stem, a 16 mm fork neck,
and a 12 mm-deep TPU key. Filling the neck was the assistant's error. A
removal-only trim to the neck's 16 mm depth has been evaluated for both the
90 mm rear and 100 mm front links. It is **not accepted for printing**.

- Boolean added volume is zero; both results are valid single solids and closed meshes.
- Head recesses extend to Y = ±8.15 mm (4.95 mm offset + 3.2 mm radius).
  Cutting to Y = ±8 mm opens each recess rim by 0.15 mm. This removes the wall
  around part of the recess; it does not mean the complete screw bearing web
  is severed.
- At the straight stem, 20 mm before the pad centre, the section changes from
  18 × 20.8 mm to 18 × 16 mm. Solid area falls 23.1%; section modulus about X
  falls **40.8%**, about Y 23.1%; second moment about X falls 54.5%.
  At equal bending moment, homogeneous beam nominal stress about X would rise
  69%. These are local geometric ratios, not a prediction of total part failure
  load, FFF strength, joint compliance or a safety factor.
- The unchanged 12 mm key is still recessed from the new faces. Therefore the
  cut does not create uniform faces through the terminal key either.
- **Visual gate: rejected.** Reviewed multi-view images show clipped horn
  surrounds and open screw-pocket rims. No manufacturing export, assembly
  update or released part version follows this study.

At the time of this study the intended shoulder remained unresolved. The
subsequent selection above supersedes that removal-only design direction.

## Files and reproduction

[Python generator](removal_study.py) uses the immutable FreeCAD benchmark
source snapshot identified in [strength-screen.json](strength-screen.json).
Run from the repository root:

```sh
hardware/freecad-run docs/design/flat-link-removal/removal_study.py
```

| Rejected trial | Native FreeCAD history | Multi-view |
|---|---|---|
| Rear, 90 mm, trimmed to 16 mm | [FCStd](removal_trial_L90_D16.FCStd) | [PNG](removal_trial_L90_D16-views.png) |
| Front, 100 mm, trimmed to 16 mm | [FCStd](removal_trial_L100_D16.FCStd) | [PNG](removal_trial_L100_D16-views.png) |

The restored benchmark passes all **76 tests**, including the original 120°
front elbow check (`hardware/build/removal-baseline-tests.log`). Both native
study documents pass save/reopen/full recompute. They are design studies,
not additions to the released-part manifest. The JSON records the generator
hash, frozen source hash, kernel geometry, section values and printability
surface screen. These do not substitute for inspecting actual sliced walls.

## Original versus additive draft at 120° elbow fold

Owner requested the original stepped link in the collision review pose and
noted that both forks retain **36.4 mm inner spacing**. That spacing is along
native X. The additive draft expanded the neck along native Y from ±8 to
±10.4 mm; these are independent dimensions.

[Original-pose Python](original_elbow_120.py) and its
[native FreeCAD document](original_elbow_120.FCStd) reproduce the 100 mm front
forearm v2 against upper arm v2 at `Translate Z70 * Rotate X120`. This is the
front lower link involved in the elbow review, not the 90 mm rear installation.
[Original clearance report](original-elbow-clearance.json).

| Same upper arm and 120° pose | Plastic overlap | Minimum separation |
|---|---|---|
| Original stepped forearm v2 | 0 mm³ | 0.51305 mm |
| Withdrawn additive draft | 34.08149 mm³ | Intersecting |

[Original image](original-elbow-120.png) and
[additive image](additive-elbow-120.png) use the same camera. The blue lower
link is translucent; the grey upper arm is unchanged. Red patches identify
additive-draft interference. [Contact-point checks](elbow-comparison.json)
place one interior point in each interference patch: both points lie inside
the upper arm and additive draft, and outside the original lower link. In
lower-link coordinates they lie near Y = −9.8 mm, beyond the old −8 mm neck
face and inside the added material. Thus the unchanged 36.4 mm fork spacing
does not rule out this new contact. This is a static plastic-to-plastic check,
not proof of whole-robot travel, print clearance or loaded movement.

## Printed strength: not verified

No tested material allowables, calibrated orthotropic FEA or physical load
results exist for this change. FFF strength depends on orientation and printed
structure; [Prusa's modelling guidance](https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135)
explains directional strength, and its [infill guidance](https://help.prusa3d.com/article/infill_42)
identifies perimeters as a major strength contributor. More infill cannot be
assumed to compensate for the removed geometry.

For an eventual acceptable cut, compare baseline and revision using the same
printer, PETG batch/profile, orientation and perimeter/infill settings. Inspect
sliced load-bearing walls and horn-pocket rims, then test the assembled horn
and pad interfaces under axial, both bending directions and torsional loads,
including sustained load/creep. Establish the working/proof loads from the
agreed robot duty first. Record exact print versions, loads, durations,
deflections and damage in the test log. Until then, strength remains unknown.
