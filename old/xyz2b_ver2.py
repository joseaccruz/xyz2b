import os

import numpy as np
import matplotlib.pyplot as plt

import compute
import utils

DATA_DIR = "/home/jcruz/Desktop/5-RESEARCH/20140314-work-fish_behaviour/faustino/data/side"
FORCE_XLS_TO_TXT = False

files = utils.list_excel(DATA_DIR)

for name_xls in files:
    print name_xls

    # get the names of the result files
    name_txt = name_xls.replace(".xlsx", ".txt")
    name_sub = name_xls.replace(".xlsx", ".sub")
    name_rep = name_xls.replace(".xlsx", ".report")

    # convert from Excel to text
    if FORCE_XLS_TO_TXT or (not os.path.isfile(name_txt)):
        utils.excel_to_txt(name_xls, name_txt)

    # get the data from the text file
    data = np.array(utils.read_txt(name_txt))

    # round the data to clean um some noise
    data = np.round(np.array(utils.read_txt(name_txt)), 2)

    # trim the initial and final NaN values
    data = compute.trim(data, 1)
    data = compute.trim(data, 2)

    # interpolate some NaN values
    compute.interpolate(data, 1)
    compute.interpolate(data, 2)

    # smooth the position data
    data_smooth = data
    data_smooth[:, 1] = compute.smooth(data[:, 1], win_size=25)
    data_smooth[:, 2] = compute.smooth(data[:, 2], win_size=25)

    # get the time variable to use in the future
    T = data[:, 0]

    # compute speed and acceleration
    (veloc, accel) = compute.velocity(data_smooth, win_size=125)

    #dchanges = compute.dir_changesX2(data, win_size=100)
    dchanges = compute.dir_changesX3(data, win_size=10)

    #(fs, es) = compute.decide(data, veloc, accel, dchanges)
    (fs, es) = compute.decide2(T, veloc, data[:, 2], accel, dchanges)

    intervals = compute.interval_list(fs, es, data, 0)
    compute.subtitle(intervals, name_sub)
    compute.report(fs, es, data, 0, name_rep)

    plt.figure(1)
    plt.subplot(5, 1, 1)
    plt.plot(T, data[:, 1])     # X

    plt.subplot(5, 1, 2)
    plt.plot(T, data[:, 2])     # Y

    plt.subplot(5, 1, 3)
    plt.plot(T, veloc, 'r')     # veloc
    plt.axhline(0.1)

    THRES = 7.5
    plt.subplot(5, 1, 4)
    plt.axhline(THRES)
    plt.plot(T, accel)          # accel
    plt.plot(T, es * THRES, 'r')
    plt.plot(T, fs * THRES, 'g')

    #plt.plot(np.ones(veloc.shape[0])*4)
    #plt.plot(np.ones(veloc.shape[0])*1)

    plt.subplot(5, 1, 5)

    plt.plot(T, dchanges[:, 0])
    plt.axhline(5)

    #plt.plot(accel[:, 1])
    plt.show()


