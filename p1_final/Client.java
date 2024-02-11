import java.io.*;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.Arrays;

public class Client {

    public static void Client_Function(String serverHostname, int serverPort, double time) throws UnknownHostException, IOException {
        try (Socket clientSocket = new Socket(serverHostname, serverPort);
             OutputStream out = clientSocket.getOutputStream()) {

            long sent = 0;
            byte[] data = new byte[1000];
            Arrays.fill(data, (byte) 0);

            long endTime = System.currentTimeMillis() + (long)(time * 1000);
            while (System.currentTimeMillis() < endTime) {
                out.write(data);
                sent += 1; // sent is in bytes
            }

            //double totalBytesSentKB = totalBytesSent / 1000.0;
            //double rateMbps = (((totalBytesSent / 1000.0) * 8 )/ 1000000.0) / time;
            System.out.printf("sent= %.2f KB rate= %.2f Mbps\n", ((double) sent), (((sent * 1000 * 8 )/ 1000000.0) / time));
        }
    }
}
