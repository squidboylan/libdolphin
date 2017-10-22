#!/usr/bin/env python3

import socket
import os
import sys
import struct
import subprocess
import binascii
import yaml

class MeleeState:
    def __init__(self):
        with open("memory.yaml", 'r') as stream:
            self.memory_meta = yaml.load(stream)

    # Load GC memory and convert to right type and print
    def process_memory(self, data):
        p = data[1].strip('\x00').zfill(8)
        processed_p = struct.unpack(self.memory_meta[data[0]]['type'],
                binascii.unhexlify(p))[int(self.memory_meta[data[0]]['elem'])]
        print(self.memory_meta[data[0]]['name'] + ": " + str(processed_p))

sock_path = "/home/squid/.local/share/dolphin-emu/MemoryWatcher/MemoryWatcher"
try:
    os.unlink(sock_path)
except:
    pass

process = subprocess.Popen("dolphin-emu")

sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
sock.bind(sock_path)

while True:
    try:
        data = sock.recvfrom(9096)[0].decode('utf-8').splitlines()
        m = MeleeState()
        m.process_memory(data)
    except socket.timeout:
        pass
