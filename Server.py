import socket
from ServerFunctions import *

BUFFER_SIZE = 1024

def main():
    serverIP = "127.0.0.1"
    serverPort = 12345
    setOfConnections = set()
    registered = {}
    groupChats = {}

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
                serverReply = disconnect(setOfConnections, registered, senderAddress)

            elif(messageObj["command"] == "/register"):
                serverReply = registerHandle(registered, senderAddress, messageObj["handle"])
            
            elif(messageObj["command"] == "/msg"):
                serverReply = unicast(serverSocket, registered, senderAddress, messageObj["handle"], messageObj["message"])
            
            elif(messageObj["command"] == "/all"):
                serverReply = broadcast(serverSocket, registered, setOfConnections, senderAddress, messageObj["message"])

            elif(messageObj["command"] == "/createGC"):
                serverReply = createGC(senderAddress, registered, groupChats, messageObj["groupName"])

            elif(messageObj["command"] == "/addGC"):
                serverReply = addGC(serverSocket, registered, groupChats, senderAddress, messageObj["groupName"], messageObj["inviteHandle"])

            elif(messageObj["command"] == "/leaveGC"):
                serverReply = leaveGC(serverSocket, registered, groupChats, senderAddress, messageObj["groupName"])

            elif(messageObj["command"] == "/msgGC"):
                serverReply = msgGC(serverSocket, registered, groupChats, senderAddress, messageObj["groupName"], messageObj["message"])

            elif(messageObj["command"] == "error"):
                serverReply = toJsonString(["error", messageObj["message"]]).encode()

            else:
                serverReply = toJsonString(["error", "Command not recognized"]).encode()

        serverSocket.sendto(serverReply, senderAddress)

main()