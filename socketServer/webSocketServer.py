import base64 
import hashlib 
import threading 
import socket

from pprint import pprint

class webSocketServer:
    def __init__(self, host, port, limit, **kwargs): 
     """ 
     Initialize websocket server. 
     :param host: Host name as IP address or text definition. 
     :param port: Port number, which server will listen. 
     :param limit: Limit of connections in queue. 
     :param kwargs: A dict of key/value pairs. It MAY contains:<br> 
     <b>onconnect</b> - function, called after client connected. 
     <b>handshake</b> - string, containing the handshake pattern. 
     <b>magic</b> - string, containing "magic" key, required for "handshake". 
     :type host: str 
     :type port: int 
     :type limit: int 
     :type kwargs: dict 
     """ 
     self.host = host 
     self.port = port 
     self.limit = limit 
     self.running = False 
     self.clients = [] 
     self.args = kwargs 

    def start(self): 
     self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
     self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
     self.socket.bind((self.host, self.port)) 
     self.socket.listen(self.limit) 
     self.running = True

     while self.running:
      print(len(self.clients))
      client, address = self.socket.accept() 
      if not self.running: break 

      self.handshake(client) 
      self.clients.append((client, address)) 

      onconnect = self.args.get("onconnect") 
      if callable(onconnect): onconnect(self, client, address) 

      threading.Thread(target=self.loop, args=(client, address)).start()

      #
      #
      #self.sendto(client,'123123')
      #
      #

     self.socket.close() 



    def stop(self):  
     self.running = False 


    def handshake(self, client): 
     handshake = 'HTTP/1.1 101 Switching Protocols\r\nConnection: Upgrade\r\nUpgrade: websocket\r\nSec-WebSocket-Accept: %s\r\n\r\n' 
     handshake = self.args.get('handshake', handshake) 
     magic = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11" 
     magic = self.args.get('magic', magic) 

     header = str(client.recv(1000)) 
     try: 
      res = header.index("Sec-WebSocket-Key") 
     except ValueError: 
      return False 
     key = header[res + 19: res + 19 + 24] 
     key += magic 
     key = hashlib.sha1(key.encode()) 
     key = base64.b64encode(key.digest()) 

     client.send(bytes((handshake % str(key,'utf-8')), 'utf-8')) 
     return True 



    def loop(self, client, address): 
     while True:
      message = ''.encode()
      m = client.recv(1) 
      while m != '': 
       message += m
       m = client.recv(1) 

      fin, text = self.decodeFrame(message) 

      if not fin:
        print('message from ')
        pprint(client)
        onmessage = self.args.get('onmessage') 
        if callable(onmessage): onmessage(self, client, text) 
      else:
        print('disconnect')
        pprint(client)
        self.clients.remove((client, address))
        ondisconnect = self.args.get('ondisconnect') 
        if callable(ondisconnect): ondisconnect(self, client, address) 
        client.close() 
        break 




    def decodeFrame(self, data): 
     if (len(data) == 0) or (data is None): 
      return True, None 
     fin = not(data[0] & 1) 
     if fin: 
      return fin, None 

     masked = not(data[1] & 1) 
     plen = data[1] - (128 if masked else 0) 

     mask_start = 2 
     if plen == 126: 
      mask_start = 4 
      plen = int.from_bytes(data[2:4], byteorder='sys.byteorder') 
     elif plen == 127: 
      mask_start = 10 
      plen = int.from_bytes(data[2:10], byteorder='sys.byteorder') 

     mask = data[mask_start:mask_start+4] 
     data = data[mask_start+4:mask_start+4+plen] 

     decoded = [] 
     i = 0 
     while i < len(data): 
      decoded.append(data[i]^mask[i%4]) 
      i+=1 

     text = str(bytearray(decoded), "utf-8") 
     return fin, text 



    def sendto(self, client, data, **kwargs):
     """ 
     Send <b>data</b> to <b>client</b>. <b>data</b> can be of type <i>str</i>, <i>bytes</i>, <i>bytearray</i>, <i>int</i>. 
     :param client: Client socket for data exchange. 
     :param data: Data, which will be sent to the client via <i>socket</i>. 
     :type client: socket 
     :type data: str|bytes|bytearray|int|float 
     """ 
     if type(data) == bytes or type(data) == bytearray: 
      frame = data 
     elif type(data) == str: 
      frame = bytes(data, kwargs.get('encoding', 'utf-8')) 
     elif type(data) == int or type(data) == float: 
      frame = bytes(str(data), kwargs.get('encoding', 'utf-8')) 
     else: 
      return None 

     framelen = len(frame) 
     head = bytes([0x81]) 

     if framelen < 126: 
      head += bytes(int.to_bytes(framelen, 1, 'big')) 
     elif 126 <= framelen < 0x10000: 
      head += bytes(126) 
      head += bytes(int.to_bytes(framelen, 2, 'big')) 
     else: 
      head += bytes(127) 
      head += bytes(int.to_bytes(framelen, 8, 'big')) 
     client.send(head + frame)