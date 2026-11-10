# FreeCAD revision archive

[Workflow](../../docs/freecad.md) · [machine-readable manifest](manifest.json) · [migration evidence](migration/README.md)

Python is authoritative. Each link below pairs a replay script with its saved document; frozen dependencies are in `sources/`. The latest review revision is listed first; accepted checkpoints and the migration benchmark remain below. The manifest is authoritative.

Native documents contain recomputable Part/Sketcher feature histories. Historical/vendor STEP references retain imported solids and source provenance; their original histories are unavailable.

## Thigh v7 thick horn lead-ins — 2026-10-01, unprinted

[Geometry and validation](../../docs/design/thigh-leadin/README.md).
Two handed thigh pairs and four walking/review poses. All 150 earlier pairs
remain unchanged; other printed designs retain their R3 versions.

| Model | Version | Python | FreeCAD |
|---|---|---|---|
| `thigh_right` | v7 | [Python](parts/thigh/v7/44ed687d14e1a9e4/thigh_right.py) | [FCStd](parts/thigh/v7/44ed687d14e1a9e4/thigh_right.FCStd) |
| `thigh_left` | v7 | [Python](parts/thigh/v7/44ed687d14e1a9e4/thigh_left.py) | [FCStd](parts/thigh/v7/44ed687d14e1a9e4/thigh_left.FCStd) |
| `koala-walking` | — | [Python](assemblies/44ed687d14e1a9e4/koala-walking.py) | [FCStd](assemblies/44ed687d14e1a9e4/koala-walking.FCStd) |
| `koala-walking-max-fold` | — | [Python](assemblies/44ed687d14e1a9e4/koala-walking-max-fold.py) | [FCStd](assemblies/44ed687d14e1a9e4/koala-walking-max-fold.FCStd) |
| `koala-walking-bend-min` | — | [Python](assemblies/44ed687d14e1a9e4/koala-walking-bend-min.py) | [FCStd](assemblies/44ed687d14e1a9e4/koala-walking-bend-min.FCStd) |
| `koala-walking-bend-max` | — | [Python](assemblies/44ed687d14e1a9e4/koala-walking-bend-max.py) | [FCStd](assemblies/44ed687d14e1a9e4/koala-walking-bend-max.FCStd) |

## R3 family exterior — 2026-10-01, unprinted

[Scope, exceptions and validation](../../docs/design/rounded-family-r3/README.md).
Twenty new part pairs cover eleven changed production designs, with six
whole-robot poses. Superseded torso v7/v8 pairs preserve their interim sources; v9
retains the native topology and restores the cassette service plane. All 122 earlier pairs
are retained unchanged.

