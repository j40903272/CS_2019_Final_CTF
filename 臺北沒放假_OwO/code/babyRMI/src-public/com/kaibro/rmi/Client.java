package com.kaibro.rmi;

import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;

public class Client {

    public static void main(String[] args) {

        String host = "140.113.203.209";
        int port = 11099;
        try {
            Registry registry = LocateRegistry.getRegistry(host, port);
            //RMIInterface stub = (RMIInterface) registry.lookup("Hello");
            RMIInterface stub = (RMIInterface) registry.lookup("FLAG");
            String[] names = registry.list();
            for (String name : names)
              System.out.println(name);
            String response = stub.sayHello();
            System.out.println("response: " + response);
            String secret = stub.getSecret();
            System.out.println("secret: " + secret);
        } catch (Exception e) {
            System.err.println("Client exception: " + e.toString());
            e.printStackTrace();
        }
    }
}
