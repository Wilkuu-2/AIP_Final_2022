
# AI&P Final project [Create M6 2022-2023]
# game/game_main.py
#
# Copyright 2023 Jakub Stachurski
# Copyright 2023 Natalia Bueno Donadeu
#

# Imports
import pygame
from input_helpers import controls
from input_helpers import InHandler
from game.player import Player
from level import Level, LevelTile
from .greedy_enemy import GreedyEnemy
from .random_enemy import RandomEnemy
from .astar_enemy import AstarEnemy
from .pellet import Pellet


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
            controls.game_keybinds)

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
        self.level = Level()
        self._input.attach("Timed_Move", self.level.clear_tile_storage)
        # Create Player and other entities
        self.populate_level()

    def populate_level(self):
        player = Player((0,0), self._input, self.level)
        for row in self.level.tiles:
            for tile in row:
                tiletype = tile.get_data(hash("MAIN"),"type")
                pos = tile.position
                match tiletype:
                    case 'P':
                        player.pos = pos
                    case '1':
                        GreedyEnemy(pos, self._input, self.level, player)
                    case '2':
                        AstarEnemy(pos, self._input, self.level, player)
                    case '3':
                        RandomEnemy(pos, self._input, self.level, player)
                    case '.':
                        Pellet(pos, self._input, self.level)




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

        # Update all the GameObjects
        self.level.update_GameObjects(dt)

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

        ih.attach("Popup_Finish", self.popup_event)

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

    def popup_event(self, is_correct: bool):
        print("Correct!" if is_correct else "Not Correct :-< !")
