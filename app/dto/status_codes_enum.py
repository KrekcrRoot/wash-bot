from enum import Enum

#IDK what shit is coded here, but it can make enum equal to multiple things
class StatusCode(Enum):
    #
    def __new__(cls, *values):
        member = object.__new__(cls)
        member._value_ = values[0]
        member.all_values = values
        return member
    #
    @classmethod
    def _missing_(cls, value):
        for member in cls:
            if value in member.all_values:
                return member
    #
    OK = 200, 201
    Error = 404
    Server_error = 500

    def __repr__(self):
        # make the repr not reduntant
        return "<%s.%s>" % (self.__class__.__name__, self.name)