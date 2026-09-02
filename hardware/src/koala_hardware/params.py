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
CLEAR_POCKET = 0.25   # [VERIFY] snug component pocket, per side
CLEAR_HOLE_M3 = 3.4   # [MEASURED 2026-09-01] coupon_ladder: 3.4 slides free,
                      # 3.2 threads in by hand (too tight for a clearance hole)
CLEAR_HOLE_M2_5 = 2.9 # [VERIFY] not yet coupon-tested; scaled from M3
INSERT_M3_DIA = 4.0   # [VERIFY] M3 brass heat-set: nominal boss hole
INSERT_M3_LEN = 5.7
CAP_M3_DIA = 5.5      # [STD] M3 socket cap head across the flats' circle
CAP_M3_H = 3.0        # [STD] cap head height - what stands proud (DEC-25)
WALL = 3.0            # default structural wall
PLATE = 5.0           # default structural plate thickness

# --- Feetech STS3215 (limb/hip servo) ---------------------------------------
# Model ST-3215-C018. TWO INDEPENDENT FEATURE FAMILIES, on two different
# datums. Keeping them apart matters: conflating them is what produced a run
# of wrong conclusions (see docs/test-log.md 2026-09-02).
#
#   1. BODY, datum = the case.       Where the servo sits and how it is held.
#   2. HORN, datum = the output axis. What the servo drives. ROTATES.
#
# The output axis sits SERVO_AXIS_X from the body centre, so a body feature
# expressed as "distance from the axis" silently depends on that offset.
# Prefer case coordinates for anything in family 1.
#
# Sources, most to least authoritative:
#   [SPEC]  Feetech ST-3215-C018 specification A/0, 2023-07-20 - the maker's
#           own document. Describes the BARE servo, no horn fitted.
#   upstream printed parts - validated by every SO-ARM100/101 ever assembled;
#           if their holes were wrong the arms would not go together.
#   [STEP]  vendor/so-arm100/STS3215_03a.step - author UNKNOWN. Distributed by
#           TheRobotStudio, not demonstrably by Feetech (it models 45.4 x 24.8
#           where Feetech states 45.23 x 24.73). Models the servo WITH horn and
#           idler fitted, which is why it carries features the drawing lacks.
#           Treat as an approximation; it has already been wrong once.

# --- family 1: the BODY (case datum) ---
# [SPEC 6-1] gives 45.2 x 24.7 x 35. The STEP models 45.4 x 24.8. Pocket
# constants stay on the STEP's larger figures deliberately: a 0.2 mm generous
# pocket is the safe direction for an error.
SERVO_L = 45.4          # [STEP] X (spec: 45.23)
SERVO_W = 24.8          # [STEP] Y (spec: 24.73)
SERVO_MASS = 55.0       # [SPEC 6-8] 55 +/- 1 g; 12 of them is 660 g
SERVO_CASE = "PA+GF"    # [SPEC 6-3] glass-filled nylon. No metal thread in the
                        # case - so nothing here takes a load-bearing thread.
SERVO_BODY_TOP = 16.2   # [STEP] case top face (below horn boss)
SERVO_BODY_BOT = -19.4  # [STEP] case bottom face

# Body mounting holes. Upstream seats the servo in a snug printed pocket and
# fixes it with 2 screws into the FRONT face and 2 into the BACK.
SERVO_TAB_Y = 10.4      # [STEP][SPEC-corroborated] +/-y. 20.8 mm apart, ~2 mm
                        # from a 24.73 case edge - matches the drawing.
SERVO_TAB_X = -20.7     # [STEP] ONLY. The drawing carries no X dimension for
                        # these. This is the least-supported number in the
                        # file and it positions every retention screw. OQ-12.
SERVO_TAB_HOLE = 4.0    # [STEP] ONLY, and an INTERPRETATION: a STEP cylinder
                        # says nothing about which side is material, so this
                        # may be a bore or a clamshell pillar. OQ-12.
# Self-tapping retention screws. Sizes are working assumptions.
SELFTAP_DIA = 2.5       # [VERIFY] screw major dia
SELFTAP_PILOT = 2.1     # [VERIFY] thread-forming pilot in PETG, ~0.85 x major
SELFTAP_CLEAR = 2.8     # [VERIFY] clearance for the same screw

