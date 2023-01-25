# AI&P Final project [Create M6 2022-2023]
# game/level/access_flags.py
#
# Copyright 2023 Jakub Stachurski
# Copyright 2023 Natalia Bueno Donadeu
#
# Imports
from enum import Enum


# ACCESS_FLAGS
#
class ACCESS_FLAGS(Enum):
    """An Enum that represents the accessibility of a tile"""
    ALL = 0b111
    PLAYER = 0b010
    AI = 0b100
    PELLET = 0b001
    NONE = 0b000

    # Overide of the "in" operator
    #
    def __contains__(self, other):
        """Checks if the other object has at least one
        of the necessary flags to enter the tile
        """
        if type(other) is type(self):
            return self.value & other.value > 0
        else:
            return self.value & other > 0
