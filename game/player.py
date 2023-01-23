
# AI&P Final project [Create M6 2023]
# game/player.py
#
# Copyright 2023 Jakub Stachurski
# Copyright 2023 Natalia Bueno Donadeu
#

# Imports
from .game_object import GameObject
from input_helpers.input_handler import InHandler
from .level.access_flags import ACCESS_FLAGS
from .level.level import Level


class Player(GameObject):
    """ The player entity, this is where the player logic lives
    pos -> see GameObject
    level -> see GameObject
    input_handler -> InHandler that will handle the movement and other actions
    """
    __name__ = "Player object"

    def __init__(self, pos: tuple[int, int], input_handler: InHandler, level: Level):
        super().__init__(pos, (1, 1), input_handler, level, ACCESS_FLAGS.PLAYER)

        input_handler.attach("UP",   self.timed_move, (0, -1))
        input_handler.attach("DOWN", self.timed_move, (0, 1))
        input_handler.attach("LEFT", self.timed_move, (-1, 0))
        input_handler.attach("RIGHT", self.timed_move, (1, 0))
