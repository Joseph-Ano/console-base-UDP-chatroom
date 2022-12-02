import socket
from ServerFunctions import *

BUFFER_SIZE = 1024
ERROR_PARAMETERS = "Command parameters do not match or is not allowed."

def main():
    serverIP = socket.gethostname()
    serverPort = 12345
    setOfConnections = set()
    handleDict = {}

    #creates datagram socket
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    #binds socket to IP and address
    serverSocket.bind((serverIP, serverPort))

    print("Waiting for client...")

    while(True):
        messageBytes, senderAddress = serverSocket.recvfrom(BUFFER_SIZE)

        messageString = messageBytes.decode()
        senderIP = senderAddress[0] 
        senderPort = senderAddress[1]

        if(senderAddress not in setOfConnections):
            setOfConnections.add(senderAddress)
            print("Connection Established with IP address: " + senderIP + " and port: " + str(senderPort))

            serverReply = toJsonString("SERVER: ", "Connection estblished with server").encode()
        
        else:
            messageObj = json.loads(messageString) 

            if(messageObj["command"] == "/join"):
                serverReply = toJsonString("SERVER: ", "You are already connected").encode()

            elif(messageObj["command"] == "/leave"):
                serverReply = disconnect(setOfConnections, handleDict, senderAddress, messageObj)

            elif(messageObj["command"] == "/register"):
                serverReply = registerHandle(handleDict, senderAddress, messageObj)
            
            elif(messageObj["command"] == "/msg"):
                serverReply = unicast(serverSocket, handleDict, messageObj, senderAddress)
            
            elif(messageObj["command"] == "/all"):
                serverReply = broadcast(serverSocket, handleDict, setOfConnections, messageObj, senderAddress)

            else:
                serverReply = toJsonString("ERROR: ", "Syntax not recognized").encode()

        serverSocket.sendto(serverReply, senderAddress)

main()