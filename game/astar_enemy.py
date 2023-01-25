from .base_enemy import BaseEnemy
from input_helpers.input_handler import InHandler
from .level.level import Level
from .level.tile import LevelTile
from .player import Player
import pygame


class AstarEnemy(BaseEnemy):
    def __init__(self, pos: tuple[int, int], input_handler: InHandler, level: Level, player: Player):
        super().__init__(pos, input_handler, level, player)

    def AI_step(self):
        start = self.get_level_tile()
        target = self.player.get_level_tile()

        priority_queue = [start]
        visited = []

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
    
    def display(self, screen: pygame.surface.Surface, screen_pos: tuple, screen_size: tuple):
        """Override of GameObject.display"""

        rect = (screen_pos[0],
                screen_pos[1],
                screen_size[0],
                screen_size[1])

        pygame.draw.ellipse(screen, (255, 150, 200), rect)
