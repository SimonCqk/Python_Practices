import cv2
import bisect
import numpy as np
from matplotlib import pyplot as plt

IMAGE_NAME = 'TEST.tif'

# 加载图像
img = cv2.imread(IMAGE_NAME, 0)
histed = cv2.equalizeHist(img)


# 图像的灰度变换
def imadjust(src, tol=1, vin=[0, 255], vout=(0, 255)):
    dst = src.copy()
    tol = max(0, min(100, tol))

    if tol > 0:
        # Compute in and out limits
        # Histogram
        hist = np.zeros(256, dtype=np.int)
        for r in range(src.shape[0]):
            for c in range(src.shape[1]):
                hist[src[r, c]] += 1
        # Cumulative histogram
        cum = hist.copy()
        for i in range(1, len(hist)):
            cum[i] = cum[i - 1] + hist[i]

        # Compute bounds
        total = src.shape[0] * src.shape[1]
        low_bound = total * tol / 100
        upp_bound = total * (100 - tol) / 100
        vin[0] = bisect.bisect_left(cum, low_bound)
        vin[1] = bisect.bisect_left(cum, upp_bound)

    # Stretching
    scale = (vout[1] - vout[0]) / (vin[1] - vin[0])
    for r in range(dst.shape[0]):
        for c in range(dst.shape[1]):
            vs = max(src[r, c] - vin[0], 0)
            vd = min(int(vs * scale + 0.5) + vout[0], vout[1])
            dst[r, c] = vd
    return dst


adjusted = imadjust(histed)
'''
# 显示均衡化和灰度变换后的图像
_, (orig, h, a) = plt.subplots(1, 3)
orig.set_title('Origin Image')
orig.imshow(sample_img, 'gray')
h.set_title('After Histogram')
h.imshow(histed, 'gray')
a.set_title('After adjusted')
a.imshow(adjusted, 'gray')
'''

# 中值滤波和均值滤波
filtered = cv2.blur(adjusted, (5, 5))  # 均值滤波
filtered = cv2.medianBlur(filtered, 5)

# 频域低通滤波
filtered = np.fft.fft2(filtered)
F = np.fft.fftshift(filtered)
G1 = np.fft.ifftshift(F)
g1 = np.real(np.fft.ifft2(G1))

plt.imshow(g1)
plt.show()
