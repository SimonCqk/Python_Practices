#!/usr/bin/python
# -*- coding:utf-8 -*-
import cv2
import numpy as np

fn = "median.jpg"
myimg = cv2.imread(fn)
img = cv2.cvtColor(myimg, cv2.COLOR_BGR2GRAY)

# 加上椒盐噪声
# 灰阶范围
w = img.shape[1]
h = img.shape[0]
newimg = np.array(img)
# 噪声点数量
noisecount = 50000
for k in range(0, noisecount):
	xi = int(np.random.uniform(0, newimg.shape[1]))
	xj = int(np.random.uniform(0, newimg.shape[0]))
	newimg[xj, xi] = 255

# 滤波去噪
lbimg = cv2.medianBlur(newimg, 3)
cv2.imshow('src', newimg)
cv2.imshow('dst', lbimg)
cv2.waitKey()
cv2.destroyAllWindows()
