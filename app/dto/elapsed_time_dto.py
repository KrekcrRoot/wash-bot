import json

class ElapsedTime_Dto:
    
    elapsedTime: float

    def __init__(self, dict):
        self.__dict__.update(dict)

def create_time(dict):
    return json.loads(json.dumps(dict), object_hook=ElapsedTime_Dto)