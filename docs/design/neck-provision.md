# Shoulder neck-cartridge provision — 2026-09-19

Status: **unprinted packaging study**, not a completed neck. The shoulder frame
reserves a removable cartridge for the **three bought STS3032M 6 V servos** in the
[BOM](../bom.md). These are the small neck servos. Their fixed leads connect via
the supplied connector boards; see [architecture](../architecture.md). No
additional servo purchase or limb-size servo is assumed.

## Size evidence and uncertainty

Feetech's [STS3032 catalogue](https://www.feetechrc.com/Data/feetechrc/upload/file/%E9%A3%9E%E7%89%B9%E4%BC%81%E4%B8%9A%E7%94%BB%E5%86%8C20200430-%E5%B7%B2%E5%8E%8B%E7%BC%A9/%E9%A3%9E%E7%89%B9%E4%BC%81%E4%B8%9A%E7%94%BB%E5%86%8C20200430-%E5%B7%B2%E5%8E%8B%E7%BC%A9.pdf)
lists **23.2 × 12.1 × 28.5 mm**. The manufacturer's
[ST-3032-C001 product page](https://www.feetechrc.com/6v-45kg-magnetic-code-360-degree-serial-bus-steering-gear.html)
and [dimensioned outline](https://www.feetechrc.com/Data/feetechrc/upload/image/20210604/6375841945336588318036432.png)
show a different envelope: 23 × 12 × 27.5 mm case, 32 mm overall ear span,
31.9 mm to the spline tip, and ears from 20.5 to 22 mm above the base. These are
published STS3032/C001 dimensions, **not measurements of the purchased M variant**.
The model combines the larger published case with a conservatively raised ear
band; it does not define servo screw holes. Case, ear, output and lead-exit
measurements remain required before making a neck carrier.

## Interface and reserved space

The source is
[`neck_space.py`](../../hardware/src/koala_hardware/parts/neck_space.py). Dimensions
below are millimetres in torso coordinates: X dorsal negative, Y lateral,
Z along the spine. The cap datum is Z = 183.5.

| Feature | Allocation | Reason |
|---|---|---|
| Three nominal case envelopes | X −43.6…−20.4; Y centres −16, 0, +16, width 12.1 each; Z 155.5…184 | Places the small cases behind the shoulder A modules |
| Case clearance | 1 mm on each face; total pack X −44.6…−19.4, Y ±23.05, Z 154.5…185 | Packaging allowance, not a fitted socket tolerance |
| Nominal ear bands | X −48…−16; same Y width; Z 176…178.5 | Separates the ears from the A modules ending at Z 173.45 |
| Ear clearance | 1 mm on each face; minimum Z 175 | 1.55 mm above the present A-module limit |
| Cap opening | X −50…−14, Y ±24, open through dorsal edge | Insert/remove the cartridge and fixed leads without threading closed cable holes |
| Cartridge interface | Four M3 clearance holes, X = −28/+2 and Y = ±30 | 30 × 60 mm mount pattern around the opening; accessible from above |
| Cartridge outer allowance | Approximately X −50…10, Y ±38, above cap | Remains inside the shoulder width; actual cartridge geometry is deferred |
| Fixed-lead drop | X −44.6…−19.4, Y ±23.05, Z 142.5…154.5 | 12 mm routing allowance below the cases; connector-board fit is unverified |
| Output allowance | Cap opening footprint, Z 183.5…207.5 | Space to develop horns and links; **not** a verified motion envelope |

The four holes attach a future cartridge to the torso; they are independent of
servo ear pitch. Torso v5 shifts the pattern 10 mm ventrally from the v4 trial,
so its screws exit below the cap into open space instead of the upper dorsal
rails. The upper rails now centre at Y±29; the inflated case pack ends at
Y±23.05, leaving 1.95 mm to each rail's inner face. The slot leaves 6 mm from its edge to the nearest hole centre.
A future cartridge can use captive metal nuts reachable from the open side and
straight screw access from above. The CAD helper supplies Ø6 × 40 mm driver
probes. Cartridge thickness, screw length, nut seats and servo restraints await
the carrier design; none is added to the printed BOM yet.

For the current root envelope, the inflated cases stop at X = −19.4 while
shoulder A starts at X = −18.35, leaving 1.05 mm. The ear allowance starts at
Z = 175, above the modules' Z = 173.45 limit. These calculated separations are
between provisional envelopes. `clearance_interferences()` also tests the
actual torso and stationary modules supplied by the assembly. The completed
2026-09-19 torso and stationary-module check reports no intersections; the
four top-access driver probes also clear the neck reservations. This validates
the allocation, not physical fit, connector-board fit or neck travel.

## What this resolves and what remains open

The dorsal slot and separate cartridge preserve compact shoulders and allow a
neck revision without remaking either shoulder socket. Removing the cartridge
should require disconnecting its three fixed leads at their boards and removing
four top-access screws. Board position and connector withdrawal clearance still
need measuring and laying out; the open slot avoids trapping them in the torso.

The three upright boxes demonstrate a compact volume allocation. They **do not
establish a working 3-RPS neck**: servo-axis orientation, horn motion and the
three pushrod attachment points have not been solved. The final mechanism may
need reoriented servos or bellcranks; neither is banked here. Retain the
[existing three-servo parallel-neck intent](../concept.md), then check linkage
geometry, loaded stroke, head centre of mass, cable bends and removal on the
actual small servos before committing the cartridge or head position. The
450 mm head-top target remains a sizing target.
