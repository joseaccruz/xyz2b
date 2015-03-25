# Kalman filter example demo in Python

# A Python implementation of the example given in pages 11-15 of "An
# Introduction to the Kalman Filter" by Greg Welch and Gary Bishop,
# University of North Carolina at Chapel Hill, Department of Computer
# Science, TR 95-041,
# http://www.cs.unc.edu/~welch/kalman/kalmanIntro.html

# by Andrew D. Straw

import numpy as np
from scipy.ndimage.filters import gaussian_filter

from utils import *


def trim(data, ndx_col):
    (ndx_start, ndx_end) = (0, data.shape[0])

    for i in xrange(data.shape[0]):
        if not np.isnan(data[i, ndx_col]):
            break
        ndx_start += 1

    for i in xrange(data.shape[0]-1, 0, -1):
        if not np.isnan(data[i, ndx_col]):
            break
        ndx_end -= 1

    if (ndx_start > 0) or (ndx_end < data.shape[0]):
        print "TRIM>", ndx_start, ndx_end
        data = data[ndx_start:ndx_end, :]

    return data


def trim3(data):
    (ndx_start, ndx_end) = (0, data.shape[0])

    # get the first not NaN
    for i in xrange(data.shape[0]):
        if (not np.isnan(data[i, 1])) and (not np.isnan(data[i, 2])):
            break
        ndx_start += 1

    # get the last not NaN
    for i in xrange(data.shape[0]-1, 0, -1):
        if (not np.isnan(data[i, 1])) and (not np.isnan(data[i, 2])):
            break
        ndx_end -= 1

    # shall we trim?
    if (ndx_start > 0) or (ndx_end < data.shape[0]):
        print "TRIM>", ndx_start, ndx_end

    return (ndx_start, ndx_end)


def interpolate(data, ndx_col):
    ndx_row = None

    for i in xrange(data.shape[0]):
        # entering a NaN window
        if np.isnan(data[i, ndx_col]) and (ndx_row is None):
            ndx_row = i - 1

        # leaving a NaN window
        if (not np.isnan(data[i, ndx_col])) and (not ndx_row is None):
            data[ndx_row+1:i, ndx_col] = np.linspace(data[ndx_row, ndx_col], data[i, ndx_col], i-ndx_row+1)[1:-1]
            ndx_row = None


def interpolate3(data, start, end):
    ndx_row = None

    for ndx_col in (1, 2):
        count = 0
        for i in xrange(start, end):
            # entering a NaN window
            if np.isnan(data[i, ndx_col]) and (ndx_row is None):
                ndx_row = i - 1

            # leaving a NaN window
            if (not np.isnan(data[i, ndx_col])) and (not ndx_row is None):
                count = i - ndx_row - 1
                data[ndx_row+1:i, ndx_col] = np.linspace(data[ndx_row, ndx_col], data[i, ndx_col], i-ndx_row+1)[1:-1]
                ndx_row = None

        print "INTERPOLATE: ", count


def diffn(A, n):
    return np.hstack((np.zeros(n), A[n:] - A[:-n]))


def smooth(data, win_size, kernel="avg"):
    # kernel == "abs"
    KERNEL = np.ones(win_size)

    if kernel == "avg":
        KERNEL = KERNEL / win_size

    return np.convolve(data, KERNEL, "same")


def smooth_gaussian(data, sigma):
    return gaussian_filter(data, sigma, mode='mirror')


def interval_list(freeze, erratic, T):
    ret = []

    start = 0
    state_old = (freeze[0], erratic[0])

    for i in xrange(T.shape[0]):
        state = (freeze[i], erratic[i])

        if (state_old != state) or ((i+1) == T.shape[0]):
            ret.append((T[start], T[i-1], state_old))
            start = i

        state_old = state

    return ret


def subtitle(intervals, fname):
    fo = open(fname, "w")

    for (i, (start, end, (f, e))) in enumerate(intervals):

        s = "%s %s" % ("FRZ" if f else "---", "ERR" if e else "---")

        fo.write("%d\n" % i)
        fo.write("%s --> %s\n" % (seconds2time(start), seconds2time(end)))
        fo.write("%s\n\n" % s)

    fo.close()


