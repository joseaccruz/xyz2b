import os

import xlrd


#
# given a directory takes all excel files on it
#
def list_excel(dir, recursive=True):
    ret = []

    for (root, dirs, files) in os.walk(dir, topdown=False):
        for name in filter(lambda f: f.endswith(".xlsx"), files):
            ret.append(os.path.join(root, name))

        if recursive:
            for name in dirs:
                ret += list_excel(name, recursive=True)

    return sorted(ret)


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

    return("%02d:%02d:%02d.%02.0f" % (h, m, s, int((t-ti)*100)))
