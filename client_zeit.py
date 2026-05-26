#!/usr/bin/env phyton3
import socket
import sys
from datetime import datetime

def client(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_adrresse = (host, port)
    print('connectiing to {} port {}'.format(*server_adrresse))

    try:
        sock.connect(server_adrresse)
        sock.sendto(b'',server_adrresse)
        data = sock.recv(1024)
        zeit =data.decode("utf-8").strip()
        print('received {!r}'.format(zeit))
        zeitdaten = zeit.split()
        print(' {!r}'.format(str(zeitdaten[1]) +" "+str(zeitdaten[2])))

    finally:
        print('closing socket')
        sock.close()
        #return 0
    return 0

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print('usage: python client_zeit.py IP PORT ')
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 10000
    client(host, port)