import socket
import json #use json.loads function to convert input to json

BUFFER_SIZE = 1024
ERROR_PARAMETERS = "Command parameters do not match or is not allowed."

def toJsonString(sender, message):
    jsonObj = {
        "sender": sender,
        "message": message
    }
    return json.dumps(jsonObj)

def registerHandle(handleDict, senderAddress, messageObj):
    if(not messageObj["parameters"]):
        reply = toJsonString("ERROR: ", ERROR_PARAMETERS).encode()
    elif(len(messageObj["parameters"]) > 1):
        reply = toJsonString("ERROR: ", "Handles must not contain spaces").encode()
    else:
        senderHandle = messageObj["parameters"][0]
        if(senderHandle not in handleDict):
            if(senderAddress in handleDict):
                 handleDict.pop(handleDict[senderAddress])
    
            handleDict[senderAddress] = senderHandle
            handleDict[senderHandle] = senderAddress
            reply = toJsonString("SERVER: ", "User handle set to " + senderHandle + "!").encode()
        else:
            return toJsonString("ERROR: ", "Registration failed. Handle: " + senderHandle + " already exists").encode()
            
    return reply 

def unicast(serverSocket, handleDict, messageObj, senderAddress):
    if(len(messageObj["parameters"]) < 2):
        senderReply = toJsonString("ERROR: ", ERROR_PARAMETERS).encode()
    else:
        recieverHandle = messageObj["parameters"][0]

        if(senderAddress not in handleDict):
            senderReply = toJsonString("ERROR: ", "Register first before sending messages.").encode()

        elif(recieverHandle in handleDict):
            receiverAddress = handleDict[recieverHandle]
            message = " ".join(messageObj["parameters"][1:])

            receiverMsg = toJsonString("[FROM " + handleDict[senderAddress] + "] ", message).encode()
            senderReply = toJsonString("[TO " + recieverHandle + "] ", message).encode()

            serverSocket.sendto(receiverMsg, receiverAddress)

        else:
            senderReply = toJsonString("ERROR: ", "Handle or alias not found.").encode()

    return senderReply

def broadcast(serverSocket, handleDict, setOfConnections, messageObj, senderAddress):
    if(not messageObj["parameters"]):
        broadcastMessage = toJsonString("ERROR: ", ERROR_PARAMETERS).encode()
    
    elif(senderAddress not in handleDict):
        broadcastMessage = toJsonString("ERROR: ", "Register first before sending messages.").encode()
    
    else:
        message = " ".join(messageObj["parameters"])
        broadcastMessage = toJsonString(handleDict[senderAddress] + ": ", message).encode()

        for address in setOfConnections:
            if(address in handleDict and address != senderAddress):
                serverSocket.sendto(broadcastMessage, address)

    return broadcastMessage

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
                print("TO DO")

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