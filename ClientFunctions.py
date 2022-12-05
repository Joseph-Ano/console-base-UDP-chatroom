import socket
import json

BUFFER_SIZE = 1024

def helpMenu():
    print("Connect to the server application: /join <server_ip_add> <port>")
    print("Disconnect to the server application: /leave")
    print("Register a unique handle or alias: /register <handle>")
    print("Send message to all: /all <message>")
    print("Send direct message to a single handle: /msg <handle> <message>")
    print("Request command help to output all Input Syntax commands for references: /?")
    print("\n\nAdditonal Features:")
    print("Creating a group chat: /createGC <group chat name>")
    print("Adding users to group chat: /addGC <group chat name> <user handle to add>")
    print("Leaving a group chat: /leaveGC <group chat name>")
    print("Messaging a group chat: /msgGC <group chat name> <message>")
    print("\n\nEmoji commands: \n ':happy:': '😊',\n':sad:': '😢',\n':laugh:':'😂',\n':angry:': '😡'")

def receiveThread(connection):
    while(True):
        try:
            replyString = connection.recvfrom(BUFFER_SIZE)[0].decode()
            print(replyString)

        except:
            pass

def connectToServer(clientSocket, serverIP, serverPort):
    try:
        msgToSend = str.encode("Requesting connection...")

        try:
            int(serverPort)
            clientSocket.sendto(msgToSend, (serverIP, int(serverPort)))

            return serverIP, serverPort

        except ValueError:
            print("Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.")
            return None, None

    except socket.gaierror:
        print("Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.")
        return None, None