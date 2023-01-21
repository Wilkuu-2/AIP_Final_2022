
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
from game.player import Player
from UI.riddle_dialogue import RiddleDialogue
from game.level.level import Level
from game.PacmanProject.board import boards, linked


# Game
#  The main class for the pygame part of this project
#
class Game:
    # Constructor
    #
    #   size -> widget size
    #   inhandler -> the input handler
    #
    def __init__(self, size: list, inhandler: InHandler):
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

        # Create Player
        self.player = Player((10, 9), self._input, self.level)

        # Create the game_objects array
        # TODO: Move the GameObjects' storage into the level
        self.game_objects = [self.player]

    # update
    # This is where the game logic lives
    #
    #   dt -> time since last frame in seconds
    #
    def update(self, dt):
        pass
        # TODO: Add enemies
        # TODO: Add level

    # display
    # This is where the game gets drawn
    #
    #   dt -> time since last frame in seconds
    #
    def display(self, dt):
        r = (self.time/10.0 + 50) % 255
        g = (self.time/10.0 + 70) % 255
        b = (-self.time/10.0 + 120) % 255
        self.screen.fill((r, g, b))

        self.level.DEBUG_DrawLevel(self.screen, self.size[0], self.size[1])
        self.level.display_GameObjects(self.screen, self.size)

        self.frameReady = True



    # frame_consume
    #   Lets QT know if a frame is ready to refresh
    def frame_consume(self):
        if self.frameReady:
            self.frameReady = False
            return True
        return False

    # loop
    #   The event loop that is called by QT
    #
    def loop(self):
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
    #   returns the screen object to QT
    #
    def get_surface(self):
        return self.screen

    # attach_game_event
    #   Attaches all sorts of events to methods inside of the instance
    def attach_game_events(self):
        ih = self._input

        # ! Template !
        # ih.attach("Input name",self.eventMethod)

        ih.attach("Test", print, "Test1")
        ih.attach("Test", lambda: print("Test2"))
        ih.attach("Test", lambda: self.test_event(3))
        ih.attach("Test", self.test_event, 4)  # Events can have arguments
        ih.attach("Test", self.test_popup)
        ih.attach("Popup_Finish", self.popup_event)

    # -- Game_Events

    # resizeEvent
    #   Resizes the screen
    #
    #   size -> size of the widget
    #

    def resizeEvent(self, size: tuple):
        self.size = size[0], int(size[0] / 750.0 * 800.0)
        self.screen = pygame.display.set_mode(self.size, self.screen_flags)

    def axisEvent(self, axis: tuple):
        pass  # TODO: Handle axis(Arrow) input

    def test_event(self, num):
        print(f"Test{num}")

    def test_popup(self):
        print("Popup")
        self._input.handle_event("ReleaseHeld")
        self.dialogue = RiddleDialogue("Riddle!", [
                                       "Right", "Wrong!", "Worng", "Wrongg"], 0, self._input, bottom_text="Bottom_Text")
        self.dialogue.run()

    def popup_event(self, is_correct: bool):
        print("Correct!" if is_correct else "Not Correct :-< !")
