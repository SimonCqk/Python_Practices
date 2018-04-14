import cv2
import numpy as np
from matplotlib import pyplot as plt

samples = dict()
samples['river'] = []
samples['others'] = []


def get_pixel(img):
    b, g, r = cv2.split(img)
    return [(_r, _g, _b) for (er, eg, eb) in zip(r, g, b)
            for (_r, _g, _b) in zip(er, eg, eb)]


def load_data(filename, label):
    img = cv2.imread(filename)
    samples[label].extend(get_pixel(img))


def calculate_average(record_dict: dict):
    """计算各个类别的均值向量"""
    average = dict()
    for cls, features in record_dict.items():
        average[cls] = np.mean(record_dict[cls], 0)  # 求各个类别的均值向量
    return average


def calculate_covariance_mat(record_dict: dict, record_avg: dict):
    """计算各个类别的协方差矩阵"""
    covariance = dict()
    for cls, features in record_dict.items():
        covariance[cls] = np.zeros((record_avg[cls].shape[0], record_avg[cls].shape[0]))
        for ft in features:
            covariance[cls] += np.matmul((ft - record_avg[cls]).T, (ft - record_avg[cls]))
    for mat in covariance.values():
        mat /= len(mat)
    return covariance


def fisher_classify(sample_img, sample_mean, sample_cov):
    """true -> 属于river, false -> 属于其他"""
    river_mean, other_mean = sample_mean.values()
    river_cov, other_cov = sample_cov.values()
    s_w = river_cov + other_cov
    u, s, v = np.linalg.svd(s_w)
    s_w_inv = np.dot(np.dot(v.T, np.linalg.inv(np.diag(s))), u.T)
    w = np.dot(s_w_inv, river_mean - other_mean)
    center_river = np.dot(w.T, river_mean)
    center_other = np.dot(w.T, other_mean)
    rows, cols = sample_img.shape[0:2]
    for row in range(rows):
        for col in range(cols):
            pos = np.dot(w.T, sample_img[row, col, :])
            if abs(pos - center_river) > abs(pos - center_other):
                continue
            else:
                sample_img[row, col, :] = (255, 255, 255)
    return sample_img


def main():
    load_data('river.jpg', 'river')
    load_data('other.jpg', 'others')
    image = cv2.imread('IMGP8080.jpg')

    sample_mean = calculate_average(samples)
    sample_cov = calculate_covariance_mat(samples, sample_mean)
    image = fisher_classify(image, sample_mean, sample_cov)
    plt.imsave('classify.jpg', image)


if __name__ == '__main__':
    main()
