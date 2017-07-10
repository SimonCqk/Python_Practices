#!/usr/bin/python
# -*- coding:utf-8 -*-
import numpy as np


# fibonacci function of python version
def fibonacci(n):
	fib = np.mat([[1, 1], [1, 0]])
	ans = (fib ** n)[0, 0]
	return ans


def quick_pow(a: int, n: int) -> int:
	ans = 1
	while n:
		if n & 1:  # n%2
			ans *= a
		n = int(n >> 1)
		a *= a
	return ans


# quick powder of matrix
def quick_pow_mat(mat, n):
	'''
	:param mat: the input matrix
	:param n: the exponent
	:return:the calculated matrix
	'''
	assert (mat.shape)[0] == (mat.shape)[1] and n is not 0, "Invalid input data , plz check the params ."
	ans = np.eye((mat.shape)[0])
	while n:
		if n & 1:
			ans = np.multiply(ans, mat)
		n = int(n >> 1)
		mat = np.multiply(mat, mat)
	return ans
