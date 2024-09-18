
class UserEntity:

    uuid: str
    telegram_id: str
    telegram_tag: str
    type: int
    kicked: bool
    count: int
    time: int
    trust_factor: int
    link_machine: object

    def __init__(self, uuid, telegram_id, telegram_tag, type, kicked, count, time, trust_factor, link_machine):
        self.uuid = uuid
        self.telegram_id = telegram_id
        self.telegram_tag = telegram_tag
        self.type = type
        self.kicked = kicked
        self.count = count
        self.time = time
        self.trust_factor = trust_factor
        self.link_machine = link_machine