import json

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
    elif(inputList[0] == "createGC"):
        msgDict = {
            "command": inputList[0],
            "groupName": inputList[1]
        }
    elif(inputList[0] == "addGC"):
        msgDict = {
            "command": inputList[0],
            "groupName": inputList[1],
            "inviteHandle": inputList[2]
        }
    elif(inputList[0] == "leaveGC"):
        msgDict = {
            "command": inputList[0],
            "groupName": inputList[1],
            "userHandle": inputList[2]
        }
    elif(inputList[0] == "msgGC"):
        msgDict = {
            "command": inputList[0],
            "groupName": inputList[1],
            "message": inputList[2]
        }
    else:
        msgDict = {
            "command": inputList[0],
            "message": inputList[1]
        }

    return json.dumps(msgDict)