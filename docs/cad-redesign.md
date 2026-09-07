# DEC-29 lower-body redesign — 2026-09-06

This replaces the defective geometry reviewed in [cad-review.md](cad-review.md).
It is a **fit-test prototype**, not an accepted structural robot.

## Parts and print orientation

| Assembly | Replacement | Bed face and load-path rationale |
|---|---|---|
| Pelvis plate + two brackets | One integrated `pelvis`, 150×170×24 mm | Deck top against bed; roots grow upward. Removes both 6 mm mounting flanges and eight screws. Root bending still loads layer interfaces. |
| Enclosing hip link | Two flat roll cheeks + open pitch saddle + removable cap, per hip | Cheeks lie flat, 5 mm thick, with roll loads in their YZ layer plane. Saddle floor and cap broad face on bed. Saddle posts remain cross-layer/creep risks. |
| Thigh upper + motor clamp | Two flat thigh cheeks + two compression spacers, per leg | Cheeks lie flat, 48×193×5 mm; layers follow the XZ hip-to-knee profile. Outer cheek is the motor faceplate; inner cheek supports the motor body. No insert-loaded thigh seam. |
| Thigh spacers | Four identical 24 mm diameter × 40 mm spacers | Circular end on bed; through-bolts compress the stack. No printed thread. Joint slip and PETG creep need tests. |

