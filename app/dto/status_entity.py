import json

class StatusEntity:

    isActive: bool
    telegramTag: str
    timeBegin: str

    def __init__(self, dict):
        self.__dict__.update(dict)


def create_status(dict):
    return json.loads(json.dumps(dict), object_hook=StatusEntity)
