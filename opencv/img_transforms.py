#!/usr/bin/python
# -*- coding:utf-8 -*-
import cv2
import numpy as np

fn = "images/for_another.jpg"
src_img = cv2.imread(fn)
img = cv2.cvtColor(src_img, cv2.COLOR_BGR2GRAY)

ft = cv2.dft(np.float32(img), flags=cv2.DFT_SCALE | cv2.DFT_REAL_OUTPUT)  # do fourier transform in settled flags
fshift = np.fft.fftshift(ft)  # shift the zero-frequency
shift_back = np.fft.ifftshift(fshift)  # shift back
img_back = cv2.idft(shift_back)  # inverse fourier transform

cv2.imshow('Result', np.abs(img_back))  # complex values are not allowed in the final sample_img
cv2.waitKey(0)
cv2.destroyAllWindows()
