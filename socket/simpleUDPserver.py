#!/usr/bin/python
# -*- coding:utf-8 -*-
'''
 run before client.
'''
import time
from socket import *

now = lambda: time.time()

HOST = ''
PORT = 21567
BUFSIZE = 10240
ADDR = (HOST, PORT)

udp_ser_sock = socket(AF_INET, SOCK_DGRAM)
udp_ser_sock.bind(ADDR)

while True:
	print('waiting for connection ...')
	data, addr = udp_ser_sock.recvfrom(BUFSIZE)
	print('connected from ...', addr)
	udp_cli_sock.sendto('[{0}] , {1}'.format(now, data), addr)
udp_ser_sock.close()  # never execute.
