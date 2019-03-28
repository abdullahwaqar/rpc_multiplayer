import socket
from _thread import *

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

def read_pos(str_buffer):
    str_buffer = str_buffer.split(',')
    return int(str_buffer[0]), int(str_buffer[1])

def make_pos(tup):
    return str(tup[0]) + ',' + str(tup[1])

pos = [(0, 0), (100, 100)]

def threaded_client(conn, player):
    #* Run as long as the client is connected
    conn.send(str.encode(make_pos(pos[player])))
    reply = ''
    while True:
        try:
            #* Recv data
            data = read_pos(conn.recv(2048).decode())
            #* Update player position
            pos[player] = data

            if not data:
                print('Disconnected')
                break
            else:
                #* If player1 then send the position of player 0 else send player 0 player's 1 pos
                if player == 1:
                    reply = pos[0]
                else:
                    reply = pos[1]
                print('Received: ', data)
                print('Sending: ', reply)
            conn.sendall(str.encode(make_pos(reply)))
        except:
            break
    print('Lost Connection')
    conn.close()

current_player = 0

while True:
    #* Accept the incoming connections
    conn, addr = s.accept()
    print('Connected to: ', addr)

    start_new_thread(threaded_client, (conn, current_player))
    current_player += 1