# AI&P Final project [Create M6 2022-2023]
# game/astar_enemy.py
#
# Copyright 2022-2023 Jakub Stachurski
# Copyright 2022-2023 Natalia Bueno Donadeu
#
# Imports
from .base_enemy import BaseEnemy
from input_helpers import InHandler
from level import LevelTile
from .player import Player
import pygame


class AstarEnemy(BaseEnemy):
    def __init__(self, tile: LevelTile, input_handler: InHandler, player: Player):
        super().__init__(tile, input_handler, player)

    def AI_step(self):
        start = self.get_level_tile()
        target = self.player.get_level_tile()

        priority_queue = [start]
        visited: list[LevelTile]= []

        self.set_data(start, "distance", 0)

        while len(priority_queue) > 0:
            current_node = priority_queue.pop(0)
            if current_node is target:
                break

            if current_node not in visited:
                visited.append(current_node)
                gscore = self.get_data(current_node, "distance") + 1
                for next_node in current_node.get_neighbors(self.access_flags):
                    hscore = self.manhattan_distance(next_node)
                    if next_node not in visited:
                        if next_node not in priority_queue:
                            self.set_data(next_node, "parent", current_node)
                            self.set_data(next_node, "distance", gscore)
                            self.set_data(next_node, "score", gscore + hscore)
                            self.insort(priority_queue, next_node, "score")

                        elif gscore < self.get_data(next_node, "distance"):
                            self.set_data(next_node, "parent", current_node)
                            self.set_data(next_node, "distance", gscore)
                            self.set_data(next_node, "score", gscore + hscore)
                            priority_queue.remove(next_node)
                            self.insort(priority_queue, next_node, "score")

        self.move_from_path(target, start, "parent")
    
    def display(self, screen: pygame.surface.Surface, screen_pos: tuple[int,int], screen_size: tuple[int,int]):
        """Override of GameObject.display"""

        rect = (screen_pos[0],
                screen_pos[1],
                screen_size[0],
                screen_size[1])

        pygame.draw.ellipse(screen, (255, 150, 200), rect)
