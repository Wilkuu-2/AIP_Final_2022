
# AI&P Final project [Create M6 2023]
# game/player.py
#
# Copyright 2023 Jakub Stachurski
# Copyright 2023 Natalia Bueno Donadeu
#

# Imports
from game.game_object import GameObject
from input_helpers.input_handler import InHandler
from game.level.access_flags import ACCESS_FLAGS


#
# Player
#
# The player entity, this is where the player logic lives
#
class Player(GameObject):
    __name__ = "Player object"

    # Constructor
    # 
    #   pos -> see GameObject
    #   level -> see GameObject
    #   input_handler -> InHandler that will handle the movement and other actions
    #
    def __init__(self, pos: tuple, input_handler: InHandler, level):
        super().__init__(pos, [1, 1], level, ACCESS_FLAGS.PLAYER)

        input_handler.attach("UP",   self.move, (0, -1))
        input_handler.attach("DOWN", self.move, (0, 1))
        input_handler.attach("LEFT", self.move, (-1, 0))
        input_handler.attach("RIGHT", self.move, (1, 0))
