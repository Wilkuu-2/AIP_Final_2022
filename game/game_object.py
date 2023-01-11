from pygame import Vector2, draw, Rect
from input_helpers.input_handler import EventMethod


class GameObject:
    __name__ = "Unnamed Game Object"

    def __init__(self, pos: tuple, size: tuple, level):
        self.pos = Vector2(pos)
        self.size = Vector2(size)
        self.collided = False
        self.level = level

    def move(self, mv: tuple):
        move = (self.pos.x + mv[0], self.pos.y + mv[1])
        col_result = self.collide(move, self.level)
        if col_result is None:
            self.pos.x = move[0]
            self.pos.y = move[1]
        else:
            v_move = Vector2(mv)
            mag = v_move.magnitude() - 1
            v_move.normalize_ip()
            v_move = v_move * mag
            self.move((v_move.x, v_move.y), self.level)

    def display(self, surface):
        rect = Rect(self.pos.x - self.size.x / 2,
                    self.pos.y - self.size.y / 2,
                    self.size.x,
                    self.size.y)
        draw.ellipse(surface, (255, 50, 50), rect)

    def update(self, dt):
        pass

    def after_update(self, dt):
        self.collided = False

    def collide(self, new_pos: tuple, level):
        pass  # TODO: Implement collision logic
        self.collided = True

    def on_collide(self, other):
        pass


class Trigger(GameObject):
    __name__ = "Trigger"

    def __init__(self, pos: tuple, size: tuple, on_trigger: EventMethod):
        super().__init__(pos, size)
        self.on_trigger = on_trigger

    def trigger(self, other):
        self.on_trigger.invoke(other)
