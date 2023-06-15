import json

json_string = op('config').text
        
def getInfo():
    return json.loads(json_string)