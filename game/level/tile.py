# AI&P Final project [Create M6 2022-2023]
# game/level/tile.py
#
# Copyright 2023 Jakub Stachurski
# Copyright 2023 Natalia Bueno Donadeu
#
# Imports
from game.level.access_flags import ACCESS_FLAGS
import pygame

# LevelTile
#   The tile of the level
#


class LevelTile:
    # Constructor
    #
    # position -> tile position of the tile
    # level    -> the level of the tile
    # access   -> the access_flags of the tile
    #
    def __init__(self, position, level, access: ACCESS_FLAGS):
        self.position = position
        self.linked = None
        self.level = level
        self.access = access
        self.storage = {}  # The AI Can store stuff here

    # get_neighbors
    #   A method for AI to get the neighboring tiles it can access
    #
    #   access -> the access level of the user
    #
    def get_neighbors(self, access):
        for neigh in self.get_adjescent():
            if neigh.test_access(access):
                yield neigh

        for neigh in self.linked:
            yield neigh

    # get_adjecent
    #   Gets all adjecent tiles
    #
    def get_adjecent(self):
        for x, y in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            try:
                yield self.get_relative_tile(x, y)
            except IndexError:
                pass

    # get_relative_tile
    #   Returns the tile relative to this tile (self)
    #
    #   x and y -> position of the target tile relative to this tile
    #
    def get_relative_tile(self, x, y):
        return self.level.get_tile(self.position[0] + x, self.position[1] + y)

    # link 
    #   Links this and the other tile together 
    def link(self, other):
        self.linked = other
        other.linked = self
        self.get_relative_tile
    
    # move_relative 
    #   get a relative tile, otherwise moving to the linked tile if it exists  
    #
    def move_relative(self, x, y):
        try:
            return self.get_relative_tile(x, y)
        except IndexError:
            if self.linked is not None:
                return self.linked
        return False
    # testAccess
    #   tests if the a object with certain access flags can access this tile
    #
    def testAccess(self, access):
        return access in self.access

    # try_move 
    #   Simulates a GameObject trying to move to a relative location
    #   with certain access flags 
    #
    def try_move(self, x, y, access):
        xstep = 0 if round(x) == 0 else x/abs(x)
        ystep = 0 if round(y) == 0 else y/abs(y)

        # Returns this tile when arrived to destination
        if xstep == 0 and ystep == 0:
            return self

        new_x = x
        new_y = y
        new_tile = False

        if xstep != 0:
            new_tile = self.move_relative(xstep, 0)
            new_x -= xstep
        else:  # ystep
            new_tile = self.move_relative(0, ystep)
            new_y -= ystep

        if new_tile is False:
            return None

        # Debug
        # print(f"input {x,y} steps {xstep, ystep}/n this_tile: {self.position} next_tile: {new_tile.position}, {new_tile.access} vs {access}")

        if new_tile.testAccess(access):
            return new_tile.try_move(new_x, new_y, access)
    # DEBUG_DrawTile
    #   Draws the tile according to the access flags it has
    #
    def DEBUG_DrawTile(self, surface: pygame.Surface, rect: tuple):
        color = ()
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

        surface.fill(color, rect)
