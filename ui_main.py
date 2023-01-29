# AI&P Final project [Create M6 2022-2023]
# ui_main.py
#
# Copyright 2022-2023 Jakub Stachurski
# Copyright 2022-2023 Natalia Bueno Donadeu
#
# Imports
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QMainWindow
from PyQt5.QtGui import QPainter, QImage
from PyQt5.QtCore import QTimer

from sys import argv
from game.game_main import Game

from input_helpers.input_handler import InHandler


class UI(QMainWindow):
    """The main UI Window"""
    def __init__(self):
        super().__init__()

        # Create the game widget
        self.pygame = PyGameWidget()

        # Put the game widget into our window
        layout = QVBoxLayout()
        layout.addWidget(self.pygame, 10)

        self.setCentralWidget(QWidget())
        self.centralWidget().setLayout(layout)

        # Set a minimum size of the window
        self.setMinimumSize(1024, 1024)

    def keyPressEvent(self, event):
        """QT Signal that gets passed to the game widget"""
        self.pygame.keyPressEvent(event)
        super().keyPressEvent(event)

    def keyReleaseEvent(self, event):
        """QT Signal that gets passed to the game widget"""
        self.pygame.keyReleaseEvent(event)
        super().keyReleaseEvent(event)


class PyGameWidget(QWidget):
    """The widget where Pygame gets drawn on"""

    def __init__(self):
        super().__init__(None)

        # Initalize the game
        self._input = InHandler()
        size = self.frameGeometry().width(), self.frameGeometry().height()
        self.game = Game(size, self._input)

        # Game loop is enbedded into the PyQt5 event loop
        self.gameTimer = QTimer()
        self.gameTimer.timeout.connect(self.game.loop)
        self.gameTimer.start(16)  # 16 ms = 60 fps

        # The timer to repaint this widget
        self.frameTimer = QTimer()
        self.frameTimer.timeout.connect(self.update)
        self.frameTimer.start(16)  # 16 ms = 60 fps

        # A variable where the game frame is stored
        self.image = None

    def paintEvent(self, e):
        """A QT Event which paints a new frame of the game"""

        # When a new frame is ready, convert it to a QImage
        if self.game.frame_consume():
            surface = self.game.get_surface()
            w = surface.get_width()
            h = surface.get_height()
            data = surface.get_buffer().raw # type: ignore
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
            self._input.handle_key(event.key(), "_KeyPress")
        super().keyPressEvent(event)

    def keyReleaseEvent(self, event):
        """A QT Event which denotes a keyboard Key being released"""
        if not event.isAutoRepeat():
            self._input.handle_key(event.key(), "_KeyRelease")
        super().keyReleaseEvent(event)

    #   
    def resizeEvent(self, event):
        """A QT Event which denotes the widget being resized"""
        size = self.frameGeometry().width(), self.frameGeometry().height()
        self.game.resizeEvent(size)


def main():
    """The entry point of the UI application"""
    app = QApplication(argv)

    ui = UI()
    ui.show()

    app.exec()


if __name__ == "__main__":
    main()
