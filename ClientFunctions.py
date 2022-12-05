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
            replyObj = json.loads(replyString)

            if(replyObj["command"] == "join"):
                 print("Connection to the Message Board Server is successful!")

            elif(replyObj["command"] == "register"):
                print("User handle successfuly set to " + replyObj["handle"])

            elif(replyObj["command"] == "msg"):
                print(replyObj["message"])

            elif(replyObj["command"] == "all"):
                print(replyObj["message"])

            elif(replyObj["command"] == "createGC"):
                print("Group chat: " + replyObj["groupName"] + " successfully created")

            elif(replyObj["command"] == "addGC"):
                print("[" + replyObj["groupName"] + "] " + replyObj["inviteHandle"]  + " has been added to the group.")

            elif(replyObj["command"] == "leaveGC"):
                print("[" + replyObj["groupName"] + "] " + replyObj["userHandle"]  + " has left the group.")

            elif(replyObj["command"] == "msgGC"):
                print("[" + replyObj["groupName"] + replyObj["message"])

            elif(replyObj["command"] == "leave"):
                print("Connection closed. Thank you!")

            elif(replyObj["command"] == "error"):
                print(replyObj["command"] + ": " + replyObj["message"])

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