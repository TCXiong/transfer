import java.io.IOException;
public class Iperfer {
  public static void main(String[] args) {
    // Checking the arguments validity
    if (args.length < 1) {
      System.out.println("Error: missing or additional arguments");
    } else if (args[0] == "-c" && (args.length < 7 || args.length > 7)) {
      System.out.println("Error: missing or additional arguments");
    }

    else if (args[0] == "-s" && (args.length < 3 || args.length > 3)) {
      System.out.println("Error: missing or additional arguments");
    }

    else if (args[0] == "-c" && (Integer.valueOf(args[4]) < 1024 || Integer.valueOf(args[4]) > 65535)) {
      System.out.println("Error: port number must be in the range 1024 to 65535");
    }

    else if (args[0] == "-s" && (Integer.valueOf(args[2]) < 1024 || Integer.valueOf(args[4]) > 65535)) {
      System.out.println("Error: port number must be in the range 1024 to 65535");
    }

    // Calling the client
    if (args[0].equals("-c")) {
	    try{
		    Client.Client_Function(args[2], Integer.parseInt(args[4]), Double.parseDouble(args[6]));
	    }catch (IOException e){
		    System.err.println("Unkown Host: "+ e.getMessage());
	    }

    }

    // Calling server
    if (args[0].equals("-s")) {
      System.out.println("Calling Server");
      Server.Server_Function(Integer.parseInt(args[2]));
    }
  }
}
