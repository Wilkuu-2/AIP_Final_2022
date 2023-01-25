from .base_enemy import BaseEnemy
from input_helpers.input_handler import InHandler
from .level.level import Level
from .level.tile import LevelTile
from .player import Player
from random import shuffle


class RandomEnemy(BaseEnemy):
    def __init__(self, pos: tuple[int, int], input_handler: InHandler, level: Level, player: Player):
        super().__init__(pos, input_handler, level, player)

    def AI_step(self):
        choices = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        for i in range(2):
            shuffle(choices)
            self.move(choices[0])
