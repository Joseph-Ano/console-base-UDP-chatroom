import socket
import json #use json.loads function to convert input to json
import threading

BUFFER_SIZE = 1024

def toJsonString(inputList, parameters):
    if(inputList[0] == "/join"):
        msgDict = {
            "command": inputList[0],
        }
        
    elif(inputList[0] == "/leave"):
        if(parameters == 1):
            msgDict = {
                "command": inputList[0]
            }
        else:
            msgDict = {
                "command": "error",
                "message": "wrong parameters"
            }


    elif(inputList[0] == "/register"):
        if(parameters == 2):
            msgDict = {
                "command": inputList[0],
                "handle": inputList[1]
            }
        else:
            msgDict = {
                "command": "error",
                "message": "handle must not contain spaces"
            }

    elif(inputList[0] == "/msg"):
        if(parameters >= 3):
            msgDict = {
                "command": inputList[0],
                "handle": inputList[1],
                "message": inputList[2:]
            }
        else:
            msgDict = {
                "command": "error",
                "message": "wrong parameters"
            }

    elif(inputList[0] == "/all"):
        if(parameters >=2):
            msgDict = {
                "command": inputList[0],
                "message": inputList[1:]
            }
        else:
            msgDict = {
                "command": "error",
                "message": "wrong parameters"
            }

    else:
        msgDict = {
            "command": inputList[0],
            "parameters": inputList[1:] if parameters > 1 else []
        }

    return json.dumps(msgDict)

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

def main():
    serverIP = None
    serverPort = None
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    threading.Thread(target=receiveThread, args=(clientSocket,)).start()

    while(True):
        inputString = input("Enter command: ")
        inputList = inputString.split(" ")
        parameters = len(inputList)
        
        if(inputList[0] == "!Stop"):
            print("Stopping client")
            exit()

        #help menu
        elif(inputList[0] == "/?"):
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
            messageString = toJsonString(inputList, parameters)
            messageBytes = messageString.encode()

            clientSocket.sendto(messageBytes, (serverIP, int(serverPort)))

            if(inputList[0] == "/leave"):
                serverIP, serverPort = None, None
main()



