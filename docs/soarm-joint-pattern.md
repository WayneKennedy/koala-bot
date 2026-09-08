# SO-101 servo joint pattern — measured from upstream CAD (2026-09-07)

**What DEC-21 "SO-ARM compatible" actually means, in numbers.** Source:
[TheRobotStudio/SO-ARM100](https://github.com/TheRobotStudio/SO-ARM100)
`STEP/SO101/SO101 Assembly.step` plus the individual part STEPs (Apache-2.0),
measured with build123d/OpenCascade booleans and trimesh sections. Every figure
is **upstream CAD nominal**, not a caliper reading. Where the upstream servo
model and the printed pocket disagree, trust the pocket: the printed parts are
proven by every arm assembled and by the press-fit results on the reference
printer (`3d-printing/docs/print-log.md`, 2026-09-06/07).

Why this exists: both koala drafts (a3f265c, DEC-29) claimed DEC-21 and followed
only the servo's outer dimensions. The maintainer, half-way through printing and
assembling an SO-101, saw the difference on the bench. This is the canonical
description of the pattern; the restart brief
([`cad-restart-brief.md`](cad-restart-brief.md)) tells the designer to build it
as a primitive and use it at every joint.

![Base joint: Base alone, with servo, with Base_motor_holder](img/soarm-base-joint.png)
![Shoulder joint: Rotation_Pitch, servo, Motor_holder_Base, Upper_arm clevis](img/soarm-shoulder-joint.png)

**Fit basis updated by DEC-33:** the maintainer has now confirmed ST3215 fit
in the SO-101 parts in both PLA+ and PETG and authorized using these nominal
interfaces without a caliper prerequisite. Figures below retain upstream-CAD
provenance. Validate the new parts using the single-joint rig.

## The pattern (same at base, shoulder, wrist)

Every powered joint puts three printed parts around one STS3215:

1. **Cradle**, part of the structural link. Three walls plus a shelf, open on the
   servo's front face and on top, so the servo drops in and the pocket prints
   support-free. It holds the **rear ~17 mm** of the case. Two of the four case
   screws pass through its side walls.
2. **Collar** (upstream: "motor holder"). A separate 3 mm sleeve, open top and
   bottom. It slides down over the servo *and* over the cradle rim, closing the
   open front against the servo's front face and doubling the wall. The other two
   case screws pass through bosses in the collar, so the servo pins collar and
   cradle together. At the base joint the collar is additionally screwed to the
   tower (two M2 self-taps into Ø1.5 pilots).
3. **Clevis** on the driven link: two ~3.5 mm plates bolted 4×M3 to the drive horn
   *and* 4×M3 to the idler horn. The servo is loaded in double shear, never as a
   cantilever off one horn. The drive-side plate also has the Ø3.2 centre hole for
   the horn's centre screw.

Retention is the pocket. The four M2 self-tappers go into the **servo's own lugs**,
never into plastic; they only stop the case lifting out.

## Numbers

| Item | Value (mm) | Where measured |
|---|---|---|
| Pocket across the output axis (case "thickness") | **34.9** | shoulder cradle inner faces; `STL/Gauges/Gauge_0` pocket |
| Pocket across the case width | **24.7** | base tower inner faces; `Gauge_0` pocket |
| `Gauge_tight_1` pocket | 34.8 × 24.6 | STL section |
| Cradle depth, shelf to wall top | 17–18.5 | shoulder: shelf Z 84.5, walls to 101.5 / 103.2 |
| Cradle wall thickness | 4.8 (back-face side), 6.3 (horn side), back wall 4.8 | shoulder, mid-height |
| Base tower socket walls | 5.0 | base, both sides |
| Collar wall | 3.0 (shoulder); 4.0–4.9 (base) | rod probes |
| Collar height / overlap below the cradle shelf | 26 / 9 | shoulder: Z 75.5–101.5 |
| Collar-to-cradle clearance | 0.0–0.4 total | shoulder |
| Collar front wall to servo front face | 0.16 (shoulder), 0 (base) | rod probes |
| Clevis plate thickness | 3.5 | Upper_arm, Rotation_Pitch |
| Horn screw holes in plastic | **Ø3.0–3.2** on a **9.9** square | Upper_arm r=1.5, Rotation_Pitch r=1.6 |
| Drive-side centre hole | Ø3.2 through the plate | Rotation_Pitch top plate, Upper_arm horn-side plate |
| Case-screw hole in plastic | **Ø2.0 clearance, 2.0–2.2 long**, wall counterbored above it | all four parts |
| Self-tap into plastic (collar → base tower) | **Ø1.5 pilot**; Ø2.0 clearance in the collar | Base r=0.75, Base_motor_holder r=1.0 |
| Screws in the upstream model | #1-42 × 3/16" ≈ **M2 × 4.8** self-tap (the supplied M2×5); M3 × 6 pan head | assembly part labels |

### Case lug positions, from the printed holes (base and shoulder agree)

Lateral: **±10.2–10.5** from the case centreline (20.4–21 apart; koala
`SERVO_TAB_Y = 10.4` stands). Along the long axis, measured from the **rear face**
of the case (the end away from the output axis):

| Face | Offset from rear face |
|---|---|
| Horn-side face (drive horn side) | **5.5–6.0** |
| Back face (idler side) | **2.0–2.2** |

The two faces are **not symmetric**. koala's single `SERVO_TAB_X = −20.7` (1.9 from
the rear face) matches the back face only. Adopt these upstream offsets under DEC-33; verify retention on the new rig.

