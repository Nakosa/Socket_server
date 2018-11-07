import asyncio
import websockets

async def echo(ws, path):
	async for message in ws:
		await ws.send(message)

server = websockets.serve(echo, 'localhost', 5554)
asyncio.get_event_loop().run_until_complete(server)
asyncio.get_event_loop().run_forever()