| Model | Version | Status | Python | FreeCAD |
|---|---|---|---|---|
| `root_socket_right` | v2 | current review | [Python](parts/root_socket/v2/4b63c47db7e3590d/root_socket_right.py) | [FCStd](parts/root_socket/v2/4b63c47db7e3590d/root_socket_right.FCStd) |
| `root_socket_left` | v2 | current review | [Python](parts/root_socket/v2/4b63c47db7e3590d/root_socket_left.py) | [FCStd](parts/root_socket/v2/4b63c47db7e3590d/root_socket_left.FCStd) |
| `thigh_right` | v6 | superseded | [Python](parts/thigh/v6/4b63c47db7e3590d/thigh_right.py) | [FCStd](parts/thigh/v6/4b63c47db7e3590d/thigh_right.FCStd) |
| `thigh_left` | v6 | superseded | [Python](parts/thigh/v6/4b63c47db7e3590d/thigh_left.py) | [FCStd](parts/thigh/v6/4b63c47db7e3590d/thigh_left.FCStd) |
| `shank_right` | v4 | current review | [Python](parts/shank/v4/4b63c47db7e3590d/shank_right.py) | [FCStd](parts/shank/v4/4b63c47db7e3590d/shank_right.FCStd) |
| `shank_left` | v4 | current review | [Python](parts/shank/v4/4b63c47db7e3590d/shank_left.py) | [FCStd](parts/shank/v4/4b63c47db7e3590d/shank_left.FCStd) |
| `foot_shank_right` | v4 | current review | [Python](parts/foot_shank/v4/4b63c47db7e3590d/foot_shank_right.py) | [FCStd](parts/foot_shank/v4/4b63c47db7e3590d/foot_shank_right.FCStd) |
| `foot_shank_left` | v4 | current review | [Python](parts/foot_shank/v4/4b63c47db7e3590d/foot_shank_left.py) | [FCStd](parts/foot_shank/v4/4b63c47db7e3590d/foot_shank_left.FCStd) |
| `hip_carrier_right` | v3 | current review | [Python](parts/hip_carrier/v3/4b63c47db7e3590d/hip_carrier_right.py) | [FCStd](parts/hip_carrier/v3/4b63c47db7e3590d/hip_carrier_right.FCStd) |
| `hip_carrier_left` | v3 | current review | [Python](parts/hip_carrier/v3/4b63c47db7e3590d/hip_carrier_left.py) | [FCStd](parts/hip_carrier/v3/4b63c47db7e3590d/hip_carrier_left.FCStd) |
| `shoulder_carrier_right` | v6 | current review | [Python](parts/shoulder_carrier/v6/4b63c47db7e3590d/shoulder_carrier_right.py) | [FCStd](parts/shoulder_carrier/v6/4b63c47db7e3590d/shoulder_carrier_right.FCStd) |
| `shoulder_carrier_left` | v6 | current review | [Python](parts/shoulder_carrier/v6/4b63c47db7e3590d/shoulder_carrier_left.py) | [FCStd](parts/shoulder_carrier/v6/4b63c47db7e3590d/shoulder_carrier_left.FCStd) |
| `upper_arm_right` | v4 | current review | [Python](parts/upper_arm/v4/4b63c47db7e3590d/upper_arm_right.py) | [FCStd](parts/upper_arm/v4/4b63c47db7e3590d/upper_arm_right.FCStd) |
| `upper_arm_left` | v4 | current review | [Python](parts/upper_arm/v4/4b63c47db7e3590d/upper_arm_left.py) | [FCStd](parts/upper_arm/v4/4b63c47db7e3590d/upper_arm_left.FCStd) |
| `forearm_right` | v5 | current review | [Python](parts/forearm/v5/4b63c47db7e3590d/forearm_right.py) | [FCStd](parts/forearm/v5/4b63c47db7e3590d/forearm_right.FCStd) |
| `forearm_left` | v5 | current review | [Python](parts/forearm/v5/4b63c47db7e3590d/forearm_left.py) | [FCStd](parts/forearm/v5/4b63c47db7e3590d/forearm_left.FCStd) |
| `shoulder_mount_right` | v2 | current review | [Python](parts/shoulder_mount/v2/4b63c47db7e3590d/shoulder_mount_right.py) | [FCStd](parts/shoulder_mount/v2/4b63c47db7e3590d/shoulder_mount_right.FCStd) |
| `shoulder_mount_left` | v2 | current review | [Python](parts/shoulder_mount/v2/4b63c47db7e3590d/shoulder_mount_left.py) | [FCStd](parts/shoulder_mount/v2/4b63c47db7e3590d/shoulder_mount_left.FCStd) |
| `torso_frame` | v9 | current review | [Python](parts/torso_frame/v9/4b63c47db7e3590d/torso_frame.py) | [FCStd](parts/torso_frame/v9/4b63c47db7e3590d/torso_frame.FCStd) |
| `e_tray` | v2 | current review | [Python](parts/e_tray/v2/4b63c47db7e3590d/e_tray.py) | [FCStd](parts/e_tray/v2/4b63c47db7e3590d/e_tray.FCStd) |
| `koala-walking` | — | superseded | [Python](assemblies/4b63c47db7e3590d/koala-walking.py) | [FCStd](assemblies/4b63c47db7e3590d/koala-walking.FCStd) |
| `koala-quadruped` | — | thigh v6 snapshot | [Python](assemblies/4b63c47db7e3590d/koala-quadruped.py) | [FCStd](assemblies/4b63c47db7e3590d/koala-quadruped.FCStd) |
| `koala-upright` | — | thigh v6 snapshot | [Python](assemblies/4b63c47db7e3590d/koala-upright.py) | [FCStd](assemblies/4b63c47db7e3590d/koala-upright.FCStd) |
| `koala-walking-max-fold` | — | superseded | [Python](assemblies/4b63c47db7e3590d/koala-walking-max-fold.py) | [FCStd](assemblies/4b63c47db7e3590d/koala-walking-max-fold.FCStd) |
| `koala-walking-bend-min` | — | superseded | [Python](assemblies/4b63c47db7e3590d/koala-walking-bend-min.py) | [FCStd](assemblies/4b63c47db7e3590d/koala-walking-bend-min.FCStd) |
| `koala-walking-bend-max` | — | superseded | [Python](assemblies/4b63c47db7e3590d/koala-walking-bend-max.py) | [FCStd](assemblies/4b63c47db7e3590d/koala-walking-bend-max.FCStd) |
| `torso_frame` | v7 | superseded | [Python](parts/torso_frame/v7/21f0d744436f45aa/torso_frame.py) | [FCStd](parts/torso_frame/v7/21f0d744436f45aa/torso_frame.FCStd) |
| `torso_frame` | v8 | superseded | [Python](parts/torso_frame/v8/c65d304cc170e9c7/torso_frame.py) | [FCStd](parts/torso_frame/v8/c65d304cc170e9c7/torso_frame.FCStd) |

## R4 family exterior — 2026-10-01, unprinted

[Scope, exceptions and validation](../../docs/design/rounded-family/README.md).
These 21 new pairs cover eight changed designs (15 handed part files) and six
assemblies. All 101 earlier pairs remain unchanged. Accepted bend caps are retained.

