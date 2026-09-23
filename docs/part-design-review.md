# Part construction and printability

Current 2026-09-19 revision: recessed **roll → pitch** front shoulders, parallel
pitch/elbow front links and the retained **pitch → roll** rear legs. Broad print
faces, enclosing sockets, open forks, filleted roots and accessible support
removal carry the rear redesign lessons into the front limbs.
[Design and assembly](cad-integrated-design.md) ·
[Front revision and views](design/front-redesign/README.md) ·
[Current slices](design/front-redesign/README.md#local-slicing-and-support-review) ·
[Earlier manufacturing records](design/manufacturing/README.md).

## Printability tags — DEC-47

Every printed design has a monotonically increasing version in
[`part-versions.json`](../hardware/part-versions.json), shown in the generated
BOM. Geometry changes require a version bump and reassessment. A `proven` tag
belongs to the version actually printed; earlier slices and prints do not
transfer automatically.

- `unknown`: the current revision has not established a reviewed manufacturing
  outcome; bed contact, layer starts or support removal still need validation.
- `assumed`: a credible print approach is recorded, without a successful
  physical print of that version. A surface-area screen alone is insufficient.
- `proven`: a physical print of that version is recorded in [the test log](test-log.md),
  with its relevant settings and limitations.

There are **19 designs / 28 handed export variants**, including six coupons
and both rear-shank alternatives. The chassis uses **28 physical prints walking
/ 26 wheeled**. **Root socket v1 alone is proven**;
the new/changed parts below remain `unknown`. The unchanged hip carriers have
plate 2 slices; no physical result is recorded here. OQ-22 records earlier
shank v2 organic slices with hashes matching the current exports; they were
not re-reviewed in this session's 11-slice batch. Sliced thigh v2 is superseded
by v3.

## Current structural parts

The table identifies the declared bed face, not a claim of support-free printing.
[Current local slices](design/front-redesign/README.md#local-slicing-and-support-review)
cover all 11 final changed handed exports, including carrier v3 and torso v5,
with matching STL hashes and inspected selected layers. They do not prove every layer start, physical support removal or fit.
STLs already carry the declared orientation. PETG support must grow from the bed only;
review layer starts and removal access before printing. TPU uses no support.

| Part / version / physical quantity | Printable | Material | Construction and print approach |
|---|---|---|---|
| `root_socket` v1 / 4, two per hand | `proven` | PETG | Plate 1, 2026-09-19: all four fit. Ear holes blocked by the old support profile need clearing with a 2.2 mm drill or reprinting; bed-only support is now configured. Flat plate down, socket up. Four captive shelf nuts and bench-fitted ear screws. Geometry unchanged; front installation now uses a removable cassette. |
| `shoulder_mount` v1 / 2, handed | `unknown` | PETG | Independent recessed-A cassette. Broad body-Y = 4 face down; open flange nut pockets and bore roofs need accessible local bed-only support. Filleted root joins a wide front flange. Preload four cassette frame nuts before bench-fitting the root socket with four M3×16; four front-access M3×20 secure it to the torso. Remove laterally outward. [Views](design/parts/shoulder_mount-views.png). |
| `shoulder_carrier` v3 / 2, handed | `unknown` | PETG | A roll fork and B socket share a broad planar block/cup floor; print that face down. R6.3 fork roots, open ear-driver tunnels and no hidden support chamber. Fit B and all four ear screws before the arm. [Views](design/parts/shoulder_carrier-views.png). |
| `hip_carrier` v1 / 2, handed | `assumed` | PETG | Owner visual review, 2026-09-18; plate 2 sliced, physical result unrecorded. DEC-55/56 block below A, 16 mm fork neck, tapered inner bevels, R6.3 fork roots, R5 socket roots and R1.5 lip. Block/socket floor down. Actual support removal, fitted travel and load/creep remain open. |
| `thigh` v3 / 2, handed | `unknown` | PETG | Tapered one-piece DEC-58 yoke and sideways knee socket retained. Corrected rounding now keeps earlier successful fillets instead of overwriting them. Cup-floor plane down; accessible tree support under the opposite cheek and pads. v2 G-code does not validate v3. [Current views](design/parts/thigh-views.png); [earlier print-form rationale](design/rear-leg/thigh-flat/README.md). |
| `upper_arm` v2 / 2, handed | `unknown` | PETG | 70 mm centres, parallel pitch/elbow axes, enclosing C socket. Thickened drive cup wall and outer fork share the bed plane; support under the opposite fork and open cup remains removable. R6.3 roots/R2 outer rounding; seven short/narrow junction edges remain sharp and are reported. [Views](design/parts/upper_arm-views.png). |
| `shank` v2 / 2, handed | `assumed` | PETG | 90 mm centres, extended open fork and flush motor/drive-fork face on bed. R6.3 fork roots, R5 motor roots, R2 outer rounding. Existing v2 bed-only organic slices retained; the unsupported motor-bore crown needs physical inspection for sag and insertion. [Record](design/rear-leg/thigh-flat/README.md). |
| `foot_shank` v1 / 2, handed, walking alternative | `unknown` | PETG | 90 mm knee-to-pad centre; shared knee horn interfaces and front TPU pad key. Long open fork, R6.3 roots and rounded taper; broad native −Y face down. Fork bores and nut-slot roof need accessible local support. New print, no inherited physical proof. [Views and checks](design/walking/README.md). |
| `forearm` v2 / 2, handed | `unknown` | PETG | 100 mm elbow-to-pad centre, long open fork, R6.3 roots/R3 taper corners and broad native −Y bed face. Fork/hole/nut-slot roofs remain accessible for support removal. Insert the captive nut before the unchanged keyed pad. [Views](design/parts/forearm-views.png). |
| `front_contact_pad` v1 / 4 walking, 2 wheeled | `assumed` | TPU | Same Ø32 rounded contact on every footed limb; truncated mating face down, tapered keyed cavity, recessed screw/washer. No support. Geometry unchanged; grade, traction and wear remain unverified. |
| `torso_frame` v5 / 1 | `unknown` | PETG | Cage extends to shoulder cap Z183.5, with 10 mm socket-lip recess, front cassette crossmembers, inward-tapering dorsal shoulder rails, neck-cartridge slot and rear driver corridors. Dorsal face down; opposite rails/cap/flange roofs need bed-only supports removable through the cage. No locating pins are claimed. [Views](design/parts/torso_frame-views.png). |
| `e_tray` v1 / 1 | `assumed` | PETG | Flat rounded plate, tapered stand-offs and strap slots. Flat down; no intrinsic support. Complete electronics packaging remains open. |
| `tray_spacer` v1 / 4 | `assumed` | PETG | Annular spacers, flat down; brim or grouping for small bed contact. |

## Coupons

| Coupon | Printable | Material | Print approach |
|---|---|---|---|
| `coupon_socket_saddle` | `assumed` | PETG | Current enclosing production pocket, floor down. Accessible support under ear-hole roofs. Checks the new mounting construction, not a repeat SO-101 fit gauge. |
| `coupon_socket_fork` | `assumed` | PETG | Current tapered production fork. Outer horn pad down; support beneath opposite cheek is reachable through the open fork. |
| `coupon_motor_ring` | `assumed` | PETG | Flat face down; vertical through-holes. |
| `coupon_motor_bore` | `assumed` | PETG | Flat labelled slab, vertical bores. |
| `coupon_ladder` | `assumed` | PETG | Flat labelled slab; the earlier printed revision remains separate evidence. |
| `coupon_seam` | `assumed` | PETG | Two flat pieces in one export; generic insert/seam practice, not a required structural joint in this design. |

## What was taken from SO-101 and the rear redesign

The [source templates](design/so101/README.md) establish enclosing sockets,
measured ear/horn datums, broad fork roots and deliberate print planes. The
accepted 34.9 × 24.7 mm pocket, four ear screws, 36.4 mm horn span, 3.5 mm
bearing webs and idler washers remain. Reusing those interfaces does not prove
fit or strength of a complete Koala link; no repeat Gauge_0 is required.

Rear links taught the practical distinction between a flat face somewhere on a
part and a useful continuous bed face. The front carrier shares its block/cup
floor, the upper arm thickens its cup wall to the fork plane, and the forearm
has a broad flat shaft. Open forks keep support reachable. The front's parallel
pitch/elbow axes permit a different form from the rear's orthogonal axes.

Root servos are fully secured on the bench. Load the cassette's four frame nuts
before attaching its front root; otherwise the root obstructs the inner nuts'
straight loading paths. Remove the complete cassette laterally outward for service. Recessing the front sockets led to
separate removable cassettes because installed access between opposing servos
would be poor. Each cassette has four frame screws and broad bearing surfaces;
it is a service seam with a defined purpose. Tool access, physical support
removal, stiffness/creep and complete harness clearance still need acceptance.

The earlier [flat-back study](design/front-carrier/README.md) and manufacturing
images are historical unless their version and STL hash match the current part.
