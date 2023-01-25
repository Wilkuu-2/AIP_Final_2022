# AI&P Final project [Create M6 2022-2023]
# game/base_enemy.py
#
# Copyright 2022-2023 Jakub Stachurski
# Copyright 2022-2023 Natalia Bueno Donadeu
#
# Imports
from .game_object import GameObject
from input_helpers.input_handler import InHandler
from level import Level, LevelTile, ACCESS_FLAGS
from .player import Player
from typing_extensions import Any


class BaseEnemy(GameObject):
    """The base class for the enemies

       Subclass of GameObject, see game/game_object.py
       player -> The player to chase
    """
    AI_ID = 0

    def __init__(self, pos: tuple[int, int], input_handler: InHandler, level: Level, player: Player):
        super().__init__(pos, (1, 1), input_handler,  level, ACCESS_FLAGS.AI)
        self.player = player

        # Create a ID for the Enemy
        self.ID = BaseEnemy.AI_ID
        BaseEnemy.AI_ID += 1

        input_handler.attach("Timed_Move", self.AI_step)

    def on_collide(self, other: GameObject):
        if other is self.player:
            self.player.handle_enemy(self)

    def _AI_step(self):
        if self.can_move:
            self.AI_step()

    def AI_step(self):
        """The method to override and implemt AI into.
        Use move((x,y)) to move in here
        """

    def manhattan_distance(self, tile):
        """Return the manhattan distance between the player and the
        """

        player_x, player_y = self.player.pos
        ai_x, ai_y = tile.position
        dx = abs(ai_x - player_x)
        dy = abs(ai_y - player_y)

        return dx + dy

    def __hash__(self):
        """Returns the ID as the hash for the tile storage
        """
        return hash(f"AI_OBJECT_{self.ID}")

    def set_data(self, tile: LevelTile, key: str, data: Any):
        """Sets data at the given tile, owned by this BaseEnemy instance
        """
        tile.set_data(hash(self), key, data)

    def get_data(self, tile: LevelTile, key: str):
        """Gets data at the given tile, owned by this BaseEnemy instance
        """
        return tile.get_data(hash(self), key)

    def insort(self, arr: list, val, key: str):
        arr.insert(self.bisect(key, arr, val), val)

    def bisect(self, key: str, arr: list, value, low=0, high=None):
        if high is None:
            high = len(arr)

        while low < high:
            middle = (low + high) // 2
            if self.get_data(arr[middle], key) < self.get_data(value, key):
                low = middle + 1
            else:
                high = middle

        return low

    def travel_back(self, start, target, key):
        nodes = [start]
        while nodes[-1] != target:
            try:
                parent = self.get_data(nodes[-1], key)
            except KeyError:
                return None
            if parent == nodes[-1]:
                break

            nodes.append(parent)

        return nodes

    def move_from_path(self, target, start, key: str):
        nodes = self.travel_back(target, start, key)
        if nodes is None:
            return

        next_node = nodes[-min(2, len(nodes))]
        dist = (next_node.position[0] - start.position[0],
                next_node.position[1] - start.position[1])
        if abs(dist[0]) > 2:
            dist = (-dist[0]/dist[0], dist[1])

        self.move(dist)
