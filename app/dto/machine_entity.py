class MachineEntity:

    uuid: str
    title: str
    isActive: bool
    broken: bool

    def __init__(self, uuid, title, isActive, broken):
        self.uuid = uuid
        self.title = title
        self.isActive = isActive
        self.broken = broken