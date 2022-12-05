import socket
import threading
import time
from ClientParser import *
from ClientFunctions import *

BUFFER_SIZE = 1024

def main():
    serverIP = None
    serverPort = None
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    thread = threading.Thread(target=receiveThread, args=(clientSocket,))
    thread.daemon = True
    thread.start()

    while(True):
        inputString = input("Enter command: ")
        inputList = inputString.strip().split(" ")
        parameters = len(inputList)

        if(inputString == "!q"):
            if(serverIP is not None and serverPort is not None):
                messageString = toJsonString(["/leave"], 1)
                messageBytes = messageString.encode()
                clientSocket.sendto(messageBytes, (serverIP, int(serverPort)))

            time.sleep(2)
            print("Exiting Client")
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

            if(inputList[0] == "/leave" and parameters == 1):
                serverIP, serverPort = None, None
main()



