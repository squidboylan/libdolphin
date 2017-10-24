#!/usr/bin/env python3

import socket
import os
import sys
import struct
import subprocess
import binascii
import yaml
import melee.gamestate

sock_path = "/home/squid/.local/share/dolphin-emu/MemoryWatcher/MemoryWatcher"
locations_path = "/home/squid/.local/share/dolphin-emu/MemoryWatcher/Locations.txt"
try:
    os.unlink(sock_path)
except:
    pass

game = melee.gamestate.GameState(sock_path)
locations_file_contents = game.generate_locations_file()

with open(locations_path, 'w') as f:
    f.write(locations_file_contents)

process = subprocess.Popen("dolphin-emu -e /home/squid/.local/share/dolphin-emu/Games/smash-1.02.iso", shell=True)
game.sock_bind()
if __name__ == "__main__":
    try:
        while True:
            game.update()
            #game.print_state()
    except:
        process.kill()
        raise
