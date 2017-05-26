#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
:keyword  Define a decorator to log function-calls locally
:reference_from 《Python3 Programming》
"""
import functools
import logging
import os
import tempfile

# 若在调式模式下
if __debug__:
	logger = logging.getLogger("Logger")
	logger.setLevel(logging.DEBUG)
	# gettempdir() 返回保存临时文件的目录
	handler = logging.FileHandler(os.path.join(tempfile.gettempdir(), "logged.log"))
	logger.addHandler(handler)


	def logged(func):

		@functools.wraps(func)
		def wrapper(*args, **kwargs):
			log = 'Called:' + func.__name__ + '('
			log += ','.join(['{0!r}'.format(a) for a in args] +
							['{0!s}={1!r}'.format(k, v) for k, v in kwargs.items()])
			result = exception = None
			try:
				result = func(*args, **kwargs)
				return result
			except Exception as error:
				exception = error
			finally:
				log += ((") -> " + str(result)) if exception is None
						else ") {0}: {1}".format(type(exception), exception))
				logger.debug(log)
				if exception is not None:
					raise exception
			return wrapper

else:
	def logged(func):
		return func