| Model | Version | Python | FreeCAD |
|---|---|---|---|
| `thigh_right` | v5 | [Python](parts/thigh/v5/0db97d8f34c2d289/thigh_right.py) | [FCStd](parts/thigh/v5/0db97d8f34c2d289/thigh_right.FCStd) |
| `thigh_left` | v5 | [Python](parts/thigh/v5/0db97d8f34c2d289/thigh_left.py) | [FCStd](parts/thigh/v5/0db97d8f34c2d289/thigh_left.FCStd) |
| `shank_right` | v3 | [Python](parts/shank/v3/0db97d8f34c2d289/shank_right.py) | [FCStd](parts/shank/v3/0db97d8f34c2d289/shank_right.FCStd) |
| `shank_left` | v3 | [Python](parts/shank/v3/0db97d8f34c2d289/shank_left.py) | [FCStd](parts/shank/v3/0db97d8f34c2d289/shank_left.FCStd) |
| `foot_shank_right` | v3 | [Python](parts/foot_shank/v3/0db97d8f34c2d289/foot_shank_right.py) | [FCStd](parts/foot_shank/v3/0db97d8f34c2d289/foot_shank_right.FCStd) |
| `foot_shank_left` | v3 | [Python](parts/foot_shank/v3/0db97d8f34c2d289/foot_shank_left.py) | [FCStd](parts/foot_shank/v3/0db97d8f34c2d289/foot_shank_left.FCStd) |
| `hip_carrier_right` | v2 | [Python](parts/hip_carrier/v2/0db97d8f34c2d289/hip_carrier_right.py) | [FCStd](parts/hip_carrier/v2/0db97d8f34c2d289/hip_carrier_right.FCStd) |
| `hip_carrier_left` | v2 | [Python](parts/hip_carrier/v2/0db97d8f34c2d289/hip_carrier_left.py) | [FCStd](parts/hip_carrier/v2/0db97d8f34c2d289/hip_carrier_left.FCStd) |
| `shoulder_carrier_right` | v5 | [Python](parts/shoulder_carrier/v5/0db97d8f34c2d289/shoulder_carrier_right.py) | [FCStd](parts/shoulder_carrier/v5/0db97d8f34c2d289/shoulder_carrier_right.FCStd) |
| `shoulder_carrier_left` | v5 | [Python](parts/shoulder_carrier/v5/0db97d8f34c2d289/shoulder_carrier_left.py) | [FCStd](parts/shoulder_carrier/v5/0db97d8f34c2d289/shoulder_carrier_left.FCStd) |
| `upper_arm_right` | v3 | [Python](parts/upper_arm/v3/0db97d8f34c2d289/upper_arm_right.py) | [FCStd](parts/upper_arm/v3/0db97d8f34c2d289/upper_arm_right.FCStd) |
| `upper_arm_left` | v3 | [Python](parts/upper_arm/v3/0db97d8f34c2d289/upper_arm_left.py) | [FCStd](parts/upper_arm/v3/0db97d8f34c2d289/upper_arm_left.FCStd) |
| `forearm_right` | v4 | [Python](parts/forearm/v4/0db97d8f34c2d289/forearm_right.py) | [FCStd](parts/forearm/v4/0db97d8f34c2d289/forearm_right.FCStd) |
| `forearm_left` | v4 | [Python](parts/forearm/v4/0db97d8f34c2d289/forearm_left.py) | [FCStd](parts/forearm/v4/0db97d8f34c2d289/forearm_left.FCStd) |
| `torso_frame` | v6 | [Python](parts/torso_frame/v6/0db97d8f34c2d289/torso_frame.py) | [FCStd](parts/torso_frame/v6/0db97d8f34c2d289/torso_frame.FCStd) |
| `koala-walking` | — | [Python](assemblies/0db97d8f34c2d289/koala-walking.py) | [FCStd](assemblies/0db97d8f34c2d289/koala-walking.FCStd) |
| `koala-quadruped` | — | [Python](assemblies/0db97d8f34c2d289/koala-quadruped.py) | [FCStd](assemblies/0db97d8f34c2d289/koala-quadruped.FCStd) |
| `koala-upright` | — | [Python](assemblies/0db97d8f34c2d289/koala-upright.py) | [FCStd](assemblies/0db97d8f34c2d289/koala-upright.FCStd) |
| `koala-walking-max-fold` | — | [Python](assemblies/0db97d8f34c2d289/koala-walking-max-fold.py) | [FCStd](assemblies/0db97d8f34c2d289/koala-walking-max-fold.FCStd) |
| `koala-walking-bend-min` | — | [Python](assemblies/0db97d8f34c2d289/koala-walking-bend-min.py) | [FCStd](assemblies/0db97d8f34c2d289/koala-walking-bend-min.FCStd) |
| `koala-walking-bend-max` | — | [Python](assemblies/0db97d8f34c2d289/koala-walking-bend-max.py) | [FCStd](assemblies/0db97d8f34c2d289/koala-walking-bend-max.FCStd) |

## Accepted 20.8 mm links — 2026-10-01

[Acceptance, bend limits and validation](../../docs/design/flat-links/README.md).
The owner passed the maximum-fold pose; no additional fold travel is wanted.
These 11 new pairs retain the original 90 benchmark pairs unchanged. Parts remain unprinted.

