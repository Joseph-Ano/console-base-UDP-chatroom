import socket
import json #use json.loads function to convert input to json

BUFFER_SIZE = 1024

def toJsonString(inputList):
    if(inputList[0] == "join"):
        msgDict = {
            "command": inputList[0],
        }
        
    elif(inputList[0] == "leave"):
        msgDict = {
            "command": inputList[0]
        }


    elif(inputList[0] == "register"):
        msgDict = {
            "command": inputList[0],
            "handle": inputList[1]
        }

    elif(inputList[0] == "msg"):
        msgDict = {
            "command": inputList[0],
            "handle": inputList[1],
            "message": inputList[2]
        }

    elif(inputList[0] == "all"):
        msgDict = {
            "command": inputList[0],
            "message": inputList[1]
        }
    else:
        msgDict = {
            "command": inputList[0],
            "message": inputList[1]
        }

    return json.dumps(msgDict)

def emojify(message):
    emojies = {
        ":happy:": "😊",
        ":sad:": "😢",
        ":laugh:":"😂",
        ":angry:": "😡"
    }
    return ' '.join(str(emojies.get(word, word)) for word in message)


def registerHandle(handleDict, senderAddress, userHandle):
    if(userHandle not in handleDict):
        if(senderAddress in handleDict): #change this if not allowed to change handle once set
                handleDict.pop(handleDict[senderAddress])

        handleDict[senderAddress] = userHandle
        handleDict[userHandle] = senderAddress
        reply = toJsonString(["register", userHandle]).encode()
    else:
        reply =  toJsonString(["error", "Registration failed. Handle: " + userHandle + " already exists"]).encode()
            
    return reply 

def unicast(serverSocket, handleDict, senderAddress, recieverHandle, message):
    if(senderAddress not in handleDict):
        senderReply = toJsonString(["error", "Register first before sending messages."]).encode()

    elif(recieverHandle in handleDict):
        receiverAddress = handleDict[recieverHandle]
        senderHandle = handleDict[senderAddress]

        message = emojify(message)

        receiverMsg = "[FROM " + senderHandle + "] " + message
        senderReply = "[TO " + recieverHandle + "] " + message
    
        receiverMsg = toJsonString(["msg", recieverHandle, receiverMsg]).encode()
        senderReply = toJsonString(["msg", senderHandle, senderReply]).encode()

        serverSocket.sendto(receiverMsg, receiverAddress)

    else:
        senderReply = toJsonString(["error", "Handle or alias not found."]).encode()

    return senderReply

def broadcast(serverSocket, handleDict, setOfConnections, message, senderAddress):
    if(senderAddress not in handleDict):
        broadcastMessage = toJsonString(["error", "Register first before sending messages."]).encode()
    
    else:
        message = handleDict[senderAddress] + ": " + emojify(message)
        broadcastMessage = toJsonString(["all", message]).encode()

        for address in setOfConnections:
            if(address in handleDict and address != senderAddress): #change this if broadcast works for connected but not registered
                serverSocket.sendto(broadcastMessage, address)

    return broadcastMessage

def disconnect(setOfConnections, handleDict, senderAddress):
    if(senderAddress in handleDict):
        senderHandle = handleDict[senderAddress]
        handleDict.pop(senderAddress)
        handleDict.pop(senderHandle)
        
    setOfConnections.remove(senderAddress)
    reply = toJsonString(["leave"]).encode()
    
    return reply

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
            print(messageObj["command"])

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