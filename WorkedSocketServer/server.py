from websocket_server import WebsocketServer
import json
from pprint import pprint


class Game:

	users = []
	locations = []

	def __init__(self, _port):
		self.server = WebsocketServer(_port)
		self.server.set_fn_new_client(self.new_client)
		self.server.set_fn_client_left(self.client_left)
		self.server.set_fn_message_received(self.message_received)
		self.server.run_forever()

	# Called for every client connecting (after handshake)
	def new_client(self, client, server):
		print("New client connected and was given id %d" % client['id'])
		server.send_message_to_all("Hey all, a new client has joined us")
		server.send_message(client, 'Welcome');
		pprint(client['headers'])
		#clients_out = Game.json_encode(Game.get_clients(server.clients))
		#server.send_message_to_all(clients_out)


	# Called for every client disconnecting
	def client_left(self, client, server):
		print("Client(%d) disconnected" % client['id'])


	# Called when a client sends a message
	def message_received(self, client, server, message):
		#print(type(message))
		#pprint(message)
		if len(message) > 200:
			message = message[:200]+'..'
		print("Client(%d) said: %s" % (client['id'], message))









	def _add_user(self, client, key):
		user = {
			'API_KEY': key,
			'CLIENT': client
		}
		data = self.preload_data('')
		self.users.append(user)




	def json_encode(arr):
		return json.dumps(arr)

	def get_clients(_clients):
		clients = []
		for _client in _clients:
			id = _client['id']
			addr = _client['address']
			clients.append({
				'id':id, 
				'address':addr
			})
		return clients

if __name__ == '__main__':
	game = Game(5554)


"""
class Users():

	USER_LIST = {}

	def __init__(self):
		pass

	def append(_socket_client):
		id = _socket_client['id']
		user = User(_socket_client)
		USER_LIST[id] = user

	def remove(self, _socket_client):
		id = _socket_client['id']
		if(self.USER_LIST[id]):
			del(self.USER_LIST[id])

class User():

	def __init__(self, _socket_client):
		API_KEY = _socket_client['API_KEY']
		user_data = self.load_data(API_KEY)
		user = {
			'socket_client': _socket_client,
			'location': user_data['Location'],
			'HP': user_data['HP'],
			'MP': user_data['MP'],

		}
"""