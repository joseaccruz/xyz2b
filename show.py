import cv2
import numpy as np

import utils

FILE_DATA = "/home/jcruz/Desktop/5-RESEARCH/20140314-work-fish_behaviour/faustino/data/side/Tu15_side.txt"
FILE_VIDEO = "/home/jcruz/Desktop/BIG_DATA/fish_videos/ana_faustino/Tu15_A__Cond1_side_2.avi"

START_T = 7 * 60 * 1000

(X_SCALE, X_TRANS) = (21.88392008, 271.97335871)
(Y_SCALE, Y_TRANS) = (-21.9054242, 407.59388039)


def on_mouse(event, x, y, flags, k):
    if event == 1:
        print "MOUSE:", x, y, flags

#
#
#
data = utils.read_txt(FILE_DATA)
cap = cv2.VideoCapture(FILE_VIDEO)

(x, y) = (10.5128689995, -7.9942489268)


cv2.namedWindow("x")
cv2.setMouseCallback("x", on_mouse)

i = 0

fpre = None

while True:
    tf = int(cap.get(cv2.cv.CV_CAP_PROP_POS_MSEC))
    td = int(data[i][0] * 1000.0)

    try:
        x = int(data[i][1] * X_SCALE + X_TRANS)
        y = int(data[i][2] * Y_SCALE + Y_TRANS)
    except ValueError:
        pass

    i += 1

    (r, f) = cap.read()

    wkey = 1
    if tf > START_T:
        if not fpre is None:
            fd = cv2.absdiff(f, fpre)
            print np.sum(fd)
            cv2.imshow("y", fd)
        fpre = f

        print tf, tf-td, x, y, data[i]
        cv2.circle(f, (x, y), 2, (255, 0, 0), -1)
        cv2.imshow("x", f)
        wkey = 0
    elif tf % 10000 == 0:
        print tf

    if cv2.waitKey(wkey) == 27:
        quit()

    
