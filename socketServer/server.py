import multiprocessing as mp
from threading import Thread
import asyncio
import websockets

class Server():

  timeout_msg_wait = 30
  timeout_msg_pong = 10

  def __init__(self, _host = 'localhost', _port = 5554):
    self.host = _host
    self.port = _port
    self.socket = WebSocket('WebSocketServer', self.host, self.port, Server.echo)

  def loop(self):
    self.socket.start()
    #while True:
      #s = input()
      #print(s + ' 123')

  @staticmethod
  async def echo(ws, path):
    while True:
      try:
          msg = await asyncio.wait_for(ws.recv(), timeout=Server.timeout_msg_wait)
      except asyncio.TimeoutError:
        # No data in 20 seconds, check the connection.
        try:
            print('no data. pong')
            pong_waiter = await ws.ping()
            await asyncio.wait_for(pong_waiter, timeout=Server.timeout_msg_pong)
        except asyncio.TimeoutError:
            print('bad pong')
            # No response to ping in 10 seconds, disconnect.
            break
      else:
        #do something with msg
        print(msg)
        pass

class WebSocket(Thread):

  def __init__(self, _name, _host, _port, _f):
    Thread.__init__(self)
    self.name = _name
    self.host = _host
    self.port = _port
    self.func = _f

  def run(self):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    ws = websockets.serve(self.func, self.host, self.port)
    asyncio.get_event_loop().run_until_complete(ws)
    asyncio.get_event_loop().run_forever()