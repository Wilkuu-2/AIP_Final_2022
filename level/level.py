# AI&P Final project [Create M6 2022-2023]
# level/level.py
#
# Copyright 2023 Jakub Stachurski
# Copyright 2023 Natalia Bueno Donadeu
#
# Imports
from level import LevelTile
from level.level_layout import parse_map_file

from pygame.surface import Surface
from typing_extensions import Self
from game import game_object

class Level:
    """The class which stores the state of the game.
       It holds the the tiles that comprise the game's world
    """

    def __init__(self):
        # Parse the map in the level_layout.py
        self.size, self.tiles, linked = parse_map_file()
        self.game_objects: list[game_object.GameObject] = []

        for tile_line in self.tiles:
            for tile in tile_line:
                tile.level = self

        # Read through the level array and construct the tiles in the tiles list

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


    def display_GameObjects(self: Self, screen: Surface, size: tuple):
        """Calls GameObject._display on all GameObjects
        see: game/game_object.py for more details
        """
        units = self.get_units(size[0], size[1])
        for game_obj in game_object.GameObject.GAME_OBJECTS:
            screen_pos = self.get_screen_position(units, *game_obj.tile.position)
            game_obj._display(screen, screen_pos, units)

    def get_tile(self: Self, x: int, y: int) -> LevelTile:
        """Returns the tile at a given position"""
        self.validate_tile_position(x, y)
        return self.tiles[round(y)][round(x)]

    def clear_tile_storage(self):
        """Clears the storage for the AI"""
        for row in self.tiles:
            for element in row:
                element.storage.clear()

    @staticmethod
    def get_GameObjects(x,y):
        return game_object.GameObject.get_gameobjects(x,y)
