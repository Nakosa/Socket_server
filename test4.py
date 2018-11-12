import select
import socket
from pprint import pprint

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('', 5554))
server_socket.listen(5)
print("Listening on port 5554")

read_list = [server_socket]
while True:
    readable, writable, errored = select.select(read_list, [], [])
    print('readable')
    pprint(readable)
    print('writable')
    pprint(writable)
    for s in readable:
        pprint(s)
        if s is server_socket:
            client_socket, address = server_socket.accept()
            read_list.append(client_socket)
            print("Connection from", address)
        else:
            data = s.recv(1024)
            if data:
                s.send(data)
            else:
                s.close()
                read_list.remove(s)