
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
    def __init__(self, pos: tuple, size: tuple, level):
        self.pos = Vector2(pos)
        self.size = Vector2(size)
        self.level = level

        # Give the object an id
        self.id = GameObject._gameobject_id
        GameObject._gameobject_id += 1

    # Move
    #   This method moves the GameObject by the vector2 given
    #
    #   mv -> The amount of movement to be done ,a tuple vector in form of (x,y)
    #
    def move(self, mv: tuple):
        move = (self.pos.x + mv[0], self.pos.y + mv[1])
        # Test for collisions
        col_result = self.collide(move, self.level)
        if col_result is None:
            # Finalize the move
            self.pos.x = move[0]
            self.pos.y = move[1]
        else:
            # Try moving closer
            v_move = Vector2(mv)
            mag = v_move.magnitude() - 1

            # When the magnitude is 0, dont bother moving
            if mag <= 0:
                return

            v_move.normalize_ip()
            v_move = v_move * mag

            self.move((v_move.x, v_move.y), self.level)

    # display
    #   A method that handles drawing of the object
    #
    #   The correct usage of GameObject involves overriding this method
    #   If that is not done, the following will act as a placeholder

    def display(self, surface):
        rect = Rect(self.pos.x - self.size.x / 2,
                    self.pos.y - self.size.y / 2,
                    self.size.x,
                    self.size.y)
        draw.ellipse(surface, (255, 50, 50), rect)

    # update
    #   A method that handles logic of the object
    #
    #   dt -> time since last frame in seconds
    #
    #   The correct usage of GameObject involves overriding this method
    #   If that is not done, the following will act as a placeholder
    def update(self, dt):
        pass

    # after_update
    #   A method that handles custom logic of the object
    #
    #   dt -> time since last frame in seconds
    #
    #   The correct usage of GameObject involves overriding this method
    #   If that is not done, the following will act as a placeholder
    def after_update(self, dt):
        self.collided = False

    # collide
    #   Inherent collision logic for game objects
    #
    #   new_pos -> tuple in form of (x.y)
    #   level   -> the level the collision occurs on
    #
    def collide(self, new_pos: tuple, level):
        pass

    # on_collide
    #   A method that handles custom logic around collisons
    #
    #   other -> The GameObject that collided with you.
    #
    #   The correct usage of GameObject involves overriding this method
    #   If that is not done, the following will act as a placeholder

    def on_collide(self, other):
        pass

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
