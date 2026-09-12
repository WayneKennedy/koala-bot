# SO-101 socket and fork construction templates

[Photo supplied by the maintainer](IMG_7004.png) ·
[Template comparison PNG](template-comparison.png) ·
[Current-part inventory PNG](current-parts-review.png) ·
[Unequal drive/idler slot views](socket-slot-comparison.png) ·
[Slot measurements](socket-slots.json) ·
[Full engineering critique](../../part-design-review.md).

| Extract | Exact source geometry | Purpose |
|---|---|---|
| Enclosed servo-base socket | [STEP](upper_socket_source.step) · [STL](upper_socket_source.stl) | Floor, enclosing walls, entry reliefs, stepped pocket and ear-screw seats |
| Robust horn fork and root | [STEP](upper_fork_source.step) · [STL](upper_fork_source.stl) | Connected broad cheeks, rounded tips, root web and horn-hole details |

These are **reference templates**, not finished koala prints. Cropping isolates
regions of the source part; the cut planes are not proposed assembly seams.
No socket dimension, screw hole, fillet or load-bearing feature was resized.
The source geometry needs adaptation to the measured koala hardware stack,
compact clearance envelope and each part's print orientation.

Source: `Upper_arm_SO101.step`, TheRobotStudio/SO-ARM100,
[commit eecbe3e0a9ebb23e25ad7b2759b03884c6660903](https://github.com/TheRobotStudio/SO-ARM100/blob/eecbe3e0a9ebb23e25ad7b2759b03884c6660903/STEP/SO101/Upper_arm_SO101.step).
Its SHA-256 is
`efa19a6dd2ccb459248500c76629cfa840630e7e15d9e146394d31da1525dd61`;
the neighbouring checkout and our vendored copy match exactly.

The original STEP and derived STEP/STL geometry are **Apache-2.0**, copyright
the upstream contributors; [licence](../../../LICENSES/Apache-2.0.txt).
Changes to the derived assets are limited to clipping and rigid transforms.
The original remains unmodified in `hardware/vendor/so-arm100/SO101/`.
The photo is the maintainer's `../IMG_7004.HEIC`, converted to PNG for viewing.

## Coordinates and regeneration

Socket template: X is the output-axis direction, Y is case width and Z points
from servo Bottom to Top. The nominal pocket floor contact is Z=0. Fork
template: output axis is X, horn centre is the origin, and +Z points towards
the connecting body. The original flat print face is native STEP Y=0, with
+Y as build direction. These are distinct reference frames, recorded in
[template-study.json](template-study.json) along with crop planes, measured
features and the complete current-part orientation inventory.

From `hardware/`:

```sh
uv run python -m koala_hardware.so101_templates
```

This writes only the study assets in `docs/design/so101/`. It does not replace
production geometry, regenerate the printed BOM, or operate a slicer/printer.

## Two-piece socket and paired-root access — DEC-45

[Split-socket image](split-socket-reference.png) ·
[Root access evidence](root-access-study.json) ·
[Engineering assessment](../../root-servo-mounts.md).

- [Under-arm socket STEP](under_socket_source.step) / [STL](under_socket_source.stl):
  cropped from the original `Under_arm_SO101.step` at native X = −24.85 mm.
- [Wrist-holder STEP](wrist_holder_source.step) / [STL](wrist_holder_source.stl):
  the complete `Motor_holder_SO101_Wrist` shape, without resizing.

Both retain native upstream coordinates and the Apache-2.0 licence above.
The newly vendored wrist holder comes from the same pinned commit; its source
hash and provenance, plus both extract validations, are in `root-access-study.json`.
The displayed separation is illustrative, not a proven installation path.
These are references for a revised mount, not new production parts.

Regenerate from `hardware/` with:

```sh
uv run python -m koala_hardware.root_socket_access
```
