# AI&P Final project [Create M6 2022-2023]
# game/random_enemt.py
#
# Copyright 2022-2023 Jakub Stachurski
# Copyright 2022-2023 Natalia Bueno Donadeu
#
# Imports
from .base_enemy import BaseEnemy
from input_helpers import InHandler
from level import LevelTile
from .player import Player
from random import shuffle
import pygame


class RandomEnemy(BaseEnemy):
    __name__ = "Random Enemy" 
    def __init__(self, tile: LevelTile, input_handler: InHandler, player: Player):
        super().__init__(tile, input_handler, player)

    def AI_step(self, target: LevelTile):
        """Override of BaseEnemy.display"""
        visited = []
        for _ in range(2):
            start = self.tile
            choices = list(start.get_neighbors(self.access_flags))
            for vis in visited:
                if vis in choices:
                    choices.remove(vis)
            shuffle(choices)
            chosen = choices[0]

            dist: list[int] = [chosen.position[0] - start.position[0],\
                chosen.position[1] - start.position[1]]

            if abs(dist[0]) > 1:
                dist[0] = round(-dist[0]/dist[0])

            self.move(tuple(dist))

    def display(self, screen: pygame.surface.Surface, screen_pos: tuple, screen_size: tuple):
        """Override of GameObject.display"""

        rect = (screen_pos[0],
                screen_pos[1],
                screen_size[0],
                screen_size[1])

        pygame.draw.ellipse(screen, (255, 180, 50), rect)

