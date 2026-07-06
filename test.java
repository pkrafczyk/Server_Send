import java.io.*;
import java.net.*;
import java.nio.charset.StandardCharsets;

public class proxy {
    private static final int PORT = 80; // Interner Port der Container (A1)

    public static void main(String[] args) {
        // Der Proxy lauscht intern auf Port 80, da das Dockerfile 
        // ihn via "-p 8087:80" auf den Host-Port 8087 mappt.
        try (ServerSocket serverSocket = new ServerSocket(80)) {
            System.out.println("Proxy läuft und wartet auf Verbindungen...");

            while (true) {
                Socket clientSocket = serverSocket.accept();
                // Jede Anfrage in einem eigenen Thread bearbeiten
                new Thread(() -> handleClient(clientSocket)).start();
            }
        } catch (IOException e) {
            System.err.println("Server-Fehler: " + e.getMessage());
        }
    }

    private static void handleClient(Socket clientSocket) {
        try (
            BufferedReader in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream(), StandardCharsets.UTF_8));
            OutputStream out = clientSocket.getOutputStream()
        ) {
            // 1. Erste Zeile (Request-Line) lesen (z.B. "GET /appA/index.html HTTP/1.1")
            String requestLine = in.readLine();
            if (requestLine == null || requestLine.isEmpty()) return;

            String[] requestParts = requestLine.split(" ");
            if (requestParts.length < 3) return;

            String method = requestParts[0];
            String rawPath = requestParts[1];
            String httpVersion = requestParts[2];

            // 2. Routing und Pfadanpassung bestimmen (A3)
            String targetHost;
            String newPath;

            if (rawPath.startsWith("/appA")) {
                targetHost = "vs-app-a"; // Docker-DNS Hostname (A2)
                newPath = rawPath.substring(5); // "/appA" abschneiden
            } else if (rawPath.startsWith("/appB")) {
                targetHost = "vs-app-b";
                newPath = rawPath.substring(5); // "/appB" abschneiden
            } else {
                // Unbekannter Pfad -> 404 zurückgeben
                send404(out);
                return;
            }

            // Falls der Pfad nach dem Abschneiden leer ist, zu "/" machen
            if (newPath.isEmpty()) {
                newPath = "/";
            }

            // Neue Request-Line zusammenbauen
            StringBuilder modifiedRequest = new StringBuilder();
            modifiedRequest.append(method).append(" ").append(newPath).append(" ").append(httpVersion).append("\r\n");

            // 3. Verbleibende Header lesen und Host-Header anpassen (A4)
            String headerLine;
            while ((headerLine = in.readLine()) != null && !headerLine.isEmpty()) {
                if (headerLine.toLowerCase().startsWith("host:")) {
                    // Host-Header durch den Docker-Hostnamen ersetzen
                    modifiedRequest.append("Host: ").append(targetHost).append("\r\n");
                } else {
                    modifiedRequest.append(headerLine).append("\r\n");
                }
            }
            // Ende der HTTP-Header markieren
            modifiedRequest.append("\r\n");

            // 4. Verbindung zur Ziel-Anwendung aufbauen und modifizierten Request senden
            try (
                Socket targetSocket = new Socket(targetHost, PORT);
                OutputStream targetOut = targetSocket.getOutputStream();
                InputStream targetIn = targetSocket.getInputStream()
            ) {
                // Request an App senden
                targetOut.write(modifiedRequest.toString().getBytes(StandardCharsets.UTF_8));
                targetOut.flush();

                // 5. Antwort der Anwendung eins-zu-eins an den Client streamen (Byte-Ebene)
                byte[] buffer = new byte[8192];
                int bytesRead;
                while ((bytesRead = targetIn.read(buffer)) != -1) {
                    out.write(buffer, 0, bytesRead);
                }
                out.flush();
            }

        } catch (IOException e) {
            System.err.println("Fehler bei der Client-Verarbeitung: " + e.getMessage());
        } finally {
            try {
                clientSocket.close();
            } catch (IOException e) {
                System.err.println("Fehler beim Schließen des Client-Sockets: " + e.getMessage());
            }
        }
    }

    private static void send404(OutputStream out) throws IOException {
        String response = "HTTP/1.1 404 Not Found\r\n" +
                          "Content-Type: text/plain; charset=UTF-8\r\n" +
                          "Content-Length: 31\r\n" +
                          "\r\n" +
                          "404 Not Found: Proxy-Routing Fehler";
        out.write(response.getBytes(StandardCharsets.UTF_8));
        out.flush();
    }
}

