#! /usr/bin/env python
# coding:utf-8

import socket

HOST = "localhost"
PORT = 25000

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((HOST,PORT))

s.send('hehe,is it works well ?')
received_data = s.recv(4096)
s.close()

print 'received from socket server',received_data
