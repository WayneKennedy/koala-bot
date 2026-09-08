# DEC-34 lower-body prototype — 2026-09-07

Replacement build123d geometry for DEC-30/31. **Digital prototype; no new part
has been sliced, printed, fitted or load-tested.** The confirmed SO-101 fit
(DEC-33) is the input, not acceptance of these new parts. Start physical work
with the five `coupon_socket_*` parts and one real servo.

## Requirements and chosen packaging

DEC-32 banks the study targets; DEC-34 records the resulting compromises.
Dimensions and assumptions live in `hardware/src/koala_hardware/params.py`.

| Item | Implemented nominal / consequence |
|---|---|
| Chain | Pelvis roll → pitch → thigh → knee → shank → direct-drive ankle wheel |
| Thigh / shank | 100 / 100 mm between axes |
| Stance | Hip 15°, knee 30°; axle under hip-pitch axis in side view |
| Deck height | 283.2 mm; 150 mm upper-body allocation gives 433.2 mm overall |
| Track | 237.3 mm wheel centres, 247.3 mm tyre outside width (239.5 / 249.5 as designed on the 37.5 span; corrected 2026-09-08 to the measured 36.4 — `params.py` derives it) |
| Hip axes | Pitch 70.115 mm forward and 34 mm outboard of roll, same height; 77.9 mm axis-centre spacing |
| Roll inspection range | ±5°; reduced from the ±10° study target to retain a track below 240 mm |
| Hip / knee inspection ranges | −10…45° / 0…90°; hip extension reduced from the −30° study target |
| Motor | Inboard 69 mm body, coaxial with wheel, no belt or ankle DOF |
| Neutral motor end gap | 55.5 mm; inward-roll/unequal-flexion poses checked separately |
| Pelvis | 180 × 150 mm deck, roll roots integral; deck top against bed |
| Upper-body interface | Four M3 through-holes on a 40 mm square for a rigid strut; future parallel-platform and shoulder-girdle interfaces remain open |

The fore/aft hip spacing buys a straight assembly path: the pitch socket
attaches beyond the roll drive cheek, and its recessed carrier screws are
installed before the pitch servo. This is a substantial packaging compromise,
not a claim of optimal hip compactness. The deck extends rearward to contain
the roll roots while the nominal wheel line sits beneath the tray origin.
Further compaction must preserve socket, driver and swept-link clearance.
The inspection ranges are **not commissioned control limits** or a promise
that every combination is a usable balanced stance.

`uv run python -m koala_hardware.leg_sizing` reproduces the preliminary
100/100 mm, 65 mm hip-stack study. Its ~298 mm nominal deck is a **candidate**;
the implemented hip has no vertical roll/pitch offset and a 50 mm deck-to-roll
drop, hence 283.2 mm. Keep the study and the implemented datums distinct.
The study's motor interval calculation includes the cylinder radius when
rolled; disjoint lateral intervals are sufficient separation, while overlapping
intervals alone do not prove a solid collision.

## Socket and load path

`servo_iface` uses X for the output axis and Z for case length. The rear case
face is Z=0. Lug positions use that case datum; horn holes use the output-axis
datum. The pocket comes from Gauge_0, **not a servo STEP**.

All six joints use the same rear cradle, sliding collar and two bolted horn
plates. Four M2x5 screws retain each case through its own lugs, with 2.2 mm
printed seats. Collar bosses slide into open lanes in the cradle; the sleeve
has ports for the opposite screws. An open-front channel reserves a provisional
cable route. Actual connectors, bend radii and articulated service loops remain
rig checks; there is no claim that a complete routed loom has been validated.

The drive plate has a blind Ø20.5 × 0.8 mm horn recess and centre access.
The **idler plate has a flat seat**: upstream's adopted idler is nominally
flush, so applying the same recess there put its annulus into the case in the
first boolean check. DEC-34 records this departure from the brief's identical
recesses. Both plates retain all four horn holes; neither uses a through-bore
in place of the idler fastening material.

Printed rectangular shoulders register the fork crossbars. The shank's motor
plates register on round shoulders and clamp against the central core.
Tapered supports expand the core/stem into each cradle shelf without an
unsupported ledge. Cheeks and motor plates print flat; cores print crossbar-end
down, so tensile loads across layers remain a physical test concern.

The left pelvis root is actually mirrored. Chiral thigh cores, pitch cradles
and collars export separate left/right STLs; symmetric cheeks and motor
plates are shared. The fit rig must check the intended hardware orientation
and cable exit before committing either handed leg.

## Fastener stacks and assembly order

The exporter generates both part quantities and the fastening schedule in
[`bom.md`](bom.md) from builder metadata. Counts cover six lower-body servos;
coupon hardware and supplier-specific wheel/hub fixings are separate.

| Interface | Candidate stack, before physical verification |
|---|---|
| Four case screws per servo | M2x5 − 2.2 mm seat = 2.8 mm nominal lug engagement |
| Drive horn square | M3x6 − 2.7 mm recess floor = 3.3 mm engagement |
| Idler horn square | M3x6 − 3.5 mm flat cheek = 2.5 mm engagement |
| Thigh/shank proximal crossbar | 35.6 mm spacer + two 3.5 mm cheeks = 42.6 mm grip; M3x50, washers and nut |
| Hip carrier | Recessed head seat to outer idler cheek = 51.85 mm grip; M3x60, nut-side washer and nut |
| Shank motor-plate seam | 35.6 + two 5 mm plates = 45.6 mm grip; M3x55, washers and nut |

