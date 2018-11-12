from pprint import pprint

import socket
import select

import sys
import struct
from base64 import b64encode
from hashlib import sha1

FIN    = 0x80
OPCODE = 0x0f
MASKED = 0x80
PAYLOAD_LEN = 0x7f
PAYLOAD_LEN_EXT16 = 0x7e
PAYLOAD_LEN_EXT64 = 0x7f

OPCODE_CONTINUATION = 0x0
OPCODE_TEXT         = 0x1
OPCODE_BINARY       = 0x2
OPCODE_CLOSE_CONN   = 0x8
OPCODE_PING         = 0x9
OPCODE_PONG         = 0xA

class MyServer:

	clients = {}
	
	id_counter = 0

	accept_per_frame = 1

	def __init__(self, _host = 'localhost', _port = 5554):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.socket.bind((_host, _port))
		self.socket.listen(5)
		self.read_list = [self.socket]
		#self.read_list = []

	def run(self):
		while True:
			print('NEW FRAME')
			readable, writable, errored = select.select(self.read_list, [], [])
			for s in readable:
				if s is self.socket:
					self._frame_listen()
				else:
					self._frame_recv(s)
			#print()

	def _frame_listen(self):
		conn, addr = self.socket.accept()
		self._new_client(conn, addr)

	def _frame_recv(self, conn):
		for _id in self.clients.keys():
			if self.clients[_id]['handler'] == conn:
				_client_id = _id
				_client = self.clients[_id]

		#print('')
		#print('frame_recv')
		#print(_client_id)
		#print(_client)

		print('RECV FROM ' + str(_client_id) + ', ' + str(_client['addr'][0]))
		if not _client['valid']:
			self.handshake(_client_id)
		else:
			self.read_msg(_client_id)

	def handshake(self, _client_id):
		#print('NEW HANDSHAKE')
		_conn = self.clients[_client_id]['handler']
		data = _conn.recv(4096)
		#print()
		#print(type(data))
		#print(len(data))
		#pprint(data)
		#print()	
		headers = self.read_http_headers(data)
		if headers:
			self.clients[_client_id]['valid'] = True
		key = headers['Sec-WebSocket-Key']
		output_headers = response_headers(key).encode('utf-8')
		_conn.send(output_headers)
		#print('')

	def read_msg(self, _client_id):
		#print('NEW MSG')
		_conn = self.clients[_client_id]['handler']
		data = _conn.recv(1)
		#print()
		#print(type(data))
		#print(len(data))
		#pprint(data)
		#print()
		if not data:
			#print('not data')
			return
		#print('data')

	def _new_client(self, _conn, _addr):
		self.id_counter += 1
		self.clients[self.id_counter] = {
			'handler': _conn,
			'addr': _addr,
			'valid': False,
		}
		self.read_list.append(_conn)
		print('new client ' + str(self.id_counter) + ': '+ _addr[0] + ':' + str(_addr[1]))

	def read_http_headers(self, data):
		if not data:
			return False

		split_data = '\r\n'
		split_item = ':'

		data_arr = data.decode("utf-8").split(split_data)

		obj = {
			'HTTP': data_arr.pop(0)
		}

		for data_item in data_arr:
			if data_item != '':
				key, value = data_item.split(split_item, 1)
				key = key.strip()
				value = value.strip()
				obj[key] = value

		pprint(obj)
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