import cv2
import numpy as np

IMG_FILE1 = 'xl-130-16.tiff'
IMG_FILE2 = 'xl-150-16.tiff'

img_1 = cv2.imread(IMG_FILE1, 0)
img_2 = cv2.imread(IMG_FILE2, 0)
img_1 = cv2.cvtColor(img_1, cv2.COLOR_BGR2GRAY)
img_2 = cv2.cvtColor(img_2, cv2.COLOR_BGR2GRAY)
