#!/usr/bin/env python3

from pathlib import Path
import copy
import configparser
import socket
import os
import sys
import struct
import subprocess
from shutil import copyfile
import time
import datetime
import binascii
import yaml
import libdolphin.melee.menu_helper
import libdolphin.melee.techskill
import libdolphin.melee.gamestate
from controller import *

class Dolphin:
    def __init__(self, game_path=str(Path.home()) + "/.local/share/dolphin-emu/Games/smash-1.02.iso", dolphin_path="dolphin-emu", bot_ports = [2], human_ports = [1]):
        self.bot_ports = bot_ports
        self.human_ports = human_ports
        self.game_path = game_path
        self.dolphin_path = dolphin_path

        self.dolphin_dir = str(Path.home()) + "/.local/share/dolphin-emu/"
        self.sock_path = self.dolphin_dir + "/MemoryWatcher/MemoryWatcher"
        self.locations_path = self.dolphin_dir + "/MemoryWatcher/Locations.txt"
        self.pipes_path = self.dolphin_dir + "/Pipes/"
        self.config_dir = str(Path.home()) + "/.config/dolphin-emu/"
        self.config_path = self.config_dir + "/Dolphin.ini"

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

    # Configure the dolphin emulator
    def configure(self):
        dolphin_config = configparser.ConfigParser()
        dolphin_config.read(self.config_path)
        try:
            dolphin_config['Core']['enablecheats'] = "True"
        except KeyError:
            dolphin_config['Core'] = {}
            dolphin_config['Core']['enablecheats'] = "True"

        with open(self.config_path, 'w') as f:
            dolphin_config.write(f)

        #copyfile(os.path.dirname(__file__) + "/melee/data/GCPadNew.ini", self.config_dir + "/GCPadNew.ini")
        gcpadnew_config = configparser.ConfigParser()
        controller_config = configparser.ConfigParser()
        controller_config.read(os.path.dirname(__file__) + "/melee/data/GCPadNew.ini")

        for i in self.bot_ports:
            gcpadnew_config['GCPad' + str(i)] = controller_config['GCPad']
            gcpadnew_config['GCPad' + str(i)]['device'] = "Pipe/0/Bot" + str(i)
            try:
                os.mkfifo(self.pipes_path + "Bot" + str(i + 1))
            except:
                pass

        for i in self.human_ports:
            gcpadnew_config['GCPad' + str(i)] = controller_config['Keyboard']

        with open(self.config_dir + "/GCPadNew.ini", 'w') as f:
            gcpadnew_config.write(f)

    def run(self):
        self.configure()
        self.process = subprocess.Popen(self.dolphin_path + " -e " + self.game_path, shell=True)

        for i in self.bot_ports:
            self.game.players[i-1].controller = Controller(str(Path.home()) + "/.local/share/dolphin-emu/Pipes/Bot" + str(i))
        self.game.sock_bind()

    def next_input(self, frame_diff):
        for i in self.game.players:
            if i.controller:
                i.controller.next_input(frame_diff)

if __name__ == "__main__":
    try:
        character = sys.argv[1]
    except IndexError:
        character = "fox"
    dolphin = Dolphin(dolphin_path="dolphin-emu")
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
                    libdolphin.melee.menu_helper.select_character(game, character,
                            game.players[1])

            if game.players[1].static_block_data['state'] == 2:
                if game_started == False:
                    game.players[1].controller.empty_queue()
                    game.players[1].controller.set_stick(libdolphin.controller.Buttons.main_stick.value,
                            0.5, 0.5, 180)
                    game_started = True

                if game.players[1].controller.input_queue.empty():
                    if character == "fox":
                        libdolphin.melee.techskill.shine(game.players[1])
                    libdolphin.melee.techskill.wavedash("left",
                            game.players[1])
                    if character == "fox":
                        libdolphin.melee.techskill.shine(game.players[1])
                    libdolphin.melee.techskill.wavedash("right",
                            game.players[1])

            dolphin.next_input(game.global_data['frame_num'] - prev_frame)

    except:
        dolphin.process.kill()
        raise
