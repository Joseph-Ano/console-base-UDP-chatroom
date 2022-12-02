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
                "message": "wrong parameters"
            }


    elif(inputList[0] == "/register"):
        if(parameters == 2):
            msgDict = {
                "command": inputList[0],
                "handle": inputList[1]
            }
        else:
            msgDict = {
                "command": "error",
                "message": "handle must not contain spaces"
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
                "message": "wrong parameters"
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
                "message": "wrong parameters"
            }

    else:
        msgDict = {
            "command": inputList[0],
            "parameters": inputList[1:] if parameters > 1 else []
        }

    return json.dumps(msgDict)