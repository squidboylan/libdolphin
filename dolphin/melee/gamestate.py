import socket
from melee.player import Player

class GameState:
    def __init__(self, sock_path):
        self.players = []
        self.sock_path = sock_path
        for i in range(4):
            self.players.append(Player(i+1))

    def sock_bind(self):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        self.sock.bind(self.sock_path)

    def update(self):
        data = self.sock.recvfrom(9096)[0].decode('utf-8').splitlines()
        for i in range(4):
            self.players[i].update(data)

    def print_state(self):
        for i in range(4):
            self.players[i].print_data()
