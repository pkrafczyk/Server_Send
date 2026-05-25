#!/usr/bin/env phyton3
import socket
import sys
def server(local,port):
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  server_adrresse = (local, port)
  print('start Sever {} port {}'.format(*server_adrresse))
  sock.bind(server_adrresse)
  sock.listen(1)
  while True:
    print('waiting for a conatct ')
    connection, client_addresse =sock.accept()
    try:
      print('connection from ', client_addresse)

      while True:
        data = connection.recv(16)
        print('received {!r}'.format(data))
        if data:
          print(' sending data back to client')
          connection.sendall(data)
        else:
          print('no data from',client_addresse)
          break

    finally:
      print('closing connection')
      connection.close()
      #return 0
  #return 1

if __name__ == '__main__':
  if len(sys.argv)<2:
    print('usage: python server_abfrage2.py IP PORT')
    sys.exit(1)

  host = sys.argv[1]
  port = int(sys.argv[2]) if len(sys.argv)>2 else 10000
  server(host, port)
