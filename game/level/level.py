from game.level.tile import LevelTile
import pygame.surface
from game.level.access_flags import ACCESS_FLAGS


class Level:
    def __init__(self, size: tuple, levelarr: list, linked: tuple):
        self.size = size
        self.tiles = []
        self.game_objects = []

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

        link1 = self.get_tile(*linked[0])
        link2 = self.get_tile(*linked[1])

        link1.link(link2)

    def DEBUG_DrawLevel(self, sur: pygame.Surface, width, height):
        unit_x, unit_y = self.get_units(width, height)

        for x in range(0, self.size[0]):
            for y in range(0, self.size[1]):
                self.get_tile(x, y).DEBUG_DrawTile(
                    sur, (x * unit_x, y * unit_y, unit_x, unit_y))

    def get_units(self, width, height):
        unit_x = (width - (width % self.size[0])) / self.size[0]
        unit_y = (height - (height % self.size[1])) / self.size[1]
        return unit_x, unit_y

    def validate_tile_position(self, x, y):
        if x < 0 or y < 0 or x > self.size[0] or y > self.size[1]:
            raise IndexError(
                f"Invalid tile position: ({x},{y})/({self.size[0]},{self.size[1]})")

    def get_screen_position(self, units, x, y):
        self.validate_tile_position(x, y)
        return x * units[0], y * units[1]

    def register_GameObject(self, game_object):
        self.game_objects.append(game_object)

    def deregister_GameObject(self, game_object):
        self.game_objects.remove(game_object)

    def get_GameObjects(self, x, y):
        found = []
        for game_object in self.game_objects:
            if (round(game_object.pos[0] == x)) and (round(game_object.pos[1]) == y):
                found.append(game_object)
        return found

    def display_GameObjects(self, screen, size):
        units = self.get_units(size[0], size[1])
        for game_object in self.game_objects:
            game_object._display(screen, units)

    def update_GameObjects(self, dt):
        for game_object in self.game_objects:
            game_object._update(dt)

    def get_tile(self, x, y) -> LevelTile:
        self.validate_tile_position(x, y)
        return self.tiles[round(x)][round(y)]
