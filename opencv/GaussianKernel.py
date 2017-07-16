'''
:keyword a Gaussian kernel - implemented by decimal
'''
from decimal import Decimal

import numpy


def get_gaussian_kernel() -> numpy.matrix:
	mask = numpy.mat("1,4,7,1,4;4,16,26,16,4;7,26,41,26,7;4,16,26,16,4;1,4,7,4,7")
	gaussian_kernel = numpy.zeros([5, 5])

	for i in range(5):
		for j in range(5):
			gaussian_kernel[i, j] = (Decimal(str(mask[i, j])) / Decimal(str(273)))
	return gaussian_kernel


# the built-in type version may runs faster while the result may be the same .
'''
def get_gaussian_kernel()-> numpy.matrix:
	mask = numpy.mat("1,4,7,1,4;4,16,26,16,4;7,26,41,26,7;4,16,26,16,4;1,4,7,4,7")
	gaussian_kernel = mask / 273
	return gaussian_kernel
'''
