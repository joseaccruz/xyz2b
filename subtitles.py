import os
"""
dname = "/home/jcruz/Desktop/5-RESEARCH/20140314-work-fish_behaviour/julia/data/raw data mov 6a"
subs = [
(3, "Mov 6A-Trial     5 (tanque 3 before alarm cue).sub"),
(2, "Mov 6A-Trial     3 (tanque 2 before alarm cue).sub"),
(2, "Mov 6A-Trial     4 (tanque 2 after alarm cue).sub"),
(1, "Mov 6A-Trial     1 (tanque 1 before alarm).sub"),
(1, "Mov 6A-Trial     2 (tanque 1 after alarm cue).sub"),
(3, "Mov 6A-Trial     6 (tanque 3 after alarme cue).sub")]
tanks = {1: (0, 0), 2: (0, 0), 3: (0, 0)}

dname = "/home/jcruz/Desktop/5-RESEARCH/20140314-work-fish_behaviour/julia/data/raw data  mov 64"
subs = [
(1, "mov_64-trial_1-tank_1.sub"),
(1, "mov_64-trial_2-tank_1.sub"),
(2, "mov_64-trial_3-tank_2.sub"),
(2, "mov_64-trial_4-tank_2.sub"),
(3, "mov_64-trial_5-tank_3.sub"),
(3, "mov_64-trial_6-tank_3.sub")]
tanks = {1: (0, 0), 2: (0, 0), 3: (0, 0)}
"""

dname = "/home/jcruz/Desktop/5-RESEARCH/20140314-work-fish_behaviour/julia/data/raw data mov 69"
subs = [
(1, "MOV 69-Trial     1(tanque 1 before alarm cue).sub"),
(1, "MOV 69-Trial     2(tanque 1 after alarm cue)).sub"),
(2, "MOV 69-Trial     3(tanque 2 before alarm cue).sub"),
(2, "MOV 69-Trial     4(tanque 2 after alarm cue).sub"),
(3, "MOV 69-Trial     5(tanque 3 before alarm cue).sub"),
(3, "MOV 69-Trial     6(tanque 3 after alarm cue).sub")]
tanks = {1: (0, 0), 2: (0, 0), 3: (0, 0)}


def seconds2time(t):
    ti = int(t)

    h = int(ti / 3600)
    m = int(ti % 3600 / 60)
    s = int(ti % 60)

    return("%02d:%02d:%02d.%02.0f" % (h, m, s, int((t-ti)*100)))


def read_data(fname, tank, sub_data):
    data = map(lambda x: map(lambda y: float(y), x.strip().split(",")), open(fname).read().strip().split("\n"))

    for (t, f, e) in data:
        if not t in sub_data.keys():
            sub_data[t] = []

        sub_data[t].append((tank, f, e))

sub_data = {}

for (tank, fname) in subs:
    read_data(dname + os.sep + fname, tank, sub_data)


count = 0
last_sub = None

for k1 in sorted(sub_data.keys()):
    #print k1, sub_data[k1]
    for (tank, f, e) in sub_data[k1]:
        #print k, tank, f, e
        tanks[tank] = (f, e)

    sub = ""
    for k2 in sorted(tanks.keys()):
        (f, e) = tanks[k2]

        if f > 0:
            sub = " FREZE " + sub
        elif e > 0:
            sub = " ERRAT " + sub
        else:
            sub = " _____ " + sub

    if last_sub:
        count += 1
        (t, s) = last_sub

        print count
        print "%s --> %s" % (t, seconds2time(k1))
        print s
        print

    last_sub = (seconds2time(k1), sub)
