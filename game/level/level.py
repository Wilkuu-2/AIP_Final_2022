
import pygame.surface
from enum import Enum


class ACCESS_FLAGS(Enum):
    ALL = 0b11
    PLAYER = 0b01
    AI = 0b10
    NONE = 0b00

    def __contains__(self, other):
        if type(other) is type(self):
            return self.value & other.value > 0
        else:
            return self.value & other > 0


class LevelTile:
    def __init__(self, position, level, access: ACCESS_FLAGS):
        self.position = position
        self.linked = None
        self.level = level
        self.access = access
        self.storage = {}  # The AI Can store stuff here

    def get_neighbors(self):
        for neigh in self.get_adjescent():
            if neigh.is_accessible:
                yield neigh

        for neigh in self.linked:
            yield neigh

    def get_adjecent(self):
        for x, y in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            try:
                yield self.get_relative_tile(x, y)
            except IndexError:
                pass

    def get_relative_tile(self, x, y):
        return self.level.get_tile(self.position[0] + x, self.position[1])

    def link(self, other):
        self.linked = other
        other.linked = self

    def move_from(self, x, y):
        try:
            return self.get_relative_tile(x, y)
        except IndexError:
            if self.linked is not None:
                return self.linked

        return False

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


class Level:
    def __init__(self, size: tuple, levelarr: list):
        self.size = size
        self.tiles = []
        self.gameobjects = []
        for x in range(0, size[0]):
            self.tiles.append([])
            for y in range(0, size[1]):
                val = levelarr[y][x]

                access = ACCESS_FLAGS.NONE

                if val in [0, 1, 2]:
                    access = ACCESS_FLAGS.ALL
                elif val == 9:
                    access = ACCESS_FLAGS.AI

                self.tiles[x].append(LevelTile((x, y), self, access))

    def DEBUG_DrawLevel(self, sur: pygame.Surface, width, height):
        unit_x = width / self.size[0]
        unit_y = height / self.size[1]

        for x in range(0, self.size[0]):
            for y in range(0, self.size[1]):
                self.get_tile(x, y).DEBUG_DrawTile(
                    sur, (x * unit_x, y * unit_y, unit_x, unit_y))

    def get_tile(self, x, y):
        return self.tiles[x][y]
