import json

def toJsonString(inputList, parameters):
    if(inputList[0] == "/join"):
        msgDict = {
            "command": inputList[0],
        }
        
    elif(inputList[0] == "/leave"):
        if(parameters == 1):
            msgDict = {
                "command": inputList[0]
            }
        else:
            msgDict = {
                "command": "error",
                "message": "Error: Command parameters do not match or is not allowed."
            }


    elif(inputList[0] == "/register"):
        if(parameters == 2):
            msgDict = {
                "command": inputList[0],
                "handle": inputList[1]
            }
        elif(parameters > 2):
            msgDict = {
                "command": "error",
                "message": "Error: handle must not contain spaces"
            }
        else:
            msgDict = {
                "command": "error",
                "message": "Error: Command parameters do not match or is not allowed."
            }

    elif(inputList[0] == "/msg"):
        if(parameters >= 3):
            msgDict = {
                "command": inputList[0],
                "handle": inputList[1],
                "message": inputList[2:]
            }
        else:
            msgDict = {
                "command": "error",
                "message": "Error: Command parameters do not match or is not allowed."
            }

    elif(inputList[0] == "/all"):
        if(parameters >=2):
            msgDict = {
                "command": inputList[0],
                "message": inputList[1:]
            }
        else:
            msgDict = {
                "command": "error",
                "message": "Error: Command parameters do not match or is not allowed."
            }

    elif(inputList[0] == "/createGC"):
        if(parameters == 2):
            msgDict = {
                "command": inputList[0],
                "groupName": inputList[1]
            }
        else:
            msgDict = {
                "command": "error",
                "message": "Error: Groupname must not include spaces."
            }
    elif(inputList[0] == "/adGC"):
        if(parameters == 3):
            msgDict = {
                "command": inputList[0],
                "groupName": inputList[1],
                "inviteHandle": inputList[2]
            }
        else:
            msgDict = {
                "command": "error",
                "message": "Error: Command parameters do not match or is not allowed."
            }

    elif(inputList[0] == "/leaveGC"):
        if(parameters == 2):
            msgDict = {
                "command": inputList[0],
                "groupName": inputList[1],
            }
        else:
            msgDict = {
                "command": "error",
                "message": "Error: Command parameters do not match or is not allowed."
            }
    
    elif(inputList[0] == "/msgGC"):
        if(parameters >= 3):
            msgDict = {
                "command": inputList[0],
                "groupName": inputList[1],
                "message": inputList[2:]
            }
        else:
            msgDict = {
                "command": "error",
                "message": "Error: Command parameters do not match or is not allowed."
            }

    else:
        msgDict = {
            "command": inputList[0]
        }

    return json.dumps(msgDict)