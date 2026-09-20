# Recessed roll-first front limbs — 2026-09-19

**Unprinted revision, not a banked decision.** The owner requested the four CAD
review findings be fixed, then the rear redesign's printability lessons applied
to roll-first front limbs, with the torso extended around recessed A servos and
provision for the three small neck servos. This record describes the resulting
prototype. [Current chassis and assembly](../../cad-integrated-design.md) ·
[Printability by version](../../part-design-review.md).

## Geometry and visual review

| Item | Result | Review image |
|---|---|---|
| Torso v5 | 150 mm hip-to-shoulder spacing retained; cap at body Z183.5; ±47 mm sides, shallow forward chest step, rear screw-driver corridors | [Four views](../parts/torso_frame-views.png) |
| Shoulder mount v1 | Separate left/right cassettes support unchanged proven root sockets; socket lips at ±37 mm give 10 mm recess; four front-access M3×20 per side | [Four views](../parts/shoulder_mount-views.png) |
| Shoulder carrier v3 | Longitudinal A roll, B pitch 40 mm outboard; broad common block/socket bed plane and open driver tunnels | [Four views](../parts/shoulder_carrier-views.png) |
| Upper arm v2 | 70 mm centres, parallel B/C shafts, thickened cup wall sharing the outer fork's print plane | [Four views](../parts/upper_arm-views.png) |
| Forearm v2 | 100 mm elbow-to-pad centre, longer open elbow fork, flat tapered shaft, unchanged keyed TPU pad | [Four views](../parts/forearm-views.png) |
| Thigh v3 correction | Earlier successful fillets now survive later split-group rounding operations; joint datums unchanged | [Four views](../parts/thigh-views.png) |

**Does the design look stupid?** Individual review: **no**. The torso/cassettes
form a compact cage with broad rails, a shallow chest step and inward socket
flanges, without outriggers or disconnected features. The front carrier and
links have continuous printable forms rather than thin unsupported decorative
features. They are acceptable structural prototypes, not an accepted finished
shell. V5's inward dorsal taper was also inspected in multiple views: it
narrows the upper back without adding a backpack or increasing the 94 mm front
width / 82 mm depth envelope. The
[assembled body views](body-views.png) were also reviewed: depth stays compact,
the front shoulder span approaches the rear wheel span, and the different
front/rear limb forms look deliberate. The head remains a sizing allocation,
so this is not approval of a finished koala shell or loaded gestures.

The recess is measured from the torso side envelope to the **socket lip**;
A's output region, horns and moving carrier project outside it. A centres are
110.23 mm apart, pitch centres 190.23 mm apart. Rear pitch centres remain
52.5 mm apart and rear wheel track remains 220 mm. Left/right symmetry is
retained; front and rear use different serial joint orders by design.

The first extended torso (v4) cleared the nominal pose but its dorsal rails
clipped the front carrier at **+1° roll**. V5 tapers those rails from Y±43 to
Y±29 over body Z106…122; the outer width, depth and socket-lip recess stay
unchanged. The cartridge hole pattern shifts +10 mm in X to clear the upper
rails. This is a correction found by moving-package checks, not evidence that
a nominal screenshot alone established travel.

The B35 shoulder-carrier v2 trial also exposed a limitation beyond nominal
checks: the full upper-arm/A-case sweep stopped at about **+6° roll**. Final
carrier v3 puts B **40 mm** outboard. At the examined ±28/29/30° roll samples
in both saved poses, B39 left 0.765 mm upper-fork / 1.065 mm horn-head clearance
to the conservative A case; B40 increases those sampled minima to
**1.765 / 2.065 mm**. Upper arm/forearm v2 and torso v5 stay unchanged.
The larger margin is a geometric allocation, not a proven loaded range.

The [neck provision](../neck-provision.md) reserves small STS3032M space and
four generic cartridge mounts, including fixed-lead routing allowance. These
reference boxes neither establish the bought variant's fit nor solve 3-RPS
linkage geometry. No new neck print is claimed.

## Printability and service

New shoulder mount v1, torso v5, front carrier v3, upper arm/forearm v2 and thigh
v3 remain **`unknown`** despite local slicing; physical support removal, fit and
strength are unverified. Root socket v1 remains **`proven`** with its ear-hole
support caveat. Unchanged shank v2 and hip carrier v1 retain `assumed`.

