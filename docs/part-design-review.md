# Part construction and printability — DEC-49/50

The accepted DEC-44 layout now has enclosing servo sockets, tapered and rounded
fork roots, rounded structural transitions, independent root-servo modules and
flatter forearms with replaceable TPU contact pads. Joint centres, pitch → roll
order, rear ankle drives and the two saved body poses are retained. DEC-49
aligns rear roll spacing with the 149 mm front spacing for common carriers;
DEC-50 corrects unequal drive/idler socket slots.

[Individual part images](design/README.md#individual-structural-prints) ·
[Slice records and layer images](design/manufacturing/README.md) ·
[SO-101 source templates](design/so101/README.md).

## Printability tags — DEC-47

Every part also carries a **design version** (`v1` for everything as of 2026-09-19;
[`hardware/part-versions.json`](../hardware/part-versions.json), shown in the BOM). A
`proven` tag is proven for the version printed; a version bump reassesses the tag.

The thighs and shanks are **v2, `assumed`** (2026-09-19): the owner reviewed the DEC-58 parts on
2026-09-18, found their general geometry good but the parts as drawn would need a lot of
support, which would probably ruin them (aesthetic judgement plus printability instinct,
not a slice; the shank is expected to be the easier fix). The root modules and hip carriers became
**`assumed`** in the same review (they look right; orientation and support are recorded
below). The other rows retain **`assumed`**. Earlier local slices apply only to their
matching STL hashes. These are **17 designs / 24 handed export variants**,
including six coupons. The robot uses 24 physical structural prints, including
two TPU pads and four tray spacers. Nothing in this revision has been printed.

- `unknown`: the current revision lacks a reviewed print approach, or bed
  contact, layer starts or support removal remain unresolved. New parts default
  to this status.
- `assumed`: a credible print approach is recorded; no successful physical
  print of that revision is recorded. A surface-area screen alone is insufficient.
- `proven`: a successful physical print of the relevant revision is recorded
  in [the test log](test-log.md), with orientation, material and support/settings
  identified to the extent known.

Both mirrored variants share a row unless evidence differs. Reassess the tag
when geometry or orientation changes. Assembly access, fit, strength, traction
and loaded joint travel are separate checks. Accepted SO-101 fit remains valid;
it does not prove a complete derived Koala print. The older printed ladder
revision does not establish `proven` for the current ladder.

## Current structural parts

Native orientation descriptions refer to each builder's part frame. Exports
are already oriented and translated onto the bed. PETG review slices use snug
supports and a brim; supports must be removed before fitting hardware. TPU uses
no support. See the recorded overrides and actual deposited-path images.

| Part / quantity | Printable | Material | Construction and print approach |
|---|---|---|---|
| `root_socket_left/right` / 4 (two of each hand) | `proven` | PETG | **Proven v1, 2026-09-19 (plate 1, PETG):** four printed, all pass for main function. The M2 ear holes came out blocked by support because the profile lacked bed-only support (fixed; `test-log.md`): drill 2.2 mm or reprint. DEC-53: one root module at all four roots; the pelvis pair is the shoulder pair turned 180° about the pitch axis. Flat 6 mm plate face down, socket opening up; nut pockets open into the shelf and bridge nothing; ear-hole roofs use accessible local support. Replaces `pelvis_socket` and `shoulder_socket` (the pelvis corner defect with them). No slice yet. |
| `shoulder_carrier_left/right` / 2 | `assumed` | PETG | DEC-49 front carrier, retained until DEC-54's roll-first shoulder chain replaces it. Flat back down; accessible local hole-roof supports. |
| `hip_carrier_left/right` / 2 | `assumed` | PETG | Assumed: owner visual review of the rear-leg viewer, 2026-09-18. DEC-55/56: 16 mm fork-width block below the pitch axis, tapered 2 mm inner-edge bevels; R6.3 fork roots, R5 socket roots and R1.5 at the narrow socket lip. Roll servo Bottom-down. Block and socket floor share the flat bed face (2080 mm²); 50.5 mm build height. Valid solid and closed handed meshes; support removal, strength and slicing remain unverified. [Current view](design/hip-carrier-refinement.png). |
| `thigh_left/right` / 2 | `assumed` | PETG | **v2 (2026-09-19):** the DEC-58 yoke with the idler-side cheek thickened to the cup-floor plane, one flat taper to the idler pad (owner's red line), convex edges rounded R2 (cup R1.5). Prints on the cup-floor plane, tree (organic) support under the drive-side cheek and both pads, 1986 mm² bed contact, 73 mm high. Assumed on the owner's judgement that the tapered form is worth a test print; the rounding pass is unreviewed. Straight servo insertion unchanged. [Record](design/rear-leg/thigh-flat/README.md). No slice yet. |
| `upper_arm_left/right` / 2 | `assumed` | PETG | The same interface family at 70 mm centres. Rounded transition sized for the shorter link. Outer horn pad down; accessible fork/socket supports. |
| `shank_left/right` / 2 | `assumed` | PETG | **v2 (2026-09-19):** 90 mm knee-to-ankle centres, extended open knee fork, R6.3 fork roots, R5 motor roots; motor-mount face flush with the drive fork's outer face (DEC-60 spacing, no step), convex edges rounded R2. Prints on that outer face, 2612 mm² bed contact, 49 mm high; support under the idler fork and the motor bore roof. Assumed on the owner-directed form and print face; the rounding pass is unreviewed. [Record](design/rear-leg/thigh-flat/README.md). No slice yet. |
| `forearm_left/right` / 2 | `assumed` | PETG | Rounded 18 × 17.9 mm shaft section with a flat native −Y bed face, integral fork and keyed pad seat. Local support under hole roofs, nut slot and projecting key is externally accessible. Insert the metal nut before attaching the pad. |
| `front_contact_pad` / 2 | `assumed` | TPU | Rounded contact preserves the 100 mm elbow-to-ball centre and Ø32 mm ground envelope. Truncated mating face down; keyed cavity tapers to the through-hole without a flat roof. No supports; recessed screw/washer, replaceable pad. Material settings remain provisional. |
| `torso_frame` / 1 | `assumed` | PETG | Rounded rail corners, continuous flanges and integral module locating pins. Declared side face down; snug supports under opposing rails and flange roofs can be removed through the open cage. |
| `e_tray` / 1 | `assumed` | PETG | Flat rounded plate with tapered stand-off roots and strap slots. Flat face down; no support intrinsically required. Two-drive electronics packaging remains open. |
| `tray_spacer` / 4 | `assumed` | PETG | Simple annular spacers, flat face down. Group or use brim for their small contact area. |

## Coupons

| Coupon | Printable | Material | Print approach |
|---|---|---|---|
| `coupon_socket_saddle` | `assumed` | PETG | Current enclosing production pocket, floor down. Accessible support under ear-hole roofs. Checks the new mounting construction, not a repeat SO-101 fit gauge. |
| `coupon_socket_fork` | `assumed` | PETG | Current tapered production fork. Outer horn pad down; support beneath opposite cheek is reachable through the open fork. |
| `coupon_motor_ring` | `assumed` | PETG | Flat face down; vertical through-holes. |
| `coupon_motor_bore` | `assumed` | PETG | Flat labelled slab, vertical bores. |
| `coupon_ladder` | `assumed` | PETG | Flat labelled slab; the earlier printed revision remains separate evidence. |
| `coupon_seam` | `assumed` | PETG | Two flat pieces in one export; generic insert/seam practice, not a required structural joint in this design. |

## What was taken from SO-101

The [Upper arm photo](design/so101/IMG_7004.png) and exact upstream STEP
sections establish the construction references: an enclosing pocket, rounded
external transitions, broad fork roots and a deliberate build face. The new
Koala pocket restores Side-wall returns around the accepted 34.9 × 24.7 mm
interface; all four ear screws remain. The 36.4 mm horn span, 3.5 mm screw-bearing
web, supplied-head counterbores and Back washers are retained.

The fork nose stays R10.4 to preserve connector clearance; the wider roots
begin farther from the axis. Copying SO-101's entire 63.4 mm outside fork width
would conflict with the compact layout. Likewise, retained pitch → roll makes
upper-link end axes perpendicular: those parts use accessible local supports.
They are not claimed to reproduce the source arm's support-free orientation.

The root mounts implement DEC-45: fully secure each servo into its own module
on the bench, then install the module using two frame bolts outside the servo
footprint. Pins on the torso engage blind module pockets. The old installed
inboard ear-screw obstruction is avoided by that assembly sequence.

The [front-carrier flat-back study](design/front-carrier/README.md) is retained
as historical evidence; its build-face principle is now implemented at all
four roots, with the head-clearance bevel removed. Current
production exports and slice records supersede the study's candidate status.
