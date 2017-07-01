#!/usr/bin/python
# -*- coding:utf-8 -*-

# -*- 异步IO -*-
import asyncio
import threading

import time

now = lambda: time.time()
start = now()


async def sub():
	print('sub start: ...')
	n = 10
	while n >= 0:
		print('yield start')
		# asyncio.sleep()也是一个coroutine类型的generator，所以线程不会中断，而是直接执行下一个循环，等待yield from的返回
		# 可以简单的理解为出现yield之后则开启一个协程(类似开启一个新线程),不管这个协程是否执行完毕，继续下一个循环
		# 开启新协程后，print('yield start')会因为继续执行循环被立即执行，可以通过打印结果观察
		r = await asyncio.sleep(1)
		n = n - 1
		print('---sub: %s,  thread:%s' % (n, threading.currentThread()))


async def add():
	print('add start: ...')
	n = 10
	while n <= 20:
		print('yield start')
		r = await asyncio.sleep(2)
		n += 1
		print('+++add: %s,  thread:%s' % (n, threading.currentThread()))


# 获取EventLoop:
loop = asyncio.get_event_loop()
# 执行coroutine
tasks = [add(), sub()]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()
print('TIME :{:.2}s'.format(now() - start))
