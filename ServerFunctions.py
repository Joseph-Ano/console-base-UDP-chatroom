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

def broadcast(serverSocket, handleDict, setOfConnections, senderAddress, message):
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

def createGC(senderAddress, handleDict, groupChats, groupName):
    if(senderAddress not in handleDict):
        reply =  toJsonString(["error", "Register before creating a group"]).encode()

    elif(groupName in groupChats):
        reply =  toJsonString(["error", "Group already exists"]).encode()

    else:
        groupChats[groupName] = set()
        groupChats[groupName].add(handleDict[senderAddress])
        reply = toJsonString(["createGC", groupName]).encode()
            
    return reply 

def inviteGC(serverSocket, handleDict, groupChats, senderAddress, groupName, inviteHandle):
    if(senderAddress not in handleDict):
        reply =  toJsonString(["error", "Register before inviting"]).encode()

    elif(groupName not in groupChats):
        reply =  toJsonString(["error", "Group chat does not exist"]).encode()

    elif(handleDict[senderAddress] in groupChats[groupName]):
        reply =  toJsonString(["error", "You are not part of this groupchat"]).encode()

    elif(inviteHandle not in handleDict):
        reply =  toJsonString(["error", "User handle does not exist"]).encode()

    elif(inviteHandle in groupChats[groupName]):
        reply =  toJsonString(["error", "User handle already in group chat"]).encode()

    else:
        groupChats[groupName].add(inviteHandle)
        reply = toJsonString(["invite", groupName, inviteHandle]).encode()
        for handle in groupChats[groupName]:
            if(handleDict[handle] != senderAddress):
                serverSocket.sendto(reply, handleDict[handle])
            
    return reply 

def leaveGC(serverSocket, handleDict, groupChats, senderAddress, groupName):
    if(senderAddress not in handleDict):
        reply =  toJsonString(["error", "Register before leaving a group"]).encode()
    elif(groupName not in groupChats):
        reply =  toJsonString(["error", "Group chat does not exist"]).encode()

    elif(handleDict[senderAddress] not in groupChats[groupName]):
        reply =  toJsonString(["error", "You are not part of this group"]).encode()
        
    else:
        groupChats[groupName].remove(handleDict[senderAddress])
        reply = toJsonString(["leaveGC", groupName, handleDict[senderAddress]]).encode()

        if(len(groupChats[groupName]) == 0):
            groupChats.pop(groupName)
        else:
            for handle in groupChats[groupName]:
                if(handleDict[handle] is not senderAddress):
                    serverSocket.sendto(reply, handleDict[handle])  

    return reply 

def msgGC(serverSocket, handleDict, groupChats, senderAddress, groupName, message):
    if(senderAddress not in handleDict):
        multicastMessage = toJsonString(["error", "Register first before sending messages."]).encode()
    
    elif(groupName not in groupChats):
        multicastMessage =  toJsonString(["error", "Group chat does not exist"]).encode()

    elif(handleDict[senderAddress] not in groupChats[groupName]):
        multicastMessage =  toJsonString(["error", "You are not part of this group"]).encode()

    else:
        message = emojify(message)
        multicastMessage = toJsonString(["msgGC", groupName, " " + handleDict[senderAddress] + "] " + message]).encode()

        for handle in groupChats[groupName]:
            if(handleDict[handle] != senderAddress): 
                serverSocket.sendto(multicastMessage, handleDict[handle])

    return multicastMessage