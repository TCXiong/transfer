import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;

public class Server {

    public static void Server_Function(int port) {
        try {
            ServerSocket serverSocket = new ServerSocket(port);
            Socket clientSocket = serverSocket.accept();
            handleClient(clientSocket);
            serverSocket.close(); // Close the server socket after client connection is closed
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static void handleClient(Socket clientSocket) {
        try (InputStream in = clientSocket.getInputStream()) {
            byte[] data = new byte[1000];
            long received = 0;
            long startTime = System.currentTimeMillis();
            int bytesRead = 0;
            while ((bytesRead = in.read(data)) != -1) {
                received += bytesRead;
            }
            double elapsedTimeSeconds = (System.currentTimeMillis() - startTime) / 1000.0;
            double totalBytesReceivedKB = received / 1000.0;
            double rateMbps = (((received  * 8) / 1000000.0)) / elapsedTimeSeconds;
            System.out.printf("received= %.2f KB rate= %.2f Mbps\n", totalBytesReceivedKB, rateMbps);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
