import json
import os
import traceback
from pathlib import Path
import socket
import sys
import shutil
import urllib.request
#import docker
import os
from threading import Thread
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
download_status = {
    "prozent": 0,
    "geladen": "0.0",
    "gesamt": "0.0"
}
def fortschricht(geladene_bytes, gesamt_groesse,connection):
    #heruntergeladen = block_anzahl * block_groesse
    global download_status
    if gesamt_groesse > 0:
        prozent = min(100, int(geladene_bytes * 100 / gesamt_groesse))
        mb_geladen = geladene_bytes / (1024 * 1024)
        mb_gesamt = gesamt_groesse / (1024 * 1024)
        #header = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n"
        #connection.sendall(header.encode('utf-8'))
       # html_snippet = (
      #      f"<script>"
       #     f"document.body.innerHTML = '"
       #     f"<div style=\"font-family: sans-serif; margin: 20px;\">"
       #     f"<h3>Download-Status: {prozent}%</h3>"
       #     f"<p>{mb_geladen:.1f} MB von {mb_gesamt:.1f} MB geladen</p>"
       #     f"</div>';"
       #     f"</script>"
        #)
        download_status["prozent"] = prozent
        download_status["geladen"] = f"{mb_geladen:.1f}"
        download_status["gesamt"] = f"{mb_gesamt:.1f}"
        print(download_status["geladen"])
        print(download_status["gesamt"])
        # Im Chunked-Verfahren muss erst die Länge (Hex) und dann der Inhalt gesendet werden
        #chunk = f"{len(html_snippet):X}\r\n{html_snippet}\r\n"
        #connection.sendall(chunk.encode('utf-8'))
        #status(prozent,mb_geladen,mb_gesamt)
        status=f"\rFortschritt: {prozent}% ({mb_geladen:.1f} MB von {mb_gesamt:.1f} MB)"
        #try:
         #   connection.sendall((chunk).encode("utf-8"))
        #except Exception as e:
         #   pass
        sys.stdout.write(status)
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
def download_hintergrund(url, end, connection):
    try:
        print("Downloading hintergrund")
        if hat_genug_speicher(url) == 1:

            with urllib.request.urlopen(url) as response:
                gesamt_groesse = int(response.headers.get('Content-Length', 0))

                dateiname = url.split("/")[3] + end
            # Rohe HTTP-Antwort (Response) manuell aufbauen
            # html_body = "<h1>Hallo aus dem rohen Python-Socket!</h1>"
            # herunterladen(url)
                http_response = (
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: application/octet-stream\r\n"
                    f"Content-Disposition: attachment; filename=\"{dateiname}\"\r\n"
                    f"Content-Length: {gesamt_groesse}\r\n"
                    "Connection: close\r\n"
                    "Cache-Control: no-store, no-cache, must-revalidate\r\n\r\n"
                )
                connection.sendall(http_response.encode("utf 8"))
                geladene_bytes = 0
                chunk_size = 65536
                while True:
                    chunk = response.read(chunk_size)
                    if not chunk:
                        break

                    connection.sendall(chunk)
                    geladene_bytes += len(chunk)
                    fortschricht(geladene_bytes, gesamt_groesse, connection)

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
        print(f"\nFehler im Download-Thread: {e}")
        traceback.print_exc()
    finally:
        try:
            connection.close()
            print("\nDownload-Verbindung geschlossen.")
        except:
            pass
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
                    elif "GET /download" in request:
                        print("start download-Theard")
                        download_thread = Thread(target=download_hintergrund, args=(url, end, connection))
                        download_thread.start()
                        # connection.close()
                    elif "GET /status" in request:
                        json_data = json.dumps(download_status)
                        response = (
                            "HTTP/1.1 200 OK\r\n"
                            "Content-Type: application/json\r\n"
                            f"Content-Length: {len(json_data)}\r\n"
                            "Connection: close\r\n\r\n"
                            f"{json_data}"
                        )
                        connection.sendall(response.encode('utf-8'))
                        connection.close()
                    elif "GET /" in request:
                        html_gui = """HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\nConnection: close\r\n\r\n
                            <!DOCTYPE html>
                                <html>
                                <head>
                                    <meta charset="utf-8">
                                    <style>body { font-family: sans-serif; margin: 40px; text-align: center; }</style>
                                    <script>
                                        function checkStatus() {
                                            fetch('/status').then(r => r.json()).then(data => {
                                            document.getElementById('progress').innerText = data.prozent + '%';
                                            document.getElementById('details').innerText = data.geladen + ' MB von ' + data.gesamt + ' MB geladen';
                                        }).catch(e => console.error(e));
                                        setInterval(checkStatus, 1000);
                                        }
                                        function starteDownload() {
                                            window.location.href = '/download'; // Nutzt den Browser-Download
                                            setInterval(checkStatus, 1000);
                                        }
                                    </script>
                                </head>
                                <body>
                                        <div style=\"font-family: sans-serif; margin: 20px;\">
                                        <h3 id="progress">Download-Status:0%</h1>
                                        <p><button onclick="starteDownload()" style="padding:10px 20px; font-size:16px;">Download starten</button></p>
                                        <p id="details">0.0 MB von 0.0 MB geladen</p>
                                </body>
                        </html>"""
                        connection.sendall(html_gui.encode("utf-8"))
                        connection.close()


                    else:
                        connection.close()
            except Exception as e:
                print(f"\nFehler beim Streaming: {e}")
                try:
                    connection.close()
                except:
                    pass
            #finally:
                #connection.close()

    except KeyboardInterrupt:
        print('closing connection')
        sock.close()

if __name__ == '__main__':
  if len(sys.argv)<5:
    print('usage: python http_doenloder.py IP PORT URL ENDUNG')
    sys.exit(1)


  host = sys.argv[1]
  port = int(sys.argv[2]) if len(sys.argv)>2 else 10000
  url = sys.argv[3]
  end = sys.argv[4]
  #zip_file = sys.argv[3]
  server(host, port ,url, end)
  #url = "http://speedtest.belwue.net/random-1G"




