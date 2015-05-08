#!/usr/bin/env python

import os
import sys

import numpy as np
import matplotlib.pyplot as plt

import compute
import utils


if len(sys.argv) != 2:
    print "\nUsage:\n\t%s <cfg_file>\n" % os.path.basename(sys.argv[0])
    quit()

cfg_file = sys.argv[1] + (".py" if not sys.argv[1].endswith(".py") else "")

if not os.path.isfile(cfg_file):
    print "\nError: File '%s' not found!." % cfg_file
    quit()

#
# default config
#
ORIG_DIR = None
DATA_DIR = "."
FORCE_XLS_TO_TXT = False
WIN_SMOOTH_SIZE = 25
WIN_VELOCITY_SIZE = 125
WIN_CHANGE_DIR_SIZE = 10
THRES_V = 0.2
THRES_Y = 0.25
THRESHOLD_DC = 5
THRESHOLD_A = 8
BIN_SIZE = None
SHOW_3D = False

XLIMS = None
YLIMS = None
ZLIMS = None

# execute the configuration data
exec open(cfg_file).read()

# colect original files
utils.collect_excel(ORIG_DIR, DATA_DIR)

# colect prepared data files
files = utils.list_excel(DATA_DIR)

# check for all pair of files "side"/"top"
fpairs = {}

if len(files) == 0:
    print "Nothing todo in '%s'" % DATA_DIR
    quit()

for name_xls in files:
    # get the names of the result files
    name_txt = name_xls.replace(".xlsx", ".txt")

    # convert from Excel to text
    if FORCE_XLS_TO_TXT or (not os.path.isfile(name_txt)):
        utils.excel_to_txt(name_xls, name_txt)

    # pair the top and side files
    key = os.path.basename(name_txt).replace("_side.txt", "").replace("_top.txt", "")

    if key not in fpairs.keys():
        fpairs[key] = []

    fpairs[key].append(name_txt)

bins_list = {}

for (key, files) in fpairs.items():
    if len(files) != 2:
        print "Missing file ('top' or 'side') in pair for assay '%s'" % key
        continue

    print "*****\n%s\n*****" % key

    name_sub = "%s/%s.sub" % (DATA_DIR, key)
    name_rep = "%s/%s.report" % (DATA_DIR, key)

    (trim_start, trim_end) = (None, None)
    for ftxt in files:
        # round the data to clean um some noise
        data = np.round(np.array(utils.read_txt(ftxt)), 2)

        # trim the initial and final NaN values
        (start, end) = compute.trim3(data)

        trim_start = start if (trim_start < start or trim_start is None) else trim_start
        trim_end   = end if (trim_end > end or trim_end is None) else trim_end

        # interpolate some NaN values
        compute.interpolate3(data, start, end)

        if "_side" in ftxt:
            data_s = data
        elif "_top" in ftxt:
            data_t = data

    print "TRIM: ", trim_start, trim_end, trim_end-trim_start
    data_s = data_s[trim_start:trim_end, :]
    data_t = data_t[trim_start:trim_end, :]

    # smooth the position data
    data_s[:, 1] = compute.smooth(data_s[:, 1], win_size=WIN_SMOOTH_SIZE)
    data_s[:, 2] = compute.smooth(data_s[:, 2], win_size=WIN_SMOOTH_SIZE)

    # smooth the position data
    data_t[:, 1] = compute.smooth(data_t[:, 1], win_size=WIN_SMOOTH_SIZE)
    data_t[:, 2] = compute.smooth(data_t[:, 2], win_size=WIN_SMOOTH_SIZE)

    # get the time variable to use in the future
    T = data_s[:, 0]

    # compute speed and acceleration
    (veloc_s, accel_s) = compute.velocity(data_s, win_size=WIN_VELOCITY_SIZE)
    (veloc_t, accel_t) = compute.velocity(data_t, win_size=WIN_VELOCITY_SIZE)

    # dchanges = compute.dir_changesX2(data, win_size=100)
    dchanges_s = compute.dir_changesX3(data_s, win_size=WIN_CHANGE_DIR_SIZE)
    dchanges_t = compute.dir_changesX3(data_t, win_size=WIN_CHANGE_DIR_SIZE)

    (fs, es, thy, thv, tha, thdc) = compute.decide3(T, data_s[:, 2], veloc_s, veloc_t, accel_s, accel_t, dchanges_s, THRES_V, THRES_Y, THRESHOLD_DC, THRESHOLD_A)

    intervals = compute.interval_list(fs, es, T)
    compute.subtitle(intervals, name_sub)
    bins = compute.report(fs, es, data_s, 0, name_rep, BIN_SIZE)
    bins_list[key] = bins

    if SHOW_3D:
        utils.plot3d(data_t[:, 1], data_t[:, 2], data_s[:, 2], fs, es, XLIMS, YLIMS, ZLIMS)

    plt.figure(1)
    plt.subplot(5, 1, 1)
    plt.plot(T, data_s[:, 1], 'b')     # X
    plt.plot(T, -data_t[:, 1], 'g')    # X

    plt.subplot(5, 1, 2)
    plt.plot(T, data_s[:, 2])     # Y
    plt.axhline(thy)

    plt.subplot(5, 1, 3)
    plt.plot(T, veloc_s, 'b')          # veloc
    plt.plot(T, veloc_t, 'g')          # veloc
    plt.plot(T, fs * 2, 'r')
    plt.axhline(thv)

    plt.subplot(5, 1, 4)
    plt.plot(T, accel_s, 'b')          # accel
    plt.plot(T, accel_t, 'g')          # accel
    plt.plot(T, es * 10, 'r')
    plt.axhline(tha)

    plt.subplot(5, 1, 5)

    plt.plot(T, dchanges_s[:, 0], 'b')
    plt.plot(T, dchanges_t[:, 0], 'g')
    plt.axhline(thdc)

    plt.show()

name_summary = "%s/summary.report" % DATA_DIR
compute.summary(bins_list, name_summary)