Span-derived grips above were shortened by 1.1 mm on 2026-09-08 when the horn
span was measured at 36.4 (test-log); screw lengths are unchanged.
| Motor face | Six M3x8 per motor, 5 mm plate → 3 mm nominal engagement; verify motor bore depth |
| Hub | 5 mm plate + 3 mm cap head + 0.5 mm axial allowance + 9.5 mm hub = 18 mm stack; verify actual hub/set-screw access |
| Tray | Four 10 mm female/female standoffs, M3x10 below 5 mm deck and M3x8 above 4 mm tray; verify thread depths |
| Driver shield | Four M3x16 through tray/standoffs and board into nuts; actual board stack remains to check |

1. Fit the rig cradle and collar to a servo using all four M2x5 screws. Check
   seating, removal, engagement and cable access without bottoming a screw.
2. Install drive/idler horns and their centre fixings as the kit requires.
   Fit both cheeks and the crossbar without drawing the plates inward to
   compensate for the wrong span. Check motion and centre-screw access.
3. For the pelvis, fit roll servos/collars, then the two roll cheeks and hip
   crossbar. Insert the recessed carrier bolts **before** fitting each pitch
   servo; the pitch servo hides these screw heads after assembly.
4. Fit thigh cheeks, thigh core and knee servo/collar; then shank cheeks/core.
   Fit the motor support/face plates, slide the motor into the body support,
   and install face screws before the hub/wheel obscures access.
5. Fit tray standoffs and electronics. Keep torso/arm/head interfaces and
   their fasteners out of this lower-body fastening count.

The long through-bolts protrude beyond their nuts (roughly 3–5 mm with the
nominal stacks). Horn heads also stand proud. Covers, final screw lengths,
pinch guards and external rounding are still OQ-10; this is a bench prototype.
No plastic threads or assumed heat-set-insert pull-out strength carry these
structural seams.

## Load budget and torque screen

Design mass ceiling is 3 kg (DEC-15/32). A **budget, not a weighing**: limb
servos 0.66 kg (12 × 55 g specification); drive units 0.50 kg; neck actuators
0.15 kg; compute/electronics 0.25 kg; battery/power 0.35 kg; lower-body prints
0.60 kg; upper-body structure 0.35 kg; wiring/fasteners/remaining allowance
0.14 kg. Sum 3.00 kg. Actual bought masses, printed mass and CoM remain open;
the generated solid-volume maximum is not a slicer mass prediction.

For a 3 kg robot sharing weight equally, knee vertical load is 14.71 N.
With equal links and hip = knee/2, the static knee moment is
`1.5 kgf × (100 sin(knee/2) / 10) cm`. At 90° knee flexion it is
**10.61 kgf·cm**. Adding either direction of a 0.5g longitudinal ground force
raises the larger magnitude to **18.91 kgf·cm**; the horizontal-force lever
includes the 40 mm wheel radius. Across arbitrary shank angles the same
force bound peaks at **19.77 kgf·cm**. Distal masses, link inertia, friction,
impact transients and thermal duty are not modelled.

Waveshare advertises **30 kg·cm at 12 V**, without establishing a continuous
holding rating in the cited specification. The ratio to these calculated
moments is therefore **not a continuous-duty margin or safety factor**.
[Waveshare ST3215 specification](https://www.waveshare.com/product/modules/st3215-servo.htm).

DEC-32's structural test targets are 29.42 N total static weight, **58.84 N
on one wheel** for the 2g case, a 10 N lateral shove at head height, and
lifting by the torso with the legs hanging. A horizontal shank under the
one-wheel 2g target would demand **60 kgf·cm** at the knee: powered holding
of that load is not supported by the advertised rating. Test printed
structure in a fixture that bypasses the servo drivetrain; establish powered
motion, load sharing and thermal limits separately. No jumping or one-leg
powered support requirement is banked here.

## Digital checks and remaining gates

- Export: all part designs must be valid connected solids (seam coupon is
  deliberately two bodies), fit ≤200 × 200 mm in their declared orientation,
  and pass the existing bed-contact/overhang screen. Handed files are explicit.
- Audit: shared socket fit and driver/cable corridors, full-depth M2 and horn
  hole probes, full crossbar/carrier/motor seam shafts, tray through-bores
  and underside driver paths, a sampled rig sweep, 27 local roll/hip/knee poses, and
  81 combinations of independent opposing-leg flexion at inward roll.
  Includes nominal horn/carrier/motor/lug heads and nuts. No continuous
  sweep, tolerance expansion, complete loom or complete tool-access proof.
- Viewer: hip and knee have distinct hierarchical pivots. Browser regression
  compares moved left/right mesh bounds against CAD, not merely slider motion.
- Unit tests: analytical link geometry/force moments and the retained
  bed-contact classifier regressions.

Read-only Moonraker checks on 2026-09-07 and at 00:01 BST on 2026-09-08
returned **printing**. No slicing
or print was started. Next: printer idle → inspect PETG layers for the five
`coupon_socket_*` parts → print and fit one joint → log it → one full leg →
the pair → documented strength, creep and motion testing (OQ-11/13).
The restart brief remains open until physical acceptance; digital checks do
not close it.
