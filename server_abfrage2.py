#!/usr/bin/env phyton3
import socket
import sys
import zipfile
from pathlib import Path
def server(local, port, zip_file):
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
      with open(zip_file,"wb") as datei:
        while True:
          data = connection.recv(4096)
          print('received {!r}'.format(data))
          if data:
            print(' sending data back to client')
            connection.sendall(data)
          else:
            print('no data from',client_addresse)
            break
          datei.write(data)

    finally:
      print('closing connection')
      connection.close()
      #return 0
  #return 1


def zipentpacken(zip_file):
  zielorder = Path.cwd()
  with zipfile.ZipFile(zip_file + '.zip', 'r') as zipf:
    zipf.extractall(zielorder + '/' + zip_file)

if __name__ == '__main__':
  if len(sys.argv)<3:
    print('usage: python server_abfrage2.py IP PORT file')
    sys.exit(1)

  host = sys.argv[1]
  port = int(sys.argv[2]) if len(sys.argv)>2 else 10000
  zip_file = sys.argv[3]+'.zip'
  server(host, port,zip_file)
  zipentpacken(zip_file)
