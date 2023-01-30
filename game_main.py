
# AI&P Final project [Create M6 2022-2023]
# game_main.py
#
# Copyright 2023 Jakub Stachurski
# Copyright 2023 Natalia Bueno Donadeu
#

# Imports
import pygame
from input_helpers import InHandler, controls
from level import Level 
from game import GameObject, Player, BaseEnemy, GreedyEnemy, RandomEnemy, AstarEnemy, Pellet
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QTimer 
from PyQt5.QtGui import QImage, QPainter


class GameWidget(QWidget):
    """
        The main class for the pygame part of this project

        size -> initial widget size
        inhandler -> the input handler
    """

    def __init__(self, parent=None):
        """
         Constructor
        """
        super().__init__(parent)
        self.image = None
        self.time = pygame.time.get_ticks()

        #self.size = self.frameGeometry().width(), self.frameGeometry().height()

        # Save the InHandler and load controls
        self.input_handler = InHandler()
        self.input_handler.set_control_scheme(
            controls.game_keybinds)

        pygame.init()
        # Create a hidden canvas for pygame
        self.screen_flags = 0 | pygame.HIDDEN
        screen_sz = self.width() , self.height()
        self.surface = pygame.display.set_mode(screen_sz, self.screen_flags)
        self.frameReady = False

        # Start timing
        self.time = pygame.time.get_ticks()

        # Create Level
        self.level = Level()
        self.input_handler.attach("Timed_Move", self.level.clear_tile_storage)
        # Create Player and other entities
        self.populate_level()

        # Game loop is enbedded into the PyQt5 event loop
        self.gameTimer = QTimer()
        self.gameTimer.timeout.connect(self.loop)
        self.gameTimer.start(16)  # 16 ms = 60 fps

        # The timer to repaint this widget
        self.frameTimer = QTimer()
        self.frameTimer.timeout.connect(self.update)
        self.frameTimer.start(16)  # 16 ms = 60 fps

    def populate_level(self):
        player = Player(self.level.get_tile(0,0), self.input_handler)

        # Register inside of the level
        player.beep_start([600,500,700,100,200,300,400,500])
        for row in self.level.tiles:
            for tile in row:
                tiletype = tile.get_data(hash("MAIN"),"type")
                match tiletype:
                    case 'P':
                        player.tile = tile
                    case '1':
                        GreedyEnemy(tile, self.input_handler, player)
                    case '2':
                        AstarEnemy(tile, self.input_handler, player)
                    case '3':
                        RandomEnemy(tile, self.input_handler, player)
                    case '.':
                        Pellet(tile, self.input_handler)

    def display(self):
        """
        This is where the game gets drawn

        dt -> time since last frame in seconds
        """
        r = (self.time/10.0 + 50) % 255
        g = (self.time/10.0 + 70) % 255
        b = (-self.time/10.0 + 120) % 255
        self.surface.fill((round(r), round(g), round(b)))

        size = self.surface.get_size()

        self.level.DEBUG_DrawLevel(self.surface, *size)
        self.level.display_GameObjects(self.surface, size)

    def loop(self):
        """
        The event loop that is called by QT
        """
        # Measure time
        current_time = pygame.time.get_ticks()
        dt = current_time - self.time
        self.time = current_time

        # Update all the GameObjects
        GameObject.update_GameObjects(dt)

        # Call the key events
        self.input_handler.heldKeyUpdate()


    def get_surface(self) -> pygame.surface.Surface:
        """
            Returns pygame screen object

            Used by QT for displaying the game
        """
        return self.surface

    # -- Game_Events

    def resizeEvent(self, event):
        """
        A QT Event which denotes the widget being resized
        """
        size = (self.width(), int(self.width() / 750.0 * 800.0))
        if size[1] > self.height():
            size = (int(self.height() / 800 * 750) ,self.height())
        self.surface = pygame.display.set_mode(size, self.screen_flags)

    def paintEvent(self, e):
        """A QT Event which paints a new frame of the game"""
        
        # Draw on the screen
        self.display()

        # Flip the pygame display
        pygame.display.flip()

        # When a new frame is ready, convert it to a QImage
        w = self.surface.get_width()
        h = self.surface.get_height()
        data = self.surface.get_buffer().raw # type: ignore
        self.image = QImage(data, w, h, QImage.Format_RGB32)

        # When the image exists draw it
        if self.image is not None:
            qp = QPainter(self)
            qp.drawImage(0, 0, self.image)

        # Pass the event
        super().paintEvent(e)

    def keyPressEvent(self, event):
        """A QT Event which denotes a keyboard Key being pressed"""
        if not event.isAutoRepeat():
            self.input_handler.handle_key(event.key(), "_KeyPress")
        super().keyPressEvent(event)

    def keyReleaseEvent(self, event):
        """A QT Event which denotes a keyboard Key being released"""
        if not event.isAutoRepeat():
            self.input_handler.handle_key(event.key(), "_KeyRelease")
        super().keyReleaseEvent(event)


    def popup_event(self, is_correct: bool):
        print("Correct!" if is_correct else "Not Correct :-< !")
