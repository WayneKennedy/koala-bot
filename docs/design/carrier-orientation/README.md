# Rear carrier rest orientation — studies, 2026-09-14/15

## Pitch socket on an inclined torso face — selected proposal, DEC-57

The maintainer initially accepted the angled-fork arrangement below, then
reopened the choice to preserve the simpler current carrier. Their proposal
is to put a non-vertical mounting face into the torso and attach the existing
pitch socket to it. On 2026-09-15 they selected the **45° variant as the proposed
A/B arrangement** and advanced to the [rear thigh and shank](../rear-leg/README.md).
The angled-fork candidate is parked.

[Rotate/compare socket tilts](pitch-socket-tilt.html) ·
[45° placement STEP](pitch-socket-45.step) · [Checks](pitch-socket-tilt.json) ·
[CAD/check builder](../../../hardware/src/koala_hardware/pitch_socket_tilt_study.py).
The local server provides the same preview at `/pitch-socket-tilt.html`.

The study keeps the current DEC-56 carrier and DEC-53 root socket unchanged,
including their print orientations. The pitch case/socket rotates about its
existing lateral shaft; the pitch/roll axes, joint centres and saved leg
coordinates do not move. A 5 mm torso-face patch has eight holes matching
the two modules' captive-nut patterns. It represents the eventual torso's
surface, **not another separate print**. The rest of the torso is omitted.

| Socket tilt relative to the current mounting face | Clear forward-pitch sample in quadruped | Later sample that intersects |
|---|---:|---:|
| Current | −6° in the earlier DEC-56 check | −15° |
| 30° away from the forward swing | −36° | −45° |
| 45° away from the forward swing | −51° | Not searched beyond −51° |

The 45° arrangement passes all tested carrier/roll-case checks against the
root module, pitch case and face patch at pitch 0°, −15°, −30°, −36°, −45°,
−51° and +30° in both saved body poses. All four right module frame-driver
approaches clear the module, case, opposite module and local face patch.
The print orientation declared for the current torso puts the proposed
mounting surface **45° to the bed**, consistent with the maintainer's
support-free slope preference. The root socket and carrier need no new
print geometry. The complete torso walls, their filleted transitions,
access through those walls and any bolt-hole roofs remain to be designed.

These are discrete local checks, not full assembly, continuous travel or
walking acceptance. The face patch is not a completed torso or a direct
replacement for its current flange. DEC-57 holds the 45° proposal; the main
assembly retains its previous torso mount. The separate rear-leg viewer uses
the proposed mount and revised downstream parts. Reproduce this earlier study with
`.venv/bin/python -m koala_hardware.pitch_socket_tilt_study` from `hardware/`.

## Angled forks, retained roll socket — clarification and construction

The maintainer clarified the proposal: keep the pitch socket as currently
mounted and attach the carrier with its fork arms down/rearward at 45°.
The connection to the roll socket and its print orientation are the questions
to resolve. The fork direction need not set the roll socket's angle.

[Rotatable candidate](angled-fork.html) · [Fitted view](angled-fork-assembly.png) ·
[Print orientation](angled-fork-print.png) · [Candidate STEP](angled-fork.step) ·
[Checks and hashes](angled-fork.json) ·
[Reproducible CAD/check builder](../../../hardware/src/koala_hardware/carrier_fork_study.py).
The running local viewer also serves the study at `/angled-fork.html`.

This separate candidate turns the forks **57.53° relative to the current
carrier**, putting their arms 45° down/rearward in the saved quadruped pose.
A continuous wedge joins them to B's socket, whose position and orientation
stay unchanged. Both hip axes and the saved leg coordinates are therefore
retained. The earlier warning about tilting the roll shaft applies to rotating
the entire old carrier, not to this new connecting geometry.

The wedge and socket floor share a flat print base. The part is printed on
that base, independently of its installed angle. R6.3 fork-root fillets, an
R5 socket-root fillet and rear gusset, an R1.5 socket-lip fillet and tapered
2 mm edge bevels retain rounded load transitions and complete horn pads.
The four roll ear-driver corridors are preserved through the new gusset.

