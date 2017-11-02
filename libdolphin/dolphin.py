#!/usr/bin/env python3

import socket
import os
import sys
import struct
import subprocess
import binascii
import yaml
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

        self.controller2 = Controller("/home/squid/.local/share/dolphin-emu/Pipes/Bot2")
        self.game.sock_bind()

if __name__ == "__main__":
    dolphin = Dolphin()
    dolphin.run()
    game = dolphin.game
    try:
        while True:
            game.update()
            game.print_state()
            if game.players[1].static_block_data['state'] == 2:
                #controller2.press_button(Buttons.A.value, Buttons.press.value)
                #controller2.set_stick(Buttons.main_stick.value, "0", "0.5")
                dolphin.controller2.set_trigger("L", "1")

    except:
        dolphin.process.kill()
        raise
