import socket
from _thread import *
import sys

server = '192.168.8.104'
port = 9000

#* Creating a socket connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#* Bind the socket to the port and server adress
try:
    s.bind((server, port))
except socket.error as e:
    str(e)

#* Number of clients that can connects the server
#* @param: 2 clients
s.listen(2)
print('Waiting for a connection, Server Started')

def threaded_client(conn):
    #* Run as long as the client is connected
    reply = ''
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode('utf-8')

            if not data:
                print('Disconnected')
                break
            else:
                print('Received: ', reply)
                print('Sending: ', reply)
            conn.sendall(str.encode(reply))
        except:
            break
    print('Lost Connection')
    conn.close()

while True:
    #* Accept the incoming connections
    conn, addr = s.accept()
    print('Connected to: ', addr)

    start_new_thread(threaded_client, (conn))