The candidate is one valid solid with a watertight STL, **60.6 × 77.7 ×
50.5 mm** in its proposed print orientation and **2,774 mm²** of bed contact.
Fork undersides and hole roofs may need accessible supports; the surface
screen flags 561 mm² for inspection. Printable remains **unknown**: no slice,
support-removal trial or physical print has been performed. The full wedge
is deliberately a first construction: **62.3 cm³ versus 36.6 cm³** for the
current carrier, about 70% more solid volume. Strength and final material
distribution remain unresolved.

Forty-four exact intersection checks pass: the pitch horn heads/washers,
roll ear heads and driver/cable corridors, five servo insertion positions,
the existing thigh at both saved rest poses, and the carrier against the
fixed root module and pitch case at quadruped pitch samples −30°, −20°,
−10°, 0°, +10°, +20° and +30°, plus upright zero. The rotated horn-pad region
is unchanged. These are scoped samples, not complete assembly, continuous
travel, walking, wiring or load acceptance. The fork and its bolt pattern
rotate together; physical servo/horn indexing remains OQ-21. The thigh's
existing fixing obstruction remains OQ-22.

To regenerate the CAD and checks, run
`.venv/bin/python -m koala_hardware.carrier_fork_study` from `hardware/`.
It also writes the ignored `angled-fork.stl` in this directory, already
oriented on the bed. The HTML uses the repository's Three.js and measured
parametric servo envelopes; the exact case checks use the locally available
servo reference identified in the check record.

**This candidate is not selected for production.** The normal viewer,
production part builders, saved poses and generated BOM are unchanged by
this construction study.

## Earlier whole-carrier placement study

[Side-view comparison](comparison.png) · [SVG](comparison.svg) ·
[Exact intersection samples and source hashes](study.json).

The proposed horizontal or 45° carrier is studied here by rotating the whole
existing carrier around the hip pitch pivot. The root module stays fixed in
the saved quadruped pose. Angles describe the direction from the pivot towards
the carrier's block/socket bottom, relative to the ground. The current
direction is 77.47° below forward, rather than exactly vertical.

| Carrier placement | Pitch delta from saved pose | Root module / pitch case | Roll shaft direction |
|---|---:|---|---|
| Current | 0° | Clear at sample | 12.53° from horizontal |
| 45° down, rearward | +57.53° | Clear at sample | 45° from horizontal |
| Horizontal, rearward | +102.53° | Clear at sample | Vertical |
| 45° down, forward | −32.47° | Carrier intersects both | 45° from horizontal |
| Horizontal, forward | −77.47° | Carrier intersects both | Vertical |

The rearward 45° placement also clears those root obstacles at pitch offsets
−20°, −10°, 0°, +10° and +20° around it. These five samples are recorded in
the JSON; the intervening motion has not been checked continuously.

It is a candidate for further design, not a selected rest pose.
Tilting the complete carrier changes the roll shaft direction and
the direction of the current thigh. A horizontal carrier makes B's axis
vertical; retaining a downward thigh would then give rotation around that
vertical axis. A diagonal carrier requires the thigh, ground contacts and
useful lateral motion to be re-derived together.

The intersections use the exact current carrier, root module and imported
servo references. The side projections can overlap when the solids are
laterally separated. Clear samples do not establish continuous travel, a
complete leg, fastener/tool access, cables, strength or walking. The thigh is
shown only as a direction line, not as accepted geometry in these placements.

Turning only B's body/socket around B's shaft would preserve the axes and is
a different option. Isolated socket/body placements turned outwards by 0°,
45° and 90° about B from the current orientation clear the root and pitch
case at the saved pose, but a connecting carrier has not
been designed or checked for those orientations.

No production orientation or saved pose was changed by this study. The viewer
contains the DEC-56 narrowing, bevels and fillets in the DEC-55 orientation;
its remaining travel limitations are recorded in [OQ-22](../../open-questions.md).
