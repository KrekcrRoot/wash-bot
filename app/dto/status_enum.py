from enum import Enum

class Status(Enum):

    Free = 'Free'
    Busy = 'Busy'
    Waiting = 'Waiting'
    Ordered = 'Ordered'