def report(freeze, erratic, data, ndx_col, fname, bsize=None):
    # compute event list
    events = []
    (fstart, estart) = (None, None)
    (ftotal, etotal) = (0, 0)

    for i in xrange(len(data)):
        t = data[i, ndx_col]

        if freeze[i] and fstart is None:
            fstart = t
        if not freeze[i] and (fstart is not None):
            events.append(('freeze', fstart, t))
            ftotal += (t-fstart)
            fstart = None
        if erratic[i] and estart is None:
            estart = t
        if not erratic[i] and (estart is not None):
            events.append(('erratic', estart, t))
            etotal += (t-estart)
            estart = None

    events.sort(key=lambda x: x[1])

    # compute bins
    if bsize is not None:
        bcount = int(t / bsize) + 1
        bins = {'freeze': [0] * bcount, 'erratic': [0] * bcount}

        for i in xrange(bcount):
            (bstart, bend) = (i*bsize, (i+1)*bsize)

            for (evt, estart, eend) in events:
                bins[evt][i] += max(min(bend, eend) - max(bstart, estart), 0)
    else:
        bins = None

    # write event list
    fo = open(fname, "w")

    fo.write("Totals\n------\n")
    fo.write("Event\tTotal (s)\tTotal\n")
    fo.write("freeze \t%8.2f\t%s\n" % (ftotal, seconds2time(ftotal)))
    fo.write("erratic\t%8.2f\t%s\n" % (etotal, seconds2time(etotal)))

    if bsize is not None:
        fo.write("\nTotals bins (bin length=%s s)\n------\n" % bsize)
        fo.write("Event\tBin\tTotal (s)\tTotal\n")

        for (k, v) in bins.items():
            for (i, t) in enumerate(v):
                fo.write("%-7s\t%3d\t%8.2f\t%s\n" % (k, i, t, seconds2time(t)))

    fo.write("\nEvents\n------\n")
    fo.write("Name\tStart\tStop\tTotal\tStart (s)\tStop (s)\tTotal (s)\n")

    for (evt, start, end) in events:
        fo.write("%-7s\t%s\t%s\t%s\t%8.2f\t%8.2f\t%8.2f\n" % (evt, seconds2time(start), seconds2time(end), seconds2time(end-start), start, end, end-start))

    fo.close()

    return bins


def summary(bins_list, fname):
    header = True

    fo = open(fname, "w")

    for k1 in sorted(bins_list.keys()):
        bins = bins_list[k1]

        if header:
            for k2 in sorted(bins.keys()):
                v = bins[k2]
                for (j, t) in enumerate(v):
                    fo.write("\t%s_%d" % (k2, j))
            fo.write("\n")
            header = False

        fo.write("%s" % k1)

        for k2 in sorted(bins.keys()):
            v = bins[k2]
            for (j, t) in enumerate(v):
                fo.write("\t%8.2f (%s)" % (t, seconds2time(t)))
        fo.write("\n")

    fo.close()

#
# Compute the mean velocity
#
def velocity(data, win_size=0):
    T = data[:, 0]

    # compute distances
    DT = diffn(T, 1)
    DX = diffn(data[:, 1], 1)
    DY = diffn(data[:, 2], 1)
    D = np.sqrt(DX**2 + DY**2)
    #D = np.abs(DX)

    # compute the velocity
    V = D / DT

    # compute the acceleration
    DV = diffn(V, 1)
    A = np.abs(DV / DT)

    # compute the mean velocity and acceleration
    if win_size > 0:
        V = smooth(V, win_size)
        A = smooth(A, win_size)

    V.shape = (len(V), 1)
    A.shape = (len(A), 1)

    return (V, A)


def acceleration(data, win_size=0):
    T = data[:, 0]
    # compute velocity
    V = diffn(data[:, 1], 1)

    # compute the velocity diffs
    DT = diffn(T, 1)
    DV = diffn(V, 1)

    # compute the aceleration
    A = np.abs(DV / DT)

    if win_size > 0:
        A = smooth(A, win_size)

    T.shape = (len(T), 1)
    A.shape = (len(A), 1)

    return np.concatenate((T, A), axis=1)


def dir_changesX(data, win_size):
    T = data[:, 0]
    DX = diffn(data[:, 1], 1)

    DX[np.abs(DX) < 0.01] = 0

    DDX = np.hstack(([1], np.sign(DX[1:] * DX[:-1])))
    DC = np.convolve(((DDX-1)*DDX)/2, np.ones(win_size), "same")

    T.shape = (len(T), 1)
    DC.shape = (len(T), 1)

    return np.concatenate((T, DC), axis=1)


def dir_changesX2(data, win_size):
    T = data[:, 0]
    DX = np.abs(diffn(data[:, 1], 1))
    R = np.zeros(len(DX))

    ndx = 0
    accum = 0.0
    last_diff = 0
    for i in xrange(len(DX)):
        accum += DX[i]

        if accum > 0.5:
            diff = data[i, 1] - data[ndx, 1]

            if (diff * last_diff) < 0:
                R[i] = 1

            ndx = i
            accum = 0
            last_diff = diff

    R = np.convolve(R, np.ones(win_size), "same")

    T.shape = (len(T), 1)
    R.shape = (len(T), 1)

    return np.concatenate((T, R), axis=1)


