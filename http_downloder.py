import socket
import sys
import shutil
  import os
def server(local, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_adrresse = (local, port)
    sock.bind(server_adrresse)
    sock.listen(5)

    try:
        while True :
            connection, client_addresse =sock.accept()
            request =connection.resv(1024).decode("utf 8")
            if request:
                print(f"\n--- Anfrage von {connection} ---")
                print(request.split("\r\n")[0]) # Nur die erste Zeile (z.B. GET / HTTP/1.1)

        # Rohe HTTP-Antwort (Response) manuell aufbauen
            html_body = "<h1>Hallo aus dem rohen Python-Socket!</h1>"

            http_response = (
                "HTTP/1.1 200 OK\r\n"                    # Status-Zeil
                "Content-Type: text/html; charset=utf-8\r\n" # Header
                f"Content-Length: {len(html_body.encode('utf-8'))}\r\n" # Header 2
                "Connection: close\r\n"                  # Header
                "\r\n"                                   # Leere Zeile trennt Header und Body
                f"{html_body}"                           # Der eigentliche Inhalt
                )
            connection.sendall(http_response.endcode("utf 8"))
            connection.close()
    finally:
        print('closing connection')

#except KeyboardInterrupt:
        sock.close()

if __name__ == '__main__':
  if len(sys.argv)<2:
    print('usage: python server_abfrage2.py IP PORT ')
    sys.exit(1)

  host = sys.argv[1]
  port = int(sys.argv[2]) if len(sys.argv)>2 else 10000
  #zip_file = sys.argv[3]
  server(host, port)



def hat_genug_speicher(ziel_pfad, dateigroesse_bytes):
      # Statistiken des Laufwerks abrufen
      freier_speicher = shutil.disk_usage(ziel_pfad).free

      # Prüfen, ob der freie Speicher größer ist als die benötigte Dateigröße
      if freier_speicher >= dateigroesse_bytes:
          return True
      else:
          return False

def voifdad():
  # Beispiel: Wir prüfen das aktuelle Verzeichnis
  pfad = "."
  # Beispiel-Dateigröße: 500 MB in Byte (500 * 1024 * 1024)
  benoetigte_bytes = 524288000

  if hat_genug_speicher(pfad, benoetigte_bytes):
      print("Es ist genügend Speicherplatz vorhanden. Download kann starten.")
  else:
      print("Warnung: Nicht genügend Speicherplatz auf der Festplatte.")