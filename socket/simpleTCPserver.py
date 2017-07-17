#!/usr/bin/python
# -*- coding:utf-8 -*-
import time
from socket import *

now = lambda: time.time()

HOST = ''
PORT = 21567
BUFSIZE = 10240
ADDR = (HOST, PORT)

tcp_ser_sock = socket(AF_INET, SOCK_STREAM)
tcp_ser_sock.bind(ADDR)
tcp_ser_sock.listen(5)

while True:
	print('waiting for connection ...')
	tcp_cli_sock, addr = tcp_ser_sock.accept()
	print('connected from ...', addr)
	while True:
		data = tcp_cli_sock.recv(BUFSIZE)
		if not data:
			break
		tcp_cli_sock.send('[{0}] {1}'.format(bytes(now(), 'utf-8'), data))
	tcp_cli_sock.close()

tcp_ser_sock.close()
