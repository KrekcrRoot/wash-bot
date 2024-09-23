import json
from app.dto.user_entity import UserEntity

class OrderEntity:
    uuid: str
    user: UserEntity
    created_at: str

    def __init__(self,dict):
        self.__dict__.update(dict)

def create_orderEntity(dict):
    return json.load(json.dumps(dict),object_hook=OrderEntity)