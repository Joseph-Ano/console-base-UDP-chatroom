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
    else:
        msgDict = {
            "command": inputList[0],
            "message": inputList[1]
        }

    return json.dumps(msgDict)