The cheeks retain rounded ends and tapered, radiused profiles. They do not
claim isotropic strength: side loads bend them out of their layer plane.
Splitting parts to choose useful orientations follows
[Prusa's design guidance](https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135);
that is a design rationale, not strength evidence for these parts.

## Packaging tradeoffs

- Roll axis is 44 mm below the deck, formerly 50 mm.
- Pitch axis is 30 mm below roll, formerly 26 mm; the extra 4 mm separates
  the moving cheeks. It is also 20 mm forward, opening the inner-thigh lane.
- Roll roots move from ±57 to ±64 mm. The motor mounts on the outer cheek
  at leg-local Y=42.4 mm, replacing Y=14 mm. Neutral motor-end gap is 74.8 mm.
- Hub stack increases from 14 to **18 mm, provisional**, clearing the 5 mm
  motor plate and nominal 3 mm cap heads. Verify shaft engagement, actual hub
  set-screw position and motor face-screw depth before assembly.
- Neutral wheel-centre track is **258.8 mm**, formerly 180 mm; overall tyre
  width is 268.8 mm. Neutral deck-to-ground height is 268 mm, formerly 270 mm.
  The width buys room for inward motor sweep; this is a substantial tradeoff,
  not a proven optimum. Forward wheel position also changes balance geometry.

## Assembly sequence and fasteners

1. Fit-test horn square, idler offset, motor boss/bore, and actual case/cable
   envelopes. The old servo-cradle coupon does **not** validate the new saddle.
   Use one saddle/cap and one cheek of each kind as joint fit samples.
2. Fit the roll servos into the integrated roots. Rear retention-hole locations
   remain **OQ-12**; the CAD does not authorize driving screws into an
   unmeasured case. The screw is now known to be **M2 self-tapping** (supplied
   with the servos, 2026-09-07); its length is not, because the wall it crosses
   is 3.95 mm at one end and 6.35 mm at the horn-side end. Roots have at least
   3 mm nominal wall beside the conservative tab keep-out.
3. Fit roll cheeks to drive and idler horns. Each has four full-depth M3
   clearances and a centre access opening. Determine horn screw lengths from
   the **5 mm plate plus measured thread engagement**; do not reuse the old
   blanket M3×6 recommendation.
4. Bolt the saddle between roll cheeks using two M3×55 through-bolts per hip,
   nuts and washers. Nominal grip is 5+40+5=50 mm. Fit the pitch servo on the
   outboard seat and clamp its case with the removable cap: two M3×8 screws
   into 5.7 mm inserts per hip. The cap is a friction-clamp experiment; preload,
   creep, connector clearance and case damage are untested.
5. Fit thigh cheeks to pitch drive/idler horns; join cheeks using two spacers
   and two M3×55 through-bolts per leg. Tighten against spacers, not by drawing
   the servo horns together. Check washer/nut stack and protrusion physically.
6. Slide the motor through the inner support bore and attach its face to the
   outer cheek (six M3 screws per motor). M3×8 is a candidate with 3 mm nominal
   engagement, **not approved until motor thread depth is measured**.
   Fit hub and wheel afterward to preserve screw access.
7. Attach tray via four 10 mm standoffs. The 5 mm pelvis deck needs **short
   inserts, at most 4 mm long**, not the former 5.7 mm insert. Coupon-test the
   selected insert's required bore; OD compatibility is unverified.

Bought wheels, hubs and nominal servo cases are visible in the viewer.
Individual bolts, nuts, cables and complete vendor internals are not rendered.
Disassembly/access order above is proposed, not demonstrated on hardware.
The modeled 0.2 mm horn-face gaps require measured shimming/fit adjustment;
do not close them by bending the cheek plates or preloading servo bearings.

## Verification and remaining acceptance gates

`cd hardware && uv run python -m koala_hardware.audit` checks:

- Valid connected solids (except the explicitly two-piece seam coupon), bed
  bounds, and 16 full-depth hole probes across four distinct cheek designs.
- Exact solid intersections at 25 local combinations: roll −10, −5, 0, +5,
  +10° × pitch −20, −10, 0, +10, +20°. Includes printed parts, nominal cases,
  motor/hub/wheel packaging and selected proud cap-head/nut envelopes.
- Nine opposing-leg poses: both hips at −10° inward roll, with independent
  −20, 0, +20° pitch. Tests both motors and the other opposite-side geometry.

These samples pass with no detected intersection above 0.01 mm³. This is
**not a continuous sweep or a clearance tolerance guarantee**. The nominal
servo reference deliberately omits the unmeasured idler, invented tab block
and cables; unresolved hardware cannot be cleared by hiding its uncertainty
inside a padded ghost. Complete tool approach and fastening are not audited.

The minimum sampled distance between printed hip-carrier parts and printed
thigh parts is **2.4 mm**; the regression requires at least 2 mm. This excludes
the intentionally close horn mating faces and does not include print errors.

The exporter now requires all vertices of a bed triangle to lie on the bed
and labels its result a **geometry screen**, not “support-free”.
Cheeks/caps/spacers have no flagged downward overhang in their orientations.
Pelvis and saddle still have flagged areas requiring slice inspection.
All STL bottom faces are exported at Z=0. The viewer Parts tab shows those
same orientations, notes and measured surface areas, not a packed print job.

Final checks on 2026-09-06: full export passed; all 16 exported STLs were
watertight and seated at Z=0; both bed-contact regression tests passed.
The live-browser smoke test rendered the scene and matched left/right posed
mesh bounds against CAD within 0.1 mm, then checked selection, notes and reset.
Replaced STL/PNG outputs were pruned; the old geometry can be regenerated from
revision `a3f265c` in a separate worktree.

**No new slicing or printing was performed.** A read-only check on 2026-09-06
found the reference printer printing; its shared slicing host was left alone.
Cached slice quantities are used only when their STL hashes match.

Before structural acceptance:

1. Inspect actual PETG sliced layers, particularly horizontal retention bores,
   saddle rails/posts, narrow roots and all insert pockets. Confirm no floating
   starts, unacceptable bridges, missing walls or support trapped in a bore.
2. Resolve measured servo/idler/cable/hub fits and every fastener's engagement,
   access and protrusion. Repeat a denser, tolerance-expanded motion audit.
3. Establish total mass and dynamic load cases. As an **illustrative test
   planning assumption only**, 3 kg gives 29.4 N static total weight; 2g on one
   wheel gives 58.9 N at that wheel. These are not accepted loads or proof
   factors. Test fore/aft bending, lateral bending, roll-root separation,
   saddle clamp slip and insert pull-out using the actual printed profile.
4. Record deflection, failure mode, repeated-cycle behaviour and sustained-load
   creep in `test-log.md`; choose perimeters/infill from those results (OQ-11).
   No allowable stress, safety factor or useful life is established here.
5. Guard pinch points and exposed fixings before child-facing use (OQ-10).
