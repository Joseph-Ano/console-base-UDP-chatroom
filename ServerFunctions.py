from ServerParser import *
 
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