| Model | Version | Python | FreeCAD |
|---|---|---|---|
| `forearm_right` | v3 | [Python](parts/forearm/v3/aeb4e11ef28feee4/forearm_right.py) | [FCStd](parts/forearm/v3/aeb4e11ef28feee4/forearm_right.FCStd) |
| `forearm_left` | v3 | [Python](parts/forearm/v3/aeb4e11ef28feee4/forearm_left.py) | [FCStd](parts/forearm/v3/aeb4e11ef28feee4/forearm_left.FCStd) |
| `foot_shank_right` | v2 | [Python](parts/foot_shank/v2/aeb4e11ef28feee4/foot_shank_right.py) | [FCStd](parts/foot_shank/v2/aeb4e11ef28feee4/foot_shank_right.FCStd) |
| `foot_shank_left` | v2 | [Python](parts/foot_shank/v2/aeb4e11ef28feee4/foot_shank_left.py) | [FCStd](parts/foot_shank/v2/aeb4e11ef28feee4/foot_shank_left.FCStd) |
| `front_contact_pad` | v2 | [Python](parts/front_contact_pad/v2/aeb4e11ef28feee4/front_contact_pad.py) | [FCStd](parts/front_contact_pad/v2/aeb4e11ef28feee4/front_contact_pad.FCStd) |
| `koala-walking` | — | [Python](assemblies/aeb4e11ef28feee4/koala-walking.py) | [FCStd](assemblies/aeb4e11ef28feee4/koala-walking.FCStd) |
| `koala-quadruped` | — | [Python](assemblies/aeb4e11ef28feee4/koala-quadruped.py) | [FCStd](assemblies/aeb4e11ef28feee4/koala-quadruped.FCStd) |
| `koala-upright` | — | [Python](assemblies/aeb4e11ef28feee4/koala-upright.py) | [FCStd](assemblies/aeb4e11ef28feee4/koala-upright.FCStd) |
| `koala-walking-max-fold` | — | [Python](assemblies/aeb4e11ef28feee4/koala-walking-max-fold.py) | [FCStd](assemblies/aeb4e11ef28feee4/koala-walking-max-fold.FCStd) |
| `koala-walking-bend-min` | — | [Python](assemblies/aeb4e11ef28feee4/koala-walking-bend-min.py) | [FCStd](assemblies/aeb4e11ef28feee4/koala-walking-bend-min.FCStd) |
| `koala-walking-bend-max` | — | [Python](assemblies/aeb4e11ef28feee4/koala-walking-bend-max.py) | [FCStd](assemblies/aeb4e11ef28feee4/koala-walking-bend-max.FCStd) |

## Migration benchmark — 2026-09-29

## Native assemblies

| Model | Version | Python | FreeCAD |
|---|---|---|---|
| `koala-walking` | — | [Python](assemblies/3c52315ce49d97f4/koala-walking.py) | [FCStd](assemblies/3c52315ce49d97f4/koala-walking.FCStd) |
| `koala-quadruped` | — | [Python](assemblies/3c52315ce49d97f4/koala-quadruped.py) | [FCStd](assemblies/3c52315ce49d97f4/koala-quadruped.FCStd) |
| `koala-upright` | — | [Python](assemblies/3c52315ce49d97f4/koala-upright.py) | [FCStd](assemblies/3c52315ce49d97f4/koala-upright.FCStd) |

## Native parts and versioned alternatives

