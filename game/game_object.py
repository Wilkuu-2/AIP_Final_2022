
# AI&P Final project [Create M6 2022-2023]
# game/game_object.py
#
# Copyright 2023 Jakub Stachurski
# Copyright 2023 Natalia Bueno Donadeu
#

# Imports
from pygame import Vector2, draw, Rect
from input_helpers.input_handler import EventMethod

#
# GameObject
#
# An entity base class for all moving or interactive objects
#


class GameObject:
    __name__ = "Unnamed Game Object"
    _gameobject_id = 0

    # Constructor
    #
    # pos -> Initial position in pixels, tuple in form of (x,y)
    # size -> Hitbox size in pixels, tuple in form of (x,y)
    # level -> The level this GameObject lives in
    #
    def __init__(self, pos: tuple, size: tuple, level, access_flags):
        self.size = Vector2(size)
        self.level = level
        self.pos = pos
        self.access_flags = access_flags

        # Give the object an id
        self.id = GameObject._gameobject_id
        GameObject._gameobject_id += 1

        # Register inside of the level
        level.register_GameObject(self)

    # Move
    #   This method moves the GameObject by the vector2 given
    #
    #   mv -> The amount of movement to be done ,a tuple vector in form of (x,y)
    #
    def move(self, mv: tuple):
        move_x, move_y = mv
        # Test for collisions and get the correct tile
        new_tile = self.collide(move_x, move_y)

        if new_tile is not True:
            # Finalize the move
            self.pos = new_tile.position

    # _display
    #   A base class side of the display method, calls display() at the end.
    #
    #   screen -> pygame surface object
    #   units -> units which symbolise 1 tile of the level
    #
    #   DO NOT OVERRIDE
    #
    def _display(self, screen, units):
        screen_pos = self.level.get_screen_position(
            units, self.pos[0], self.pos[1])
        screen_size = (units[0] * self.size[0], units[1] * self.size[1])

        self.display(screen, screen_pos, screen_size)

    # display
    #   A method that handles drawing of the object
    #
    #   screen -> pygame screen object
    #   screen_pos -> position of the object on the screen
    #   screen_size -> size of the object on the screen
    #
    #   The correct usage of GameObject involves overriding this method
    #   If that is not done, the following will act as a placeholder

    def display(self, screen, screen_pos, screen_size):
        rect = Rect(screen_pos[0],
                    screen_pos[1],
                    screen_size[0],
                    screen_size[1])

        draw.ellipse(screen, (255, 50, 50), rect)

    # _update
    #  The base class side pf the update method
    #
    #   dt -> time since last frame in seconds
    #
    #  DO NOT OVERRIDE
    #
    def _update(self, dt):
        self.update(dt)

    # update
    #   A method that handles logic of the object
    #
    #   dt -> time since last frame in seconds
    #
    #   The correct usage of GameObject involves overriding this method
    #   If that is not done, the following will act as a placeholder
    def update(self, dt):
        pass

    # collide
    #   Inherent collision logic for game objects
    #
    #   new_pos -> relative position of the collision
    #
    def collide(self, x, y):
        tile = self.get_level_tile()
        next_tile = tile.try_move(x, y, self.access_flags)

        if next_tile is None:
            return True

        abs_x, abs_y = next_tile.position

        for other in self.level.get_GameObjects(abs_x, abs_y):
            self.on_collide(other)
            other.on_collide(self)

        return next_tile

    # on_collide
    #   A method that handles custom logic around collisons
    #
    #   other -> The GameObject that collided with you.
    #
    #   The correct usage of GameObject involves overriding this method
    #   If that is not done, the following will act as a placeholder

    def on_collide(self, other):
        pass

    # get_level_tile(self)
    #   returns the tile the GameObject is on
    #
    def get_level_tile(self):
        return self.level.get_tile(self.pos[0], self.pos[1])

#
#   Trigger
#
#   A template for a simple boundary trigger
#   that is based on the GameObject class
#


class Trigger(GameObject):
    __name__ = "Trigger"

    # Constructor
    # pos, size -> See GameObject
    # on_trigger-> EventMethod that will be invoked when
    #               another GameObject gets into this Trigger's hitbox
    #
    def __init__(self, pos: tuple, size: tuple, on_trigger: EventMethod):
        super().__init__(pos, size)
        self.on_trigger = on_trigger

    # Override: See GameObject.on_collide
    def on_collide(self, other):
        self.on_trigger.invoke(self, other)
