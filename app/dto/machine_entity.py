import json

class MachineEntity:

    uuid: str
    title: str
    isActive: bool
    broken: bool

    def __init__(self, dict):
        self.__dict__.update(dict)

def create_machine(dict):
    return json.loads(json.dumps(dict), object_hook=MachineEntity)