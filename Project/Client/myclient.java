package demoortry;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.URL;
import java.net.URLConnection;

public class myclient {

    static String command, hostname, fileName, httpv = "HTTP/1.1", response = null, line = "";
    static Socket s = null;
    static PrintWriter pwforSocket = null;
    static BufferedReader br = null;
    static File f1, f2;
    static int port;
    static URLConnection con;
    static URL url;

    public static void main(String[] args) {
        //variable
        try {
            command = args[2];
            hostname = args[0];
            fileName = args[3];
        } catch (Exception e) {
            System.out.println("it takes 4 arguments"
                    + "\n1) IP address"
                    + "\n2) port no."
                    + "\n3) command \"GET\" or \"PUT\""
                    + "\n4) filename to get ");
        }

        try {
            port = Integer.valueOf(args[1]);
        } catch (Exception e) {
            System.out.println("port shoult be an integer");
            return;
        }
        if (command.equals("GET")) {
            try {
                sendGetRequest();
            } catch (Exception ex) {
                System.out.println("error in sending request " + ex);
            }
        } else if (command.equals("PUT")) {
            sendPutRequest();
        } else {
            System.out.println("command should be GET or PUT");
        }
    }

    private static void sendGetRequest() {
        BufferedReader in = null;
        PrintWriter pw = null;
        try {
            url = new URL("http://" + hostname + ":" + port + "/" + fileName);
            con = url.openConnection();
            in = new BufferedReader(
                    new InputStreamReader(
                            con.getInputStream()));
            System.out.println("Response-Header..........");
            System.out.println(con.getHeaderField(0));
            System.out.println();
            String line;
            f1 = new File("index.txt");
            f2 = new File(fileName);
            if (f2.exists()) {
                f2.delete();
            }
            pw = new PrintWriter(new FileWriter(f1));
            System.out.println("Data.....................");
            while ((line = in.readLine()) != null) {
                System.out.println(line);
                pw.println(line);
            }

        } catch (FileNotFoundException ex) {
            System.out.println("Response-Header..........");
            System.out.println(con.getHeaderField(0));
            return;
        } catch (Exception ex) {
            System.out.println("error: " + ex);
        }
        try {
            in.close();
            pw.close();
            f1.renameTo(f2);
        } catch (Exception ex) {
            System.out.println("error: " + ex);
        }
    }

    private static void sendPutRequest() {
        String endingHeader = "Connection: keep-alive\r\nPragma: no-cache\r\nCache-Control: no-cache\r\n\r\n";
        f1 = new File(fileName);
        if (f1.exists()) {
            try {
                s = new Socket(hostname, port);
                pwforSocket = new PrintWriter(s.getOutputStream(), true);
                br = new BufferedReader(new InputStreamReader(s.getInputStream()));
            } catch (Exception ex) {
                System.out.println("error occured during connection");
            }
            pwforSocket.flush();
            pwforSocket.println(command + " /" + fileName + " " + httpv);
            pwforSocket.println(endingHeader);
            //pwforSocket.flush();
            try {
                //sleep(500);
                BufferedReader brforFile = new BufferedReader(new FileReader(f1));
                //System.out.println("sending lines after reading file");    
                while ((line = brforFile.readLine()) != null) {
                    pwforSocket.println(line);//write(line+"\n");
                    //System.out.println(line);
                }
                //System.out.println("file completed");
                pwforSocket.println();
                //  System.out.println("writing completed");
                brforFile.close();

            } catch (Exception ex) {
                System.out.println("file reading error" + ex);
            }
            try {
                while (!line.equals("")) {
                    //System.out.println("in while reading response");
                    line = br.readLine();
                    //System.out.println(line);  
                }
            } catch (Exception ex) {
                System.out.println("Response-Header..........");
                System.out.println("HTTP1.1 201 Created");
            } finally {
                pwforSocket.close();
                try {
                    br.close();
                } catch (IOException ex) {
                    System.out.println("error during in finally" + ex);
                    //Logger.getLogger(myclient2.class.getName()).log(Level.SEVERE, null, ex);
                }
            }
        } else {
            System.out.println("file does not exist");
        }
    }
}
