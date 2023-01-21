from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QMainWindow
from PyQt5.QtGui import QPainter, QImage
from PyQt5.QtCore import QTimer

from sys import argv
from game.game_main import Game

from input_helpers.input_handler import InHandler


# UI
# The main UI Window 
# 
class UI(QMainWindow):
    # Constructor
    #
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

    # keyPressEvent
    #  QT Signal that gets passed to the game widget 
    #
    def keyPressEvent(self, event):
        self.pygame.keyPressEvent(event)
        super().keyPressEvent(event)
    
    # keyReleaseEvent
    #  QT Signal that gets passed to the game widget 
    #
    def keyReleaseEvent(self, event):
        self.pygame.keyReleaseEvent(event)
        super().keyReleaseEvent(event)


# PyGameWidget 
# The widget where Pygame gets drawn on
#
#
class PyGameWidget(QWidget):
    # Constructor
    #
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

    # paintEvent
    #   A QT Event which paints a new frame of the game 
    #
    #
    def paintEvent(self, e):
        
        # When a new frame is ready, convert it to a QImage
        if self.game.frame_consume():
            surface = self.game.get_surface()
            w = surface.get_width()
            h = surface.get_height()
            data = surface.get_buffer().raw
            self.image = QImage(data, w, h, QImage.Format_RGB32)
        
        # When the image exists draw it
        if self.image is not None:
            qp = QPainter(self)
            qp.drawImage(0, 0, self.image)
        
        # Pass the event 
        super().paintEvent(e)
    
    # keyPressEvent
    #   A QT Event which denotes a keyboard Key being pressed
    #
    def keyPressEvent(self, event):
        if not event.isAutoRepeat():
            self._input.handle_key(event.key(), "_KeyPress")
        super().keyPressEvent(event)

    # keyPressEvent
    #   A QT Event which denotes a keyboard Key being released
    #
    def keyReleaseEvent(self, event):
        if not event.isAutoRepeat():
            self._input.handle_key(event.key(), "_KeyRelease")
        super().keyReleaseEvent(event)

    # keyPressEvent
    #   A QT Event which denotes the widget being resized
    #
    def resizeEvent(self, event):
        size = self.frameGeometry().width(), self.frameGeometry().height()
        self.game.resizeEvent(size)

# main 
# The entry point of the UI application
#
def main():
    app = QApplication(argv)

    ui = UI()
    ui.show()

    app.exec()


if __name__ == "__main__":
    main()
