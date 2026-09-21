# Open Questions (pending decisions)

Unresolved. Resolve -> move to [`decisions.md`](decisions.md).

- **OQ-26 — Battery: capacity undecided; inclination is 3S2P Li-ion 21700,
  half on each torso side, removable for charging.** Maintainer, 2026-09-14.
  Capacity waits on a power budget that does not exist yet: the only figure
  in the record is the 32 A fault case of twelve stalled STS3215s
  (`architecture.md`); typical walking, balancing and idle draws are
  unmeasured. Facts for sizing: a 21700 cell is Ø21 × 70 mm, about 70 g, 4–5 Ah
  and, depending on the cell, 10–35 A continuous; 3S2P is 8–10 Ah, 11.1 V
  nominal, roughly 90–110 Wh and about 420 g of cells plus holders and BMS,
  against the 1.5–3 kg whole-robot budget (DEC-15). Choose a high-drain cell
  over a high-capacity one: the pack must ride servo transients, and Li-ion
  sags more than the "stiff LiPo" DEC-20 assumes, so bulk capacitance on the
  servo bus matters more, not less. One 3S1P stick per side is three cells
  abreast, about 66 × 73 × 23 mm wrapped, which fits lengthwise inside the
  150 mm torso below the shoulders. Conflict to resolve with OQ-23: DEC-54
  puts the shoulder root sockets on the same torso sides; the sticks would
  sit below them, and the side walls then carry sockets, packs and a
  removal path, which drives the torso width. Chemistry change from the
  `architecture.md` "3S LiPo" is within its 3S-only rule (12.6 V full).
  Decide capacity once a first leg has been driven and current measured.

- **OQ-25 — Optional sideways "hug" elbow.** The 2026-09-19 front prototype
  uses **parallel B pitch / C elbow axes**, preserving sagittal leg shortening
  for support and the lift-to-balance transition. That is the current CAD
  implementation, not a banked rejection of the alternative. An elbow parallel
  to A's longitudinal roll axis would fold inward for a hug but change
  foreleg shortening, foot placement and the upper-arm/socket print form.
  Revisit only against concrete desired gestures and supported movement;
  assess the existing roll-first prototype first.

- **OQ-23 — Shoulder/neck and battery packaging acceptance.** The owner's
  2026-09-19 instruction to recess front A and extend the surrounding frame is
  implemented as an **unprinted revision**: torso sides Y±47 mm, socket lips
  Y±37 mm (10 mm recess), A centres 110.23 mm apart and B pitch centres
  190.23 mm apart. Frame cap Z183.5 extends around the roots while the
  hip-to-shoulder spacing stays 150 mm. Independent front-access cassettes
  retain bench access to the proven root modules.
  [Current front geometry and evidence](design/front-redesign/README.md).
  The horns/moving carrier still project; recess depth is not a flush-skin claim.

  The dorsal cap has an open slot and four M3 points for a removable cartridge
  holding the **small bought STS3032M** servos. Published 23.2×12.1×28.5 mm case
  envelopes with 1 mm clearance fit the allocated bay; purchased M dimensions,
  ears, fixed-lead exits, connector-board fit and complete removal paths need
  checking. The packed upright boxes do not solve the 3-RPS axis/linkage
  arrangement. [Neck provision and source uncertainty](design/neck-provision.md).
  Check as-built moving A/B clearance, gestures from rest, cable loops,
  side-battery packaging (OQ-26), head mass and load paths before acceptance.
  The [earlier shoulder-axis study](design/shoulder-axis-review.png) explains
  the review trigger; it predates this implemented chain.

  The former shank-inset/track choice is resolved by **DEC-60**: rear pitch
  centres are 52.5 mm apart, preserving 220 mm track with the flush shank face.
  It is no longer a pending width choice. Neck/head placement and the 450 mm
  sizing target remain separate from the torso extension.

