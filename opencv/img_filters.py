#!/usr/bin/python
# -*- coding:utf-8 -*-
import cv2
import numpy as np

fn = "images/for_test.jpg"
src_img = cv2.imread(fn)
img = cv2.cvtColor(src_img, cv2.COLOR_BGR2GRAY)

# add spiced salt noise

w, h = img.shape[1], img.shape[0]  # gray scale range
new_img = np.array(img)
# the number of noise dots
noise_count = 60000
for k in range(0, noise_count):
	xi = int(np.random.uniform(0, new_img.shape[1]))
	xj = int(np.random.uniform(0, new_img.shape[0]))
	new_img[xj, xi] = 255

cv2.imshow('src noised img', new_img)

# median filter
mfiltered_img = cv2.medianBlur(new_img, 5)
cv2.imshow('median filter', mfiltered_img)
# average filter
afiltered_img = cv2.blur(new_img, (5, 5))
cv2.imshow('average filter', afiltered_img)
# gaussian filter
gfiltered_img = cv2.GaussianBlur(new_img, (5, 5), 0)
cv2.imshow('gaussian filter', gfiltered_img)
# bilateral filter
bfiltered_img = cv2.bilateralFilter(new_img, 9, 75, 75)
cv2.imshow('bilateral filter', bfiltered_img)

cv2.waitKey(0)
cv2.destroyAllWindows()
