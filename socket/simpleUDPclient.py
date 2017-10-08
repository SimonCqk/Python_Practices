#!/usr/bin/python
# -*- coding:utf-8 -*-
import time
from socket import *

now = lambda: time.time()

HOST = '127.0.0.1'  # or 'localhost'
PORT = 21567  # same as server port.
BUFSIZE = 10240
ADDR = (HOST, PORT)

udp_clt_sock = socket(AF_INET, SOCK_DGRAM)
udp_clt_sock.connect(ADDR)

while True:
	data = input('data >:')
	if not data:
		break
	udp_clt_sock.sendto(data, ADDR)
	data, ADDR = udp_clt_sock.recvfrom(BUFSIZE)
	if not data:
		break
	print(data.decode('utf-8'))

udp_clt_sock.close()