- **OQ-22 — Root joint construction and travel acceptance.**
  **Current, 2026-09-19:** the main assembly carries DEC-61's inclined 45°
  rear root mount. Torso v5 adds full-length rear screwdriver corridors and
  removable front shoulder cassettes; driver checks include the actual torso.
  Front limbs now use roll → pitch → elbow with the rear printability lessons.
  [Front evidence](design/front-redesign/README.md) and
  [rear evidence](design/rear-leg/README.md) have distinct scopes.
  Still open: support removal on current print versions, actual servo indexing,
  cables, fastener engagement, fork stiffness/creep and loaded motion. Local
  adjacent-joint samples do not establish whole-robot or continuous travel.
  Root socket v1 is physically proven with the recorded ear-hole support caveat;
  hip carrier v1 has plate 2 slices but no recorded physical result. Prior
  shank v2 slice records below match the current STL hashes; those layers were
  not re-reviewed in the current front/thigh/torso slice batch. The following
  dated records apply only to their identified revisions and investigations.

  **Historical issue: the pelvis socket module was weak and
  hard to print.** Raised by the maintainer 2026-09-14 against the DEC-49
  `pelvis_socket` (`parts/pelvis.py`), the piece between the torso and the
  pitch servo. The `root_carrier` one joint out was reviewed at the same time
  and is acceptable (below).

  **Pelvis socket module (maintainer's finding: unprintable as drawn,
  inherently weak).** The pitch servo hangs 46 mm below the torso flange
  plate, held only by the 5 mm socket-floor web (67 mm tall) that meets the
  5 mm flange plate (86 mm long) at a single right-angle corner. That corner
  is two separately filleted boxes overlapped, with no inside fillet
  (fillet-after-union rule, `integrated-links.md`). The plate then carries the
  whole leg as a cantilever to two M3 frame bolts at x = −30 and −20, only
  10 mm apart in one row at y = 34, plus two Ø4 × 2 mm locating pins, 60–70 mm
  from the corner. Every leg moment is resolved by prying over that 10 mm
  bolt pitch and by the pins in 2 mm of plastic. Printed socket-floor down as
  declared, the flange stands as an 86 mm tall, 5 mm thick wall on a small
  footprint, with its hole roofs near the top. The shoulder module has no
  web (flat plate on the frame face) but the same two-bolt cantilever.
  Construction options, none modelled:
  1. **Box the module.** Side cheeks join web and flange into a closed
     C-section; union first, fillet the outside edges and the concave junction
     edges; spread the frame bolts to four corners of the plate or add a
     second row. Keeps DEC-45's bench-assembled independent modules. Minimum
     fix; still a cantilever off the frame face.
  2. **Let the frame carry the moment.** The module is captured by the torso
     frame (tongue between the flange and the y = ±36 rails, or a dovetail)
     so broad faces take the leg moment and the bolts only clamp, which is
     what DEC-45 intended and the implementation does not deliver.
  3. **Socket cast into a one-piece crossmember, SO-101 Base pattern.** The
     pitch servo sits inside the torso's own structure with no module and no
     cantilever. Needs a new answer to DEC-45's blocked inboard ear screws:
     capture the inboard ears in a blind slot the servo slides into and screw
     only the outboard ears, or retain by cradle plus collar as SO-101's base
     does. Unverified; the strongest and cleanest if the retention works.
  Recommended: 3 if the ear retention can be shown on a coupon; else 1 + 2
  together.

  **Trial, 2026-09-14: the shoulder module at both roots does not work with
  the carrier as built.** Three edits (rear `pitch_socket` as the front's
  rotated 180° about the pitch axis so the case stands into the torso; the
  front plate and no web at the rear; `ROOT_REAR_MOUNT_Z = ROOT_MOUNT_Z`),
  then the viewer's limit search. Result: the saved **upright pose itself
  intersects** (`pelvis_socket` vs `rear_carrier`: the carrier's flat back is
  40.1 mm from the pitch axis and its corners sweep 45.97 mm, the plate sits
  at 40.1) and **quadruped pitch max falls from 91° to 42.5°**, stopped by
  the rear carrier against the vertical pitch case. The plate clash is the
  5.9 mm DEC-49 moved the flange; the case clash is why DEC-49 also turned
  the case horizontal, which is what forces the web and the right-angle
  return. So the root module's shape is set by the carrier: the roll servo
  sits on the torso side of the pitch axis, and its back sweeps through
  wherever a vertical case would stand. The real choice is therefore
  (a) keep the carrier and rebuild the module's construction (options 1–3),
  or (b) move the roll servo beside the pitch servo (L-block or SO-101
  end-on, below), which shrinks the carrier's swept radius to about a case
  half-width, lets the pitch case stand vertical at both roots, and makes
  the flat shoulder module the single root part, printed four times.
  **DEC-52/53/55 settle it:** separate modules with four ear screws and
  captive M3 nuts under the servo (DEC-53), vertical cases at both roots, and
  a hip carrier below the pitch axis with the roll servo Bottom-down (DEC-55).
  Still open here: physical acceptance of the hip carrier and the new thigh
  forks (no slice, no print), the thigh's zero margin between roll socket and
  knee shelf at 85 mm, and the shoulder carrier, which waits for DEC-54.
  **Travel found by the viewer search, 2026-09-14, DEC-55 as committed:**
  roll −3.5° to 9.75° in both poses (was −5° to 116°), stopped inward by the
  thigh slab tipping under the carrier block and outward by the slab's flat
  top against B's flat socket floor 2 mm above it; quadruped pitch −2.75° to
  96° (was −27° to 91°), the hind leg's forward swing stopped by the carrier
  block's top corners against the root module's Side-wall returns, both
  lying on the same 18 mm radius about the pitch axis; upright pitch −77° to
  131° (was −101° to 58°). Candidate fixes, unmodelled: (a) make B's socket
  underside and the thigh slab top concentric cylinders about the roll axis
  so outward roll is free; (b) shorten the module's Side-wall returns or
  taper the block's forward corner so the hind leg can protract; inward roll
  was already ≈5° and is bounded by the block. Judge in the viewer before
  changing either part.

  **DEC-56 carrier refinement, 2026-09-14:** the 16 mm block, tapered 2 mm
  bevels and filleted structural joins are implemented. The viewer now gives
  quadruped pitch −7° to 96.25° and upright pitch −81.5° to 131.25°; the
  forward stop is the carrier against the pitch servo, instead of the root
  module. Roll is still −3.5° to 9.75°. [View and checks](design/hip-carrier-refinement.json).
  These are displayed mesh/fallback-case bounds, **not accepted full-reference
  endpoints**: the imported STEP intersects the carrier's inner idler-root
  fillet by 0.0134 mm³ at quadruped −7° and 0.0200 mm³ at upright −81.5°.
  Quadruped −6° has zero overlap against both references at that sample.
  The maintainer still finds forward travel insufficient for quadruped walking;
  a required foot trajectory and rest configuration have not been selected.
  Carrier printability and unchanged whole-joint strength remain unverified.
  The thigh's obstructed fixings and unfilleted joins below are deferred
  until the carrier review is complete. The nut-reference and audit issues
  are also still open; these new carrier checks do not close them.

  **Carrier orientation proposal, 2026-09-14:** the maintainer proposed a
  horizontal carrier or 45° down in four-legged rest, instead of either
  vertical orientation. [Side-view placement study](design/carrier-orientation/README.md)
  rotates the existing carrier about A's pitch pivot, with the root fixed.
  Its current bottom direction is 77.47° below world forward. At 45° down
  rearward (pitch delta +57.53°), the carrier and B case clear the root module
  and A case at that sample and at ±10°/±20° around it; horizontal rearward also clears those two
  obstacles. Forward 45° and horizontal placements intersect the root and
  A case. A whole-carrier rotation also tilts B's shaft: 45° at the diagonal
  placements, vertical at horizontal placements. The thigh, foot location
  and useful lateral motion must therefore be re-derived before accepting
  such a rest pose. Rotating only B's body/socket about its own shaft is a
  distinct alternative that retains the axes but needs a new connecting
  bridge. **No new orientation is selected or implemented.**

  **Clarification and connected candidate, 2026-09-14:** retain the pitch
  socket and put the fork arms 45° down/rearward; the roll-socket connection
  and printing are the questions. A [separate angled-fork candidate](design/carrier-orientation/README.md)
  joins those forks to the unchanged roll socket with a filleted/gusseted
  wedge and common flat print base. The roll shaft need not tilt with the
  forks. The candidate is a valid single solid, 60.6 × 77.7 × 50.5 mm;
  44 scoped checks pass, including seven quadruped pitch samples from −30°
  through +30° against the fixed root module and pitch case. The horn pads
  are preserved and the existing thigh clears at both saved rest poses.
  Its solid volume is about 70% greater than the current carrier: refine the
  material distribution and assess strength/support removal before adopting
  it. Printable remains `unknown`; no slice, print, continuous travel or
  gait acceptance. Production geometry and saved poses are unchanged.

  **Reopened in favour of the simpler carrier, 2026-09-14:** after initially
  accepting the angled-fork arrangement, the maintainer proposed tilting the
  pitch socket and putting its non-vertical mounting face into the torso.
  They favour a 45° slope for printing. Carrier lightening is paused.
  The [inclined-face study](design/carrier-orientation/README.md) retains both
  existing joint prints and their print orientations. A −45° socket rotation
  about the unchanged pitch shaft passes sampled carrier/roll-case clearance
  against the module, pitch case and matching face patch through −51° forward
  pitch and at +30° in both saved poses. The four local frame-driver paths
  clear; access through a completed torso is not yet modelled. With the current
  torso print orientation, the proposed surface is 45° to the bed. The 5 mm
  patch represents a torso surface, not a new separate print. Complete the
  torso wall transitions and travel/access review remain open. DEC-57 now
  selects 45° as the proposal and the rear-leg study implements that placement;
  no main-assembly mount or saved pose change has been made.

  **CAD review, 2026-09-14 (DEC-53/55, source at `44a8a8e`, before DEC-56):**
  - **Thigh roll-horn fixings are obstructed.** In `upper_link(..., hip=True)`,
    the cheek/join boxes start at Z = 5 mm and are added after the horn holes
    and head recesses were cut. They refill the knee-facing pair on each
    horn: four screws per thigh. Individual-solid BREP checks find
    96.706 mm³ total intrusion into the four supplied heads and two idler
    washers, on both hands in both saved poses. The through-bores are also
    partly filled. [Sections through the heads](design/hind-root-review.png).
    Restore the bores, recesses and straight driver approaches after the
    structural unions, then recheck the remaining plastic section.
  - **The new thigh and hip carrier still have square internal junctions.**
    The cheek/join/shelf and fork/block unions return without the internal
    fillets or gussets required by `integrated-links.md`. Review those load
    turns in section; no strength failure is inferred from their shape alone.
  - **The full nominal assembly audit fails in both poses despite all 25 unit
    tests passing.** `pelvis.fixing_envelopes()` represents each captive hex
    nut by its circumscribed cylinder, giving 35.372 mm³ false interference
    per root module. A matching 5.5 AF hexagonal nut gives zero overlap in
    the 5.7 AF pocket; correct the reference, not the pocket. Compound
    hardware intersections also give pose-dependent misses/false positives:
    check their component solids separately. This confirms the thigh/head
    clash above but finds no roll/knee ear-head clash at rest. The viewer
    skips rigid pairs on the assumption that this audit has passed, so a
    successful limit-cache build does not establish assembly clearance.
  - The current cache matches its scene and engine hashes. Independent BREP
    checks confirm the carrier/thigh pair clears at roll −3.5°/9.75° and the
    module/carrier pair clears at quadruped pitch −2.75°; interference starts
    just beyond the reserved ranges. These are selected-pair checks, not a
    new full endpoint acceptance. The published `travel-endpoints.json`
    still describes the earlier geometry and needs regeneration after the
    baseline audit is repaired. Roll/knee socket ear-driver and nominal
    cable probes clear their owning new prints at rest.
  - The viewer's assembly metadata lookup still uses the retired
    `root_carrier`, `pelvis_socket` and `shoulder_socket` design names;
    all eight installed carriers/root modules consequently have null
    printability tags. Update the mapping and the obsolete all-`assumed`
    browser smoke assertions when validating this revision.

  **Root carrier: acceptable (maintainer, 2026-09-14).** The session's first
  review called its 16 × 15 mm bridge weak; that was overstated and is
  withdrawn. Pitch centres ±24 mm, roll centres ±74.5 mm, roll socket floor
  40 mm below the pitch axis (`parts/links.py` `carrier()`). A 15 N leg load
  (half of a 3 kg robot on two legs, DEC-15) at the 50.5 mm reach gives
  ≈ 0.76 N·m at the bridge and ≈ 1.3 MPa bending stress, far inside PETG.
  Printed back-down the bending tension lies in the layer plane, not across
  it; the horn discs print as supported towers, which the local slice
  already covers. Dynamic and torsional loads are unmeasured (OQ-16). Layout
  alternatives are noted only in case the roll arrangement is revisited: an
  L-block with the roll servo alongside the pitch servo (SpotMicro / Orion
  pattern, roll axis ≈ 54 mm, no reach) or the SO-101 end-on shoulder (roll
  axis ≈ 85 mm); dropping rear roll for V1 would free two ST3215s but is a
  concept change. None is required.

  The module construction above was subsequently replaced by DEC-53/55;
  current acceptance remains version-specific.
  **Print planned 2026-09-19 (owner, 2026-09-18); plate 1 printed 2026-09-19, fit passes, ear holes blocked by support (profile fixed, see `test-log.md`); plate 2 re-sliced with bed-only support:** the root socket (2 per hand) and hip
  carrier (1 per hand), PETG, sliced on `printhub` (online for slicer access since
  2026-09-18). Root socket v1 is now `proven` with the ear-hole caveat;
  hip carrier v1 remains `assumed` until plate 2's result is recorded. The
  thigh/shank forms rejected on 2026-09-18 have since been replaced; see
  [current part versions and print approaches](part-design-review.md).
  **Sliced 2026-09-18 (printhub clock 2026-09-19 00:50 BST), nothing printed:** base
  `~/slicer/ender5s1_petg.ini` plus `hardware/print/manufacturing-petg.ini` (4 perimeters,
  30 % grid, snug supports from 45°, 4 mm brim, 240/80 °C), Debian `prusa-slicer` 2.5.0 with
  `--merge --center 104,123`. In Mainsail: `koala-root-socket-x4.gcode` (2 left + 2 right,
  9 h 10 min, 89 g, footprint X 46–162 Y 75–171) and `koala-hip-carrier-x2.gcode` (left +
  right, 7 h 00 min, 68 g, X 52–156 Y 71–175); both inside the probed mesh. STL SHA-256
  prefixes: root_socket 298f0eff (L) / cbd58598 (R), hip_carrier eb5a282a (L) / ad7843e2 (R),
  from the 2026-09-18 export. Times and masses are slicer estimates. **Slicer fact for the
  3d-printing repo:** the Flathub PrusaSlicer 2.9.6 segfaults (exit 139) on `--merge` with
  these STLs, single-part slicing works, and `slice-plate.sh` prints "Done" on that crash
  because its pipeline hides the exit code; the Debian 2.5.0 binary merges correctly.
  **Re-sliced and sliced 2026-09-19 after plate 1, all with support from the bed only:**
  `koala-hip-carrier-x2.gcode` re-sliced (Debian 2.5.0, snug bed-only: 6 h 42 min, 66 g, no
  support at all now; the earlier file had 900 support blocks, all off the part). The v2 legs,
  one part per job on the Flathub 2.9.6 slicer with organic support from the bed
  (`manufacturing-petg-tree.ini`): `koala-thigh-v2-left.gcode` 4 h 57 min / 49 g,
  `koala-thigh-v2-right.gcode` 5 h 03 min / 50 g, `koala-shank-v2-left.gcode` 3 h 56 min / 39 g,
  `koala-shank-v2-right.gcode` 3 h 59 min / 39 g. STL SHA-256 prefixes: thigh bca33526 (L) /
  15ea8a90 (R), shank 335d9f74 (L) / ae2ac311 (R), v2 exports of 2026-09-19. Known consequence of
  bed-only support on the shank: the Ø39 motor bore's roof prints unsupported as an arc, so
  expect some sag at the top of the bore; check the 37D still slides in and file if needed.

