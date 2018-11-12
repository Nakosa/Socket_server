from pprint import pprint

import socket
import select

import sys
import struct
from base64 import b64encode
from hashlib import sha1

import time
import os
import math
import string
import random
import secrets

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

	users = []

	FPS = 0
	frames_per_second = 20

	def __init__(self, _host = 'localhost', _port = 5554):
		self.conn = Socket_Component(self, _host, _port)
		self.frame_ms_time = float(1000 / self.frames_per_second)

	def run(self):
		while True:

			frame_start = time.time()

			self.conn.frame()

			self._frame_users()
			self._frame_mobs()
			self._frame_nps()
			self._frame_objects()
			self._frame_locations()
			self._frame_items()

			self._frame_sleep(frame_start)
			self._tps_counter(frame_start)
			#print(self.FPS)

	

	def _frame_users(self):
		pass

	def _frame_mobs(self):
		pass

	def _frame_nps(self):
		pass

	def _frame_objects(self):
		pass

	def _frame_locations(self):
		pass

	def _frame_items(self):
		pass

	def _frame_sleep(self, frame_start):
		frame_time = time.time() - frame_start
		if frame_time < self.frame_ms_time:
			frame_time_remaining_ms = round(self.frame_ms_time - frame_time, 4)
			frame_time_remaining_min = float(frame_time_remaining_ms / 1000)
			time.sleep(frame_time_remaining_min)

	def _tps_counter(self, frame_start):
		delta = time.time() - frame_start
		if delta <= 0:
			delta = 1 / 10 ** 10
		try:
			self.FPS = int(math.ceil(1.0 / delta))
			if self.FPS > self.frames_per_second:
				self.FPS = self.frames_per_second
		except:
			pass

	def new_msg(self, data, _id):
		#pass
		print('new msg')
		print(data)
		print(_id)

	def new_client(self, _id):
		#pass
		print('new client')
		print(_id)
	




class Socket_Component:

	clients = []

	id_counter = 0

	listen_count = 5

	accept_per_frame = 1

	def __init__(self, server, host, port):
		self.server = server
		self.socket = socket.socket()
		self.socket.setblocking(0)
		self.socket.bind((host, port))
		self.socket.listen(self.listen_count)

	def frame(self):
		self._frame_listen()
		self._frame_recv()

	def _frame_listen(self):
		for i in range(self.accept_per_frame):
			try:
				conn, addr = self.socket.accept()
			except:
				conn, addr = 0, 0
			if not conn and not addr:
				return
			self._new_client(conn, addr)

	def _frame_recv(self):
		for _client in self.clients:
			if not _client['valid']:
				self.handshake(_client)
			else:
				self.read_msg(_client)

	def handshake(self, _client):
		_conn = _client['handler']
		try:
			data = _conn.recv(1024)
		except:
			data = False
		if not data:
			return
		headers = self.read_http_headers(data)
		if headers:
			_client['valid'] = True
		key = headers['Sec-WebSocket-Key']
		output_headers = self.response_headers(key).encode('utf-8')
		_conn.send(output_headers)

	def read_msg(self, _client):
		_conn = _client['handler']
		try:
			data = _conn.recv(4096)
		except:
			data = False
		if not data:
			return
		_id = _client['id']
		self.server.new_msg(data, _id)

	def _new_client(self, _conn, _addr):
		self.id_counter += 1
		self.clients.append({
			'id': self.id_counter,
			'handler': _conn,
			'addr': _addr,
			'valid': False,
		})
		self.server.new_client(self.id_counter)

	def send_user(self, data, client):
		self._send(data, client)

	def send_all(self, data):
		self._send(data)

	def _send(self, data = {}, _client = False):
		if not _client:
			self.socket.sendall(data)
		else:
			conn = _client['handler']
			conn.send(data)

	def read_http_headers(self, data):
		if not data:
			return

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

		return obj

	def response_headers(self, key):
		return \
		  'HTTP/1.1 101 Switching Protocols\r\n'\
		  'Upgrade: websocket\r\n'			  \
		  'Connection: Upgrade\r\n'			 \
		  'Sec-WebSocket-Accept: %s\r\n'		\
		  '\r\n' % self.calculate_response_key(key)

	def calculate_response_key(self, key):
		GUID = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
		hash = sha1(key.encode() + GUID.encode())
		response_key = b64encode(hash.digest()).strip()
		return response_key.decode('ASCII')

class Users:

	users = []

	def __init__(self):
		pass

	def load_users(self):
		pass

	def append(self, id, api_key):
		pass

	def remove(self, id):
		pass

class User:

	max_hp = 100
	max_mp = 100

	def __init__(self, id = False, api_key = False):

		self.conn_id = _id
		self.api_key = _api_key
		self.online = True if _id and _api_key else False

		data = self.load_data()

		if data:
			self.user_id = data['id']
			self.location = data['location']
			#characteristics
			self.hp = data['hp']
			self.mp = data['mp']
			#
			self.items = data['items']

	def load_data(self):
		return {
			'id': random(64),
			'location': random(16),

			'hp': self.max_hp,
			'mp': self.max_mp,

			'items': {

			},
		}

	def random(self, len = 8, alphabet = string.ascii_uppercase + string.digits):
		return ''.join(secrets.choice(alphabet) for _ in range(len))