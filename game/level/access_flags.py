
from enum import Enum

class ACCESS_FLAGS(Enum):
    ALL = 0b11
    PLAYER = 0b01
    AI = 0b10
    NONE = 0b00

    def __contains__(self, other):
        if type(other) is type(self):
            return self.value & other.value > 0
        else:
            return self.value & other > 0
