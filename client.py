#!/usr/bin/env phyton 3
import socket
import sys

def client(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_adrresse = (host, port)
    print('connectiing to {} port {}'.format(*server_adrresse))
    sock.connect(server_adrresse)
    try:
        message = b'This is the message . It will be repeated.'
        print('sending {!r}'.format(message))
        sock.sendall(message)
        amount_received =0
        amount_expected = len(message)

        while amount_received < amount_expected:
            data = sock.recv(16)
            amount_received += len(data)
            print('received {!r}'.format(data))
    finally:
        print('closing socket')
        sock.close()
        #return 0
    return 0