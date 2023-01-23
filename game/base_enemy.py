from .game_object import GameObject
from input_helpers.input_handler import InHandler
from .level.level import Level
from .level.tile import LevelTile
from .level.access_flags import ACCESS_FLAGS
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

    def on_collide(self: GameObject, other: GameObject):
        if other is self.player:
            print("Collided with player")

    def AI_step(self):
        """The method to override and implement AI into.
        Use move((x,y)) to move in here
        """
        pass

    def get_neighbors(self):
        """A wrapper that get the neighbors for the AI
        """
        return self.get_level_tile().get_neighbors(self.access_flags)

    def manhattan_distance(self):
        """Return the manhattan distance between the player and the 
        """
        player_x, player_y = self.player.pos
        ai_x, ai_y = self.pos
        return abs(ai_x - player_x) + abs(ai_y - player_y)

    def __hash__(self):
        """Returns the ID as the hash for the tile storage 
        """
        return self.ID

    def set_data(self, tile: LevelTile, key: str, data: Any):
        """Sets data at the given tile, owned by this BaseEnemy instance
        """
        tile.set_data(hash(self), key, data)

    def get_data(self, tile: LevelTile, key: str):
        """Gets data at the given tile, owned by this BaseEnemy instance
        """
        return tile.get_data(hash(self), key)

    def set_data_here(self, key: str, data: Any):
        """Sets data at the current tile, owned by this BaseEnemy instance
        """
        self.get_level_tile.set_data(hash(self), key, data)

    def get_data_here(self, key: str):
        """Gets data at the current tile, owned by this BaseEnemy instance
        """
        self.get_level_tile().get_data(hash(self), key)
