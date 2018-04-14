import math
import numpy as np
from matplotlib import pyplot as plt

SENSOR_NODE_NUM = 100
INIT_COM_RADIUS = 0.1
RADIUS_STEP = 0.001
TOTAL_TEST_LEVEL = 5


def generate_rdn_wsn(n: int, r: float):
    """生成给定网络规模数量为n 通信半径为r的WSN"""
    orig = np.matrix(np.random.random((n, n)))
    orig[orig > r] = 0  # 距离大于通信半径的都为不连通
    orig[orig > 0] = 1
    return orig


def get_levels_wsn(level_num=TOTAL_TEST_LEVEL):
    """
    一次获得不同能量级别(通信半径范围)的随机传感网络矩阵
    之后的实验都在这些网络上进行，不再重新生成
    """
    nets = []
    radius = INIT_COM_RADIUS
    for i in range(0, level_num):
        nets.append(generate_rdn_wsn(SENSOR_NODE_NUM, radius))
        radius += RADIUS_STEP
    return nets


def get_coverage_radio(mat, r):
    n = mat.shape[0]
    grid = 1 / n
    img = np.zeros(mat.shape)
    for i in range(0, n):
        for j in range(0, n):
            if mat[i, j]:
                cov_r = r / grid
                points = [(x, y) for x in range(int(i - cov_r), int(i + cov_r), 1) for y in
                          range(int(j - cov_r), int(j + cov_r), 1) if
                          n > x >= 0 and n > y >= 0]
                for x, y in points:
                    img[x, y] = 1
    plt.imshow(img)
    plt.imsave('test.png', img)


if __name__ == '__main__':
    m = generate_rdn_wsn(SENSOR_NODE_NUM, 0.1)
    get_coverage_radio(m, 0.1)
