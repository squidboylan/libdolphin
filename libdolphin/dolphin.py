#!/usr/bin/env python3

import socket
import os
import sys
import struct
import subprocess
import time
import datetime
import binascii
import yaml
import libdolphin.melee.gamestate
import libdolphin.melee.techskill
from controller import *

class Dolphin:
    def __init__(self, game_path="/home/squid/.local/share/dolphin-emu/Games/smash-1.02.iso", dolphin_path="dolphin-emu"):
        self.sock_path = "/home/squid/.local/share/dolphin-emu/MemoryWatcher/MemoryWatcher"
        self.locations_path = "/home/squid/.local/share/dolphin-emu/MemoryWatcher/Locations.txt"
        self.game_path = game_path
        self.dolphin_path = dolphin_path
        try:
            os.unlink(self.sock_path)
        except:
            pass

        self.game = libdolphin.melee.gamestate.GameState(self.sock_path)
        locations_file_contents = self.game.generate_locations_file()

        with open(self.locations_path, 'w') as f:
            f.write(locations_file_contents)

        try:
            os.mkdir(os.path.split(self.sock_path)[0])
        except FileExistsError:
            pass

    def run(self):
        self.process = subprocess.Popen("dolphin-emu -e /home/squid/.local/share/dolphin-emu/Games/smash-1.02.iso", shell=True)

        self.controller2 = Controller("/home/squid/.local/share/dolphin-emu/Pipes/Bot2")
        self.game.sock_bind()

if __name__ == "__main__":
    dolphin = Dolphin()
    dolphin.run()
    game = dolphin.game
    curr_time = None
    prev_time = None
    frame_time = 1000000/60.0
    sleep_time = None
    try:
        while True:
            #prev_time = time.time()
            #prev_time = datetime.datetime.now()
            prev_frame = game.global_data['frame_num']

            game.update()

            if game.players[1].static_block_data['state'] == 2:
                if dolphin.controller2.input_queue.empty():
                    #dolphin.controller2.set_trigger("L", "1", 30)
                    #dolphin.controller2.set_trigger("L", "0", 30)
                    libdolphin.melee.techskill.wavedash("left",
                            dolphin.controller2,
                            game.players[1].character_data['jump_squat'])
                    libdolphin.melee.techskill.wavedash("right",
                            dolphin.controller2,
                            game.players[1].character_data['jump_squat'])

            dolphin.controller2.next_input(game.global_data['frame_num'] - prev_frame)

            #curr_time = datetime.datetime.now()
            #diff = curr_time - prev_time
            #sleep_time = (frame_time - diff.microseconds)/1000000.0
            #curr_time = time.time()
            #diff = curr_time - prev_time
            #sleep_time = frame_time - diff
            #print(sleep_time)
            #if sleep_time > 0:
                #time.sleep(sleep_time)

    except:
        dolphin.process.kill()
        raise
