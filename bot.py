import socket
import os
import sys
import subprocess

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
        print(data)
    except socket.timeout:
        pass
