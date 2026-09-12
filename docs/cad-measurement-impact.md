# Measurement impact assessment — 2026-09-08

**Historical assessment of `f541600`.** [DEC-40](cad-integrated-design.md)
implements the corrections in the integrated four-limb chassis. The findings
below describe the pre-correction geometry, not the current build.
The latest measurements invalidate the earlier socket clearance and fastening
claims. Updating the horn-span constant alone has also opened a gap in the hip
carrier. The six-servo architecture and 100/100 mm links remain a usable starting
point; their revised packaging has not passed the full motion audit.

## Baseline and evidence

Fetched and fast-forwarded `main` from `3893b88` to `f541600`: 22 commits.
The main changes are:

- `c46d1d6` / `7d5fa9f`: fitted horn span is 36.4 mm; 37.5 was a probing error.
- `1e9ac89` / `14be251`: printed-part STEP evidence corrects retention, plate
  faces and head pockets; the SO-101 elbow saddle is a separate exception.
- `ad811e9` through `aa23fb7`: fitted idler, centre boss, supplied screw heads,
  asymmetric case planes, face terminology and connector-bay measurements.
- `1022303` / `f19356f` / `ab12a26`: reference geometry gains the stepped case,
  centred raised pads and optional maintainer-supplied STEP case.
- `95206c0` / `3648f2d` / `f541600`: press-fit overlap allowance, disjoint
  boolean handling and removal of the third-party model from version control.
- `91b663b`: blake becomes the canonical viewer host (DEC-35).

Measurement provenance and remaining uncertainty belong in
[`test-log.md`](test-log.md) and [`soarm-joint-pattern.md`](soarm-joint-pattern.md).
This assessment uses their current conclusions, including withdrawn photo
interpretations, rather than treating every intermediate commit as authoritative.
The existing confirmed SO-101 fit remains valid; no repeat-gauge prerequisite
is reinstated. It did not establish that the DEC-34 primitive reproduced SO-101.

## Findings and correction scope

| Priority | Finding at `f541600` | Required response |
|---|---|---|
| Blocking | Front plate intersects the centre pan head by **26.389 mm³**. Back plate intersects the measured boss by **35.186 mm³** with the fallback reference, **46.420 mm³** with the STEP reference. | Replace the incorrect Ø20.5 horn recess with flat horn contact; provide Front centre-head clearance and a Back blind boss recess. Both retain four horn-square fixings. |
| Blocking | `V2_HIP_STEM_X` remains 22.75, while the Front roll-cheek outer face moved to 22.10. Solid-to-solid distance is **0.65 mm**. | Derive the stem mating datum from the final cheek geometry. Verify bearing contact and compression through the complete carrier stack; aligned screw bores alone are insufficient. |
| Blocking | Cradle takes both Back ears and collar both Front ears. Upstream splits them by Side position, with one Front and one Back ear on each part. Walls still end at the widest-case planes rather than bossing inward to the ear faces. | Rebuild the shared cradle/collar retention and remove the invented boss lanes. Propagate through integral roots and supports; demonstrate Side insertion and collar assembly. |
| Blocking | At the nominal ear centres, the current wall-to-ear gaps are **1.05 Front / 2.05 Back mm**. M2x5 minus a 2.2 mm seat and these gaps leaves only **1.75 / 0.75 mm** nominal penetration, not 2.8. | Bring bosses to the ear planes; use the corrected printed-part lug positions and seat geometry. Confirm actual engagement and absence of bottoming on the rig. |
| Required | Horn-square head pockets are absent. `audit.horn_heads()` still models proud Ø5.5 × 3 cap heads, despite the supplied Ø5.2 × 2 pan-head constants. | Use the measured hardware and the brief's ≥Ø6 × ≥2.5 counterbores over a 3.5 mm web. Recheck pad strength, print orientation and screw stack. M3x6 projects 2.5 mm beyond that web against a 2.1 mm tapped idler body; bottoming remains a rig question. |
| Required | `SOCKET_BAY_Z` is unused by the keepouts. Current cable probes exit through the Bottom/open Side; the connectors face out from the Back. A Ø28 Back plate reaches Z21.115, overlapping the bay's height band by **3.385 mm**. | Replace the cable envelope with the actual Back exit and an articulated service loop. Ø24 alone still overlaps the height band by 1.385 mm: check connectors explicitly and trim the plate if needed. Height overlap is a clearance concern, not proof of a connector-solid collision. |

Ear-gap arithmetic uses the pocket planes ±17.45 and ear planes +16.4/−15.4
from the measured +0.5 seat offset. These are nominal calculations, not thread
pull-out predictions or additional caliper measurements. The corrected lateral
hole centres are ±10.25 rather than ±10.4; Back heights are 2.2–2.3 rather
than 2.1, while the existing Front 5.8 lies within the upstream 5.7–6.1 range.
The fourth upstream collar hole's missing M2 seat remains a bench question;
do not copy an unexplained through-hole as a verified fastening stack.

The brief requests a Front centre countersink while DEC-25 forbids countersinks
in plastic. Resolve this explicitly in the correction: the centre feature clears
an already installed pan head; it must not become a conical load-bearing screw
seat. A flat-bottom clearance pocket is a candidate, subject to remaining web
and printability. Counterbores on the opposite plate face also require a fresh
orientation/overhang check.