- **OQ-21 — Physical joint travel and control limits.** DEC-48 implements
  DEC-46's pose-dependent viewer search using the printed geometry and nominal
  hardware envelopes. The search uses 0.25° steps and a 2° reserve before the
  first intersection, within a ±180° search ceiling. Servo indexing, actual
  electrical limits, tolerances, complete cables/guards and loaded operation
  remain unverified. This is a finite-resolution clearance aid, not continuous
  swept-volume certification or a gait controller limit. The 2026-09-19 front
  roll-first/rear pitch-first chains have different transforms. Complete front
  moving-package checks clear commanded roll ±30° at 2° samples in both saved
  configurations; installed two-front checks cover five roll settings with
  both case models. The 1° adjacent-joint native carrier-only range is narrower
  evidence, not a complete limb limit. Accept continuous/load-bearing movement
  and useful gestures separately.

- **OQ-20 — Physical acceptance of the SO-101 construction adaptation.**
  The current enclosing sockets, filleted fork roots, independent root modules
  and broad print faces need physical support-removal, assembly and load/creep
  checks. The old DEC-49 pelvis corner defect was replaced by DEC-53/55; it is
  not a defect in the current proven root socket v1. That print establishes
  socket geometry/fit with its ear-hole caveat, not acceptance of the complete
  chassis. Changed shoulder parts, torso v5 and thigh v3 are `unknown`.
  No repeat Gauge_0 is required. [Part review](part-design-review.md).

