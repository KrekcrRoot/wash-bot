import json
from app.dto.user_entity import UserEntity

class OrderEntity:
    uuid: str
    created_at: str
    user: UserEntity

    def __init__(self,dict):
        self.__dict__.update(dict)

def create_orderEntity(dict):
    return json.loads(json.dumps(dict),object_hook=OrderEntity)