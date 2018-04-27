import math
from collections import defaultdict

import numpy as np


def read_wine_data():
    """逐行从wine.data读取样本数据"""
    with open('wine.data', 'r') as fp:
        data = fp.readline()
        while data and data != '\n':
            yield data
            data = fp.readline()


def build_wine_group():
    """每一行样本数据，对不同的class进行group by"""
    records_ = defaultdict(list)
    for each in read_wine_data():
        splits = each.split(',')
        records_[splits[0]].append(np.matrix([float(s) for s in splits[1:]]))  # 将数据从字符串还原为float类型并加入总集合
    return records_


def get_probability(record: dict):
    """得到每个类别的先验概率"""
    pb = dict()
    total = 0
    for cls, data in record.items():
        pb[cls] = len(data)
        total += len(data)
    for cls in pb.keys():
        pb[cls] /= total
    return pb


def get_each_mean(record: dict):
    average = dict()
    for cls, features in record.items():
        average[cls] = np.mean(record[cls], 0)  # 求各个类别的均值向量
    return average


def get_cov_matrix(record: dict, record_avg: dict):
    covariance = dict()
    for cls, features in record.items():
        covariance[cls] = np.zeros([13, 13])
        for ft in features:
            covariance[cls] += np.matmul((ft - record_avg[cls]).T, (ft - record_avg[cls]))
    for cls, mat in covariance.items():
        mat /= len(record[cls])
    return covariance


def bayes_classify(samples, avg, cov) -> list:
    """对每个样本进行贝叶斯分类，返回分类的结果"""
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


def test_performance(test_ans, record):
    """
        测试贝叶斯分类的性能 统计各个类别的分类正确率
        最终结果为：Accuracy of class-1 is 100.00%
                   Accuracy of class-2 is 100.00%
                   Accuracy of class-3 is 100.00%
        """
    accuracy = dict()
    test_classes = (test_ans[0:len(record['1'])], test_ans[len(record['1']):len(record['1']) + len(record['2'])],
                    test_ans[-len(record['3']):])
    classes = ['1', '2', '3']
    for each, cls in zip(test_classes, classes):
        right = 0
        for _t in each:
            if _t == cls:
                right += 1
        accuracy[cls] = right / len(each)
    for cls, acc in accuracy.items():
        print('Accuracy of class-{cls} is {acc:.2f}%'.format(cls=cls, acc=acc * 100))


if __name__ == '__main__':
    records = build_wine_group()
    prob = get_probability(records)
    average = get_each_mean(records)
    cov = get_cov_matrix(records, average)
    raw = [val for each in records.values() for val in each]  # 原数据
    classified_ans = bayes_classify(raw, average, cov)
    test_performance(classified_ans, records)