- **OQ-20 — Pace and scope.** (Owner, 2026-09-18.) The design continues as a
  **background task**, paced by the owner's frontier-AI token limits rather than by the
  project. The owner doubts the ambition of a unique limb geometry — the CAD is far from
  done and no part of the current revision has been printed — and keeps returning to
  "build something proven that you can print and assemble as easily as SO-ARM was".
  **The problem is not kinematics or gait** (owner correction, 2026-09-18): it is
  aesthetics and printability — the AI assistants keep producing unprintable designs, and
  describing 3D geometry in words, against what an image shows, is the draining part.
  Reviews of CAD should therefore go through rendered images (the viewer, the slice and
  layer images under `docs/design/manufacturing/`) and marked-up screenshots, which
  assistants can read, rather than prose descriptions of geometry.
  Not a pivot and not a parking: koala-bot stays active at background pace. Which proven
  build, if any, runs alongside it is a family question in
  [wk-robotics `status.md`](https://github.com/WayneKennedy/wk-robotics/blob/main/docs/status.md).
  **DEC-59, 2026-09-18:** the owner probed the 29 decisions banked since the restart and
  found most were turns of this review loop. Twelve are reclassified as revision notes;
  the rule for what a DEC is now lives in `AGENTS.md`. **Proposed next gate (assistant,
  2026-09-18, not agreed):** the next commit that touches geometry is a physical print of
  the `root_socket` module — the smallest new part, on every limb's load path — recorded
  in `test-log.md`; no further revision note until it has been handled.

- **OQ-19 — Front-foot contact acceptance.** DEC-43 fixes the rear ankle-wheel
  location and retains current size. The CAD uses a 75 mm forearm plus 25 mm
  hand to a fixed Ø32 mm ball centre, with both front feet on the floor in the
  supported pose. DEC-48 selects separate TPU pads with keyed seats and recessed
  fixings. Establish TPU grade/settings, grip, wear and contact behaviour under
  load; the geometry and local slice do not establish traction.
- **OQ-18 — Detailed packaging and contact transition.** Check the transition
  from front feet plus rear wheel contacts to rear-wheel balance: CoM/support
  polygons, clearances, body-weight shifts and servo forces throughout. Define
  physical haunch/rest supports if needed. Head position and mounting are
  undecided; DEC-49 removes the unsupported placeholder from structural CAD
  and clearance searches. The shoulder now reserves a cartridge for three
  small STS3032M servos ([provision](design/neck-provision.md)); its retention,
  3-RPS linkage and head location are still open. Complete battery/electronics,
  harnesses and guards. Power-off standing needs a demonstrated support path.
- **OQ-17 — Two-wheel drive acceptance and later gait.** Wheel location and
  bought 37D retention are settled by DEC-43; no knee-drive or belt study is
  required for V1. Establish actual drive current/thermal duty, axle/hub loads
  and rear-pair balance recovery on the assembled robot. Uneven-terrain stepping
  with wheel-feet, including wheel holding and traction, remains a later
  experiment. [Historical motor comparison](drive-motor-sizing.md).
- **OQ-16 — Limb physical acceptance.** Twelve STS3215s needed — **eight in hand**
  since four went to SO-ARM101 permanently on 2026-09-12; **a 6-pack was ordered on
  2026-09-14** to backfill (AliExpress, shipped 2026-09-15, in UK customs with the final courier on 2026-09-21, expected within 2–3 days (owner); `bom.md`). Removing front
  drives reduces arm swing loads; rear wheel mass remains at the ankles.
  Establish actual mass/CoM, continuous torque/temperature, ground reactions
  and printed joint strength for support and transition. Digital collision
  checks do not validate loaded motion. Fit one joint, then complete limbs
  and loaded support.

- **OQ-13 - Lower-body mechanical redesign and FDM validation.** Two drafts
  have been discarded (DEC-30): a3f265c for interference, blind holes and an
  unassemblable motor clamp ([review](cad-review.md)); DEC-29 for breaching
  DEC-21's mounting pattern and widening the track to 258.8 mm as a packaging
  escape ([record](cad-redesign.md)). Neither reached a structural print. The
  redesign now follows [`cad-restart-brief.md`](cad-restart-brief.md) in
  order: use the confirmed SO-101 fit (DEC-33), bank requirements, reserve
  swept envelopes, design with the socket primitive, then print one joint rig.
  DEC-40 replaces DEC-34 with integrated four-limb geometry and the corrected
  interface ([design record](cad-integrated-design.md)). No new part
  has yet been sliced or printed. **Closes when** a full lower body passes fit and a documented load test
  (OQ-11). Retention dimensions remain OQ-12; the leg's open choices are OQ-16.

- **OQ-14 - micro-ROS on the bought Teensy 4.0.** **Resolved 2026-09-18 by DEC-18 as amended:
  the question is retired unanswered - the robot moves to a Teensy 4.1 NE instead of testing the
  4.0.** The owner's reasoning: a passing test would prove one version works on one day, not that
  the board is supported, and "Not tested" means it is in nobody's CI, so the risk is standing
  rather than one-off. That is the wrong footing for a load-bearing reflex tier (DEC-04, and the
  family's two-tier rule), and ~GBP 30 also standardises the MCU across three robots. The 4.0
  goes to the bench logger, where micro-ROS is not used. Original text kept below.

  Upstream lists the 4.0 as
  "Not tested" where the 4.1 is Supported. DEC-18 bought the 4.0, and DEC-04 makes
  the bridge load-bearing, so the untested board sits on a load-bearing path
  rather than a peripheral one. The board table and the shared reasoning
  live in
  [wk-robotics](https://github.com/WayneKennedy/wk-robotics/blob/main/docs/common.md#micro-ros-how-the-mcu-joins-the-graph),
  not here.
  **Cheap to close, and worth closing before firmware:** flash a micro-ROS example
  to the 4.0, then log the result in [`test-log.md`](test-log.md). If it fails the
  fallback is a Teensy 4.1 or the ESP32 named in
  [`architecture.md`](architecture.md#bridge--contract) - not a redesign. Since
  2026-09-11 the family holds an **unallocated Teensy 4.1 NE**
  ([wk-robotics `common.md`](https://github.com/WayneKennedy/wk-robotics/blob/main/docs/common.md#drive-motors-drivers-and-mcus-in-hand)),
  so the fallback costs nothing to buy - but it is first-come, not reserved for koala.
  **This is now koala's risk alone:** wk-devastator closed its half as DEC-10 - it
  buys a 4.1 rather than prove a 4.0 - and confirmed koala's 4.0 is committed to
  this build, not a family spare. Whether an untested board already bought is worth
  proving or writing off is a koala decision nobody else shares.

- **OQ-03 - Torso platform's 3 DOF.** pitch + roll + **yaw** (twist, very lifelike) vs
  pitch + roll + **heave** (breathing bob). Can't have all four from 3 actuators.
- **OQ-04 - Head eyes & mass.** Screen/OLED eyes (light, expressive) vs mechanical eye
  servos (mass). Confirm the < ~250-300 g head budget that keeps micro servos viable.
- **OQ-09 - Swappable limb-ends in V1.** Design the quick-swap wrist/ankle mount into V1,
  or defer to the climber sibling?
- **OQ-11 - Structural print profile.** The BOM's measured filament and time come
  from the reference printer's **general-purpose** PETG profile (3 perimeters, 15 %
  grid) — that profile was measured *with*, not chosen *for*, koala-bot. Load-bearing
  parts (hip link, thigh, hip bracket) may want 4-5 perimeters, since perimeters buy
  more strength per gram than infill; the cost is time and filament, and the BOM
  totals move with it. **Resolve on evidence:** print one structural part, load it to
  failure or to visible flex, and compare. Until then the profile table in
  [`bom.md`](bom.md) is a record of how the numbers were produced, not a decision.
- **OQ-12 - New socket rig acceptance.** DEC-33 removes the caliper and
  repeat-gauge prerequisite: the maintainer confirms ST3215 fit in the
  SO-101 parts in PLA+ and PETG. Adopt the upstream printed-part pocket,
  asymmetric lug positions and the corrected measured horn stack in
  [`soarm-joint-pattern.md`](soarm-joint-pattern.md); the 2026-09-08 caliper
  evidence is recorded in `test-log.md`. The [DEC-40 implementation](cad-integrated-design.md) addresses the earlier
  interface failures; demonstrate its **new four-ear saddle and integrated
  double-horn clevis** on a real servo: insertion and removal, M2x5 engagement
  without bottoming, both horn patterns, M3 engagement and centre-screw
  access, free rotation without axial preload, and cable clearance. Log
  the rig fit before printing a full leg. Full-body strength remains OQ-13.

- **OQ-10 - Child-safety spec** (audience 2-5; DEC-15). Resolve during design: pinch-point
  guarding at every joint/linkage; software speed & torque limits + e-stop; graceful-fall
  behaviour; protected/enclosed LiPo; no small detachable parts; rounded edges; no hot
  exposed surfaces. Reference EN 71 (toy safety) for guidance, not as a certification target.
