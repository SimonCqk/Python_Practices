#!/usr/bin/python
# -*- coding:utf-8 -*-
import socket
import time


def now(): return time.time()


HOST = '127.0.0.1'  # or 'localhost'
PORT = 21567  # same as server port.
BUFSIZE = 10240
ADDR = (HOST, PORT)

tcp_clt_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_clt_sock.connect(ADDR)

while True:
    data = input('data >:')
    if not data:
        break
    tcp_clt_sock.send(data.encode('utf-8'))
    data = tcp_clt_sock.recv(BUFSIZE)
    if not data:
        break
    print(data.decode('utf-8'))

tcp_clt_sock.close()
