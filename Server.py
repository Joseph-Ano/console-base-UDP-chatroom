import socket
from ServerFunctions import *

BUFFER_SIZE = 1024

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

            serverReply = toJsonString(["join"]).encode()
        
        else:
            messageObj = json.loads(messageString) 

            if(messageObj["command"] == "/join"):
                serverReply = toJsonString(["error",  "Already connected to a server"]).encode()

            elif(messageObj["command"] == "/leave"):
                serverReply = disconnect(setOfConnections, handleDict, senderAddress)

            elif(messageObj["command"] == "/register"):
                serverReply = registerHandle(handleDict, senderAddress, messageObj["handle"])
            
            elif(messageObj["command"] == "/msg"):
                serverReply = unicast(serverSocket, handleDict, senderAddress, messageObj["handle"], messageObj["message"])
            
            elif(messageObj["command"] == "/all"):
                serverReply = broadcast(serverSocket, handleDict, setOfConnections, messageObj["message"], senderAddress)
            
            elif(messageObj["command"] == "error"):
                serverReply = toJsonString(["error", messageObj["message"]]).encode()

            else:
                serverReply = toJsonString(["error", "Syntax not recognized"]).encode()

        serverSocket.sendto(serverReply, senderAddress)

main()