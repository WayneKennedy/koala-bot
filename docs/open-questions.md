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

- **OQ-25 — Elbow axis in the roll direction: the "hug".** Raised with
  DEC-54. With the elbow axis parallel to the shoulder roll axis (along the
  spine), the forearms fold sideways and inward: in upright with the arms
  forward the axes are vertical and both forearms close like a hug, the
  clinging grip a koala uses on a trunk and a possible basis for climbing;
  in quadruped the axes are horizontal fore-aft and a front foot lifts by
  folding the forearm inward under the body, a sprawling rather than a
  sagittal knee. What it gives up: the forearm no longer shortens the leg in
  the sagittal plane, so fore-aft foot placement comes from shoulder pitch
  alone, and the front step length is bounded by that swing. Four-foot walking
  is already experimental (DEC-43), so this is a small further bet on the
  supported stance and the lift-to-balance transition working with a
  sideways-folding foreleg. It also decides the shoulder block's form: with a
  sagittal elbow, B (pitch) and C (elbow) are parallel and can share one
  block on A's horn with a link down the upper arm, the Orion pattern; with
  the hug elbow they are perpendicular, as B and C already are at the rear,
  and C must sit on the upper arm. Decide before the front upper arm is
  drawn; it changes the elbow socket's attitude and the shoulder block.

- **OQ-23 — Torso width and neck servo packaging.** The two shoulder socket
  modules meet at the centreline with a 0.6 mm gap (DEC-48), so the shoulder
  girdle, where `architecture.md` mounts the three STS3032M neck servos,
  has no room for them. DEC-53 expects a wider torso. Widening moves
  `ROOT_PITCH_Y` (48 mm centres, DEC-41) and with it the carrier reach, the
  149 mm roll centres and the 220 mm track (DEC-40/41/49); the head envelope
  and neck length (DEC-37/49) are unchanged by it. Decide the width once the
  leg (DEC-53) fixes the root module and carrier, and before the torso frame.

- **OQ-22 — Root joint construction: the pelvis socket module is weak and
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

  Decide the module construction before any root part is printed; re-run
  frame contact and OQ-21 clearance checks for the chosen option.

- **OQ-21 — Physical joint travel and control limits.** DEC-48 implements
  DEC-46's pose-dependent viewer search using the printed geometry and nominal
  hardware envelopes. The search uses 0.25° steps and a 1° reserve before the
  first intersection, within a ±180° search ceiling. Servo indexing, actual
  electrical limits, tolerances, complete cables/guards and loaded operation
  remain unverified. This is a finite-resolution clearance aid, not continuous
  swept-volume certification or a gait controller limit.

- **OQ-20 — Physical acceptance of the SO-101 construction adaptation.**
  DEC-48/49/50 implement enclosing asymmetric sockets, rounded links/forks,
  common carriers at all four roots and independent root modules. **Known
  defect, 2026-09-14:** the `pelvis_socket` return corner is two separately
  filleted boxes overlapped with no inside fillet (fillet-after-union rule,
  `integrated-links.md`); its construction as a whole is OQ-22. Audit the
  other parts for the same corner construction. Bench driver approaches, nominal
  insertion and CAD clearances are checked; local slices support `assumed`
  printability. Check real support removal, mounting fit, assembly/service
  access and load/creep on the revised parts. No repeat Gauge_0 is required.
  [Part review](part-design-review.md).

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
  and clearance searches. Complete neck, battery/electronics,
  harnesses and guards. Power-off standing needs a demonstrated support path.
- **OQ-17 — Two-wheel drive acceptance and later gait.** Wheel location and
  bought 37D retention are settled by DEC-43; no knee-drive or belt study is
  required for V1. Establish actual drive current/thermal duty, axle/hub loads
  and rear-pair balance recovery on the assembled robot. Uneven-terrain stepping
  with wheel-feet, including wheel holding and traction, remains a later
  experiment. [Historical motor comparison](drive-motor-sizing.md).
- **OQ-16 — Limb physical acceptance.** Twelve STS3215s needed — **eight in hand**
  since four went to SO-ARM101 permanently on 2026-09-12; **a 6-pack was ordered from
  RCmall on 2026-09-14** to backfill (`bom.md`), arrival not yet recorded. Removing front
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

- **OQ-14 - micro-ROS on the bought Teensy 4.0.** Upstream lists the 4.0 as
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
