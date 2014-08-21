import os

import numpy as np
import matplotlib.pyplot as plt

import compute
import utils

DATA_DIR = "/home/jcruz/Desktop/5-RESEARCH/20140314-work-fish_behaviour/faustino/data"
FORCE_XLS_TO_TXT = False

files = utils.list_excel(DATA_DIR)

for name_xls in files:
    print name_xls

    # get the names of the result files
    name_txt = name_xls.replace(".xlsx", ".txt")
    name_sub = name_xls.replace(".xlsx", ".sub")

    # convert from Excel to text
    if FORCE_XLS_TO_TXT or (not os.path.isfile(name_txt)):
        utils.excel_to_txt(name_xls, name_txt)

    # get the data from the text file
    data = np.array(utils.read_txt(name_txt))

    # round the data to clean um some noise
    data = np.round(np.array(utils.read_txt(name_txt)), 2)

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
    (fs, es) = compute.decide(T, veloc, data[:, 2], dchanges)

    fsub = open(name_sub, "w")
    (lf, le) = (-1, -1)
    for (t, f, e) in zip(data[:, 0], fs, es):
        if f != lf or e != le:
            (lf, le) = (f, e)
            fsub.write("%f, %d, %d\n" % (t, f, e))
    fsub.close()

    plt.figure(1)
    plt.subplot(4, 1, 1)
    plt.plot(T, data[:, 1])     # Y

    plt.subplot(4, 1, 2)
    plt.plot(T, veloc, 'r')     # veloc
    plt.axhline(0.1)

    THRES = 7.5
    plt.subplot(4, 1, 3)
    plt.axhline(THRES)
    plt.plot(T, accel)          # accel
    plt.plot(T, es * THRES, 'r')
    plt.plot(T, fs * THRES, 'g')

    #plt.plot(np.ones(veloc.shape[0])*4)
    #plt.plot(np.ones(veloc.shape[0])*1)

    plt.subplot(4, 1, 4)

    plt.plot(T, dchanges[:, 0])
    plt.axhline(5)

    #plt.plot(accel[:, 1])
    plt.show()