### The M2×5 length problem, answered

The Ø2.0 clearance section is only 2.0–2.2 mm long inside walls that are 5–7.5 mm
thick: upstream counterbores the wall so ~2.2 mm of plastic sits under the screw
head and the supplied M2×5 still reaches the lug. koala's test-log entry of
2026-09-07 ("M2×5 too short for our 3.95 / 6.35 mm walls") is therefore solved by
geometry, not by buying longer screws.

### Clevis span

Base joint: Rotation_Pitch's plates bear on the horn faces, **36.4 apart**.
`Rotation_Pitch_SO101.step` has its arm inner faces at Y = 10.0 and Y = 46.4
(36.4), matching calipers on the printed part and on a servo with both horns
fitted (test-log 2026-09-08) and the SO-100 bracket (test-log 2026-09-02).
The 37.5 that this document carried until 2026-09-08, and that DEC-33 adopted,
was a **measurement error in this review**: the probe along the axis of the
idler-side arm read the floor of a shallow centre recess (about 1 mm deep,
under 8 mm across, present only at the axis) instead of the arm face. Upstream's
CAD was right. Two consequences for the primitive: `SOCKET_HORN_SPAN = 36.4`,
and the idler-side plate wants that small centre recess for whatever stands
proud at the idler's centre — measure it. The drive-side arm has a Ø3.2 centre
through-hole instead. Other stand-offs in this section remain CAD-only until the
remaining caliper items in the test-log are taken.

## The interface, read from the printed parts alone (2026-09-08)

The maintainer's point, and the right method: the SO-101 printed-part STEPs
are proven by fit, so every **part-intrinsic** dimension below is a fact about
the servo interface. Rod probes at set radii from each joint axis and cylinder
listings around each hole, on `Rotation_Pitch`, `Upper_arm`, `Base` and
`Motor_holder_Base`. Where two parts carry the same feature, both are given.

| Feature | Value (mm) | Parts |
|---|---|---|
| Clevis span, arm inner face to arm inner face | **36.4** (65.78−29.38; 20.24−(−16.16)) | Rotation_Pitch, Upper_arm |
| Clevis arm faces | **flat** — no Ø20 horn recess on either side; the horn and idler bear on plain faces | both |
| Drive-side arm centre | Ø3.2 through hole, plus a countersink/recess: cone Ø8 at the face to Ø3.6 at 2.4 deep (Rotation_Pitch); Ø7.5 × 1.5 with a chamfer to Ø10.5 (Upper_arm) | both |
| Idler-side arm centre | blind recess Ø6 × 1.0 chamfered to Ø8 (Rotation_Pitch); Ø8 × 1.5 chamfered to Ø11 (Upper_arm). No through hole | both |
| Horn screw holes | Ø3.2 (Rotation_Pitch) / Ø3.0 (Upper_arm), **3.53 long**, 9.9 square; pan heads sit in a Ø24 pocket behind the web | both |
| Arm outline at the horn | Ø24 round pad, edge chamfered ~1.5 | both |
| Pocket across the output axis / across the width | **34.9 / 24.7** | Rotation_Pitch / Base |
| Lug hole stack, three of four positions | **Ø2.0 × 2.2 seat, then Ø4.0 counterbore** to the outside (4.5–7.8 long) | Rotation_Pitch both walls, Base roof, Motor_holder_Base idler-side boss |
| Lug hole stack, fourth position | **Ø4.0 straight through** the 8.5 mm boss, no seat | Motor_holder_Base horn-side boss — see bench question 3 |
| Base floor (idler-side lug) | Ø2.0 through a 2.0 mm floor; heads exposed underneath | Base |
| Lug offsets from the shelf / rear wall | idler side **2.2–2.3**, horn side **5.7–6.1** | Rotation_Pitch (from shelf), Base (from rear wall inner face) |
| Lug offset from the case centreline | **±10.25** | all |
| Rear tab clamp | Base roof underside to floor top **32.9** — 1.0 per side inside the 34.9 pocket, so the lug tab region is stepped below the main flat | Base |
| Cable exit, base joint | window in the tower's rear wall **24.7 wide × 22 tall** (Z 35.6–57.7 against a case at Z 28–63), then a Ø11 vertical channel | Base |
| Cable exit, shoulder joint | the shelf under the servo is **solid** across the whole footprint; no hole. The cable must leave sideways toward the open front | Rotation_Pitch |
| Collar | 3.0 walls, 26 tall, 9 below the shelf, 0.1 per side to the cradle, 0.16 to the servo front face | Motor_holder_Base |

