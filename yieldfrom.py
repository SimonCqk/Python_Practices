#!/usr/bin/python
# -*- coding:utf-8 -*-
'''
:summary -> a clear practice to understand how generator&yield from syntax works.
'''
from collections import namedtuple

Result = namedtuple('Result', ['count', 'average'])


# 子生成器
def averager() -> Result:
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield
        total += term
        count += 1
        average = total / count
        return Result(count, average)


# 委派生成器
def grouper(results: dict, key):
    while True:
        results[key] = yield from averager()


# 输出报告
def report(results):
    for key, result in sorted(results.items()):
        group, unit = key.split('-')
        print('{:2} {:5} averaging {:.2f}{}'.format(result.count, group, result.average, unit))


# 客户端代码，即调用方
def main(data):
    results = {}
    for key, values in data.items():
        group = grouper(results, key)
        next(group)  # 预激生成器
        for value in values:
            group.send(value)
        group.close  # 关闭generator,如果group.send(None) 则result[key]全变None.
    report(results)


data = {
    'Girls-kg':
        [40.9, 38.5, 44.3, 42.2, 45.2, 41.7, 44.5, 38.0, 40.6, 44.5],
    'Girls-m':
        [1.6, 1.51, 1.4, 1.3, 1.41, 1.39, 1.33, 1.46, 1.45, 1.43],
    'Boys-kg':
        [39.0, 40.8, 43.2, 40.8, 43.1, 38.6, 41.4, 40.6, 36.3],
    'Boys-m':
        [1.38, 1.5, 1.32, 1.25, 1.37, 1.48, 1.25, 1.49, 1.46]
}

if __name__ == '__main__':
    main(data)
