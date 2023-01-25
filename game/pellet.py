from level import Level
from game import GameObject
from input_helpers import InHandler
from level import Level, ACCESS_FLAGS
from pygame.surface import Surface
from pygame import draw

class Pellet(GameObject):
    __name__ = "Pellet"
    PELLET_AMOUNT = 0
    PELLET_RADIUS = 0.1
    def __init__(self, 
                 pos: tuple[int, int],
                 input_handler: InHandler,
                 level: Level):
        super().__init__(pos, (1,1), input_handler, level, ACCESS_FLAGS.PELLET)
        Pellet.PELLET_AMOUNT += 1

    def display(self, screen: Surface, screen_pos: tuple, screen_size: tuple):
        rect = (screen_pos[0]+screen_size[0]*(0.5-self.PELLET_RADIUS),
                screen_pos[1]+screen_size[1]*(0.5-self.PELLET_RADIUS),
                screen_size[0] * 2 * self.PELLET_RADIUS,
                screen_size[0] * 2 * self.PELLET_RADIUS)

        draw.ellipse(screen,(255,255,255), rect)
    
    def on_collide(self, other: GameObject):
        if other.__name__ == "Player":
            self.level.deregister_GameObject(self)
            Pellet.PELLET_AMOUNT -= 1
            if Pellet.PELLET_AMOUNT == 0:
                other.handle_end(True) # type: ignore


        






