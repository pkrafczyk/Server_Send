#!/usr/bin/env phyton3
import socket
import sys
import zipfile
from pathlib import Path

def client(host, port , zip_file):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_adrresse = (host, port)
    print('connectiing to {} port {}'.format(*server_adrresse))
    sock.connect(server_adrresse)
    try:
        with open(zip_file, 'rb') as zip_file:

            print('sending {!r}'.format(zip_file))
            sock.sendall(zip_file.read())
            amount_received =0
            amount_expected = len(zip_file.read())

            while amount_received < amount_expected:
                data = sock.recv(4096)
                amount_received += len(data)
                print('received {!r}'.format(data))
    finally:
        print('closing socket')
        sock.close()
        #return 0
    return 0



def zipkomprimireren(zip_file):

  with zipfile.ZipFile(zip_file + ".zip", "w", zipfile.ZIP_DEFLATED) as zipf:
    zipf.write(zip_file)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('usage: python client2.py IP PORT file')
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 10000
    zipfile = sys.argv[3]
    zipkomprimireren(zipfile)
    client(host, port,zipfile +".zip")