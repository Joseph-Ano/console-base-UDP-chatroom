from ServerParser import *
 
def emojify(message):
    emojies = {
        ":happy:": "😊",
        ":sad:": "😢",
        ":laugh:":"😂",
        ":angry:": "😡"
    }
    return ' '.join(str(emojies.get(word, word)) for word in message)

def registerHandle(registered, senderAddress, userHandle):
    if(userHandle not in registered):
        if(senderAddress in registered): 
            reply =  toJsonString(["error", "Registration failed. You are already registered"]).encode()

        else:
            registered[senderAddress] = userHandle
            registered[userHandle] = senderAddress
            reply = toJsonString(["register", userHandle]).encode()
    else:
        reply =  toJsonString(["error", "Registration failed. Handle: " + userHandle + " already exists"]).encode()
            
    return reply 

def unicast(serverSocket, registered, senderAddress, recieverHandle, message):
    if(senderAddress not in registered):
        senderReply = toJsonString(["error", "Register first before sending messages."]).encode()

    elif(recieverHandle in registered):
        receiverAddress = registered[recieverHandle]
        senderHandle = registered[senderAddress]

        message = emojify(message)

        receiverMsg = "[FROM " + senderHandle + "] " + message
        senderReply = "[TO " + recieverHandle + "] " + message
    
        receiverMsg = toJsonString(["msg", recieverHandle, receiverMsg]).encode()
        senderReply = toJsonString(["msg", senderHandle, senderReply]).encode()

        serverSocket.sendto(receiverMsg, receiverAddress)

    else:
        senderReply = toJsonString(["error", "Handle or alias not found."]).encode()

    return senderReply

def broadcast(serverSocket, registered, setOfConnections, senderAddress, message):
    if(senderAddress not in registered):
        broadcastMessage = toJsonString(["error", "Register first before sending messages."]).encode()
    
    else:
        message = registered[senderAddress] + ": " + emojify(message)
        broadcastMessage = toJsonString(["all", message]).encode()

        for address in setOfConnections:
            if(address in registered and address != senderAddress): #change this if broadcast works for connected but not registered
                serverSocket.sendto(broadcastMessage, address)

    return broadcastMessage

def disconnect(setOfConnections, registered, senderAddress):
    if(senderAddress in registered):
        senderHandle = registered[senderAddress]
        registered.pop(senderAddress)
        registered.pop(senderHandle)
        
    setOfConnections.remove(senderAddress)
    reply = toJsonString(["leave"]).encode()
    
    return reply

def createGC(senderAddress, registered, groupChats, groupName):
    if(senderAddress not in registered):
        reply =  toJsonString(["error", "Register before creating a group"]).encode()

    elif(groupName in groupChats):
        reply =  toJsonString(["error", "Group already exists"]).encode()

    else:
        groupChats[groupName] = set()
        groupChats[groupName].add(registered[senderAddress])
        reply = toJsonString(["createGC", groupName]).encode()
            
    return reply 

def addGC(serverSocket, registered, groupChats, senderAddress, groupName, inviteHandle):
    if(senderAddress not in registered):
        reply =  toJsonString(["error", "Register before inviting"]).encode()

    elif(groupName not in groupChats):
        reply =  toJsonString(["error", "Group chat does not exist"]).encode()

    elif(registered[senderAddress] in groupChats[groupName]):
        reply =  toJsonString(["error", "You are not part of this groupchat"]).encode()

    elif(inviteHandle not in registered):
        reply =  toJsonString(["error", "User handle does not exist"]).encode()

    elif(inviteHandle in groupChats[groupName]):
        reply =  toJsonString(["error", "User handle already in group chat"]).encode()

    else:
        groupChats[groupName].add(inviteHandle)
        reply = toJsonString(["addGC", groupName, inviteHandle]).encode()
        for handle in groupChats[groupName]:
            if(registered[handle] != senderAddress):
                serverSocket.sendto(reply, registered[handle])
            
    return reply 

def leaveGC(serverSocket, registered, groupChats, senderAddress, groupName):
    if(senderAddress not in registered):
        reply =  toJsonString(["error", "Register before leaving a group"]).encode()
    elif(groupName not in groupChats):
        reply =  toJsonString(["error", "Group chat does not exist"]).encode()

    elif(registered[senderAddress] not in groupChats[groupName]):
        reply =  toJsonString(["error", "You are not part of this group"]).encode()
        
    else:
        groupChats[groupName].remove(registered[senderAddress])
        reply = toJsonString(["leaveGC", groupName, registered[senderAddress]]).encode()

        if(len(groupChats[groupName]) == 0):
            groupChats.pop(groupName)
        else:
            for handle in groupChats[groupName]:
                if(registered[handle] is not senderAddress):
                    serverSocket.sendto(reply, registered[handle])  

    return reply 

def msgGC(serverSocket, registered, groupChats, senderAddress, groupName, message):
    if(senderAddress not in registered):
        multicastMessage = toJsonString(["error", "Register first before sending messages."]).encode()
    
    elif(groupName not in groupChats):
        multicastMessage =  toJsonString(["error", "Group chat does not exist"]).encode()

    elif(registered[senderAddress] not in groupChats[groupName]):
        multicastMessage =  toJsonString(["error", "You are not part of this group"]).encode()

    else:
        message = emojify(message)
        multicastMessage = toJsonString(["msgGC", groupName, " " + registered[senderAddress] + "] " + message]).encode()

        for handle in groupChats[groupName]:
            if(registered[handle] != senderAddress): 
                serverSocket.sendto(multicastMessage, registered[handle])

    return multicastMessage