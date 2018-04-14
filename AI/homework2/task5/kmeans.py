import cv2
import random
import numpy as np
from matplotlib import pyplot as plt

samples = []


def get_pixel(img):
    b, g, r = cv2.split(img)
    return [(_r, _g, _b) for (er, eg, eb) in zip(r, g, b)
            for (_r, _g, _b) in zip(er, eg, eb)]


def load_data(filename):
    img = cv2.imread(filename)
    samples.extend(get_pixel(img))
    return img, np.mat(samples)


def init_centroids(data: np.matrix, k=2):
    # 随机初始化中心点
    sample_num, dim = data.shape
    centroids = np.zeros((k, dim))
    for i in range(k):
        index = int(random.uniform(0, sample_num))
        centroids[i, :] = data[index, :]
    return centroids


def k_means(data, k=2):
    # k means算法的主要实现部分
    sample_num = data.shape[0]
    # 第一列存储属于的聚类，第二列存储此列样本和中心点的误差
    clusters = np.zeros((sample_num, 2))
    cluster_changed = True

    centroids = init_centroids(data, k)
    while cluster_changed:
        cluster_changed = False
        for i in range(sample_num):
            min_dist = 1 << 31
            min_idx = 0
            # 找到最近的聚类中心
            for j in range(k):
                dist = np.linalg.norm(centroids[j, :] - data[i, :])
                if dist < min_dist:
                    min_dist, min_idx = dist, j
            # 更新聚类
            if clusters[i, 0] != min_idx:
                cluster_changed = True
                clusters[i, :] = min_idx, min_dist ** 2

            # 更新聚类中心
        for j in range(k):
            points_in_cluster = data[np.nonzero(clusters[:, 0] == j)[0]]
            centroids[j, :] = np.mean(points_in_cluster, 0)
    return centroids, clusters


def main():
    img, data = load_data('IMGP8080.jpg')

    centroids, clusters = k_means(data)
    rows, cols = img.shape[0:2]
    for row in range(rows):
        for col in range(cols):
            if clusters[row * cols + col, 0] == 0:
                img[row, col, :] = (255, 255, 255)
    plt.imsave('cluster.jpg', img)


if __name__ == '__main__':
    main()
