# XYZ2B - Fish XYZ to Behaviour

A set of python scripts that infer freezing (FREEZE) and erratic movement (EM) behaviour from X, Y, Z data produced by the Ethovision (R) Tracking Software (ETS).

## Installation

### Requirements

To use the scripts you will need to have the following requirements installed in your computer:

#### Python 2.7.*

Download and install `Python` from [here](https://www.python.org/download/).

#### XLRD

Download and install the `XLRD` package from [here](https://pypi.python.org/pypi/xlrd/0.7.9).

#### NumPy and SciPy

Download and install the `NumPy` and `SciPy` packages from [here](http://www.scipy.org/scipylib/download.html).

#### Matplotlib

Download and install the `Matplotlib` package from [here](http://matplotlib.org/downloads.html).


### The Scripts

You can find the `XYZ2B` scripts and docs from the [GitHub page](https://github.com/joseaccruz/xyz2b) of the project.

1. Click in the download box at the right side of the page to download the files.

2. Unzip the files to some directory in your computer.

3. Open a terminal window (if you don't known what a terminal window is check it [here](http://www.makeuseof.com/tag/a-beginners-guide-to-the-windows-command-line/).

4. Change the directory to the one where you downloaded the scripts:

    `cd <your-dir-name>`

5. Type something like:

    `python xyz2b.py`
    
    or
    
    `python2.7 xyz2b.py`
    
    If you got a nice help message it is working!


## How to use


### Intro

The script expects, for each assay, the following data:

1. One file with the (X, Z) coordinates obtained by a side view camera ("side" data).

2. A file with the (X, Y) coordinates obtained by a top view camera ("top" data).

All data should be in excel files exactly as produced by ETS.

Files can be automatically collected from the original directories to the final data processing directory.

**Important**

1. Files must have the experiment name in the 'A10' cell.

2. The experiment name must end with either `_side` or `_top`.

3. The experiment names corresponding to the same subject must have the same prefix:

    `Exp1_T2_side`
    `Exp1_T2_top`

    `Exp2_T2_side`
    `Exp2_T2_top`
     

After running the script with the appropriate parameters (see bellow __Running the Script__) it will generate in the `/<data directory>` the following files for each assay:

    <subject_N>.txt    - A textual version of the Excel data.
    <subject_N>.sub    - The subtitles for the respective video.
    <subject_N>.report - A textual report with the FREEZE and EM windows.
    summary.report   - A textual report with the summary of all subjects (should be easily copied to Excel).
    <subject_N_fig1>.svg    - A scalable vector graphics file with the graphical thresholds for FREEZE and EM.
    <subject_N_fig2>.svg    - A scalable vector graphics file with the 3D plot for FREEZE and EM visualization.


### Running the Script

To generate the FRZ and EM annotations do:

1) Create a configuration file for your experiment (an experiment is a set of assays that will be processed toghether). Use the `example_cfg.py` as an example. See __Configuring the Script__ for more info about configuration.

2) Run the script:

    python2.7 xyz2b.py <config file>

If no errors occurred check the directory specified by the `DATA_DIR` variable for results.


### Configuring the Script

To create the configuration for a given experiment start by copying the example file `cfg_example.py` to another file (ex: `exp1.py`) and edit the new file. The available configurations are:

    ORIG_DIR = "<path>"         # Full path of the original raw data Excel files as produced by the ETS.

    DATA_DIR = "<path>"         # Full path of the data directory which will contain the renamed raw data files, the processed subject data files and the report results.

    FORCE_XLS_TO_TXT = False    # Forces the Excel files to be (re)read.

    WIN_SMOOTH_SIZE = 25        # Size of the X, Y, Z smooth window in frames.
    WIN_VELOCITY_SIZE = 125     # Size of the velocity smooth window in frames.
    WIN_CHANGE_DIR_SIZE = 10    # Size of the direction changes smooth window in frames (not used).

    THRES_V = 0.2               # Velocity threshold for Freezing decision.
    THRES_Y = 0.25              # Y position threshold for Freezing decision.
    THRESHOLD_DC = 5            # Direction change threshold for erratic movement decision (not used).
    THRESHOLD_A = 8             # Acceleration threshold for erratic movement decision.

    BIN_SIZE = 300              # Time bin length in seconds.
    
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


### Decision Criteria

The script computes the following variables from the position (X, Y, Z) raw data:

    Velocity (top and side) - Computed as the instantaneous velocity over the smoothed position data, and then smoothed again.
    Acceleration (top and side) - Computed as the instantaneous acceleration over the instantaneous velocity data (DV/DT, pre-smooth), and then smoothed again.

It decides if the fish is in freezing if both conditions apply:

    Velocity < THRES_V (both top and side)
    Y position < THRES_Y (in percentage of the full range of Y positions registered)

It decides if the fish is in erratic movement if one condition applies:

    Acceleration > THRESHOLD_A (both top and side)

