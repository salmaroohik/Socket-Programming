
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.concurrent.Executors;
import java.util.concurrent.ThreadPoolExecutor;

public class finalServer {

    static String[] temp = new String[3];
    static ServerSocket ss;
    static Socket s;
    static BufferedReader br;
    static String line = "";
    static ThreadPoolExecutor pool = (ThreadPoolExecutor) Executors.newFixedThreadPool(1024);
    static PrintWriter pw = null;

    public static void main(String args[]) throws Exception {
        int port;
        System.out.println("starting Server");
        try {
            port = Integer.valueOf(args[0]);
            if (port <= 5000) {
                throw new Exception("advisable port number is greater than 5000\n");
            }
        } catch (Exception e) {
            System.out.println("error with port number, provide proper port no.\n" + e);
            return;
        }
        ss = new ServerSocket(port);
        System.out.println("Server is listening on port " + port + " for clients\n");
        while (!line.equals("close")) {
            s = ss.accept();
            br = new BufferedReader(new InputStreamReader(s.getInputStream()));
            pw = new PrintWriter(s.getOutputStream(), true);
            line = br.readLine();
            if(line.equals("close")){
                br.close();
                pw.close();
                s.close();
                ss.close();
                break;
            }
            System.out.println("***Request-Header***");
            System.out.println(line);
            temp = line.split(" ");
            while (!line.equals("")) {
                line = br.readLine();
                System.out.println(line);
            }
            System.out.println("********************\n");

            if (temp[0].equals("GET")) {
                MyServerThread thread = new MyServerThread(br, pw, temp[0], temp[1], temp[2]);
                pool.execute(thread);
            } else {
                forPut(pw);
            }
        }
        System.out.println("closing server");
    }

    static void forPut(PrintWriter pw) {
        String fileName = temp[1].substring(1), httpv = temp[2], status;
        File f1 = new File(fileName);
        String tempFileName = fileName.substring(0, fileName.indexOf(".")) + ".txt";
        File f2 = new File(tempFileName);
        PrintWriter pwforSocket = pw;
        PrintWriter pwforFile = null;

        if (f1.exists()) {
            f1.delete();
        }

        try {
            pwforFile = new PrintWriter(new FileWriter(f1));
            System.out.println(br.readLine());
            line = "just for temporary";
            while (!line.equals("")) {
                line = br.readLine();
                pwforFile.println(line);
            }
            System.out.println("File written.\n");
            br.close();
            pwforFile.close();
            //System.out.println("before changing name file name is: "+f2.getName());
            f2 = new File(fileName);
            f1.renameTo(f2);
        } catch (IOException ex) {
            System.out.println("error in writing file");
        }

        pwforSocket.flush();
        pwforSocket.println(httpv + " 200 OK ");
        pwforSocket.println("Content-Location : " + fileName);
        pwforSocket.println("Connection: close");
        pwforSocket.println();
        try {
            f1 = null;
            f2 = null;
            System.gc();
            br.close();
            pwforFile.close();
            pwforSocket.close();
        } catch (Exception ex) {
            System.out.println("error in closing...");
        }
    }

    static class MyServerThread implements Runnable {

        File f1 = null;
        PrintWriter pwforSocket = null, pwforFile = null;
        String status, httpv, line, method, fileName;
        BufferedReader brforFile = null, brforSocket = null;

        MyServerThread(BufferedReader brforSocket, PrintWriter pw1, String command, String fileName, String httpversion) {
            this.httpv = httpversion;
            this.method = command;
            this.pwforSocket = pw1;
            if (fileName.equals("/")) {
                this.fileName = fileName.substring(1);
            } else {
                this.fileName = "index.html";
            }
            this.brforSocket = brforSocket;
            f1 = new File(fileName.substring(1));
        }

        @Override
        public void run() {
            forGet();
        }

        void forGet() {
            if (f1.exists()) {
                status = httpv + " 200 OK\r\n";
                pwforSocket.write(status);
                pwforSocket.write("Content-Type: text/html\r\nConnection: close\r\n\r\n");
                try {
                    brforFile = new BufferedReader(new FileReader(f1));
                    while ((line = brforFile.readLine()) != null) {
                        pwforSocket.write(line + "\n");
                    }
                    pwforSocket.write("\r\n");
                } catch (Exception ex) {
                    System.out.println("error :" + ex);

                } finally {
                    try {
                        brforFile.close();
                        pwforSocket.close();
                    } catch (Exception ex) {
                        System.out.println("error in closing");
                    }
                }
            } else {
                status = httpv + " 404 File Not Found";
                pwforSocket.write(status);
            }
            pwforSocket.close();
        }
    }
}
