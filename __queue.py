#!/usr/bin/python
# -*- coding:utf-8 -*-
import threading
import time
from queue import Queue
from random import randint


def writeQ(queue):
	print('Producing objects for Q...')
	queue.put('xxx', 1)
	print('SIZE now ---> ', queue.qsize())


def readQ(queue):
	val = queue.get(1)
	print('Consumed object from Q ... and size now', queue.qsize())


def writer(queue, loops):
	for i in range(loops):
		readQ(queue)
		time.sleep(randint(1, 3))


def reader(queue, loops):
	for i in range(loops):
		readQ(queue)
		time.sleep(randint(1, 3))


funcs = [writer, reader]
nfuncs = range(len(funcs))


def main():
	nloops = randint(2, 5)
	q = Queue(32)
	threads = []
	for i in nfuncs:
		t = threading.Thread(target=funcs[i], args=(q, nloops), name=funcs[i].__name__)
		threads.append(t)
		t.start()
	for i in nfuncs:
		threads[i].join()
	print("ALL DONE .")


if __name__ == '__main__':
	main()