The carrier prints on its common block/cup floor, the upper arm on its shared
drive-side fork/cup plane, and the forearm on its broad −Y face. Open forks
make supports accessible. Seven short/narrow upper-arm junction edges reject
R2 and remain sharp; the builder warns explicitly instead of silently undoing
rounding. The accepted ear seats, horn webs and driver approaches remain.

Recessing A would obstruct installed inboard root screws. **Load the four frame
nuts into the bare cassette first:** a fitted root blocks the two inner nuts'
straight insertion paths. Then bolt the root to the cassette on the bench and
attach the complete cassette to the ventral frame with four front-access screws.
For root service, remove those frame screws and slide the cassette **laterally
outward**, keeping the opposite A module installed. The seam has a service purpose; links remain single prints.
The robot now uses 26 physical prints from 18 designs / 26 handed exports,
including six separate coupon designs in the design/export count.

## Local slicing and support review

[Machine-readable slice records](slices.json) identify each STL/G-code version
and hash, plus the base profile and override hashes. PrusaSlicer **2.7.2** came
from the Ubuntu noble package, extracted locally with dependencies; no host
installation or printer connection was used. Review settings were **0.2 mm
layers, four walls, 30% gyroid, 4 mm brim and organic supports from the bed only**.

| Current part | Selected deposited-layer views |
|---|---|
| Forearm v2 | [Left](forearm_left-layers.png) · [Right](forearm_right-layers.png) |
| Shoulder carrier v3 | [Left](shoulder_carrier_left-layers.png) · [Right](shoulder_carrier_right-layers.png) |
| Shoulder mount v1 | [Left](shoulder_mount_left-layers.png) · [Right](shoulder_mount_right-layers.png) |
| Upper arm v2 | [Left](upper_arm_left-layers.png) · [Right](upper_arm_right-layers.png) |
| Thigh v3 | [Left](thigh_left-layers.png) · [Right](thigh_right-layers.png) |
| Torso v5 | [Layer views](torso_frame-layers.png) |

