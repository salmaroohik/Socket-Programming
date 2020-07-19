import java.io.IOException;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.logging.Level;
import java.util.logging.Logger;

public class closeServer {
    static int port;
    static Socket s;
    static PrintWriter pw;
    static String ip;
    public static void main(String args[]){
        if(args.length<2){
            System.out.println("provied first argument IP address of server and second port number");
            return;
        }
        ip=args[0];
        port = Integer.valueOf(args[1]);
        try {
            s = new Socket(ip,port);
            pw =  new PrintWriter(s.getOutputStream(),true);
            pw.println("close");
        } catch (IOException ex) {
            Logger.getLogger(closeServer.class.getName()).log(Level.SEVERE, null, ex);
        }
        
    }
}