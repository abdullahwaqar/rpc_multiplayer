import socket
import pickle
from _thread import *
from player import Player

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

players = [Player(0, 0, 50, 50, (255, 0, 0)), Player(100, 100, 50, 50, (0, 0, 255))]

def threaded_client(conn, player):
    #* Run as long as the client is connected
    conn.send(pickle.dumps(players[player]))
    reply = ''
    while True:
        try:
            #* Recv data
            data = pickle.loads(conn.recv(2048))
            #* Update player position
            players[player] = data

            if not data:
                print('Disconnected')
                break
            else:
                #* If player1 then send the position of player 0 else send player 0 player's 1 pos
                if player == 1:
                    reply = players[0]
                else:
                    reply = players[1]
                print('Received: ', data)
                print('Sending: ', reply)
            conn.sendall(pickle.dumps(reply))
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