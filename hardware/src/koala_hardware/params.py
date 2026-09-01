# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Single source of dimensional truth (mm). DEC-09: bed_size and scale are parameters.

Provenance tags:
  [STEP]    measured from vendor STEP (vendor/so-arm100/STS3215_03a.step)
  [VENDOR]  stated on the vendor product page
  [STD]     published standard (Arduino Uno drawing, insert catalogues)
  [VERIFY]  best-available figure - confirm against the physical part before
            printing anything that depends on it (see parts/coupons.py)
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
CLEAR_HOLE_M3 = 3.4   # clearance hole dia for M3
CLEAR_HOLE_M2_5 = 2.9 # clearance hole dia for M2.5
INSERT_M3_DIA = 4.0   # [VERIFY] M3 brass heat-set: nominal boss hole
INSERT_M3_LEN = 5.7
CAP_M3_DIA = 5.5      # [STD] M3 socket cap head across the flats' circle
CAP_M3_H = 3.0        # [STD] cap head height - what stands proud (DEC-25)
WALL = 3.0            # default structural wall
PLATE = 5.0           # default structural plate thickness

# --- Feetech STS3215 (limb/hip servo) - axes as in the vendor STEP -----------
# Body is a box centred on origin in X/Y; output (spline) axis is +Z at
# (SERVO_AXIS_X, 0). Horn top face at +Z, idler hub at -Z (double-sided joint).
SERVO_L = 45.4          # [STEP] X
SERVO_W = 24.8          # [STEP] Y
SERVO_BODY_TOP = 16.2   # [STEP] case top face (below horn boss)
SERVO_BODY_BOT = -19.4  # [STEP] case bottom face
SERVO_AXIS_X = 12.5     # [STEP] output axis offset from body centre
SERVO_HORN_TOP = 20.2   # [STEP] top face of fitted metal horn disc
SERVO_HORN_DIA = 20.0   # [STEP] horn / idler hub disc
SERVO_IDLER_BOT = -19.4 # [STEP] idler hub bottom face = case bottom plane
SERVO_DRIVE_SQ = 9.9    # [STEP] 4x M2.5 drive holes on a 9.9 x 9.9 square
SERVO_DRIVE_SCREW = CLEAR_HOLE_M2_5
SERVO_HORN_BOSS_DIA = 9.0   # [STEP] centre boss under horn - keep clear
SERVO_TAB_X = -20.7     # [STEP] rear mounting tab hole centre (x)
SERVO_TAB_Y = 10.4      # [STEP] rear tab hole centre (+/-y)
SERVO_TAB_HOLE = 4.0    # [STEP] rear tab through-hole dia
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
