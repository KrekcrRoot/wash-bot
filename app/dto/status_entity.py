import json
from app.dto.status_enum import Status

class StatusEntity:

    status: Status
    telegramTag: str
    timeBegin: str
    reportBody: str

    def __init__(self, dict):
        self.__dict__.update(dict)


def create_status(dict):
    return json.loads(json.dumps(dict), object_hook=StatusEntity)
