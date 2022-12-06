import socket
import threading
import time
from ClientParser import *
from ClientFunctions import *

BUFFER_SIZE = 1024

class ConnectedServer:
  def __init__(self, ip, port):
    self.ip = ip
    self.port = port

def main():
    connectedServer = ConnectedServer(None, None)
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    thread = threading.Thread(target=receiveThread, args=(clientSocket, connectedServer))
    thread.daemon = True
    thread.start()

    while(True):
        inputString = input("Enter command: ")
        inputList = inputString.strip().split(" ")
        parameters = len(inputList)

        if(inputString == "!q"):
            if(connectedServer.ip is not None and connectedServer.port is not None):
                messageString = toJsonString(["/leave"], 1)
                messageBytes = messageString.encode()
                clientSocket.sendto(messageBytes, (connectedServer.ip, int(connectedServer.port)))

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
        elif(connectedServer.ip == None and connectedServer.port == None):
            if(inputList[0] == "/join"):
                if(parameters == 3):
                    connectedServer.ip, connectedServer.port = connectToServer(clientSocket, inputList[1], inputList[2])
                else:
                    print("input is incorrect")
            elif(inputList[0] == "/leave"):
                print("Error: Disconnection failed. Please connect to the server first.")
            else:
                print("Error: Please connect to the server first.")

        #connected to server
        elif(connectedServer.ip is not None and connectedServer.port is not None):
            messageString = toJsonString(inputList, parameters)
            messageBytes = messageString.encode()

            clientSocket.sendto(messageBytes, (connectedServer.ip, int(connectedServer.port)))

            if(inputList[0] == "/leave" and parameters == 1):
                connectedServer.ip, connectedServer.port = None, None
main()



