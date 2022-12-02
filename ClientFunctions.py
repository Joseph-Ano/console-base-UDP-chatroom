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
    print("Emoji commands: \n ':happy:': '😊',\n':sad:': '😢',\n':laugh:':'😂',\n':angry:': '😡'")

def receiveThread(connection):
    while(True):
        try:
            replyString = connection.recvfrom(BUFFER_SIZE)[0].decode()
            replyObj = json.loads(replyString)

            if(replyObj["command"] == "join"):
                 print("Successfully connected to server")

            elif(replyObj["command"] == "register"):
                print("User handle successfuly set to " + replyObj["handle"])

            elif(replyObj["command"] == "msg"):
                print(replyObj["message"])

            elif(replyObj["command"] == "all"):
                print(replyObj["message"])

            elif(replyObj["command"] == "leave"):
                print("Successfully disconected from server")

            elif(replyObj["command"] == "error"):
                print(replyObj["command"] + ": " + replyObj["message"])

        except:
            pass

def connectToServer(clientSocket, serverIP, serverPort):
    try:
        msgToSend = str.encode("Requesting connection...")

        clientSocket.sendto(msgToSend, (serverIP, int(serverPort)))

        return serverIP, serverPort

    except socket.gaierror:
        print("Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.")
        return None, None