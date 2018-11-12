import socket
from pprint import pprint

FIN	= 0x80
OPCODE = 0x0f
MASKED = 0x80
PAYLOAD_LEN = 0x7f
PAYLOAD_LEN_EXT16 = 0x7e
PAYLOAD_LEN_EXT64 = 0x7f

OPCODE_CONTINUATION = 0x0
OPCODE_TEXT		 = 0x1
OPCODE_BINARY	   = 0x2
OPCODE_CLOSE_CONN   = 0x8
OPCODE_PING		 = 0x9
OPCODE_PONG		 = 0xA

# create a raw socket and bind it to the public interface
s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
s.bind(('localhost', 5554))

# Include IP headers
s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
while True:
	msg, addr = s.recvfrom(65565)
	bytearr = bytearray(msg)

	b1, b2 = bytearr[0], bytearr[1]

	fin	= b1 & FIN
	opcode = b1 & OPCODE
	masked = b2 & MASKED
	payload_length = b2 & PAYLOAD_LEN

	print('fin')
	print(fin)
	print('opcode')
	print(opcode)
	print('masked')
	print(masked)
	print('payload_length')
	print(payload_length)

	if opcode == OPCODE_CLOSE_CONN:
		print("Client asked to close connection.")
		continue
	if not masked:
		print("Client must always be masked.")
		continue
	if opcode == OPCODE_CONTINUATION:
		print("Continuation frames are not supported.")
		continue
	elif opcode == OPCODE_BINARY:
		print("Binary frames are not supported.")
		continue
	elif opcode == OPCODE_TEXT:
		opcode_handler = '_message_received_'
	elif opcode == OPCODE_PING:
		opcode_handler = '_ping_received_'
	elif opcode == OPCODE_PONG:
		opcode_handler = '_pong_received_'
	else:
		print("Unknown opcode %#x." % opcode)
		continue
	"""
	if payload_length == 126:
		payload_length = struct.unpack(">H", self.rfile.read(2))[0]
	elif payload_length == 127:
		payload_length = struct.unpack(">Q", self.rfile.read(8))[0]

	masks = self.read_bytes(4)
	message_bytes = bytearray()
	for message_byte in self.read_bytes(payload_length):
		message_byte ^= masks[len(message_bytes) % 4]
		message_bytes.append(message_byte)
	"""
	print(opcode_handler)

	print(bytearr)
	print(len(bytearr))
	print(msg)
	print(len(msg))
	print(msg[0])
	print(msg[1])
	print(msg[2])
	print(msg[3])
	if int(addr[1]) != 0:
		print(msg.decode('utf-8'))