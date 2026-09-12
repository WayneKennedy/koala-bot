# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Single source of dimensional truth (mm). DEC-09: bed_size and scale are parameters.

Provenance tags:
  [STEP]    measured from vendor STEP (vendor/so-arm100/STS3215_03a.step)
  [VENDOR]  stated on the vendor product page
  [STD]     published standard (Arduino Uno drawing, insert catalogues)
  [SPEC]    stated in the Feetech ST-3215-C018 product specification (A/0,
            2023-07-20) - the vendor's own document, which outranks the STEP
  [VERIFY]  best-available figure - confirm against the physical part before
            printing anything that depends on it (see parts/coupons.py)
  [MEASURED] confirmed by a printed coupon on the reference printer, dated;
            results and their caveats live in docs/test-log.md
  [DESIGN]  chosen design target or nominal geometry, not a measurement
  [SUPPLIED] read off hardware that arrived in the box, dated; what the vendor
            actually ships, which is not always what the spec sheet says
"""

# --- Printer / process -------------------------------------------------------
BED_X = 200.0  # DEC-09 hard limit
BED_Y = 200.0
BED_Z = 200.0

# Fit constants - calibrate once with the coupon prints on the Ender-5 S1,
# then they hold for every part (DEC-23). These are REFERENCE-PRINTER values:
# derive them from a coupon *fit* (smallest size that accepts the real part),
# on a printer whose flow and XY accuracy are already calibrated - otherwise
# they absorb that machine's error. See hardware/README "Reading a coupon
# result".
CLEAR_POCKET = 0.25   # [VERIFY] generic non-servo fits; servo uses SOCKET_CLEAR
CLEAR_HOLE_M3 = 3.4   # [MEASURED 2026-09-01] coupon_ladder: 3.4 slides free,
                      # 3.2 threads in by hand (too tight for a clearance hole)
CLEAR_HOLE_M2_5 = 2.9 # [VERIFY] not yet coupon-tested; scaled from M3
INSERT_M3_DIA = 4.0   # [VERIFY] M3 brass heat-set: nominal boss hole
INSERT_M3_LEN = 5.7
CAP_M3_DIA = 5.5      # [STD] M3 socket cap head across the flats' circle
CAP_M3_H = 3.0        # [STD] cap head height - what stands proud (DEC-25)
WALL = 3.0            # default structural wall
PLATE = 5.0           # default structural plate thickness

# --- Shared ST3215 / SO-101 horn inputs ------------------------------------
SERVO_AXIS_X = 12.5    # [SPEC] axis offset from case length centre
SERVO_DRIVE_SQ = 9.9   # [STEP] SO-101 printed horn hole pattern
SERVO_MASS = 55.0      # [SPEC] per bare servo, nominal
SELFTAP_DIA = 2.0      # [SUPPLIED 2026-09-07] M2x5 case-lug screws (Waveshare); RCmall packs read M2x6, unmeasured (test-log 2026-09-12)
HORN_SCREW = "M3x6"    # [SUPPLIED 2026-09-08] pan head, in the Waveshare ST3215 box;
HORN_SCREW_HEAD_DIA = 5.2  # [SUPPLIED 2026-09-08] Waveshare box; RCmall packs ship the same M3x6 pan head, head not re-measured (2026-09-12)
HORN_SCREW_HEAD_H = 2.0    # [SUPPLIED 2026-09-08] upstream's fork counterbores are too
                           # small for these heads; size koala's to them

# --- Drive motor - DFRobot FIT0403 37D 12V 122rpm w/encoder (Pi Hut) ---------
# Manufacturer drawing:
# https://dfimg.dfrobot.com/wiki/17480/FIT0403_gb37y3530-12v-90en_dimension_1.0.jpg
MOTOR_DIA = 37.0        # [VENDOR] gearbox diameter
MOTOR_BODY_LEN = 69.0   # [VENDOR] mounting face -> encoder cap: 6+24+29+10
MOTOR_LEN = 90.0        # [VENDOR] overall envelope: 69 body + 21 shaft
MOTOR_FACE_BOSS_DIA = 12.0  # [VERIFY] centre boss on faceplate
MOTOR_FACE_BOSS_H = 2.0     # [VERIFY]
MOTOR_BCD = 31.0        # [VENDOR] 6x M3, adjacent spacing 15.5 => hex on d31
MOTOR_FACE_SCREWS = 6
MOTOR_SHAFT_DIA = 6.0   # [VENDOR] D-shaft
MOTOR_SHAFT_LEN = 21.0  # [VENDOR] mounting face -> shaft tip
MOTOR_D_LEN = 15.5      # [VENDOR] length of the D-shaped portion

# --- Wheel & hub (Pololu 80x10 + 6mm universal hub) --------------------------
WHEEL_DIA = 80.0        # [VENDOR] DEC-19 fixed control constant
WHEEL_W = 10.0          # [VENDOR]
HUB_DIA = 25.4          # [VENDOR] Pololu 1999 mechanical drawing
HUB_T = 9.5             # [VENDOR] axial thickness
HUB_STACK = 18.0        # [VERIFY] clears 5 mm cheek + 3 mm heads + 9.5 mm hub
WHEEL_CLEAR = 4.0       # radial/axial clearance kept around the tyre

# --- Electronics (tray patterns) --------------------------------------------
# Arduino Uno R3 hole pattern (TB9051FTG shield) - origin at board corner.
UNO_BOARD = (68.58, 53.34)                       # [STD]
UNO_HOLES = [(13.97, 2.54), (15.24, 50.8),
             (66.04, 17.78), (66.04, 45.72)]     # [STD]
TEENSY_BOARD = (35.56, 17.78)                    # [STD] no mounting holes
BNO085_BOARD = (25.4, 19.5)                      # [VERIFY] Adafruit 4754
STANDOFF_H = 5.0        # printed standoffs under the driver shield
TRAY_GAP = 10.0         # bought M3 standoffs, pelvis top -> tray underside

# --- DEC-36/37/38/40 body master and structural assembly ------------------
# [DESIGN] Maintainer-adopted GPT schematics, 2026-09-08. See docs/body-layout.md.
# Segment lengths govern the next layout. DEC-37 resolves pose/envelope
# annotations; DEC-40 implements the compact links and adjusts packaging.
BODY_STANDING_HEIGHT_MM = 450.0
BODY_HEAD_LENGTH_MM = 85.0
BODY_HEAD_WIDTH_MM = 110.0    # engineering packaging envelope, DEC-37
BODY_HEAD_HEIGHT_MM = 75.0
BODY_NECK_LENGTH_MM = 35.0
BODY_TORSO_LENGTH_MM = 150.0    # shoulder axis to hip axis
BODY_RUMP_LENGTH_MM = 70.0     # hip to rear envelope
BODY_UPPER_ARM_MM = 70.0       # shoulder to elbow
BODY_FOREARM_MM = 75.0         # elbow to nominal wrist, DEC-43
BODY_HAND_MM = 25.0            # wrist to fixed ball centre, along forearm
BODY_FRONT_FOOT_RADIUS_MM = 16.0 # integral rounded foot; grip/loads unverified
BODY_THIGH_MM = 85.0           # hip pitch to knee
BODY_SHANK_MM = 90.0           # knee to ankle/wheel axis
BODY_WHEEL_COUNT = 2           # rear ankles only, DEC-43
BODY_DRIVE_MOTOR_COUNT = 2     # bought 37D pair
BODY_WHEEL_DIA_MM = WHEEL_DIA  # 80 mm rear wheels
BODY_LENGTH_TARGET_MM = 340.0  # nose to rear, closed quadruped envelope ~339.6
BODY_WHEELBASE_TARGET_MM = 260.0 # front foot to rear wheel contact centres
BODY_TRACK_TARGET_MM = 220.0   # DEC-40: retains clearance with inward roll and bought 69 mm motors
BODY_SHOULDER_WIDTH_MM = 149.0
BODY_QUAD_SHOULDER_HEIGHT_MM = 165.0 # axis height, from closed front-leg IK
BODY_QUAD_HIP_HEIGHT_MM = 175.0
BODY_QUAD_REAR_OFFSET_MM = 55.0 # rear wheel axle behind hip in quad stance
BODY_MOTOR_GAP_MIN_MM = 4.0
BODY_QUAD_RUMP_HEIGHT_MM = 220.0
BODY_UPRIGHT_SHOULDER_HEIGHT_MM = 340.0 # 190 hip + 150 torso
BODY_GROUND_CLEARANCE_MM = 60.0 # lowest body point, excludes limbs/wheels
BODY_UPRIGHT_WRIST_X_MM = 100.0 # front ball centre; historical WRIST name retained
BODY_UPRIGHT_WRIST_RISE_MM = -10.0 # front ball centre relative to shoulder

# --- Historical DEC-32 / DEC-34 sizing study, superseded by DEC-36 ---------
# Independent of the discarded assembly above. [DESIGN] is an engineering
# target/assumption, NOT measured hardware or an accepted mechanical layout.
RESTART_MASS_KG = 3.0            # [DESIGN] upper end of DEC-15
RESTART_THIGH_MM = 100.0        # [DESIGN] OQ-16 candidate axis-to-axis length
RESTART_SHANK_MM = 100.0        # [DESIGN] OQ-16 candidate axis-to-axis length
RESTART_DECK_TO_ROLL_MM = 40.0  # [DESIGN] packaging allocation, not socket CAD
RESTART_ROLL_TO_PITCH_MM = 25.0 # [DESIGN] vertical packaging allocation
RESTART_ROLL_HALF_MM = 60.0     # [DESIGN] sensitivity-study datum only
RESTART_UPPER_HEIGHT_MM = 150.0 # [DESIGN] deck to head top allocation
RESTART_KNEE_NOMINAL_DEG = 30.0 # [DESIGN] bent stance candidate
RESTART_KNEE_RANGE_DEG = (0.0, 90.0)   # [DESIGN] clearance-study target
RESTART_HIP_RANGE_DEG = (-30.0, 45.0) # [DESIGN] clearance-study target
RESTART_ROLL_RANGE_DEG = (-10.0, 10.0) # [DESIGN] clearance-study target
RESTART_TRACK_TARGET_MM = 240.0 # [DESIGN] preferred maximum; feasibility open
RESTART_MOTOR_GAP_MM = 2.0      # [DESIGN] nominal analytical separation target
RESTART_ACCEL_G = 0.5           # [DESIGN] fore/aft load-case assumption
RESTART_ONE_WHEEL_LOAD_G = 2.0  # [DESIGN] structural proof-load target
RESTART_SHOVE_N = 10.0          # [DESIGN] lateral load at head-top allocation
RESTART_TORQUE_KGFCM = 30.0     # [VENDOR] Waveshare ST3215 12V advertised torque;
                               # not an established continuous torque rating
STANDARD_GRAVITY = 9.80665      # [STD] m/s²

# --- DEC-33 SO-101 socket, native X = output axis, Z = long case axis -------
# Servo face words (docs/soarm-joint-pattern.md, Terminology): FRONT = the
# drive-horn face (+X), BACK = the idler/connector face (-X), BOTTOM = the end
# it stands on (Z=0, ears near it), TOP = the end nearest the output axis
# (Z=45.23), SIDES = the two flat long faces (+-Y). The pocket (widest faces)
# is centred at X=0. No pocket derives from a servo STEP.
SOCKET_CASE_X = 34.9       # [STEP] SO-101 Gauge_0 pocket, across output axis;
                           # calipers 2026-09-08: the widest case faces are ~34.8
# The case has THREE face planes on each side of the output axis
# (calipers, 2026-09-08). Distances are face-to-face across the axis:
SOCKET_EAR_X = 31.8        # [MEASURED 2026-09-08] faces carrying the M2 lug holes;
                           # the SO-101 cradle walls boss inward to exactly 31.8
                           # at the holes (STEP: 15.6 + 16.2)
SOCKET_HORN_SEAT_X = 28.8  # [MEASURED 2026-09-08] faces the drive horn and idler
                           # sit on, flat
SOCKET_IDLER_T = 3.1       # [MEASURED 2026-09-08] idler thickness; sits flat on the seat
# Where each plane runs along the height (from the Bottom). Measured on the
# BACK (photos IMG_6993/6994, lettered A-D): ears 0-5.3, widest 5.3-18.8, then
# the seat level to the Top; the output axis is the C/D line at 35.2 (spec
# 35.1). The Ø20 seat is a RAISED pad the idler covers exactly; the general
# face around it in C/D is lower still, so modelling C/D at the seat plane is
# conservative for Back clearance. Front pad height instead uses the supplied
# STEP envelope below; its physical region lengths have not been measured.
SOCKET_REGION_Z = (5.3, 18.8)  # [MEASURED 2026-09-08 Back] ear|widest, widest|seat
# [STEP 2026-09-11] pinned SO101/Upper_arm: unequal recess widths.
# Drive: Y +/-7 from the floor. Idler: Y +/-9.25, starting Z=5.
# These are socket features, not inferred symmetric servo dimensions.
SOCKET_DRIVE_SLOT_Y = 14.0
SOCKET_IDLER_SLOT_Y = 18.5  # also consistent with the measured Back pad
SOCKET_IDLER_SLOT_Z = 5.0
SOCKET_DRIVE_PAD_TOP = 25.55 # [STEP envelope] supplied case plane ends at 25.5444;
                            # conservative fallback only, not a pocket datum
SOCKET_BOSS_DIA = 8.0      # [VERIFY] Back boss through the idler, from the photos
SOCKET_BAY_Z = (18.8, 24.5)  # [MEASURED 2026-09-08] connector bay on the Back, height band;
                             # connectors face out along the axis - keep it uncovered
SOCKET_IDLER_BOSS_PROUD = 0.7  # [MEASURED 2026-09-08] the servo's Back boss above the
                               # idler's outer face; the Back plate needs a >=0.7
                               # deep blind centre recess
SOCKET_CASE_Y = 24.7       # [STEP] SO-101 Gauge_0 pocket, case width
SOCKET_CASE_L = 45.23      # [SPEC] nominal case length
SOCKET_CLEAR = 0.0        # [MEASURED 2026-09-07] maintainer: SO-101 fits PLA+/PETG
SOCKET_AXIS_Z = SOCKET_CASE_L / 2 + SERVO_AXIS_X  # [SPEC] rear-face to axis
SOCKET_WALL = 5.0         # [DESIGN] SO-101 nominal wall >=4.8
SOCKET_DEPTH = 17.0       # [STEP] SO-101 rear-case capture depth
SOCKET_SHELF = 5.0        # [DESIGN] cradle floor under the servo's Bottom
SOCKET_COLLAR_WALL = 3.0  # [STEP] SO-101 sleeve
SOCKET_COLLAR_BOTTOM = -9.0 # [STEP] sleeve overlap below the servo's Bottom
SOCKET_COLLAR_CLEAR = 0.1 # [DESIGN] per side = 0.2 total
SOCKET_FRONT_CLEAR = 0.16 # [STEP] upstream front-wall contact allowance
SOCKET_LUG_BACK_Z = 2.25   # [STEP] SO-101 printed holes, not a caliper measurement
SOCKET_LUG_DRIVE_Z = 5.8  # [STEP] SO-101 printed holes, not a caliper measurement
SOCKET_LUG_Y = 10.25       # [STEP][SPEC] offset from case width centre
SOCKET_M2_CLEAR = 2.0     # [STEP] clearance in print; not the case pilot diameter
SOCKET_M2_SEAT = 2.2      # [STEP] plastic under supplied M2x5 head
SOCKET_M2_HEAD = 4.0      # [VERIFY] head clearance for supplied M2 self-tapper
SOCKET_M2_TOOL = 6.0      # [DESIGN] straight driver envelope
SOCKET_BOSS_W = 6.0       # [DESIGN] collar lug boss width
SOCKET_BOSS_CLEAR = 0.2   # [DESIGN] clearance between collar bosses and cradle
SOCKET_SEAT_OFFSET = 0.5   # [MEASURED 2026-09-08] the widest faces are NOT symmetric
                           # about the horn seats: seat->widest is 2.5 on the drive
                           # side and 3.5 on the back (connector/idler) side. The
                           # pocket (34.8/34.9) is the cradle datum at X=0, so the
                           # seat mid-plane sits +0.5 toward the drive side.
SOCKET_IDLER_FACE = SOCKET_SEAT_OFFSET - (SOCKET_HORN_SEAT_X / 2 + SOCKET_IDLER_T)
                           # [MEASURED] -17.0: idler outer face, 0.4 INSIDE the
                           # widest Back plane (-17.45), so the Back plate (R 14)
                           # must not reach any height where the case is at full
                           # width - plane heights still to measure.
SOCKET_HORN_SPAN = 36.4   # [MEASURED 2026-09-08] calipers: drive horn outer face
                          # to idler wheel outer face on a Waveshare ST3215 with
                          # both horns fitted = 36.4; the printed SO-101
                          # Rotation_Pitch fork measures 36.4 inner face to inner
                          # face, and Rotation_Pitch_SO101.step agrees (arm faces
                          # at Y=10.0 and 46.4). The earlier 37.5 was a probing
                          # error in docs/soarm-joint-pattern.md, not upstream's.
SOCKET_DRIVE_FACE = SOCKET_IDLER_FACE + SOCKET_HORN_SPAN
SOCKET_HORN_DIA = 20.0    # [STEP] both horn discs
SOCKET_PLATE_T = 3.5      # [STEP] SO-101 clevis plates
SOCKET_PLATE_R = 10.4     # [DESIGN] compact root; Back connector clearance
SOCKET_CENTRE_CLEAR = 3.2 # [STEP] drive centre screw access
SOCKET_ARM_LENGTH = 32.0 # [DESIGN] joint-rig clevis arm, from output axis
SOCKET_ARM_HALF_W = 8.0 # [DESIGN] flat cheek width
SOCKET_CABLE_W = 8.0     # [VERIFY] connector/loom corridor width, rig fit check
SOCKET_CABLE_H = 6.0     # [VERIFY] rear-case cable corridor height

SOCKET_M2_HEAD_H = 1.4 # [VERIFY] supplied self-tapper head; rig check

# --- DEC-43 integrated structural CAD [DESIGN], dimensions in mm --------
SOCKET_PAD_T = 6.3       # 3.5 mm bearing web + 2.8 mm pan-head/washer pocket
SOCKET_HEAD_CLEAR = 6.4
LINK_BRIDGE_START = 18.0 # from proximal axis; outside nominal case nose
LINK_BRIDGE_END = 32.0
LINK_SPINE_HALF = 8.0
ROOT_PITCH_Y = 24.0     # lateral first-axis centres; roll follows pitch (DEC-41)
ROOT_MOUNT_Z = SOCKET_AXIS_Z + SOCKET_SHELF
ROOT_REAR_MOUNT_Z = 46.0 # [DESIGN DEC-49] head underside at 43: clears the
                         # common carrier back's 40.91 mm radial sweep by >2 mm
ROOT_FRAME_HOLES = ((-30.,-34.),(-30.,34.),(-20.,-34.),(-20.,34.))  # outside case/driver footprints
FRAME_PLATE_T = 5.0
MOTOR_MOUNT_T = 5.0
MOTOR_MOUNT_R = 23.0
MOTOR_SUPPORT_T = 5.0
MOTOR_SUPPORT_OFFSET = 24.0

HORN_IDLER_WASHER_T = 0.5  # [DESIGN] M3 narrow washer, prevents nominal idler bottoming
HORN_IDLER_WASHER_OD = 6.0 # [DESIGN] procure matching narrow washer


# DEC-48 manufacturing revision, preserving DEC-44 joint centres.
ROOT_MODULE_GAP = 0.6       # removable left/right socket plates
ROOT_LOCATOR_DIA = 4.0      # integral locating pins, not threaded plastic
ROOT_LOCATOR_DEPTH = 2.0
FRONT_PAD_START = 96.0     # 100 mm nominal ball centre, truncated top
FRONT_PAD_NUT_Z = 92.0
