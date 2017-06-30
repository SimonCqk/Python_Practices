#!/usr/bin/python
# -*- coding:utf-8 -*-
import asyncio
import functools
import time

now = lambda: time.time()


async def do_some_work(n):
	if n <= 0:
		return
	print("It's work {}".format(n))
	time.sleep(1)
	await do_other_work(n - 1)


async def do_other_work(n):
	print("It's another work {}".format(n))
	time.sleep(1)
	await do_some_work(n - 1)


#  callback function (回调函数)
def callback(t, future):
	print("Call back :", t, future.result())


# task=asyncio.ensure_future(do_some_work(5))
loop = asyncio.get_event_loop()
task = loop.create_task(do_some_work(5))  # create a task
task.add_done_callback(functools.partial(callback, 5))  # 绑定
loop.run_until_complete(task)
loop.close()
