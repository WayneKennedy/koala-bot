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

Every current part below is **`assumed`**. Each has an explicit orientation,
a reviewed support/removal approach, a closed mesh and a successful local slice
of the exported STL. These are **17 designs / 24 handed export variants**,
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
| `pelvis_socket_left/right` / 2 | `assumed` | PETG | Rear case points forward in the torso frame. Integral right-angle return meets the frame flange raised to Z=46 mm for carrier clearance. Socket-floor face down, opening up; flange grows as a vertical wall. Local hole/pocket-roof supports are externally accessible. |
| `shoulder_socket_left/right` / 2 | `assumed` | PETG | Same installation principle in the shoulder orientation. Full servo retention on the bench; locating pockets and externally accessible frame bolts. Flat frame face down. |
| `root_carrier_left/right` / 4 (two of each hand) | `assumed` | PETG | Identical front/rear carrier per hand; viewer keeps `front_carrier*` / `rear_carrier*` instance names. Continuous unbevelled flat back joins fork and socket floor. Back down; accessible local hole-roof supports. |
| `thigh_left/right` / 2 | `assumed` | PETG | 85 mm centres, orthogonal interfaces retained. Rounded spine and tapered socket transition; broad fork roots. Outer horn pad down; remove supports from the open fork and socket before inserting the servo. |
| `upper_arm_left/right` / 2 | `assumed` | PETG | The same interface family at 70 mm centres. Rounded transition sized for the shorter link. Outer horn pad down; accessible fork/socket supports. |
| `shank_left/right` / 2 | `assumed` | PETG | 90 mm knee-to-ankle centres. Rounded spine and bridge connect the fork to the 37D face and body support. Outer horn pad down; support under the face/ring is removable through the open axial bore before motor insertion. |
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
