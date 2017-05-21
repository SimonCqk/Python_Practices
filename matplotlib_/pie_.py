#!/usr/bin/python
# -*- coding:utf-8 -*-

import matplotlib.pyplot as plt

labels = ('what', 'the', 'e.g.s')
sizes = [20, 30, 50]
explode = [0, 0.1, 0]
plt.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
plt.axis('equal')  # make the pie parts evenly
plt.show()
