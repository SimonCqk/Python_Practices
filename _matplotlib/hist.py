#!/usr/bin/python
# -*- coding:utf-8 -*-
import matplotlib.pyplot as plt
import numpy

numpy.random.seed(0)
avg, sigma = 100, 20  # 均值 标准差
a = numpy.random.normal(avg, sigma, size=100)

plt.hist(a, 40, normed=1, histtype='stepfilled', facecolor='b', alpha=0.75)
plt.title('Histogram')

plt.show()
