# -*- coding:utf-8 -*-

from math import sqrt
from random import random
from time import clock

DARTS = 1000000
hits = 0
clock()
for i in range(DARTS):
	x, y = random(), random()
	dist = sqrt(x ** 2 + y ** 2)
	if dist <= 1.0:
		hits = hits + 1
pi = 4 * (hits / DARTS)
print('Pi的值是:%s' % pi)
print('程序运行时间是%-5.5s s' % clock())
