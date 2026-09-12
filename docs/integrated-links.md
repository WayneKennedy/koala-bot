# Integrated limb structures — DEC-39

**DEC-45 root-mount exception:** pelvis/shoulder pitch servos require a
pair of independently removable socket modules because each servo blocks
its sibling's inboard screws. Fully fasten each servo off the robot, then attach
its module with accessible frame hardware;
[required assembly sequence](root-servo-mounts.md). This functional seam does
not change the one-main-print principle for limb links.

**DEC-49/50 refinement:** all four roots use a common unbevelled carrier, two
prints per hand. Shared sockets now preserve the 14/18.5 mm drive/idler slots.

**DEC-48 construction:** production sockets now have enclosing Side-wall
returns; links have rounded/tapered transitions. [The part review](part-design-review.md)
records each orientation and its assumed printability with local slice evidence.

**DEC-43 (2026-09-10):** rear wheels stay at the ankles; front drives are
replaced with integrated rounded feet. The knee-wheel detour is deferred.



The previous draft over-decomposed its links. A flat manufacturing face is not
a reason by itself to add a structural seam. Design each link as a continuous
load path and choose its print orientation afterwards.

## Upstream evidence

TheRobotStudio's `Upper_arm_SO101.step` and `Under_arm_SO101.step` were inspected
at upstream commit `eecbe3e0a9ebb23e25ad7b2759b03884c6660903`:

| STEP | Connected solids | Bounding box in source coordinates (mm) |
|---|---:|---:|
| Upper arm | 1, valid | 142.17 × 24.50 × 67.30 |
| Under arm | 1, valid | 130.70 × 24.00 × 64.40 |

Both are integral link bodies, not cheek/crossbar kits. The upper arm terminates
in the elbow's open saddle; the under arm carries a clevis and the wrist-servo
cradle, with its removable motor holder. The [measured joint-pattern record](soarm-joint-pattern.md)
documents their retention and horn interfaces. Their unchanged STEP files are
kept in [`hardware/vendor/so-arm100/SO101/`](../hardware/vendor/so-arm100/SO101/)
under the upstream Apache-2.0 licence; provenance is recorded there.

Upstream's [printing instructions](https://github.com/TheRobotStudio/SO-ARM100/blob/eecbe3e0a9ebb23e25ad7b2759b03884c6660903/README.md)
allow support material and provide arranged print plates. SO-101 is therefore
not evidence that every integral link must be support-free. Its print settings
are a reference, not a replacement for koala's PETG/load validation.

## What to combine

| Link or assembly | Integrated structural body | Separates only when needed |
|---|---|---|
| Upper arm / thigh | Two proximal horn forks + bridge/spine + distal servo cradle or four-ear saddle | Collar where its closing/retention function is needed |
| Shank | Two proximal horn forks + spine + 37D motor face mount and body support | Service retainer if motor insertion/removal requires one |
| Forearm | Two elbow horn forks + flat-section shaft + keyed hand end | Replaceable TPU ground pad, recessed metal fixing (DEC-48) |
| Orthogonal hip / shoulder carrier | Horn fork and next-axis socket carrier where hardware access permits | An explicitly justified installation/service closure |

The wheel-end link houses a **DC motor**, not another joint servo. The two rear
wheel drives do not add active wrist/ankle articulation. Motor-face screws go
in before a hub/wheel obscures their access; the motor must have a genuine
insertion/removal path rather than relying on spreading a closed printed cage.

For the old rear links this targets three thigh pieces → one main print and
five shank pieces → one main print, excluding collars and any necessary
retainer. It removes cheek/crossbar registration shoulders, long seam bolts,
washers and nuts where the seam disappears. DEC-40 now implements these reductions; the generated BOM covers all four
limbs and uses no link seam bolts. All current sockets use the four-ear saddle,
so they need no collar.

## Rules for the detailed CAD

- Reuse the confirmed SO-101 pocket and corrected horn/ear interface. Change
  the connecting structure to achieve the 70/75 mm arm and 85/90 mm leg lengths, plus the 25 mm fixed hand;
  never scale an upstream part uniformly, which would alter servo fit.
- Preserve both horn attachment patterns and a continuous connection between
  the forks. Use the upstream saddle variant where appropriate; a collar is
  a functional closure, not a compulsory additional part at every joint.
- Keep the open end for case insertion, ear-screw/tool access, horn-centre
  clearance, supplied screw-head pockets and the Back connector exit.
- Compare orientations for the whole link. Prefer continuous material through
  the bending load path; add accessible local supports where they give a
  better result than a bolted seam. Keep supports away from critical fits
  where practical, and check the resulting surfaces after removal.
- The area/overhang screen identifies places to inspect; it cannot establish
  print failure or justify an automatic split. Bed fit, sliced layers,
  assembly access and load tests still have to be checked.

The integrated parts are implemented and exported under
[DEC-48](cad-integrated-design.md). They have not been physically accepted.
The viewer has been rebuilt around both adopted poses, corrected interfaces
and two rear motor mounts and fixed front feet.
