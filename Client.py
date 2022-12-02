import socket
import threading
from ClientParser import *
from ClientFunctions import *

BUFFER_SIZE = 1024

<<<<<<< Updated upstream
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

            print(replyObj["sender"] + "".join(replyObj["message"]))
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

def toJsonString(inputList):
    jsonObj = {
        "command": inputList[0],
        "parameters": inputList[1:] if len(inputList) > 1 else []
    }
    return json.dumps(jsonObj)

=======
>>>>>>> Stashed changes
def main():
    serverIP = None
    serverPort = None
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    threading.Thread(target=receiveThread, args=(clientSocket,)).start()

    while(True):
        inputString = input("Enter command: ")
        inputList = inputString.split(" ")
        parameters = len(inputList)
        
        #help menu
        if(inputList[0] == "/?"):
            if(parameters == 1):
                helpMenu()
            else:
                print("Error: wrong parameters")

        #not connected to a server
        elif(serverIP == None and serverPort == None):
            if(inputList[0] == "/join"):
                if(parameters == 3):
                    serverIP, serverPort = connectToServer(clientSocket, inputList[1], inputList[2])
                else:
                    print("input is incorrect")
            elif(inputList[0] == "/leave"):
                print("Error: Disconnection failed. Please connect to the server first.")
            else:
                print("Error: Please connect to the server first.")

        #connected to server
        elif(serverIP is not None and serverPort is not None):
            messageString = toJsonString(inputList)
            messageBytes = messageString.encode()

            clientSocket.sendto(messageBytes, (serverIP, int(serverPort)))

            if(inputList[0] == "/leave"):
                serverIP, serverPort = None, None
main()



