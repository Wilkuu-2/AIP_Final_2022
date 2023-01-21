from game.level.access_flags import ACCESS_FLAGS
import pygame

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

    def move_relative(self, x, y):
        try:
            return self.get_relative_tile(x, y)
        except IndexError:
            if self.linked is not None:
                return self.linked
        return False

    def testAccess(self, access):
        return access in self.access

    def try_move(self, x, y,): 
        new_tile = self.move_relative(self, x, y)
        if new_tile is False:
            return None

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
