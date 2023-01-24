
# AI&P Final project [Create M6 2022-2023]
# game/game_main.py
#
# Copyright 2023 Jakub Stachurski
# Copyright 2023 Natalia Bueno Donadeu
#

# Imports
import pygame
from input_helpers import controls
from input_helpers.input_handler import InHandler
from input_helpers.event_method import EventMethod
from game.player import Player
from UI.riddle_dialogue import RiddleDialogue
from game.level.level import Level
from game.PacmanProject.board import boards, linked
from .greedy_enemy import GreedyEnemy
from .random_enemy import RandomEnemy
from .astar_enemy import AstarEnemy


class Game:
    """
        The main class for the pygame part of this project

        size -> initial widget size
        inhandler -> the input handler
    """

    def __init__(self, size: tuple, inhandler: InHandler):
        """
         Constructor
        """
        # Save the InHandler and load controls
        self._input = inhandler
        self._input.set_control_scheme(
            controls.game_keybinds, controls.getAxis)

        pygame.init()

        # Create a hidden canvas for pygame
        self.screen_flags = 0 | pygame.HIDDEN
        self.size = size
        self.screen = pygame.display.set_mode(self.size, self.screen_flags)
        self.frameReady = False

        self.attach_game_events()

        # Start timing
        self.time = pygame.time.get_ticks()

        # Create Level
        size = (len(boards[0]), len(boards))
        self.level = Level(size, boards, linked)

        self._input.attach("Timed_Move", self.level.clear_tile_storage)

        # Create Player
        player = Player((2, 2), self._input, self.level)
        enemy1 = GreedyEnemy((16, 16), self._input, self.level, player)
        enemy2 = RandomEnemy((17, 16), self._input, self.level, player)
        enemy3 = AstarEnemy((15, 16), self._input, self.level, player)

    def update(self, dt: float):
        """
        This is where the game logic lives

        dt -> time since last frame in seconds

        """
        pass
        # TODO: Add enemies
        # TODO: Add level

    def display(self, dt: float):
        """
        This is where the game gets drawn

        dt -> time since last frame in seconds
        """
        r = (self.time/10.0 + 50) % 255
        g = (self.time/10.0 + 70) % 255
        b = (-self.time/10.0 + 120) % 255
        self.screen.fill((round(r), round(g), round(b)))

        self.level.DEBUG_DrawLevel(self.screen, self.size[0], self.size[1])
        self.level.display_GameObjects(self.screen, self.size)

        self.frameReady = True

    def frame_consume(self) -> bool:
        """
        Lets QT know if a frame is ready to refresh
        """
        self.display
        if self.frameReady:
            self.frameReady = False
            return True
        return False

    # loop
    #
    def loop(self):
        """
        The event loop that is called by QT
        """
        # Measure time
        current_time = pygame.time.get_ticks()
        dt = current_time - self.time
        self.time = current_time

        # Axis event
        self.axisEvent(self._input.getAxis())

        # Update all the GameObjects
        self.level.update_GameObjects(dt)

        # Update the game state
        self.update(dt)

        # Call the key events
        self._input.heldKeyUpdate()

        # Draw on the screen
        self.display(dt)

        # Flip the pygame display
        pygame.display.flip()

    # get_surface
    #
    def get_surface(self) -> pygame.surface.Surface:
        """
            Returns pygame screen object

            Used by QT for displaying the game
        """
        return self.screen

    # attach_game_event
    def attach_game_events(self):
        """
           Attaches all sorts of events to methods inside of this instance of the Game class 

           A helper method for the constructor
        """

        ih = self._input

        # ! Template !
        # ih.attach("Input name",self.eventMethod)

        ih.attach("Test", self.test_popup)
        ih.attach("Popup_Finish", self.popup_event)
        ih.hardware_event.startShakeEvent(
            EventMethod(lambda: print("SHAKE")), 10)

    # -- Game_Events

    # resizeEvent
    #

    def resizeEvent(self, size: tuple):
        """
        Resizes the screen

        size -> size of the widget
        """
        self.size = (size[0], int(size[0] / 750.0 * 800.0))
        self.screen = pygame.display.set_mode(self.size, self.screen_flags)

    def axisEvent(self, axis: tuple):
        pass  # TODO: Handle axis(Arrow) input

    def test_popup(self):
        print("Popup")
        self._input.handle_event("ReleaseHeld")
        self.dialogue = RiddleDialogue("Riddle!", [
                                       "Right", "Wrong!", "Worng", "Wrongg"], 0, self._input, bottom_text="Bottom_Text")
        self.dialogue.run()

    def popup_event(self, is_correct: bool):
        print("Correct!" if is_correct else "Not Correct :-< !")