The selected layer plots show broad bases and support trees outside the solids
or in open forks/cups, without an enclosed support cage in the inspected layers.
The torso v5 plot shows branches through its open cage to the opposing rails
and cap. **All 11 final review slices match the current STL versions/hashes**,
including carrier v3 and torso v5, with **zero recorded slicer diagnostics**.
The final carrier layers and B40 body views have been inspected. Selected
layers do not establish every layer start or physical support removal;
surface quality, fit and strength remain unverified and changed parts stay
`unknown`. Tiny forearm STL coordinate roundoff was corrected by persisting the
same default vertex merge already used in mesh validation; BREP geometry and
merge tolerance did not change. [Digital correction](../../test-log.md#2026-09-19--forearm-v2-stl-roundoff-persistence-corrected-digital-only).

Shank v2 is outside this 11-slice batch. [OQ-22](../../open-questions.md)
records earlier organic slices with STL hash prefixes 335d9f74 (left) and
ae2ac311 (right), matching the current exports; those G-code files and layers
were not re-reviewed here. Older manufacturing-report shank slices predate v2.

To reproduce one organic review slice, run from `hardware/` with an
organic-capable PrusaSlicer and the sibling `3d-printing` checkout:

```sh
mkdir -p build/manufacturing
prusa-slicer \
  --load ../../3d-printing/reference/ender5s1_petg_koala.ini \
  --load print/manufacturing-petg-tree.ini \
  --export-gcode \
  --output build/manufacturing/upper_arm_right-v2-tree.gcode \
  build/stl/upper_arm_right.stl
```

Substitute the current exported part name and version for other parts, slicing
one at a time. Match the recorded slicer/profile hashes when comparing this
review's toolpaths. The command writes a local file; it does not submit a print.

## Digital evidence and limits

The [consolidated validation record](../cad-validation.json) links the final
versions, exports, slices and main/rear checks.

The [complete driven-package report](driven-package-clearance.json) is the
primary shoulder roll check: **outward-positive commanded roll −30…30° at 2°
intervals**, in both saved pitch/elbow configurations. It checks the entire
right moving front chain and hardware against its fixed A imported/caliper
cases, socket module, cassette and fixings: **31 samples / 2,604 pairs per
pose, zero overlap**. It covers the upper-arm/A-case interaction missed by the
earlier carrier-only trial.

The [installed-front report](installed-front-clearance.json) also moves **both
front limbs** at roll −30/−25/0/+25/+30°, with the rear limbs nominal, in both
saved poses and with both imported/caliper cases. All pairs involving the
moving fronts participate against the torso, catalogue neck envelopes, fixed
roots, opposite front limb and stationary rear hardware, except the intended
owning-socket contact regions: **20 configurations / 1,236 candidate solid
pairs, zero hits**. These two reports identify their geometry-source hashes.

Additional evidence has narrower scope:

| Check | Scope and result |
|---|---|
| [Adjacent joints](local-clearance.json) | 1° samples with both case models: native carrier-only roll −30…60°, pitch ±90°, elbow 0…120°; 2,296 pairs, zero overlap. The native roll axis/range is not the whole-limb commanded range above. |
| [B-offset study](roll-offset-study.json) | Documents the B35 obstruction and B40 choice; sampled conservative A-case margins at ±28/29/30° are 1.765 mm for the upper fork and 2.065 mm for horn heads. |
| [Dorsal-rail sweep](shoulder-rail-sweep.json) | Final B40/carrier v3 and torso v5: 12 moving front-chain solids against conservative unfilleted rail/transition envelopes over ±30° roll at 2° in both saved poses, zero overlap. |
| [Complete assembly audit](assembly-audit.json) | 62 samples around both saved poses pass; each nominal pose checks 180 pairs. Also checks the 19-angle interface rig, insertion, frame contact and driver paths. |
| [Fallback audit](assembly-audit-fallback.json) | Both nominal poses pass with conservative parametric servo cases; 180 pairs each. |
| Neck and service access | Reserved neck volumes/four cartridge driver paths clear; three service regressions protect cassette nut loading/seating and lateral removal. |
| Python regression suite | **65 tests pass**, including version guarding, front print/kinematic checks and STL closure after merging only identical coordinates. |
| Exports and slicing | **26 handed part exports, two assembly STEP exports, 11 current review slices** pass; generated BOM updated. |
| [Main browser verification](browser-verification.json) | Both poses, all three sliders, mirrored CAD/browser motion, backdrop alignment, part metadata and reset pass; four current captures inspected. |
| [Main viewer endpoints](viewer-endpoints.json) | All 12 initial grouped-slider endpoints checked against the complete assembly with both case models: 24 configurations / 1,452 candidate solid pairs, zero hits. |
| [Rear production review](../rear-leg/README.md) | Refreshed current parts, sections and views; both browser poses/seven checks and all 12 initial bounds plus four combined solid-CAD configurations pass. Front/neck geometry is omitted from this separate review. |

The main viewer rolls all four limbs together. Its initial common roll range
is **−5.5…29.25°** in quadruped and **−5…29.25°** upright, including the 2°
search reserve. Rear motor proximity sets the inward bound; the front socket/
carrier sets the outward bound. The front-only ±30° checks above leave the
rear joints nominal and therefore do not establish that grouped range.

The solid intersection threshold is **0.01 mm³**. These are finite samples,
with stated pose/obstacle coverage, not continuous swept volumes, calibrated
servo limits or loaded motion. Ground interaction, full cables, guards and
as-built tolerances are not established. The earlier four findings and their
corrections are recorded in the [test log](../../test-log.md#2026-09-19--four-cad-review-defects-corrected-digital-only).

The **main browser smoke and solid-CAD endpoint checks pass**; its four current
pose/view captures have been inspected. A [metadata-only refresh](viewer-metadata-refresh.json)
updates prior hip/shank slice notes and verifies every non-note scene field is
unchanged. The rear review also passes its browser and endpoint checks. Of its
16 broader exploratory rear-assembly samples, 15 clear; quadruped pitch −45°
intersects torso/thigh outside the current −28.25° viewer bound. That sample is
not accepted travel. Earlier manufacturing reports and
thigh v2 slices do not validate these revised parts. No physical print,
fitting, support removal, load/creep or loaded transition is asserted by this record.
