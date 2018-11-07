import socket

class GameServer():

	users = {}
	
	objects = {}
	mobs = {}
	nps = {}

	locations = {}

	FRAME_PER_SEC = 20

	ACCEPT_PER_FRAME = 100
	CONNECTIONS_LISTENING = 1000

	def __init__(self, _host = '127.0.0.1', _port = 5554):
		self.keep_alive = True
		self.timeout_frame = 1000/self.FRAME_PER_SEC
		print('timeout: ' + str(self.timeout_frame))

		self.id_counter = 0

		self.socket = socket.socket()
		self.socket.bind((_host, _port))
		self.socket.listen(self.CONNECTIONS_LISTENING)

	def run(self):
		while self.keep_alive:
			print('--------------- new frame  ---------------')
			print('')
			print('start accepting')
			for i in range(self.ACCEPT_PER_FRAME):
				print('new conn')
				conn, addr = self.socket.accept()
				self.id_counter += 1
				self.users[self.id_counter] = User(conn, addr)
			print('end accepting')
			print('')
			print('start accepting')
			for _user in self.users:
				_user.frame()
			print('end accepting')
			"""
			print('')
			print('start objects frame')
			for _object in self.objects:
				_object.frame()
			print('end objects frame')
			print('')
			print('start mobs frame')
			for _mob in self.mobs:
				_mob.frame()
			print('end mobs frame')
			print('')
			print('start nps frame')
			for _nps in self.nps:
				_nps.frame()
			print('end nps frame')
			print('')
			print('start location frame')
			for _location in self.locations:
				_location.frame()
			print('end location frame')
			"""
			print('')

	def _message_received(self):
		pass




class User:

	DATA_LEN = 4096

	def __init__(self, _conn, _addr):
		self.conn = _conn
		self.addr = _addr

		if self._is_new_user():
			self._load_new_data()
		else:
			self._load_data()

	def frame(self):
		data = self.conn.recv(self.DATA_LEN)
		print('new data from:')
		print(self.addr)
		print(type(data))
		pprint(data)

	def _is_new_user(self):
		return False

	def _load_new_data(self):
		pass

	def _load_data(self):
		pass

	def _get_data(self):
		pass
