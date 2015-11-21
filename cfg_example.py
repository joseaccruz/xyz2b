# Full path of the top level directory containing the assay data

ORIG_DIR = "/home/jcruz/Desktop/5-RESEARCH/20140314-work-fish_behaviour/faustino/exp3/original"
DATA_DIR = "/home/jcruz/Desktop/5-RESEARCH/20140314-work-fish_behaviour/faustino/exp1"

FORCE_XLS_TO_TXT = False    # Forces the Excel files to be read

WIN_SMOOTH_SIZE = 25        # Size of the X, Y, Z smooth window in frames.
WIN_VELOCITY_SIZE = 125     # Size of the velocity smooth window in frames.
WIN_CHANGE_DIR_SIZE = 10    # Size of the direction changes smooth window in frames (not used).

THRES_V = 0.2               # Velocity threshold for Freezing decision.
THRES_Y = 0.25              # Y position threshold for Freezing decision.
THRESHOLD_DC = 5            # Direction change threshold for erratic movement decision (not used).
THRESHOLD_A = 8             # Acceleration threshold for erratic movement decision.

BIN_SIZE = 150              # Bin size in seconds.

SHOW_3D = True

XLIMS = (0, 10.5)
YLIMS = (0, 10.5)
ZLIMS = (0, 11)

FIG_FORMAT = "svg"          # picture format (.png, .svg)
FIG_DPI = 300               # picture resolution in dots per inch

FIG3D = {"elev": 27, "azim": 133}   # orientation of the 3D plot

FIG3D_NORMAL  = {"linestyle": "-", "linewidth": 0.5, "color": "g"}          # 'normal' behaviour settings
FIG3D_ERRATIC = {"linestyle": "-", "linewidth": 1.5, "color": "orange"}     # 'erratic' behaviour settings
FIG3D_FREEZE  = {"size": 150, "color": "r"}                                 # 'freeze' behaviour settings
