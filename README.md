# XYZ2B - Fish XYZ to Behaviour


A set of python scripts that infer freezing (FREEZE) and erratic movements (EM) behaviour from X, Y, Z data produced by the Ethovision (R) Tracking Software (ETS).

## Installation

### Requirements

To use the scripts you will need to have the following requirements installed in your computer:

#### Python 2.7.*

Download and install `Python` from [here](https://www.python.org/download/).

#### XLRD

Download and install the `XLRD` package from [here](https://pypi.python.org/pypi/xlrd/0.7.9).

#### NumPy

Download and install the `NumPy` package from [here](http://www.scipy.org/scipylib/download.html).

#### Matplotlib

Download and install the `Matplotlib` package from [here](http://matplotlib.org/downloads.html).


### The Scripts

You can find the `XYZ2B` scripts and docs from the [GitHub page]() of the project.

1. Click in the download box at the right side of the page to download de files.

2. Unzip the files to some directory in your computer.

3. Open a terminal window (if you don't known what a terminal window is check it [here](http://www.makeuseof.com/tag/a-beginners-guide-to-the-windows-command-line/)).

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

All data should be in excel files exactly as produced by ETS and all files should be organized in a directory structure like this:

    /<experiment directory>
        /<config>.py
        /<data directory>
            /<assay_1>_side.xls
            /<assay_1>_top.xls
            /<assay_2>_side.xls
            /<assay_2>_top.xls
            /<assay_3>_side.xls
            /<assay_3>_top.xls

**Important**

1. Files must finish with "_side.xls" or "_side.xls".

2. Files of the same assay must have the same prefix:

    `Exp1_T2_side.xls`
    `Exp2_T2_side.xls`
     

After running the script with the appropriate parameters (see bellow __Running the Script__) it will generate in the `/<data directory>` the following files for each assay:

    <assay_N>.txt    - A textual version of the Excel data.
    <assay_N>.sub    - The subtitles for the respective video.
    <assay_N>.report - A textual report with the FREEZE and EM windows.


### Running the Stript

To generate the FRZ and EM annotations do:

1) Create a configuration file for your experiment (an experiment is a set of assays that will be processed toghether). Use the `example_cfg.py` as an example. See __Configuring the Script__ for more info about configuration.

2) Run the script:

    python2.7 xyz2b.py <config file>

If no errors occurred check the directory specified by the `DATA_DIR` variable for results.


### Configuring the Script

The configurations for each experiment can be put all toghther in the same file. To create the configuration for a given expriment start by copying the example file `cfg_example.py` to another file (ex: `exp1.py`) and edit the new file accordingly. The available configurations are:

    DATA_DIR = "<path>"         # Full path of the top level directory containing the assay data.

    FORCE_XLS_TO_TXT = False    # Forces the Excel files to be read.

    WIN_SMOOTH_SIZE = 25        # Size of the X, Y, Z smooth window in frames.
    WIN_VELOCITY_SIZE = 125     # Size of the velocity smooth window in frames.
    WIN_CHANGE_DIR_SIZE = 10    # Size of the direction changes smooth window in frames (not used).

    THRES_V = 0.2               # Velocity threshold for Freezing decision.
    THRES_Y = 0.25              # Y position threshold for Freezing decision.
    THRESHOLD_DC = 5            # Direction change threshold for erratic movement decision (not used).
    THRESHOLD_A = 8             # Acceleration threshold for erratic movement decision.


### Decision Criteria

The script computes the following variables from the position (X, Y, Z) raw data:

    Velocity (top and side)- Computed as the instantaneous velocity over the smoothed position data, and then smoothed again.
    Acceleration (top and side)- Computed as the instantaneous acceleration over the instantaneous velocity data (DV/DT, pre-smooth), and then smoothed again.

It decides if the fish is freezed if both conditions apply:

    Velocity < THRES_V  (both top and side)
    Y position < THRES_Y (in percentage of the full range of Y positions observed)

It decides if the fish is in erratic movement if both conditions apply:

    Acceleration > THRESHOLD_A (both top and side)

