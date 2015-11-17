#! /usr/bin/env python
# coding:utf-8

import socket

HOST = "0.0.0.0"
PORT = 25000

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((HOST,PORT))
s.listen(3)
conn,addr = s.accept()

print 'Connect by ',addr
while 1:
	data = conn.recv(4096)
	print '\n recv = ',data
	if not data:break
	conn.sendall(data.upper())
conn.close()