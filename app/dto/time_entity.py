import json

class TimeEntity:
    
    elapsedTime: float

    def __init__(self, dict):
        self.__dict__.update(dict)

def create_time(dict):
    return json.loads(json.dumps(dict), object_hook=TimeEntity)