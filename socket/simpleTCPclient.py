#!/usr/bin/python
# -*- coding:utf-8 -*-
import time
from socket import *

now = lambda: time.time()

HOST = '127.0.0.1'
PORT = 21567
BUFSIZE = 10240
ADDR = (HOST, PORT)

tcp_clt_sock = socket(AF_INET, SOCK_STREAM)
tcp_clt_sock.connect(ADDR)

while True:
	data = input('data >:')
	if not data:
		break
	tcp_clt_sock.send(data)
	data = tcp_clt_sock.recv(BUFSIZE)
	if not data:
		break
	print(data.decode('utf-8'))

tcp_clt_sock.close()
