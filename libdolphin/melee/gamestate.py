import socket
from libdolphin.melee.player import Player
from libdolphin.melee.stage import Stage
import struct
import yaml
import binascii
import os

class GameState:
    #Initialize the global data section
    def __init__(self, sock_path):
        self.players = []
        self.sock_path = sock_path
        for i in range(4):
            self.players.append(Player(i+1))

        self.stage = Stage()

        with open(os.path.dirname(__file__) + "/data/globals.yaml", "r") as f:
            self.global_data_config = yaml.load(f.read())

        #Initialize the global_data dict to use names as keys instead of
        #addresses as configured in the yaml file
        self.global_data = {}
        for i in self.global_data_config.keys():
            for j in self.global_data_config[i]:
                self.global_data[j["name"]] = 0

   #Bind to the socket for reading from later
    def sock_bind(self):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        self.sock.bind(self.sock_path)

    #Read from the socket and upate the appropriate dictionaries
    def update(self):
        #Read from the socket
        while True:
            data = self.sock.recvfrom(9096)[0].decode('utf-8').splitlines()

            #If the address of the data is in the global data section, update the
            #global data, else update the players
            if data[0] in self.global_data_config:
                val = data[1].strip('\x00').zfill(8)
                for i in self.global_data_config[data[0]]:
                    val_tmp = struct.unpack(i['type'], binascii.unhexlify(val))[i['index']]
                    self.global_data[i['name']] = val_tmp

                    # If the frame has incrememnted return so logic can process
                    # the new frame
                    if i['name'] == "frame_num":
                        return

            r = self.stage.update(data)
            if r == 1:
                continue

            else:
                for i in range(4):
                    r = self.players[i].update(data)
                    if r == 1:
                        break


    # Generate the locations.txt file contents
    def generate_locations_file(self):
        contents = "#START OF GLOBAL DATA\n"
        for i in self.global_data_config.keys():
            contents += i + '\n'

        contents = self.stage.generate_locations_file(contents)

        for i in range(4):
            contents = self.players[i].generate_locations_file(contents)

        return contents

    #Print out the values scraped from the emulator, this is for debugging
    #purposes, has little to no use in an actual program
    def print_state(self):
        print(self.global_data)
        self.stage.print_data()
        for i in range(4):
            self.players[i].print_data()
