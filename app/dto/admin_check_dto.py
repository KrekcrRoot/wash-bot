import json

class AdminCheckDto:
    isAdmin: bool

    def __init__(self,dict):
        self.__dict__.update(dict)

def create_admin_check_dto(dict):
    return json.loads(json.dumps(dict),object_hook=AdminCheckDto)