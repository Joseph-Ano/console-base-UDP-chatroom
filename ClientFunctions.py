import socket

BUFFER_SIZE = 1024

def helpMenu():
    print("""
+------------------------------+----------------------------------------+
|                               HELP MENU                               |
+------------------------------+----------------------------------------+
| /?                           | Request command help to output all     |
|                              | Input Syntax commands for references.  |
+------------------------------+----------------------------------------+
| /join <server_ip_add> <port> | Connect to the server application.     |
+------------------------------+----------------------------------------+
| /leave                       | Disconnect to the server application.  |
+------------------------------+----------------------------------------+
| /register <handle>           | Register a unique handle or alias.     |
+------------------------------+----------------------------------------+
| /all <message>               | Send message to all.                   |
+------------------------------+----------------------------------------+
| /msg <handle> <message>      | Send direct message to a single        |
|                              | handle.                                |
+------------------------------+----------------------------------------+

+-----------+----+
| LIST OF EMOJIS |
+-----------+----+
| :happy:   | 😊 |         
+-----------+----+
| :sad:     | 😢 |
+-----------+----+
| :laugh:   | 😂 |         
+-----------+----+
| :angry:   | 😡 |         
+-----------+----+

+------------------------------+----------------------------------------+
|                          GROUP CHAT COMMANDS                          |
+------------------------------+----------------------------------------+
| /createGC <group chat name>  | Creates a new group chat.              |
+------------------------------+----------------------------------------+
| /addGC <group chat name>     | Adds a user to a group chat.           |
| <user handle to add>         |                                        |
+------------------------------+----------------------------------------+
| /msgGC <group chat name>     | Send a message to a group chat         |
| <message>                    |                                        |
+------------------------------+----------------------------------------+
| /leaveGC <group chat name>   | Leave a group chat.                    |
+------------------------------+----------------------------------------+""")

def receiveThread(connection, server):
    while(True):
        try:
            
            try:
                replyString = connection.recvfrom(BUFFER_SIZE)[0].decode()
                print(replyString)
                connection.settimeout(None)

            except socket.timeout:
                print("Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.")
                server.ip = None
                server.port = None
                connection.settimeout(None)

        except:
            pass

def connectToServer(clientSocket, serverIP, serverPort):
    try:
        msgToSend = str.encode("Requesting connection...")

        try:
            int(serverPort)
            clientSocket.sendto(msgToSend, (serverIP, int(serverPort)))
            clientSocket.settimeout(1)
            return serverIP, serverPort

        except ValueError:
            print("Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.")
            return None, None

    except:
        print("Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.")
        return None, None