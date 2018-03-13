import math
from collections import defaultdict

import numpy as np


def read_iris_data():
    """逐行从iris.data读取样本数据"""
    with open('iris.data', 'r') as fp:
        data = fp.readline()
        while data and data != '\n':
            yield data
            data = fp.readline()


def build_iris_group():
    """每一行样本数据，对不同的class进行group by"""
    record = defaultdict(list)
    for each in read_iris_data():
        splits = each.split(',')
        record[splits[-1]].append(np.matrix([float(s) for s in splits[:-1]]))  # 将数据从字符串还原为float类型并加入总集合
    return record


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
        covariance[cls] = np.zeros([4, 4])
        for ft in features:
            covariance[cls] += np.matmul((ft - record_avg[cls]).T, (ft - record_avg[cls]))
    for mat in covariance.values():
        mat /= 50
    return covariance


# https://wenku.baidu.com/view/5e48bfa3524de518964b7dd1.html
def classify(samples, avg, cov) -> list:
    """对每个样本进行分类，返回分类的结果"""
    classes = [key for key in cov.keys()]
    class_cov = [val for val in cov.values()]
    averages = [a for a in avg.values()]
    answers = []
    for sample in samples:
        res0 = -1 / 2 * (sample - averages[0]) * np.matrix(class_cov[0]).I * \
               (sample - averages[0]).T - 1 / 2 * math.log(np.e, np.linalg.det(class_cov[0]))
        res1 = -1 / 2 * (sample - averages[1]) * np.matrix(class_cov[1]).I * \
               (sample - averages[1]).T - 1 / 2 * math.log(np.e, np.linalg.det(class_cov[1]))
        res2 = -1 / 2 * (sample - averages[2]) * np.matrix(class_cov[2]).I * \
               (sample - averages[2]).T - 1 / 2 * math.log(np.e, np.linalg.det(class_cov[2]))
        ans = max(res0, res1, res2)
        if ans == res0:
            ans = classes[0]
        elif ans == res1:
            ans = classes[1]
        else:
            ans = classes[2]
        answers.append(ans)
    return answers


def test_performance(test_ans):
    """
    测试贝叶斯分类的性能 统计各个类别的分类正确率
    最终结果为：Accuracy of class-Iris-setosa is 100.00%
               Accuracy of class-Iris-versicolor is 94.00%
               Accuracy of class-Iris-virginica is 100.00%
    """
    accuracy = dict()
    test_classes = (test_ans[0:50], test_ans[50:100], test_ans[100:])
    classes = ['Iris-setosa\n', 'Iris-versicolor\n', 'Iris-virginica\n']
    for each, cls in zip(test_classes, classes):
        right = 0
        for _t in each:
            if _t == cls:
                right += 1
        accuracy[cls] = right / len(each)
    for cls, acc in accuracy.items():
        print('Accuracy of class-{cls} is {acc:.2f}%'.format(cls=cls, acc=acc * 100))


if __name__ == '__main__':
    records = build_iris_group()  # 读取各个类别的数据
    records_avg = calculate_average(records)  # 计算各个类别特征均值
    records_cov = calculate_covariance_mat(records, records_avg)  # 计算各个类别的方差
    raw_records = [val for each in records.values() for val in each]  # 原数据
    test_answers = classify(raw_records, records_avg, records_cov)  # 得到分类结果
    test_performance(test_answers)  # 对分类器进行性能测试
