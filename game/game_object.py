
# AI&P Final project [Create M6 2022-2023]
# game/game_object.py
#
# Copyright 2023 Jakub Stachurski
# Copyright 2023 Natalia Bueno Donadeu
#

# Imports
from pygame import draw, Rect
from pygame.surface import Surface
from input_helpers.input_handler import InHandler, EventMethod
from .level.access_flags import ACCESS_FLAGS
from .level.level import Level, LevelTile
from typing_extensions import Self, Literal
from typing import Union



class GameObject:
    """An entity base class for all moving or interactive objects

    pos -> Initial position in pixels, tuple in form of (x,y)
    size -> Hitbox size in pixels, tuple in form of (x,y)
    level -> The level this GameObject lives in
    """

    __name__ = "Unnamed Game Object"
    _gameobject_id = 0

    def __init__(self: Self,
                 pos: tuple[int, int],
                 size: tuple[int, int],
                 input_handler: Union[InHandler, Literal[None]],
                 level: Level, access_flags: ACCESS_FLAGS):

        self.size = size
        self.level = level
        self.pos = pos
        self.access_flags = access_flags
        self.input_handler = input_handler
        self.queued_movement: Union[tuple[int, int], Literal[None]] = None
        self.can_move = True
        self.blocking = True

        # Attach to timed move if we have a input_handler
        if self.input_handler is not None:
            self.input_handler.attach("Timed_Move", self.timed_move_execute)
            self.input_handler.attach(
                "Popup_Start", lambda: self.setCanMove(False))
            self.input_handler.attach(
                "Popup_Finish", lambda x:  self.setCanMove(True))

        # Give the object an id
        self.id = GameObject._gameobject_id
        GameObject._gameobject_id += 1

        # Register inside of the level
        level.register_GameObject(self)

    def setCanMove(self, status: bool):
        self.can_move = status

    def timed_move(self, mv: tuple):
        """ Defers the movement to the Timed_Move event instead of moving instantly 
        """
        self.queued_movement = mv

    def timed_move_execute(self):
        """ Event handle for timed_move
        """
        if self.queued_movement is not None:
            self.move(self.queued_movement)
            self.queued_movement = None

    def move(self, mv: tuple[int, int]):
        """Moves the GameObject by the vector2 given

        mv -> The amount of movement to be done, a tuple vector in form of (x,y)
        """
        if not self.can_move:
            return

        move_x, move_y = mv
        # Test for collisions and get the correct tile
        new_tile = self.collide(move_x, move_y)

        if new_tile is not True:
            # Finalize the move
            self.pos = new_tile.position

    def _display(self: Self, screen: Surface, units: tuple):
        """A base class side of the display method, calls display() at the end.

        screen -> pygame surface object
        units -> units which symbolise 1 tile of the level

        DO NOT OVERRIDE
        """
        screen_pos = self.level.get_screen_position(
            units, self.pos[0], self.pos[1])
        screen_size = (units[0] * self.size[0], units[1] * self.size[1])

        self.display(screen, screen_pos, screen_size)

    # display

    def display(self: Self, screen: Surface, screen_pos: tuple, screen_size: tuple):
        """A method that handles drawing of the object

        screen -> pygame screen object
        screen_pos -> position of the object on the screen
        screen_size -> size of the object on the screen

        The correct usage of GameObject involves overriding this method
        If that is not done, the following will act as a placeholder
        """

        rect = Rect(screen_pos[0],
                    screen_pos[1],
                    screen_size[0],
                    screen_size[1])

        draw.ellipse(screen, (100, 0, 255), rect)

    def _update(self: Self, dt: float):
        """The base class side pf the update method

        dt -> time since last frame in seconds

        DO NOT OVERRIDE
        """
        self.update(dt)

    def update(self: Self, dt: float):
        """A method that handles logic of the object

        dt -> time since last frame in seconds

        The correct usage of GameObject involves overriding this method
        If that is not done, the following will act as a placeholder
        """
        pass

    def collide(self: Self, x: int, y: int):
        """Inherent collision logic for game objects

        new_pos -> relative position of the collision
        """
        tile = self.get_level_tile()
        next_tile = tile.try_move(x, y, self.access_flags)

        if next_tile is None:
            return True

        abs_x, abs_y = next_tile.position
        others = self.level.get_GameObjects(abs_x, abs_y)

        blocked = False
        for other in others:
            self.on_collide(other)
            other.on_collide(self)
            blocked = blocked or other.blocking

        if blocked:
            return True

        return next_tile

    def on_collide(self: Self, other: Self):
        """A method that handles custom logic around collisons

        other -> The GameObject that collided with you.

        The correct usage of GameObject involves overriding this method
        If that is not done, the following will act as a placeholder
        """
        pass

    def get_level_tile(self) -> LevelTile:
        """returns the tile the GameObject is on
        """
        return self.level.get_tile(self.pos[0], self.pos[1])

#
#   Trigger
#
#


class Trigger(GameObject):
    """A template for a simple boundary trigger that is based on the GameObject class

    Showcases the usage of the game object

    pos, size -> See GameObject
    on_trigger-> EventMethod that will be invoked when
                 another GameObject gets into this Trigger's hitbox
    """
    __name__ = "Trigger"

    def __init__(self: Self, pos: tuple[int, int], size: tuple[int, int], on_trigger: EventMethod, level: Level):
        super().__init__(pos, size, level, ACCESS_FLAGS.ALL)
        self.on_trigger = on_trigger

    def on_collide(self: Self, other: GameObject):
        """Override of GameObject.on_collide"""
        self.on_trigger.invoke(self, other)
