# AI&P Final project [Create M6 2022-2023]
# game/level/level.py
#
# Copyright 2023 Jakub Stachurski
# Copyright 2023 Natalia Bueno Donadeu
#
# Imports
from .tile import LevelTile
from pygame.surface import Surface
from .access_flags import ACCESS_FLAGS
from game.game_object import GameObject
from typing import Self


class Level:
    """The class which stores the state of the game.
       It holds the gameobjects and the tiles that comprise the game's world

        size -> the size of the level
        levelarr -> the list that stores the level in integers
        linked -> a tuple of two position on the level, which are to be linked
                  TODO: Find a way to get those parsed in the arr
    """

    def __init__(self: Self, size: tuple[int, int], levelarr: list[list[int]], linked: tuple[tuple, tuple]):
        self.size = size
        self.tiles: list[list[LevelTile]] = []
        self.game_objects: list[GameObject] = []

        # Read through the level array and construct the tiles in the tiles list
        for x in range(0, size[0]):
            self.tiles.append([])
            for y in range(0, size[1]):
                val = levelarr[y][x]

                # Gives the tile a access flag which will determine if things can enter that tile or not
                access = ACCESS_FLAGS.NONE

                if val in [0, 1, 2]:    # 0, 1, 2: Passible tiles with or without the dots
                    access = ACCESS_FLAGS.ALL
                elif val == 9:          # 9: Gate of the enemy base
                    access = ACCESS_FLAGS.AI

                # Construct the tile
                self.tiles[x].append(LevelTile((x, y), self, access))

        # Link the two looping spots together
        link1 = self.get_tile(*linked[0])
        link2 = self.get_tile(*linked[1])

        link1.link(link2)

    def DEBUG_DrawLevel(self: Self, surface: Surface, width: int, height: int):
        """A Debug way to draw the tiles based on the access flags of the tile
        """

        unit_x, unit_y = self.get_units(width, height)

        for x in range(0, self.size[0]):
            for y in range(0, self.size[1]):
                self.get_tile(x, y).DEBUG_DrawTile(
                    surface, (x * unit_x, y * unit_y, unit_x, unit_y))

    def get_units(self: Self, width: int, height: int) -> tuple:
        """ Returns the screen size of single tile in the X and Y directions
            given the available size on the screen
        """
        unit_x = width // self.size[0]
        unit_y = height // self.size[1]
        return unit_x, unit_y

    def validate_tile_position(self: Self, x: int, y: int):
        """Validate of the position matches the size of the level

        x and y -> the position to be checked

        Raises IndexError on invalid input
        """
        if x < 0 or y < 0 or x > self.size[0] or y > self.size[1]:
            raise IndexError(
                f"Invalid tile position: ({x},{y})/({self.size[0]},{self.size[1]})")

    def get_screen_position(self: Self, units: tuple, x: int, y: int) -> tuple:
        """Gets the top left position of the given tile in screen space

        units   -> units
        x and y -> the position to be converted
        """
        self.validate_tile_position(x, y)
        return x * units[0], y * units[1]

    def register_GameObject(self: Self, game_object: GameObject):
        """
       Adds a game object onto the game_objects list
        """
        # The game_object should be in the array only once
        if game_object in self.game_objects:
            raise ValueError("Duplicate registration of a GameObject")

        self.game_objects.append(game_object)

    def deregister_GameObject(self: Self, game_object: GameObject):
        """Removes a game object from the game_objects list"""
        self.game_objects.remove(game_object)

    def get_GameObjects(self: Self, x: int, y: int) -> list:
        """Returns all GameObjects that occupy the tile
           on tile coordinates x, y"""
        self.validate_tile_position(x, y)

        found = []
        for game_object in self.game_objects:
            if (round(game_object.pos[0] == x)) and (round(game_object.pos[1]) == y):
                found.append(game_object)
        return found

    def display_GameObjects(self: Self, screen: Surface, size: tuple):
        """Calls GameObject._display on all GameObjects
        see: game/game_object.py for more details
        """
        units = self.get_units(size[0], size[1])
        for game_object in self.game_objects:
            game_object._display(screen, units)

    def update_GameObjects(self: Self, dt: float):
        """Calls GameObject._update on all GameObjects
        see: game/game_object.py for more details
        """
        for game_object in self.game_objects:
            game_object._update(dt)

    def get_tile(self: Self, x: int, y: int) -> LevelTile:
        """Returns the tile at a given position"""
        self.validate_tile_position(x, y)
        return self.tiles[round(x)][round(y)]
