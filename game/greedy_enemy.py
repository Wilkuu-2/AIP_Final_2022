# AI&P Final project [Create M6 2022-2023]
# game/greedy_enemy.py
#
# Copyright 2022-2023 Jakub Stachurski
# Copyright 2022-2023 Natalia Bueno Donadeu
#
# Imports
from .base_enemy import BaseEnemy
from input_helpers.input_handler import InHandler
from level import LevelTile
from pygame import draw
from pygame.surface import Surface
from .player import Player


class GreedyEnemy(BaseEnemy):
    def __init__(self, tile: LevelTile, input_handler: InHandler, player: Player):
        super().__init__(tile, input_handler, player)

    def AI_step(self):
        start = self.get_level_tile()
        target = self.player.get_level_tile()

        priority_queue = [start]
        visited = []

        while len(priority_queue) > 0:
            current_node = priority_queue.pop(0)
            if current_node is target:
                break

            if current_node not in visited:
                visited.append(current_node)
                neighbours = current_node.get_neighbors(self.access_flags)
                for next_node in neighbours:
                    if next_node not in visited:
                        self.set_data(next_node, "parent", current_node)
                        gscore = self.manhattan_distance(next_node)
                        self.set_data(next_node, "score", gscore)
                        self.insort(priority_queue, next_node, "score")

        self.move_from_path(target, start, "parent")

    def display(self, screen: Surface, screen_pos: tuple, screen_size: tuple):
        """Override of GameObject.display"""

        rect = (screen_pos[0],
                screen_pos[1],
                screen_size[0],
                screen_size[1])

        draw.ellipse(screen, (200, 30, 30), rect)
