import json
import os
import shutil

import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

import xlrd


#
# given a directory takes all excel files on it
#
def list_excel(dir, recursive=True):
    ret = []

    for (root, dirs, files) in os.walk(dir, topdown=False):
        # print root, dirs, files
        for name in filter(lambda f: f.endswith(".xlsx"), files):
            ret.append(os.path.join(root, name))

        if recursive:
            for name in dirs:
                ret += list_excel(name, recursive=True)

    return sorted(ret)


#
# given a directory list all excel files found in all subdirectories
#
def collect_excel(dir_orig, dir_data, recursive=True):
    print "Collecting files from original directory: '%s'" % dir_orig

    orig_cache_name = "%s/cache.dat" % dir_data

    if os.path.isfile(orig_cache_name):
        orig_cache = json.loads(open(orig_cache_name).read())
    else:
        orig_cache = []

    for f in list_excel(dir_orig):
        # 1. check if the file was collected
        if f not in orig_cache:
            orig_cache.append(f)

            # 2. open the Excel file and search for a suitable name
            wb = xlrd.open_workbook(f)
            ws = wb.sheet_by_index(0)
            name = str(ws.row(9)[1].value).lower()
            print name

            # 3. decide if the name is ok
            if name.endswith("_side") or name.endswith("_top"):
                target = "%s/%s.xlsx" % (dir_data, name)

                # 4. copy the file with the new name to the final directory
                print "Copying file '%s' to '%s'" % (f, target)
                shutil.copyfile(f, target)
            else:
                print "Missing '_side', '_top' in cell A10 of file %s (found '%s')!" % (f, name)

    open(orig_cache_name, "w").write(json.dumps(orig_cache))


#
# given an excel file extracts the raw data to a text easy to read file
#
def excel_to_txt(input, output):
    wb = xlrd.open_workbook(input)
    ws = wb.sheet_by_index(0)

    nrows = ws.nrows - 1
    row = int(ws.row(0)[1].value)

    fo = open(output, "w")

    while row < nrows:
        data = ws.row(row)

        (t, x, y) = (data[0].value, data[2].value, data[3].value)

        if (x == "-") or (y == "-"):
            (x, y) = ("NaN", "NaN")

        fo.write("%s,%s,%s\n" % (t, x, y))

        row += 1

    fo.close()


def read_txt(input):
    return map(lambda x: map(float, x.strip().split(",")), open(input) .read().strip().split("\n"))


def seconds2time(t):
    ti = int(t)

    h = int(ti / 3600)
    m = int(ti % 3600 / 60)
    s = int(ti % 60)

    return("%02d:%02d:%02d.%02.0f" % (h, m, s, int((t - ti) * 100)))


def plot3d(x, y, z, f, e, xl, yl, zl, fname=None, fdpi=None, style={}, style_normal={}, style_erratic={}, style_freeze={}):
    fs = []
    fsizes = []
    (start, out) = (None, True)

    for (i, n) in enumerate(f):
        if (n > 0) and out:
            (start, out) = (i, False)

        if (n < 1.0) and (not out):
            tmp = np.zeros(len(f))
            tmp[start + (i - start) / 2] = 1.0

            fs.append(tmp)
            fsizes.append((i - start))

            (start, out) = (None, True)

    mpl.rcParams['legend.fontsize'] = 10

    fig = plt.figure()
    # ax = fig.gca(projection='3d')
    ax = Axes3D(fig)

    ax.plot(x, y, z, style_normal.get("linestyle", None), c=style_normal.get("color", None), label='Normal', linewidth=style_normal.get("linewidth", None))

    ax.plot(x[e > 0], y[e > 0], z[e > 0], style_erratic.get("linestyle", None), c=style_erratic.get("color", None), label='Erratic', linewidth=style_erratic.get("linewidth", None))
    # ax.scatter(x[e > 0], y[e > 0], z[e > 0], c='b', label='Erratic Movement')

    # ax.scatter(x[ff > 0], y[ff > 0], z[ff > 0], c=style_freeze.get("color", None), s=style_freeze.get("size", None), label='Freezing')

    for (fx, fsize) in zip(fs, fsizes):
        ax.scatter(x[fx > 0], y[fx > 0], z[fx > 0], c=style_freeze.get("color", None), s=fsize / style_freeze.get("size"), label='Freezing')

    ax.view_init(elev=style.get("elev", None), azim=style.get("azim", None))
    ax.legend()

    if xl is not None:
        ax.set_xlim(xl)

    if yl is not None:
        ax.set_ylim(yl)

    if zl is not None:
        ax.set_zlim(zl)

    if fname is not None:
        plt.savefig(fname, dpi=fdpi)

    plt.show()