| Model | Version | Python | FreeCAD |
|---|---|---|---|
| `root_socket_right` | v1 | [Python](parts/root_socket/v1/3c52315ce49d97f4/root_socket_right.py) | [FCStd](parts/root_socket/v1/3c52315ce49d97f4/root_socket_right.FCStd) |
| `root_socket_left` | v1 | [Python](parts/root_socket/v1/3c52315ce49d97f4/root_socket_left.py) | [FCStd](parts/root_socket/v1/3c52315ce49d97f4/root_socket_left.FCStd) |
| `thigh_right` | v4 | [Python](parts/thigh/v4/3c52315ce49d97f4/thigh_right.py) | [FCStd](parts/thigh/v4/3c52315ce49d97f4/thigh_right.FCStd) |
| `thigh_left` | v4 | [Python](parts/thigh/v4/3c52315ce49d97f4/thigh_left.py) | [FCStd](parts/thigh/v4/3c52315ce49d97f4/thigh_left.FCStd) |
| `shank_right` | v2 | [Python](parts/shank/v2/3c52315ce49d97f4/shank_right.py) | [FCStd](parts/shank/v2/3c52315ce49d97f4/shank_right.FCStd) |
| `shank_left` | v2 | [Python](parts/shank/v2/3c52315ce49d97f4/shank_left.py) | [FCStd](parts/shank/v2/3c52315ce49d97f4/shank_left.FCStd) |
| `foot_shank_right` | v1 | [Python](parts/foot_shank/v1/3c52315ce49d97f4/foot_shank_right.py) | [FCStd](parts/foot_shank/v1/3c52315ce49d97f4/foot_shank_right.FCStd) |
| `foot_shank_left` | v1 | [Python](parts/foot_shank/v1/3c52315ce49d97f4/foot_shank_left.py) | [FCStd](parts/foot_shank/v1/3c52315ce49d97f4/foot_shank_left.FCStd) |
| `hip_carrier_right` | v1 | [Python](parts/hip_carrier/v1/3c52315ce49d97f4/hip_carrier_right.py) | [FCStd](parts/hip_carrier/v1/3c52315ce49d97f4/hip_carrier_right.FCStd) |
| `hip_carrier_left` | v1 | [Python](parts/hip_carrier/v1/3c52315ce49d97f4/hip_carrier_left.py) | [FCStd](parts/hip_carrier/v1/3c52315ce49d97f4/hip_carrier_left.FCStd) |
| `front_contact_pad` | v1 | [Python](parts/front_contact_pad/v1/3c52315ce49d97f4/front_contact_pad.py) | [FCStd](parts/front_contact_pad/v1/3c52315ce49d97f4/front_contact_pad.FCStd) |
| `shoulder_carrier_right` | v4 | [Python](parts/shoulder_carrier/v4/3c52315ce49d97f4/shoulder_carrier_right.py) | [FCStd](parts/shoulder_carrier/v4/3c52315ce49d97f4/shoulder_carrier_right.FCStd) |
| `shoulder_carrier_left` | v4 | [Python](parts/shoulder_carrier/v4/3c52315ce49d97f4/shoulder_carrier_left.py) | [FCStd](parts/shoulder_carrier/v4/3c52315ce49d97f4/shoulder_carrier_left.FCStd) |
| `upper_arm_right` | v2 | [Python](parts/upper_arm/v2/3c52315ce49d97f4/upper_arm_right.py) | [FCStd](parts/upper_arm/v2/3c52315ce49d97f4/upper_arm_right.FCStd) |
| `upper_arm_left` | v2 | [Python](parts/upper_arm/v2/3c52315ce49d97f4/upper_arm_left.py) | [FCStd](parts/upper_arm/v2/3c52315ce49d97f4/upper_arm_left.FCStd) |
| `forearm_right` | v2 | [Python](parts/forearm/v2/3c52315ce49d97f4/forearm_right.py) | [FCStd](parts/forearm/v2/3c52315ce49d97f4/forearm_right.FCStd) |
| `forearm_left` | v2 | [Python](parts/forearm/v2/3c52315ce49d97f4/forearm_left.py) | [FCStd](parts/forearm/v2/3c52315ce49d97f4/forearm_left.FCStd) |
| `shoulder_mount_right` | v1 | [Python](parts/shoulder_mount/v1/3c52315ce49d97f4/shoulder_mount_right.py) | [FCStd](parts/shoulder_mount/v1/3c52315ce49d97f4/shoulder_mount_right.FCStd) |
| `shoulder_mount_left` | v1 | [Python](parts/shoulder_mount/v1/3c52315ce49d97f4/shoulder_mount_left.py) | [FCStd](parts/shoulder_mount/v1/3c52315ce49d97f4/shoulder_mount_left.FCStd) |
| `torso_frame` | v5 | [Python](parts/torso_frame/v5/3c52315ce49d97f4/torso_frame.py) | [FCStd](parts/torso_frame/v5/3c52315ce49d97f4/torso_frame.FCStd) |
| `e_tray` | v1 | [Python](parts/e_tray/v1/3c52315ce49d97f4/e_tray.py) | [FCStd](parts/e_tray/v1/3c52315ce49d97f4/e_tray.FCStd) |
| `tray_spacer` | v1 | [Python](parts/tray_spacer/v1/3c52315ce49d97f4/tray_spacer.py) | [FCStd](parts/tray_spacer/v1/3c52315ce49d97f4/tray_spacer.FCStd) |
| `coupon_socket_saddle` | v1 | [Python](parts/coupon_socket_saddle/v1/3c52315ce49d97f4/coupon_socket_saddle.py) | [FCStd](parts/coupon_socket_saddle/v1/3c52315ce49d97f4/coupon_socket_saddle.FCStd) |
| `coupon_socket_fork` | v1 | [Python](parts/coupon_socket_fork/v1/3c52315ce49d97f4/coupon_socket_fork.py) | [FCStd](parts/coupon_socket_fork/v1/3c52315ce49d97f4/coupon_socket_fork.FCStd) |
| `coupon_motor_ring` | v1 | [Python](parts/coupon_motor_ring/v1/3c52315ce49d97f4/coupon_motor_ring.py) | [FCStd](parts/coupon_motor_ring/v1/3c52315ce49d97f4/coupon_motor_ring.FCStd) |
| `coupon_motor_bore` | v1 | [Python](parts/coupon_motor_bore/v1/3c52315ce49d97f4/coupon_motor_bore.py) | [FCStd](parts/coupon_motor_bore/v1/3c52315ce49d97f4/coupon_motor_bore.FCStd) |
| `coupon_ladder` | v1 | [Python](parts/coupon_ladder/v1/3c52315ce49d97f4/coupon_ladder.py) | [FCStd](parts/coupon_ladder/v1/3c52315ce49d97f4/coupon_ladder.FCStd) |
| `coupon_seam` | v1 | [Python](parts/coupon_seam/v1/3c52315ce49d97f4/coupon_seam.py) | [FCStd](parts/coupon_seam/v1/3c52315ce49d97f4/coupon_seam.FCStd) |
| `thigh_frame_right` | v1 | [Python](parts/thigh_frame/v1/3c52315ce49d97f4/thigh_frame_right.py) | [FCStd](parts/thigh_frame/v1/3c52315ce49d97f4/thigh_frame_right.FCStd) |
| `thigh_frame_left` | v1 | [Python](parts/thigh_frame/v1/3c52315ce49d97f4/thigh_frame_left.py) | [FCStd](parts/thigh_frame/v1/3c52315ce49d97f4/thigh_frame_left.FCStd) |
| `thigh_body_right` | v1 | [Python](parts/thigh_body/v1/3c52315ce49d97f4/thigh_body_right.py) | [FCStd](parts/thigh_body/v1/3c52315ce49d97f4/thigh_body_right.FCStd) |
| `thigh_body_left` | v1 | [Python](parts/thigh_body/v1/3c52315ce49d97f4/thigh_body_left.py) | [FCStd](parts/thigh_body/v1/3c52315ce49d97f4/thigh_body_left.FCStd) |
| `thigh_cheek_right` | v1 | [Python](parts/thigh_cheek/v1/3c52315ce49d97f4/thigh_cheek_right.py) | [FCStd](parts/thigh_cheek/v1/3c52315ce49d97f4/thigh_cheek_right.FCStd) |
| `thigh_cheek_left` | v1 | [Python](parts/thigh_cheek/v1/3c52315ce49d97f4/thigh_cheek_left.py) | [FCStd](parts/thigh_cheek/v1/3c52315ce49d97f4/thigh_cheek_left.FCStd) |
| `thigh_flat_right` | v1 | [Python](parts/thigh_flat/v1/3c52315ce49d97f4/thigh_flat_right.py) | [FCStd](parts/thigh_flat/v1/3c52315ce49d97f4/thigh_flat_right.FCStd) |
| `thigh_flat_left` | v1 | [Python](parts/thigh_flat/v1/3c52315ce49d97f4/thigh_flat_left.py) | [FCStd](parts/thigh_flat/v1/3c52315ce49d97f4/thigh_flat_left.FCStd) |
| `shank_flush_right` | v2 | [Python](parts/shank_flush/v2/3c52315ce49d97f4/shank_flush_right.py) | [FCStd](parts/shank_flush/v2/3c52315ce49d97f4/shank_flush_right.FCStd) |
| `shank_flush_left` | v2 | [Python](parts/shank_flush/v2/3c52315ce49d97f4/shank_flush_left.py) | [FCStd](parts/shank_flush/v2/3c52315ce49d97f4/shank_flush_left.FCStd) |

