import pygame
import input_helpers.controls as controls
from game.player import Player


class Game:
    def __init__(self, size, inhandler):
        self._input = inhandler
        self._input.set_control_scheme(
            controls.game_keybinds, controls.getAxis)
        pygame.init()

        self.screen_flags = 0 | pygame.HIDDEN
        self.size = size
        self.screen = pygame.display.set_mode(self.size, self.screen_flags)
        self.frameReady = False

        self.attach_game_events()

        self.time = pygame.time.get_ticks()
        self.player = Player((200,200), self._input, 0)

        self.game_objects = [self.player]

    def update(self, dt):
        self._input.heldKeyUpdate()
        for game_object in self.game_objects:
            game_object.update(dt)
        # TODO: Add enemies
        # TODO: Add level
        for game_object in self.game_objects:
            game_object.after_update(dt)

    def display(self, dt):
        # TODO: Render display
        r = (self.time/10.0 + 50) % 255
        g = (self.time/10.0 + 70) % 255
        b = (-self.time/10.0 + 120) % 255
        self.screen.fill((r, g, b))
        
        for game_object in self.game_objects:
            game_object.display(self.screen)
        
        self.frameReady = True

    # Lets QT know if a frame is ready to refresh
    def frame_consume(self):
        if self.frameReady:
            self.frameReady = False
            return True
        return False

    # This is what is called by QT
    def loop(self):
        current_time = pygame.time.get_ticks()
        dt = current_time - self.time
        self.time = current_time

        self.axisEvent(self._input.getAxis())
        self.update(dt)
        self.display(dt)
        pygame.display.flip()

    def get_surface(self):
        return self.screen

    # Game_Events
    def resizeEvent(self, size: tuple):
        self.size = size[0], int(size[0] / 16.0 * 9.0)
        self.screen = pygame.display.set_mode(self.size, self.screen_flags)

    def axisEvent(self, axis: tuple):
        pass  # TODO: Handle axis(Arrow) input

    def attach_game_events(self):
        ih = self._input

        # TODO: Use the events

        # ! Template !
        # ih.attach("Input name",self.eventMethod)

        ih.attach("Test", print, "Test1")
        ih.attach("Test", lambda: print("Test2"))
        ih.attach("Test", lambda: self.test_event(3))
        ih.attach("Test", self.test_event, 4) # Events can have arguments 

    def test_event(self, num):
        print(f"Test{num}")
