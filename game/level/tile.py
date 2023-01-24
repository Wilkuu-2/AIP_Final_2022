# AI&P Final project [Create M6 2022-2023]
# game/level/tile.py
#
# Copyright 2023 Jakub Stachurski
# Copyright 2023 Natalia Bueno Donadeu
#
# Imports
from .access_flags import ACCESS_FLAGS
from pygame.surface import Surface
from typing_extensions import Self, Any
from typing import Union, Literal


class LevelTile:
    """A tile of the level

    position -> tile position of the tile
    level    -> the level of the tile
    access   -> the access_flags of the tile
    """

    def __init__(self: Self, position: tuple[int, int], level, access: ACCESS_FLAGS):
        self.position = position
        self.linked = None
        self.level = level
        self.access = access
        # The AI Can store stuff here
        self.storage: dict[hash, dict[str, Any]] = {}

    def get_neighbors(self: Self, access: ACCESS_FLAGS):
        """A method for AI to get the neighboring tiles it can access"""
        for neigh in self.get_adjecent():
            if neigh.testAccess(access):
                yield neigh

        if self.linked is not None:
            self.linked

    def get_adjecent(self: Self):
        """Gets all adjecent tiles"""
        for x, y in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            try:
                yield self.get_relative_tile(x, y)
            except IndexError:
                pass

    def get_relative_tile(self: Self, x: int, y: int):
        """Returns the tile relative to this tile"""
        return self.level.get_tile(self.position[0] + x, self.position[1] + y)

    def link(self: Self, other: Self):
        """Links this and the other tile together"""
        self.linked = other
        other.linked = self
        self.get_relative_tile

    def move_relative(self: Self, x: int, y: int) -> Union[Self, Literal[None]]:
        """Get a relative tile if it exists, otherwise moving to the linked tile if it exists"""
        try:
            return self.get_relative_tile(x, y)
        except IndexError:
            if self.linked is not None:
                return self.linked

    def testAccess(self: Self, access: ACCESS_FLAGS) -> bool:
        """Tests if the a object with certain access flags can access this tile"""
        return access in self.access

    def try_move(self: Self, x: int, y: int, access: ACCESS_FLAGS) -> Union[Self, Literal[None]]:
        """Simulates a GameObject trying to move to a relative location
        with certain access flags.

        Returns

        Recursive, checks in a straight line in the x direction than the y direction.
        """
        xstep = 0 if round(x) == 0 else round(x/abs(x))
        ystep = 0 if round(y) == 0 else round(y/abs(y))

        # Returns this tile when arrived to destination
        if xstep == 0 and ystep == 0:
            return self

        new_x = x
        new_y = y
        new_tile: Union[LevelTile, Literal[None]] = None

        # Get the next tile in the path
        if xstep != 0:  # xstep
            new_tile = self.move_relative(xstep, 0)
            new_x -= xstep
        else:  # ystep
            new_tile = self.move_relative(0, ystep)
            new_y -= ystep

        # Check is new_tile exits
        if new_tile is None:
            return None

        # Debug
        # print(f"input {x,y} steps {xstep, ystep}/n this_tile: {self.position} next_tile: {new_tile.position}, {new_tile.access} vs {access}")

        # Test if the tile is accessible
        if new_tile.testAccess(access):
            return new_tile.try_move(new_x, new_y, access)

    def set_data(self, ai_hash: hash, key: str, data: any):
        if ai_hash not in self.storage:
            self.storage[ai_hash] = {}
        self.storage[ai_hash][key] = data

    def get_data(self, ai_hash: hash, key: str):
        return self.storage[ai_hash][key]

    def DEBUG_DrawTile(self: Self, surface: Surface, rect: tuple[int, int, int, int]):
        """
        Draws the tile according to the access flags it has
        """
        # Get the proper color
        color = (0, 0, 0)
        match self.access:
            case ACCESS_FLAGS.ALL:
                color = (0, 255, 0)
            case ACCESS_FLAGS.NONE:
                color = (255, 0, 0)
            case ACCESS_FLAGS.AI:
                color = (255, 255, 0)
            case ACCESS_FLAGS.PLAYER:
                color = (0, 0, 255)
            case _:
                color = (255, 255, 255)

        # Draw call
        surface.fill(color, rect)

    def __repr__(self):
        return str(self.position)