## Propagation beyond the socket

All six lower-body servo positions are affected: pelvis roll roots, both hip
pitch cradles, knee cradles within the thigh cores, six collars and twelve horn
cheeks. All five joint-rig parts need regeneration. Changed mating faces affect
hip crossbars, thigh/shank crossbars, registration shoulders, the hip stem,
motor-plate placement, fastener grips and hardware envelopes.

Current derived values below describe the **uncorrected implementation**, not
approved dimensions for the replacement:

| Quantity | `3893b88` | `f541600` |
|---|---:|---:|
| Horn outer-face span | 37.5 | 36.4 |
| Back / Front horn face X | −17.45 / +20.05 | −17.00 / +19.40 |
| Crossbar mating-face span | 36.7 | 35.6 |
| Proximal fork grip, including cheeks | 43.7 | 42.6 |
| Hip carrier head seat to outer Back cheek | 52.95 | 52.50 |
| Motor-plate seam grip | 46.7 | 45.6 |
| Wheel-centre track | 239.5 | 238.2 |
| Neutral motor end gap | 55.5 | 54.2 |

The intermediate documented track 237.3 and hip grip 51.85 missed the later
asymmetric face shift. Removing the 0.8 mm Front recess alone would make the
bridge span 36.4 and track 239.8, assuming all other datums stay fixed. That is
a sensitivity calculation, **not the final layout**: thicker horn pads and
the carrier contact repair must be designed together before resampling motion.

Nothing in these measurements requires changing the DOF count, link lengths,
nominal hip/knee angles or wheel/motor bought-part specification. The 283.2 mm
nominal deck height and analytical sagittal torque screen retain their stated
assumptions. Printed mass, lateral clearances and loaded performance must be
reassessed after the geometry changes. No direct e-tray redesign is identified.

## Checks run and gaps in validation

On ivory, against `f541600`, using `uv run` from `hardware/`:

- `python -m koala_hardware.audit`: **fails** at `rig drive -90/case:
  26.389 mm³ overlap`, both without the STEP and with the same 4,372,667-byte
  ignored model present on blake. The model was copied privately for this
  assessment; it remains untracked. See its [provenance](../hardware/vendor/st3215/README.md).
- Independent plate/reference intersections at −90…90° in 10° steps confirm
  the table's Front and Back failures at **all 19 angles** with each reference.
  Ø8 boss diameter and Front case-region heights remain unverified.
- Layout, connected-solid/bed-envelope and pelvis-symmetry checks preceding
  the audit failure passed. `audit.check_mounting()` also passed independently,
  despite the measured 0.65 mm carrier gap: its probes check holes, not contact.
- `python -m unittest discover -s tests`: **8 passed**. These cover sizing and
  the printability classifier, not the corrected servo interface.
- The full 27-pose and 81 opposing-leg audits were **not reached**. No new export,
  surface screen, browser/CAD parity, slicing, printing or load test is claimed.

**Reference composition also needs correction.** The imported bare case already
contains a central Back projection: its intersection with the Back plate is
27.310 mm³, reaching X=−18.2 (1.2 mm beyond the measured idler face). Adding a
measured 0.7 mm boss by union does not remove that imported projection. This
explains the STEP's larger Back overlap; it is not a new physical measurement.
Isolate or replace this feature so the reference actually follows the measured
boss envelope before interpreting the remaining collision volumes.

The STEP case/cradle overlap is 8.930 mm³ (fallback: zero), below the new
50 mm³ socket press-fit allowance. The full-pose loop still applies 0.01 mm³
to these reference/print pairs, so its treatment of intended contact is
inconsistent. Localize allowed contact to the intended pocket regions and
apply it consistently; do not relax plate, hardware or moving-part checks.
Neither reference includes a complete plugged-in loom. A successful export
or viewer rebuild is therefore not evidence of an audit pass.

## Repair sequence and acceptance

1. Correct the shared primitive from the latest printed-part pattern and
   measured hardware: retention, ear seats, flat horn faces, centre clearances,
   head pockets and Back connector envelope. Keep Gauge_0's pocket unchanged.
2. Derive all mating datums, including the hip stem, from those interfaces.
   Recalculate grips and screw engagement before settling hardware lengths.
3. Add focused checks for required bearing contact, ear-seat gaps, actual
   screw-head seating and Back connector clearance; reconcile the imported
   boss with the measured reference and intended press-fit contact between
   primitive and assembly audits.
4. Regenerate the rig and dependent structures; rerun export/surface checks,
   both reference audits, motion samples and browser/CAD parity. Regenerate the
   BOM from metadata and update dimension/assembly claims only from that result.
5. Follow the existing one-joint fit → one leg → pair → load/creep sequence
   (OQ-12/13). This assessment neither changes DEC-33 nor accepts a physical part.

The canonical viewer remains on blake under DEC-35. Its service rebuilds only
on restart and can retain an older scene after a failed build; a visible scene
does not establish that it represents the latest commit. No viewer service was
changed during this assessment.