def dir_changesX3(data, win_size):
    THRESHOLD = 1

    X = data[:, 1]

    sc = np.zeros(len(X))
    dds = np.zeros(len(X))

    last_signal = 0
    max_win = 0

    for i in xrange(len(X)):
        s = max(0, i-win_size)
        e = min(len(X)-1, i+win_size)

        dds[i] = X[s] - X[e]

        max_win = max(max_win, np.abs(dds[i]))

        # changed signal?
        if np.sign(dds[i]) != np.sign(last_signal):
            if max_win > THRESHOLD:
                sc[i] = 1
                max_win = 0
                last_signal = np.sign(dds[i])
            else:
                last_signal = 0

    R = smooth(sc, 240, "abs")
    R.shape = (len(X), 1)

    """
    import matplotlib.pyplot as plt
    plt.plot(T, X)
    plt.plot(T, sc)
    plt.plot(T, dds)
    plt.plot(T, R)
    plt.axhline(0)
    plt.axhline(5)
    plt.axhline(0.5)
    plt.axhline(-0.5)
    plt.show()
    """

    return R


def kalman_window(win):
    n_iter = len(win)

    Q = 1e-5    # process variance
    R = 0.1**2                   # estimate of measurement variance, change to see effect

    # intial guesses
    xhat = np.mean(win)
    P = 1.0

    for k in range(1, n_iter):
        # time update
        xhatminus = xhat
        Pminus = P + Q

        # measurement update
        K = Pminus / (Pminus + R)
        xhat = xhatminus + K * (win[k] - xhatminus)
        P = (1 - K) * Pminus

    # the last estimate
    return xhat


def kalman(data, win_size):
    ret = np.zeros((len(data), 3))

    for i in xrange(0, len(data) - win_size):
        kx = kalman_window(data[i:i+win_size, 1])
        ky = kalman_window(data[i:i+win_size, 2])

        ret[i+int(win_size/2), :] = [data[i+int(win_size/2), 0], kx, ky]

    return ret


def decide(T, V, Y, DC):
    THRESHOLD_V = 0.15
    THRESHOLD_Y = np.min(Y) + ((np.max(Y) - np.min(Y)) * 0.25)  # 25% of the range
    THRESHOLD_DC = 5

    freezes = np.zeros(len(V))
    (freeze_state, freeze_t0) = (False, None)

    erratics = np.zeros(len(V))
    (erratic_state, erratic_t0) = (False, 0)

    for (i, (t, v, y, dc)) in enumerate(zip(T, V, Y, DC)):
        if v < THRESHOLD_V and y < THRESHOLD_Y:
            if not freeze_state:
                if not freeze_t0:
                    freeze_t0 = t

                if (t-freeze_t0) > 2.0:
                    (freeze_state, freeze_t0) = (True, None)

        else:
            if freeze_state:
                if not freeze_t0:
                    freeze_t0 = t

                if (t-freeze_t0) > 0.25:
                    (freeze_state, freeze_t0) = (False, None)

        freezes[i] = 1 if freeze_state else 0

        if dc >= THRESHOLD_DC:
            if not erratic_state:
                if not erratic_t0:
                    erratic_t0 = t

                if (t-erratic_t0) > 2.0:
                    (erratic_state, erratic_t0) = (True, None)

        else:
            if erratic_state:
                if not erratic_t0:
                    erratic_t0 = t

                if (t-erratic_t0) > 1.0:
                    (erratic_state, erratic_t0) = (False, None)

        erratics[i] = 1 if erratic_state else 0

    return (freezes, erratics)


def decide2(T, V, Y, A, DC):
    # decision limits for freezing
    THRESHOLD_V = 0.15
    THRESHOLD_Y = np.min(Y) + ((np.max(Y) - np.min(Y)) * 0.25)  # 10% of the range

    # decision limits for erratic movement
    THRESHOLD_DC = 5
    THRESHOLD_A = 7.5

    freeze = np.ones(len(V))
    freeze[V[:, 0] > THRESHOLD_V] = 0
    freeze[Y > THRESHOLD_Y] = 0

    erratic = np.ones(len(V))
    erratic[A[:, 0] < THRESHOLD_A] = 0
    erratic[DC[:, 0] < THRESHOLD_DC] = 0

    return (freeze, erratic)


def decide3(T, YS, VS, VT, AS, AT, DCS, thrs_v, thrs_y, thrs_dc, thrs_a):
    # decision limits for freezing
    THRESHOLD_Y = np.min(YS) + ((np.max(YS) - np.min(YS)) * thrs_y)  # 25% of the range

    # decision limits for erratic movement
    freeze = np.ones(len(VS))
    freeze[VS[:, 0] > thrs_v] = 0
    freeze[VT[:, 0] > thrs_v] = 0
    freeze[YS > THRESHOLD_Y] = 0

    erratic = np.ones(len(VS))
    erratic[AS[:, 0] < thrs_a] = 0
    erratic[AT[:, 0] < thrs_a] = 0
    #erratic[DC[:, 0] < thrs_dc] = 0

    return (freeze, erratic, THRESHOLD_Y, thrs_v, thrs_a, thrs_dc)
