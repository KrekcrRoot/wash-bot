import json
from app.dto.machine_entity import MachineEntity

class UserEntity:

    uuid: str
    telegram_id: str
    telegram_tag: str
    type: int
    kicked: bool
    count: int
    time: int
    trust_factor: int
    link_machine: MachineEntity

    def __init__(self, dict):
        self.__dict__.update(dict)


def create_user(dict):
    return json.loads(json.dumps(dict), object_hook=UserEntity)
