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
try:
    os.unlink(sock_path)
except:
    pass

game = melee.gamestate.GameState(sock_path)
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
