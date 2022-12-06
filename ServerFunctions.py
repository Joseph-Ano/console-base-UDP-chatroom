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
            reply = "Error: Registration failed. You are already registered"

        else:
            registered[senderAddress] = userHandle
            registered[userHandle] = senderAddress
            reply = "Welcome " + str(userHandle)
    else:
        reply = "Error: Registration failed. Handle or alias already exists."
            
    return reply.encode()

def unicast(serverSocket, registered, senderAddress, recieverHandle, message):
    if(senderAddress not in registered):
        senderReply = "Error: Register first before sending messages.".encode()

    elif(recieverHandle in registered):
        receiverAddress = registered[recieverHandle]
        senderHandle = registered[senderAddress]

        message = emojify(message)

        receiverMsg = "[FROM " + str(senderHandle) + "] " + message
        senderReply = "[TO " + str(recieverHandle) + "] " + message
    
        receiverMsg = receiverMsg.encode()
        senderReply = senderReply.encode()

        serverSocket.sendto(receiverMsg, receiverAddress)

    else:
        senderReply = "Error: Handle or alias not found.".encode()

    return senderReply

def broadcast(serverSocket, registered, setOfConnections, senderAddress, message):
    if(senderAddress not in registered):
        broadcastMessage = "Error: Register first before sending messages.".encode()
    
    else:
        message = emojify(message)
        broadcastMessage = (str(registered[senderAddress]) + ": " + message).encode()

        for address in setOfConnections:
            if(address in registered and address != senderAddress):
                serverSocket.sendto(broadcastMessage, address)

    return broadcastMessage

def disconnect(setOfConnections, registered, senderAddress):
    if(senderAddress in registered):
        senderHandle = registered[senderAddress]
        registered.pop(senderAddress)
        registered.pop(senderHandle)
        
    setOfConnections.remove(senderAddress)
    reply = "Connection closed. Thank you!"
    
    return reply.encode()

def createGC(senderAddress, registered, groupChats, groupName):
    if(senderAddress not in registered):
        reply = "Error: Register before creating a group"

    elif(groupName in groupChats):
        reply = "Error: Group already exists"

    else:
        groupChats[groupName] = set()
        groupChats[groupName].add(registered[senderAddress])
        reply = "Group Chat " + groupName + " has been created"
            
    return reply.encode()

def addGC(serverSocket, registered, groupChats, senderAddress, groupName, inviteHandle):
    if(senderAddress not in registered):
        reply = "Error: Register before inviting".encode()

    elif(groupName not in groupChats):
        reply = "Error: Group chat does not exist".encode()

    elif(registered[senderAddress] not in groupChats[groupName]):
        reply = "Error: You are not part of this groupchat".encode()

    elif(inviteHandle not in registered):
        reply = "Error: Handle or alias not found".encode()

    elif(inviteHandle in groupChats[groupName]):
        reply = "Error: User handle already in group chat".encode()

    else:
        groupChats[groupName].add(inviteHandle)
        reply = (str(inviteHandle) + " has been added to " + str(groupName)).encode()
        for handle in groupChats[groupName]:
            if(registered[handle] != senderAddress):
                serverSocket.sendto(reply, registered[handle])
            
    return reply 

def leaveGC(serverSocket, registered, groupChats, senderAddress, groupName):
    if(senderAddress not in registered):
        reply = "Error: Register before leaving a group".encode()
    elif(groupName not in groupChats):
        reply = "Error: Group chat does not exist".encode()

    elif(registered[senderAddress] not in groupChats[groupName]):
        reply = "Error: You are not part of this group".encode()
        
    else:
        groupChats[groupName].remove(registered[senderAddress])
        reply = (str(registered[senderAddress]) + " has left the group chat " + str(groupName)).encode()

        if(len(groupChats[groupName]) == 0):
            groupChats.pop(groupName)
        else:
            for handle in groupChats[groupName]:
                if(registered[handle] is not senderAddress):
                    serverSocket.sendto(reply, registered[handle])  

    return reply 

def msgGC(serverSocket, registered, groupChats, senderAddress, groupName, message):
    if(senderAddress not in registered):
        multicastMessage = "Error: Register first before sending messages.".encode()
    
    elif(groupName not in groupChats):
        multicastMessage = "Error: Group chat does not exist".encode()

    elif(registered[senderAddress] not in groupChats[groupName]):
        multicastMessage = "Error: You are not part of this group".encode()

    else:
        message = emojify(message)
        multicastMessage = ("["+str(groupName)+" "+str(registered[senderAddress])+"] "+message).encode()

        for handle in groupChats[groupName]:
            if(registered[handle] != senderAddress): 
                serverSocket.sendto(multicastMessage, registered[handle])

    return multicastMessage