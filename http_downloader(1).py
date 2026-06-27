import json
import os
from pathlib import Path
import socket
import sys
import shutil
import urllib.request
#import docker
import os

import render_template
import requests
#from fastapi import FastAPI
#from fastapi.staticfiles import StaticFiles
#from fastapi.responses import FileResponse
#from flask import Flask, render_template, Response
#app = FastAPI()

#@app.get("/")
#def serve_home():
 #   return FileResponse("templates/intex.html")

#@app.get('/status')
#def status(prozent,mb_geladen,mb_gesamt):
 #   return render_template('intex.html',
  #                         prozent=prozent,
   #                        geladen=mb_geladen,
    #                       gesamt=mb_gesamt)

def fortschricht(geladene_bytes, gesamt_groesse):
    #heruntergeladen = block_anzahl * block_groesse

    if gesamt_groesse > 0:
        prozent = min(100, int(geladene_bytes * 100 / gesamt_groesse))
        mb_geladen = geladene_bytes / (1024 * 1024)
        mb_gesamt = gesamt_groesse / (1024 * 1024)
        #status(prozent,mb_geladen,mb_gesamt)
        sys.stdout.write(f"\rFortschritt: {prozent}% ({mb_geladen:.1f} MB von {mb_gesamt:.1f} MB)")
        sys.stdout.flush()
def hat_genug_speicher(url):
    if os.name == 'nt':  # Windows
        #download_pfad = Path("C:/Downloads")
        download_pfad = Path.home() / "Downloads"
    else:  # Linux und andere (z.B. macOS)
        download_pfad = Path.home() / "Downloads"
    response = requests.head(url)
    file_size = int(response.headers.get('content-length', 0))
    free_space = shutil.disk_usage(download_pfad).free


    if free_space > file_size:
        print("Genug Speicherplatz vorhanden. Download startet...")
        return 1
    else:
        print("Zu wenig Speicherplatz!")
        return 0
def server(local, port,url, end):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_adrresse = (local, port)
    sock.bind(server_adrresse)
    sock.listen(5)
    print(f"http://{local}:{port}")

    try:
        print("Sever starten...")
        while True :
            connection, client_addresse =sock.accept()
            try:
                    request =connection.recv(1024).decode("utf 8")

                    print(f"\n--- Anfrage von {connection} ---")
                    print(request.split("\r\n")[0])  # Nur die erste Zeile (z.B. GET / HTTP/1.1)
                    if not request.strip():
                        connection.close()
                        continue
                    if "GET /favicon.ico" in request:
                        connection.sendall(b"HTTP/1.1 404 Not Found\r\nContent-Length: 0\r\n\r\n")
                        connection.close()
                        continue
                    if  hat_genug_speicher (url)==1:

                            with urllib.request.urlopen(url) as response:
                                gesamt_groesse =int(response.headers.get('Content-Length', 0))

                                dateiname = url.split("/")[3] + end
                        # Rohe HTTP-Antwort (Response) manuell aufbauen
                        #html_body = "<h1>Hallo aus dem rohen Python-Socket!</h1>"
                        #herunterladen(url)
                                http_response = (
                                    "HTTP/1.1 200 OK\r\n"                    # Status-Zeil
                                    "Content-Type: application/octet-stream\r\n"
                                    f"Content-Disposition: attachment; filename=\"{dateiname}\"\r\n"
                                    f"Content-Length: {gesamt_groesse}\r\n"
                                    "Connection: close\r\n"                  # Header
                                    "Cache-Control: no-store, no-cache, must-revalidate, max-age=0\r\n"  # Erzwingt immer Neu-Download
                                    "Pragma: no-cache\r\n"                                                # Für ältere HTTP/1.0 Clients
                                    "Expires: 0\r\n"  
                                    "\r\n"                                   # Leere Zeile trennt Header und Body
                                )
                                connection.sendall(http_response.encode("utf 8"))
                                geladene_bytes=0
                                chunk_size = 65536
                                while True:
                                    chunk = response.read(chunk_size)
                                    if not chunk:
                                        break

                                    connection.sendall(chunk)
                                    geladene_bytes += len(chunk)
                                    fortschricht(geladene_bytes,gesamt_groesse)
                    else:
                    # Antwort senden, falls nicht genug Speicherplatz vorhanden ist
                        error_response = (
                            "HTTP/1.1 507 Insufficient Storage\r\n"
                            "Content-Type: text/plain\r\n"
                            "Connection: close\r\n"
                            "\r\n"
                            "Server hat nicht genug Speicherplatz für diesen Download."
                        )
                        connection.sendall(error_response.encode("utf-8"))
            except Exception as e:
                print(f"\nFehler beim Streaming: {e}")
            finally:
                connection.close()

    except KeyboardInterrupt:
        print('closing connection')
        sock.close()

if __name__ == '__main__':
  if len(sys.argv)<5:
    print('usage: python http_doenloder.py IP PORT ')
    sys.exit(1)

  url = sys.argv[3]
  host = sys.argv[1]
  port = int(sys.argv[2]) if len(sys.argv)>2 else 10000
  end = sys.argv[4]
  #zip_file = sys.argv[3]
  server(host, port ,url, end)
  #url = "http://speedtest.belwue.net/random-1G"




