# Full path of the top level directory containing the assay data
DATA_DIR = "/home/jcruz/Desktop/5-RESEARCH/20140314-work-fish_behaviour/faustino/data"

FORCE_XLS_TO_TXT = False    # Forces the Excel files to be read

WIN_SMOOTH_SIZE = 25        # Size of the X, Y, Z smooth window in frames.
WIN_VELOCITY_SIZE = 125     # Size of the velocity smooth window in frames.
WIN_CHANGE_DIR_SIZE = 10    # Size of the direction changes smooth window in frames (not used).

THRES_V = 0.2               # Velocity threshold for Freezing decision.
THRES_Y = 0.25              # Y position threshold for Freezing decision.
THRESHOLD_DC = 5            # Direction change threshold for erratic movement decision (not used).
THRESHOLD_A = 8             # Acceleration threshold for erratic movement decision.

