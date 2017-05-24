#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
@version of decorator to boost fibonacci function
"""
import time


def decorator(func):
	cache = dict()

	def wrap(*args):
		for arg in args:
			return cache.setdefault(arg, func(arg))

	return wrap


@decorator
def fibonacci(n: int) -> int:

	if n == 0 or n == 1:
		return 1
	else:
		return fibonacci(n - 1) + fibonacci(n - 2)


start = time.clock()
print(fibonacci(10))
end = time.clock()
print("Running time:{}s".format(end - start))

"""
No-Recursive version:

def fibonacci(*n):
	for item in n:
		a, b = 0, 1
		while a < item:
			print(a, end=' ')
			a, b = b, a + b
		print()
"""