# --- family 2: the HORN (output-axis datum) - THIS ROTATES ---
# NOT servo geometry. [SPEC 11] "No Accessories": Feetech ships the servo bare,
# so the horn comes from the kit vendor and these numbers follow whichever horn
# is actually fitted. Filed here for convenience, but they are horn constants.
SERVO_AXIS_X = 12.5     # [STEP][SPEC-dimensioned] axis offset from body centre
SERVO_HORN_TOP = 20.2   # [STEP] top face of the fitted metal horn disc
SERVO_HORN_DIA = 20.0   # [STEP] horn / idler disc - matches assembly photos
SERVO_IDLER_BOT = -19.4 # [STEP] idler disc bottom = case bottom plane
SERVO_HORN_BOSS_DIA = 9.0   # [STEP] centre boss under the horn - keep clear
SERVO_HORN_SCREW = "M3x6"   # [SPEC 6-13] the single CENTRE screw fixing the
                            # horn to the 25T spline. Says nothing about the
                            # 4-hole drive square below. Not supplied.
SERVO_DRIVE_SQ = 9.9    # [STEP] 4x drive holes on a 9.9 mm square
SERVO_DRIVE_SCREW = CLEAR_HOLE_M3
# M3, not M2.5. The STEP models these at 2.5 - the M3 TAPPING DRILL - which an
# earlier session read as an M2.5 clearance hole. Upstream's own bracket drills
# 3.2 (M3 clearance) on this same square, and their arms assemble, so M3 is
# right. An M3 will not pass through 2.9.

# clearance; the hold is made against the servo. Threading only the print does
# nothing - the screw would rattle in the servo's Ø4 bore.
# OPEN (OQ-12): whether those screws thread the servo's case, or become a
# through-bolt + nut clamping both walls onto its end faces. The latter cuts no
# thread in a PA+GF case, which wears with reassembly, and suits a load-bearing
# hip better than an arm. Clearance in the print keeps both options live.
SERVO_TAB_TOP = 17.0    # [STEP] tab top face height (approx; tab is proud of case)

# --- Drive motor - DFRobot FIT0403 37D 12V 122rpm w/encoder (Pi Hut) ---------
MOTOR_DIA = 37.0        # [VENDOR] gearbox diameter
MOTOR_LEN = 90.0        # [VERIFY] overall incl. encoder; envelope only
MOTOR_FACE_BOSS_DIA = 12.0  # [VERIFY] centre boss on faceplate
MOTOR_FACE_BOSS_H = 2.0     # [VERIFY]
MOTOR_BCD = 31.0        # [VENDOR] 6x M3, adjacent spacing 15.5 => hex on d31
MOTOR_FACE_SCREWS = 6
MOTOR_SHAFT_DIA = 6.0   # [VENDOR] D-shaft
MOTOR_SHAFT_LEN = 15.5  # [VENDOR]

# --- Wheel & hub (Pololu 80x10 + 6mm universal hub) --------------------------
WHEEL_DIA = 80.0        # [VENDOR] DEC-19 fixed control constant
WHEEL_W = 10.0          # [VENDOR]
HUB_STACK = 14.0        # [VERIFY] motor face -> wheel inner face (hub + margin)
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

# --- Assembly layout (v0 draft) ----------------------------------------------
TRACK_HALF = 66.0       # pelvis centre -> wheel mid-plane (HIP_ROLL_Y + 33)
THIGH_DROP = 120.0      # hip-pitch axis -> wheel axis
PELVIS_PLATE = (150.0, 100.0, PLATE)
HIP_ROLL_Y = 33.0       # pelvis centre -> hip-roll axis (Y)
HIP_ROLL_DROP = 50.0    # pelvis top -> hip-roll axis (Z); clears SERVO_ABOVE
HIP_PITCH_DROP = 60.0   # hip-roll axis -> hip-pitch axis

# Servo extents measured from its OUTPUT AXIS (not its body centre): the axis
# is offset SERVO_AXIS_X from centre, so the body reaches much further one way.
SERVO_ABOVE = SERVO_AXIS_X + SERVO_L / 2   # 35.2 - axis to far (tab) end
SERVO_BELOW = SERVO_L / 2 - SERVO_AXIS_X   # 10.2 - axis to output end