**What the STEPs cannot give: the split of the horn stack between the two
sides.** Span minus pocket fixes the total at 36.4 − 34.9 = 1.5, but the two
joints in upstream's *assembly* place the parts inconsistently:

| Joint | Horn-side stand-off | Idler-side stand-off | Basis |
|---|---|---|---|
| Shoulder | −0.64 (plate inside the pocket plane — impossible) | +2.14 | Upper_arm plate faces vs Rotation_Pitch pocket faces |
| Base | +1.29 | +0.21 | Rotation_Pitch arms vs the Base roof/floor, assuming the rear tab is centred on the case |

Individual part files do not know where the servo sits inside them, and the
assembly mates are demonstrably off by ~1.9 mm at the shoulder. The base-joint
figures are the physically possible pair and agree with the design's current
assumption (drive horn ~1.3–1.5 proud, idler near flush), but they rest on a
centred-tab assumption. **One bench observation closes it**: whether the idler
wheel stands proud of the case's main flat, and by roughly how much.

### Corrections to the primitive that follow from this

1. Split the four lug screws by **lateral position**, as upstream does: each
   cradle side wall takes one lug (one drive-face, one back-face) at the rear
   lateral position; the collar's two bosses at the open front corners take the
   other two. No lanes through the cradle wall.
2. **Flat clevis plates.** Drop the Ø20.5 × 0.8 horn recess (an invention that
   originated in this document's first version). Keep the drive-side Ø3.2 centre
   hole with a countersink; add the idler-side centre recess, about Ø8 × 1.5.
3. Lug stack Ø2.0 × 2.2 seat plus Ø4.0 counterbore, matching three of upstream's
   four positions.
4. Cable: the base joint exits rearward through a 22 mm window in the wall behind
   the rear face; the shoulder has no shelf opening. Decide per joint after bench
   question 2.

## Upstream CAD caveat

The assembly's `ST3215_Servo_v2` model overlaps the cradle's back-face wall by up to
~2 mm and models the back cover as a hollow shell. The printed pocket is 34.9 wide
and fits real servos as a press fit, so the servo model is the suspect — exactly the
lesson already learned from `STS3215_03a.step` (test-log 2026-09-02). **Derive pockets
from upstream printed parts and calipers, never from a servo model.**

## Fit evidence on the reference printer

From `3d-printing/docs/print-log.md`: `Gauge_0` (zero-clearance 34.9 × 24.7 pocket)
is a tight friction fit on the Ender-5 S1 in **PLA+** at 220/215 with
`elefant_foot_compensation = 0`; the printed `Base` socket is a solid press fit.
koala prints **PETG**, whose shrinkage differs, so `CLEAR_POCKET` (0.25, `[VERIFY]`)
was originally awaiting a PETG gauge. **Superseded by DEC-33:** the maintainer
confirms the SO-101 fit in PETG too; `SOCKET_CLEAR = 0` is specific to this
pocket. Generic non-servo `CLEAR_POCKET` is unchanged.

## Reproducing the principal measurements

From `hardware/`, with the STEPs downloaded from the upstream `STEP/SO101/` folder
into a scratch directory `$D`:

```sh
uv run python - <<'PY'
import re
from build123d import import_step, Box, Pos
asm = import_step("$D/SO101 Assembly.step")          # 97 children, 266 solids
def pick(rx, near=None):
    for k in asm.children:
        if re.search(rx, k.label):
            if near is None: return k
            c = k.bounding_box().center()
            if max(abs(c.X-near[0]), abs(c.Y-near[1]), abs(c.Z-near[2])) < 15: return k
parts = {'RotPitch': pick(r'^Rotation_Pitch'), 'Collar': pick(r'^Motor_holder_SO101_Base'),
         'Servo': pick(r'^ST3215', (2, -38, 107))}   # the shoulder servo, output axis X
rod = Pos(0, -38.55, 95) * Box(400, 0.02, 0.02)     # along X through the servo centre
for n, k in parts.items():
    hits = sorted((round(b.min.X, 2), round(b.max.X, 2))
                  for s in k.solids() if (h := s & rod) is not None
                  for b in (t.bounding_box() for t in h.solids()) if b.size.X > 0.05)
    print(n, hits)   # cradle walls [-23.1,-16.8] [18.1,22.9] -> pocket 34.9; collar 3.0 walls
PY
```

Hole positions came from listing cylindrical faces (r ≤ 1.7 and r ≥ 8) of each
part in the assembly frame; pocket widths from the rod probes above; gauge
pockets from trimesh sections of the STLs. The scripts are not kept in the repo;
the recipe above regenerates the load-bearing numbers.
