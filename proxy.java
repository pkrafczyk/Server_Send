import java.io.*;
import java.net.*;
import java.nio.charset.StandardCharsets;

public class proxy {
    private static final int PORT = 80; 
    public static void main(String[] args) {
        try(ServerSocket serverSocket = new ServerSocket(PORT)){
            System.out.println("start Sever... ");
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
             String clintheader=in.readLine();
             System.out.println(clintheader);
             if (clintheader == null||clintheader.isEmpty()) return;
             String[] vision =clintheader.split(" ");
             String host;
            // viosen[1].startsWith("/app");
             switch (vision[1]){
                 case String s2 when s2.startsWith("/appA") :
                     System.out.println("AppA");
                     host="vs-app-a";
                     vision[1]=vision[1].substring(5);
                     break;
                 case String s2 when s2.startsWith("/appB") :
                     System.out.println("AppB");
                     host="vs-app-b";
                     vision[1]=vision[1].substring(5);
                     break;
                 default:
                     System.err.println("ERrror" );
                     send404(out);
                     return;

             }
             if (vision[1].isEmpty()){
                 vision[1]= "/";
             }

             StringBuilder modifiedRequest = new StringBuilder();
             modifiedRequest.append(vision[0]).append(" ").append(vision[1]).append(" ").append(vision[2]).append("\r\n");
             header(in,modifiedRequest,host);
             System.out.println(modifiedRequest);

             try (Socket targetserver= new Socket(host,PORT);
             OutputStream targetOut = targetserver.getOutputStream();
             InputStream targetIn = targetserver.getInputStream()
             ){
                targetOut.write(modifiedRequest.toString().getBytes(StandardCharsets.UTF_8));
                targetOut.flush();
                byte[] buffer= new byte[8192];
                int byteREad;
                while ((byteREad= targetIn.read(buffer)) !=-1){
                    out.write(buffer,0,byteREad);

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
    private static StringBuilder header(BufferedReader in, StringBuilder stringbulderRequest,String host) throws IOException {
        String headerline;
        while ((headerline =in.readLine())!= null && !headerline.isEmpty()){
            if(headerline.toLowerCase().startsWith("host:")){
                stringbulderRequest.append("Host: ").append(host).append("\r\n");
            } else {
                stringbulderRequest.append(headerline).append("\r\n");
            }
            stringbulderRequest.append("\r\n");

        }
        return stringbulderRequest;
    }
}
