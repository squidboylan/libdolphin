import socket
from melee.player import Player
import struct
import yaml
import binascii

class GameState:
    def __init__(self, sock_path):
        self.players = []
        self.sock_path = sock_path
        for i in range(4):
            self.players.append(Player(i+1))

        with open("melee/data/globals.yaml", "r") as f:
            self.global_data_config = yaml.load(f.read())

        self.global_data = {}
        for i in self.global_data_config.keys():
            self.global_data[self.global_data_config[i]["name"]] = 0

    def sock_bind(self):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        self.sock.bind(self.sock_path)

    def update(self):
        data = self.sock.recvfrom(9096)[0].decode('utf-8').splitlines()
        if data[0] in self.global_data_config.keys():
            val = data[1].strip('\x00').zfill(8)
            val = struct.unpack(self.global_data_config[data[0]]['type'],
                    binascii.unhexlify(val))[self.global_data_config[data[0]]['index']]
            self.global_data[self.global_data_config[data[0]]['name']] = val
        else:
            for i in range(4):
                self.players[i].update(data)

    def print_state(self):
        for i in range(4):
            self.players[i].print_data()
