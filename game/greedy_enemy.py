from .base_enemy import BaseEnemy
from input_helpers.input_handler import InHandler
from .level.level import Level
from .level.tile import LevelTile
from .player import Player


class GreedyEnemy(BaseEnemy):
    def __init__(self, pos: tuple[int, int], input_handler: InHandler, level: Level, player: Player):
        super().__init__(pos, input_handler, level, player)

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
