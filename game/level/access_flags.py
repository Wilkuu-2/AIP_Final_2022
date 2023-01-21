# AI&P Final project [Create M6 2022-2023]
# game/level/access_flags.py
#
# Copyright 2023 Jakub Stachurski
# Copyright 2023 Natalia Bueno Donadeu
#
# Imports
from enum import Enum


# ACCESS_FLAGS
#   An Enum that represents the accessibility of a tile
#
class ACCESS_FLAGS(Enum):
    ALL = 0b11
    PLAYER = 0b01
    AI = 0b10
    NONE = 0b00

    # Overide of the "in" operator
    #   Checks if the other object has at least
    #   one of the necessary flags to enter the tile
    #
    def __contains__(self, other):
        if type(other) is type(self):
            return self.value & other.value > 0
        else:
            return self.value & other > 0
