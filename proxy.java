import java.io.*;
import java.net.*;
import java.nio.charset.StandardCharsets;

public class proxy {
    private static final int PORT = 80; 
    public static void main(String[] args) {
        try(ServerSocket serverSocket = new ServerSocket(Port)){
            while (true){
                Socket clientSocket = serverSocket.accept();
                new Thread(() -> handleClient(clientSocket)).start();
            }
        }
        catch (IOException e){
            System.err.println("Server-Fehler: " + e.getMessage());
        }
    }
    private static void handleClient(Socket clientSocket) {
         try (
            BufferedReader in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream(), StandardCharsets.UTF_8));
            OutputStream out = clientSocket.getOutputStream()
        ) {
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
}
