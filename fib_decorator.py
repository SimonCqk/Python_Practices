#!/usr/bin/python
# -*- coding:utf-8 -*-

"""
@version of decorator to boost fibonacci function
"""
import time


def fib_decorator(func):
	cache = dict()

	def wrap(*args):
		return cache.setdefault(args, func(*args))

	return wrap


@fib_decorator
def fibonacci(*n):
	for item in n:
		a, b = 0, 1
		while a < item:
			print(a, end=' ')
			a, b = b, a + b
		print()


# Test .

start = time.clock()
fib_decorator(10000)
end = time.clock()
print("Running time:{}s".format(end-start))