## Native studies

| Model | Version | Python | FreeCAD |
|---|---|---|---|
| `angled-fork` | — | [Python](studies/3c52315ce49d97f4/angled-fork.py) | [FCStd](studies/3c52315ce49d97f4/angled-fork.FCStd) |
| `pitch-mount-face` | — | [Python](studies/3c52315ce49d97f4/pitch-mount-face.py) | [FCStd](studies/3c52315ce49d97f4/pitch-mount-face.FCStd) |
| `body-walking` | — | [Python](studies/3c52315ce49d97f4/body-walking.py) | [FCStd](studies/3c52315ce49d97f4/body-walking.FCStd) |
| `body-quadruped` | — | [Python](studies/3c52315ce49d97f4/body-quadruped.py) | [FCStd](studies/3c52315ce49d97f4/body-quadruped.FCStd) |
| `body-upright` | — | [Python](studies/3c52315ce49d97f4/body-upright.py) | [FCStd](studies/3c52315ce49d97f4/body-upright.FCStd) |
| `rear-leg-current-quadruped` | — | [Python](studies/3c52315ce49d97f4/rear-leg-current-quadruped.py) | [FCStd](studies/3c52315ce49d97f4/rear-leg-current-quadruped.FCStd) |
| `rear-leg-current-upright` | — | [Python](studies/3c52315ce49d97f4/rear-leg-current-upright.py) | [FCStd](studies/3c52315ce49d97f4/rear-leg-current-upright.FCStd) |
| `rear-leg-options-quadruped` | — | [Python](studies/3c52315ce49d97f4/rear-leg-options-quadruped.py) | [FCStd](studies/3c52315ce49d97f4/rear-leg-options-quadruped.FCStd) |
| `rear-leg-options-upright` | — | [Python](studies/3c52315ce49d97f4/rear-leg-options-upright.py) | [FCStd](studies/3c52315ce49d97f4/rear-leg-options-upright.FCStd) |
| `rear-leg-flat-quadruped` | — | [Python](studies/3c52315ce49d97f4/rear-leg-flat-quadruped.py) | [FCStd](studies/3c52315ce49d97f4/rear-leg-flat-quadruped.FCStd) |
| `rear-leg-flat-upright` | — | [Python](studies/3c52315ce49d97f4/rear-leg-flat-upright.py) | [FCStd](studies/3c52315ce49d97f4/rear-leg-flat-upright.FCStd) |
| `pitch-socket-45` | — | [Python](studies/3c52315ce49d97f4/pitch-socket-45.py) | [FCStd](studies/3c52315ce49d97f4/pitch-socket-45.FCStd) |

## Frozen STEP references

