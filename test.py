"""
import socket

def init():
	global sock
	sock = socket.socket()
	sock.bind(('127.0.0.1', 5554))
	sock.listen(1)

def run():
	global sock
	while True:


if __name__ == '__main__':
	init()
	run()
	input()
"""

import sys
import struct
from base64 import b64encode
from hashlib import sha1

import socket
from pprint import pprint


def init():
	global sock
	sock = socket.socket()
	sock.bind(('', 5554))

def run():
	global sock
	sock.listen(10)
	for i in range(100):
		conn, addr = sock.accept()
		print()
		print('con')
		print(conn)
		print(addr)
		pprint(sock.recvfrom(2))
	input()
	print('connected:', addr)
	pprint(conn)
	input()
	while True:
		print()
		print('new data')
		data = conn.recv(2)
		#data = conn.recvmsg(2)
		print(type(data))
		print(len(data))
		pprint(data.encode('utf-8'))
		input()
		if not data:
			break
		headers = read_http_headers(data)
		key = headers['Sec-WebSocket-Key']
		output_headers = response_headers(key).encode('utf-8')
		conn.send(output_headers)
		#conn.close()

def read_http_headers(data):
	if not data:
		return False

	split_data = '\r\n'
	split_item = ':'

	data_arr = data.decode("utf-8").split(split_data)

	print()
	pprint(data_arr)
	print()

	obj = {
		'HTTP': data_arr.pop(0)
	}

	for data_item in data_arr:
		if data_item != '':
			key, value = data_item.split(split_item, 1)
			key = key.strip()
			value = value.strip()
			obj[key] = value

	return obj



	

def response_headers(key):
	return \
	  'HTTP/1.1 101 Switching Protocols\r\n'\
	  'Upgrade: websocket\r\n'			  \
	  'Connection: Upgrade\r\n'			 \
	  'Sec-WebSocket-Accept: %s\r\n'		\
	  '\r\n' % calculate_response_key(key)

def calculate_response_key(key):
	GUID = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
	hash = sha1(key.encode() + GUID.encode())
	response_key = b64encode(hash.digest()).strip()
	return response_key.decode('ASCII')


if __name__ == '__main__':
	init()
	run()
	print()
	print('end')
	input()