from game.game_object import GameObject
from input_helpers.input_handler import InHandler


class Player(GameObject):
    __name__ = "Player object"

    def __init__(self, pos: tuple, input_handler: InHandler, level):
        super().__init__(pos, [10, 10], level)

        input_handler.attach("UP",   self.move, (0, -1))
        input_handler.attach("DOWN", self.move, (0, 1))
        input_handler.attach("LEFT", self.move, (-1, 0))
        input_handler.attach("RIGHT", self.move, (1, 0))

        print(self.__name__)
