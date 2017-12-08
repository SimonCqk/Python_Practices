#!/usr/bin/python
# -*- coding:utf-8 -*-
'''
 run before client.
'''
import socket
import threading
import time


def now(): return time.time()


def tcp_link_worker(sock, addr):
    print('connected from ...', addr)
    while True:
        data = sock.recv(BUFSIZE)
        print('received: ', data.decode('utf-8'))
        if not data:
            break
        sock.send('[{0}] {1}'.format(now(), data).encode('utf-8'))
    sock.close()


HOST = ''
PORT = 21567
BUFSIZE = 10240
ADDR = (HOST, PORT)

tcp_ser_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_ser_sock.bind(ADDR)
tcp_ser_sock.listen(5)  # max income connection is 5.

while True:
    print('waiting for connection ...')
    tcp_cli_sock, addr = tcp_ser_sock.accept()
    t = threading.Thread(target=tcp_link_worker, args=(tcp_cli_sock, addr))
    t.start()
tcp_ser_sock.close()  # never execute.
