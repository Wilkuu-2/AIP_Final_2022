# AI&P Final project [Create M6 2022-2023]
# game/level/level.py
#
# Copyright 2023 Jakub Stachurski
# Copyright 2023 Natalia Bueno Donadeu
#
# Imports 
from game.level.tile import LevelTile
import pygame.surface
from game.level.access_flags import ACCESS_FLAGS

# Level
#   The class which stores the state of the game.
#   It holds the gameobjects and the tiles that comprise the game's world
#


class Level:
    # Constructor
    #   size -> the size of the level
    #   levelarr -> the list that stores the level in integers
    #   linked -> a tuple of two position on the level, which are to be linked
    #             TODO: Find a way to get those parsed in the arr
    #
    def __init__(self, size: tuple, levelarr: list, linked: tuple):
        self.size = size
        self.tiles = []
        self.game_objects = []

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

    # DEBUG_DrawLevel
    #   A Debug way to draw the tiles based on the access flags of the tile
    #
    #   surface -> The pygame surface object to draw onto
    #   width -> the width of the surface
    #   height -> the height of the surface
    #
    def DEBUG_DrawLevel(self, surface: pygame.Surface, width, height):
        unit_x, unit_y = self.get_units(width, height)

        for x in range(0, self.size[0]):
            for y in range(0, self.size[1]):
                self.get_tile(x, y).DEBUG_DrawTile(
                    surface, (x * unit_x, y * unit_y, unit_x, unit_y))

    # get_units
    #   Calculated how big a single tile is in the X and Y directions
    #
    #   width -> the width of the surface that gets drawn onto
    #   height -> the height of the surface that gets drawn onto
    #
    def get_units(self, width, height):
        unit_x = width // self.size[0]
        unit_y = height // self.size[1]
        return unit_x, unit_y

    # validate_tile_position
    #   Validate of the position matches the size of the level
    #
    #   x and y -> the position to be checked
    #
    def validate_tile_position(self, x, y):
        if x < 0 or y < 0 or x > self.size[0] or y > self.size[1]:
            raise IndexError(
                f"Invalid tile position: ({x},{y})/({self.size[0]},{self.size[1]})")

    # get_screen_position
    #   Gets the top left position of the given tile in screen space
    #
    #   units   -> units
    #   x and y -> the position to be converted
    #
    def get_screen_position(self, units, x, y):
        self.validate_tile_position(x, y)
        return x * units[0], y * units[1]

    # register_GameObject
    #   Adds a game object onto the game_objects list
    #
    #   game_object -> the GameObject to be added
    #
    def register_GameObject(self, game_object):
        # The game_object should be in the array only once
        if game_object in self.game_objects:
            raise ValueError("Duplicate registration of a GameObject")

        self.game_objects.append(game_object)

    # deregister_GameObject
    #   Removes a game object from the game_objects list
    #
    #   game_object -> the GameObject to be removed
    #
    def deregister_GameObject(self, game_object):
        self.game_objects.remove(game_object)

    # get_GameObjects
    #   Returns all GameObjects that occupy the tile
    #
    #   x and y -> the tile position to search
    #
    def get_GameObjects(self, x, y):
        found = []
        for game_object in self.game_objects:
            if (round(game_object.pos[0] == x)) and (round(game_object.pos[1]) == y):
                found.append(game_object)
        return found

    # display_GameObjects
    #   Calls GameObject._display on all GameObjects
    #   see: game/game_object.py for more details
    #
    def display_GameObjects(self, screen, size):
        units = self.get_units(size[0], size[1])
        for game_object in self.game_objects:
            game_object._display(screen, units)

    # update_GameObjects
    #   Calls GameObject._update on all GameObjects
    #   see: game/game_object.py for more details
    #
    def update_GameObjects(self, dt):
        for game_object in self.game_objects:
            game_object._update(dt)

    # get_tile
    #   Returns the tile at a given position
    #
    #   x and y -> Tile position of the wanted tile
    #
    def get_tile(self, x, y) -> LevelTile:
        self.validate_tile_position(x, y)
        return self.tiles[round(x)][round(y)]