| Model | Version | Python | FreeCAD |
|---|---|---|---|
| `docs/design/body-quadruped.step` | — | [Python](references/a6b86da674f3133e/docs__design__body-quadruped.py) | [FCStd](references/a6b86da674f3133e/docs__design__body-quadruped.FCStd) |
| `docs/design/body-upright.step` | — | [Python](references/aba9e5a28ac666aa/docs__design__body-upright.py) | [FCStd](references/aba9e5a28ac666aa/docs__design__body-upright.FCStd) |
| `docs/design/body-walking.step` | — | [Python](references/7245f61dbba9294c/docs__design__body-walking.py) | [FCStd](references/7245f61dbba9294c/docs__design__body-walking.FCStd) |
| `docs/design/carrier-orientation/angled-fork.step` | — | [Python](references/d378833f23642f94/docs__design__carrier-orientation__angled-fork.py) | [FCStd](references/d378833f23642f94/docs__design__carrier-orientation__angled-fork.FCStd) |
| `docs/design/carrier-orientation/pitch-socket-45.step` | — | [Python](references/842f324a147b6823/docs__design__carrier-orientation__pitch-socket-45.py) | [FCStd](references/842f324a147b6823/docs__design__carrier-orientation__pitch-socket-45.FCStd) |
| `docs/design/front-carrier/flat-back-candidate.step` | — | [Python](references/0116530139181f6e/docs__design__front-carrier__flat-back-candidate.py) | [FCStd](references/0116530139181f6e/docs__design__front-carrier__flat-back-candidate.FCStd) |
| `docs/design/rear-leg/rear-leg-quadruped.step` | — | [Python](references/635fb8551fd735c9/docs__design__rear-leg__rear-leg-quadruped.py) | [FCStd](references/635fb8551fd735c9/docs__design__rear-leg__rear-leg-quadruped.FCStd) |
| `docs/design/rear-leg/rear-leg-upright.step` | — | [Python](references/b01caeb2f8b2f136/docs__design__rear-leg__rear-leg-upright.py) | [FCStd](references/b01caeb2f8b2f136/docs__design__rear-leg__rear-leg-upright.FCStd) |
| `docs/design/rear-leg/shank-left.step` | — | [Python](references/df997fed83cd6ba1/docs__design__rear-leg__shank-left.py) | [FCStd](references/df997fed83cd6ba1/docs__design__rear-leg__shank-left.FCStd) |
| `docs/design/rear-leg/shank-right.step` | — | [Python](references/6c2eac81e1e5f9ed/docs__design__rear-leg__shank-right.py) | [FCStd](references/6c2eac81e1e5f9ed/docs__design__rear-leg__shank-right.FCStd) |
| `docs/design/rear-leg/thigh-flat/rear-leg-quadruped.step` | — | [Python](references/866627a4b37cb21b/docs__design__rear-leg__thigh-flat__rear-leg-quadruped.py) | [FCStd](references/866627a4b37cb21b/docs__design__rear-leg__thigh-flat__rear-leg-quadruped.FCStd) |
| `docs/design/rear-leg/thigh-flat/rear-leg-upright.step` | — | [Python](references/e938f8b76e8e1d45/docs__design__rear-leg__thigh-flat__rear-leg-upright.py) | [FCStd](references/e938f8b76e8e1d45/docs__design__rear-leg__thigh-flat__rear-leg-upright.FCStd) |
| `docs/design/rear-leg/thigh-flat/shank_flush-left.step` | — | [Python](references/1379069b0cde9340/docs__design__rear-leg__thigh-flat__shank_flush-left.py) | [FCStd](references/1379069b0cde9340/docs__design__rear-leg__thigh-flat__shank_flush-left.FCStd) |
| `docs/design/rear-leg/thigh-flat/shank_flush-right.step` | — | [Python](references/e00373e466ebc9a9/docs__design__rear-leg__thigh-flat__shank_flush-right.py) | [FCStd](references/e00373e466ebc9a9/docs__design__rear-leg__thigh-flat__shank_flush-right.FCStd) |
| `docs/design/rear-leg/thigh-flat/thigh_flat-left.step` | — | [Python](references/81700a8dbcebb01d/docs__design__rear-leg__thigh-flat__thigh_flat-left.py) | [FCStd](references/81700a8dbcebb01d/docs__design__rear-leg__thigh-flat__thigh_flat-left.FCStd) |
| `docs/design/rear-leg/thigh-flat/thigh_flat-right.step` | — | [Python](references/3dd6d4c842e903c5/docs__design__rear-leg__thigh-flat__thigh_flat-right.py) | [FCStd](references/3dd6d4c842e903c5/docs__design__rear-leg__thigh-flat__thigh_flat-right.FCStd) |
| `docs/design/rear-leg/thigh-left.step` | — | [Python](references/f07b1d419f9f26df/docs__design__rear-leg__thigh-left.py) | [FCStd](references/f07b1d419f9f26df/docs__design__rear-leg__thigh-left.FCStd) |
| `docs/design/rear-leg/thigh-options/rear-leg-quadruped.step` | — | [Python](references/0509ea648dec3da1/docs__design__rear-leg__thigh-options__rear-leg-quadruped.py) | [FCStd](references/0509ea648dec3da1/docs__design__rear-leg__thigh-options__rear-leg-quadruped.FCStd) |
| `docs/design/rear-leg/thigh-options/rear-leg-upright.step` | — | [Python](references/f008ed3d6d620572/docs__design__rear-leg__thigh-options__rear-leg-upright.py) | [FCStd](references/f008ed3d6d620572/docs__design__rear-leg__thigh-options__rear-leg-upright.FCStd) |
| `docs/design/rear-leg/thigh-options/thigh_body-left.step` | — | [Python](references/f523a8a3f7423bb2/docs__design__rear-leg__thigh-options__thigh_body-left.py) | [FCStd](references/f523a8a3f7423bb2/docs__design__rear-leg__thigh-options__thigh_body-left.FCStd) |
| `docs/design/rear-leg/thigh-options/thigh_body-right.step` | — | [Python](references/fd4975d2f4c1c389/docs__design__rear-leg__thigh-options__thigh_body-right.py) | [FCStd](references/fd4975d2f4c1c389/docs__design__rear-leg__thigh-options__thigh_body-right.FCStd) |
| `docs/design/rear-leg/thigh-options/thigh_cheek-left.step` | — | [Python](references/f1f1aee9fd127091/docs__design__rear-leg__thigh-options__thigh_cheek-left.py) | [FCStd](references/f1f1aee9fd127091/docs__design__rear-leg__thigh-options__thigh_cheek-left.FCStd) |
| `docs/design/rear-leg/thigh-options/thigh_cheek-right.step` | — | [Python](references/8dca46ecd88c50c1/docs__design__rear-leg__thigh-options__thigh_cheek-right.py) | [FCStd](references/8dca46ecd88c50c1/docs__design__rear-leg__thigh-options__thigh_cheek-right.FCStd) |
| `docs/design/rear-leg/thigh-options/thigh_frame-left.step` | — | [Python](references/0d66bae2f3d6028e/docs__design__rear-leg__thigh-options__thigh_frame-left.py) | [FCStd](references/0d66bae2f3d6028e/docs__design__rear-leg__thigh-options__thigh_frame-left.FCStd) |
| `docs/design/rear-leg/thigh-options/thigh_frame-right.step` | — | [Python](references/25f339e846058422/docs__design__rear-leg__thigh-options__thigh_frame-right.py) | [FCStd](references/25f339e846058422/docs__design__rear-leg__thigh-options__thigh_frame-right.FCStd) |
| `docs/design/rear-leg/thigh-right.step` | — | [Python](references/45445ce22e89a3f7/docs__design__rear-leg__thigh-right.py) | [FCStd](references/45445ce22e89a3f7/docs__design__rear-leg__thigh-right.FCStd) |
| `docs/design/so101/under_socket_source.step` | — | [Python](references/aed104cf7d720d55/docs__design__so101__under_socket_source.py) | [FCStd](references/aed104cf7d720d55/docs__design__so101__under_socket_source.FCStd) |
| `docs/design/so101/upper_fork_source.step` | — | [Python](references/a00d3c1372eba8bd/docs__design__so101__upper_fork_source.py) | [FCStd](references/a00d3c1372eba8bd/docs__design__so101__upper_fork_source.FCStd) |
| `docs/design/so101/upper_socket_source.step` | — | [Python](references/899abc4835343a2a/docs__design__so101__upper_socket_source.py) | [FCStd](references/899abc4835343a2a/docs__design__so101__upper_socket_source.FCStd) |
| `docs/design/so101/wrist_holder_source.step` | — | [Python](references/e58d86502535a5a4/docs__design__so101__wrist_holder_source.py) | [FCStd](references/e58d86502535a5a4/docs__design__so101__wrist_holder_source.FCStd) |
| `docs/design/walking/foot_shank_left-v1.step` | — | [Python](references/227d822576ed7e68/docs__design__walking__foot_shank_left-v1.py) | [FCStd](references/227d822576ed7e68/docs__design__walking__foot_shank_left-v1.FCStd) |
| `docs/design/walking/foot_shank_right-v1.step` | — | [Python](references/e53d35b44c9cba21/docs__design__walking__foot_shank_right-v1.py) | [FCStd](references/e53d35b44c9cba21/docs__design__walking__foot_shank_right-v1.FCStd) |
| `hardware/vendor/so-arm100/Rotation_Pitch_08i.step` | — | [Python](references/de12d52e931e827d/hardware__vendor__so-arm100__Rotation_Pitch_08i.py) | [FCStd](references/de12d52e931e827d/hardware__vendor__so-arm100__Rotation_Pitch_08i.FCStd) |
| `hardware/vendor/so-arm100/SO101/Motor_holder_SO101_Wrist.step` | — | [Python](references/e58d86502535a5a4/hardware__vendor__so-arm100__SO101__Motor_holder_SO101_Wrist.py) | [FCStd](references/e58d86502535a5a4/hardware__vendor__so-arm100__SO101__Motor_holder_SO101_Wrist.FCStd) |
| `hardware/vendor/so-arm100/SO101/Under_arm_SO101.step` | — | [Python](references/677a1a57efeddc43/hardware__vendor__so-arm100__SO101__Under_arm_SO101.py) | [FCStd](references/677a1a57efeddc43/hardware__vendor__so-arm100__SO101__Under_arm_SO101.FCStd) |
| `hardware/vendor/so-arm100/SO101/Upper_arm_SO101.step` | — | [Python](references/efa19a6dd2ccb459/hardware__vendor__so-arm100__SO101__Upper_arm_SO101.py) | [FCStd](references/efa19a6dd2ccb459/hardware__vendor__so-arm100__SO101__Upper_arm_SO101.FCStd) |
| `hardware/vendor/so-arm100/STS3215_03a.step` | — | [Python](references/cacd717c2f22bec8/hardware__vendor__so-arm100__STS3215_03a.py) | [FCStd](references/cacd717c2f22bec8/hardware__vendor__so-arm100__STS3215_03a.FCStd) |
