import socket
import pickle
from _thread import *
from game import Game

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
s.listen()
print('Waiting for a connection, Server Started')

connected = set()
games = {}
id_count = 0

def threaded_client(conn, p, game_id):
    global id_count
    conn.send(str.encode(str(p)))
    reply =''

    while True:
        try:
            data = conn.recv(4096).decode()

            if gameId in games:
                game = games[game_id]

                if not data:
                    break
                elif data == 'reset':
                    game.reset()
                elif data != 'get:':
                    game.play(p, data)

                reply = game
                conn.sendall(pickle.dumps(reply))
            else:
                break
        except:
            break

    print('Lost Connection')
    try:
        del games[game_id]
        print('Closing game', game_id)
    except:
        pass
    id_count -= 1
    conn.close()

while True:
    #* Accept the incoming connections
    conn, addr = s.accept()
    print('Connected to: ', addr)

    id_count += 1
    p = 0
    game_id = (id_count - 1) / 2
    if id_count % 2 == 1:
        games[game_id] = Game(game_id)
        print('Creating new game...')
    else:
        games[game_id].ready = True
        p = 1
    start_new_thread(threaded_client, (conn, p, game_id))