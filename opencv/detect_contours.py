#!/usr/bin/python
# -*- coding:utf-8 -*-
import cv2

src_img = cv2.imread('opencv/images/moonlight.png')
img = cv2.cvtColor(src_img, cv2.COLOR_BGR2GRAY)
ret, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)  # cvt to a binary(only black & white) img

_, contours, _ = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
cv2.drawContours(img, contours, -1, (0, 0, 255), 3)

cv2.imshow("Result", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
