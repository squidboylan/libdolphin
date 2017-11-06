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
import libdolphin.melee.menu_helper
import libdolphin.melee.techskill
import libdolphin.melee.gamestate
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

        self.game.players[1].controller = Controller("/home/squid/.local/share/dolphin-emu/Pipes/Bot2")
        self.game.sock_bind()

    def next_input(self, frame_diff):
        for i in self.game.players:
            if i.controller:
                i.controller.next_input(frame_diff)

if __name__ == "__main__":
    dolphin = Dolphin()
    dolphin.run()
    game = dolphin.game
    curr_time = None
    prev_time = None
    frame_time = 1000000/60.0
    sleep_time = None
    game_started = False
    try:
        while True:
            prev_frame = game.global_data['frame_num']

            game.update()
            game.print_state()


            if game.players[1].static_block_data['state'] == 0:
                if game.players[1].controller.input_queue.empty():
                    libdolphin.melee.menu_helper.select_character(game, "fox",
                            game.players[1])

            if game.players[1].static_block_data['state'] == 2:
                if game_started == False:
                    game.players[1].controller.empty_queue()
                    game.players[1].controller.set_stick(libdolphin.controller.Buttons.main_stick.value,
                            0.5, 0.5, 300)
                    #libdolphin.melee.techskill.shine(game.players[1])
                    game_started = True

                if game.players[1].controller.input_queue.empty():
                    libdolphin.melee.techskill.multishine(game.players[1])
                """
                    libdolphin.melee.techskill.wavedash("left",
                            game.players[1])
                    game.players[1].controller.set_stick(libdolphin.controller.Buttons.main_stick.value,
                            0.5, 0.5, 5)
                    libdolphin.melee.techskill.wavedash("right",
                            game.players[1])
                    game.players[1].controller.set_stick(libdolphin.controller.Buttons.main_stick.value,
                            0.5, 0.5, 5)
                """

            dolphin.next_input(game.global_data['frame_num'] - prev_frame)

    except:
        dolphin.process.kill()
        raise
