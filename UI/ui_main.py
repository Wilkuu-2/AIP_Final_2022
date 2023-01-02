from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QMainWindow
from PyQt5.QtGui import QPainter, QImage
from PyQt5.QtCore import QTimer

from sys import argv
from game.game_main import Game

from input_helpers.input_handler import InHandler


class UI(QMainWindow):
    def __init__(self):
        super().__init__()  # TODO: Initialize UI Here
        self.pygame = PyGameWidget()

        layout = QVBoxLayout()
        layout.addWidget(self.pygame, 10)

        self.setCentralWidget(QWidget())
        self.centralWidget().setLayout(layout)

        self.setMinimumSize(1024, 576)

    def keyPressEvent(self, event):
        self.pygame.keyPressEvent(event)
        super().keyPressEvent(event)

    def keyReleaseEvent(self, event):
        self.pygame.keyReleaseEvent(event)
        super().keyReleaseEvent(event)


class PyGameWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._input = InHandler()

        size = self.frameGeometry().width(), self.frameGeometry().height()
        self.game = Game(size, self._input)

        # Game loop is enbedded into the PyQt5 event loop
        self.gameTimer = QTimer()
        self.gameTimer.timeout.connect(self.game.loop)
        self.gameTimer.start(8)  # 8 ms = 120 fps

        self.frameTimer = QTimer()
        self.frameTimer.timeout.connect(self.update)
        self.frameTimer.start(16)  # 16 ms = 60 fps

        self.image = None

    def paintEvent(self, e):
        if self.game.frame_consume():
            surface = self.game.get_surface()
            w = surface.get_width()
            h = surface.get_height()
            data = surface.get_buffer().raw
            self.image = QImage(data, w, h, QImage.Format_RGB32)

        if self.image is not None:
            qp = QPainter(self)
            qp.drawImage(0, 0, self.image)
        super().paintEvent(e)

    def keyPressEvent(self, event):
        self._input.handle(event.key(), "_KeyPress")
        super().keyPressEvent(event)

    def keyReleaseEvent(self, event):
        self._input.handle(event.key(), "_KeyRelease")
        super().keyReleaseEvent(event)

    def resizeEvent(self, event):
        size = self.frameGeometry().width(), self.frameGeometry().height()
        self.game.resizeEvent(size)


def main():
    app = QApplication(argv)

    ui = UI()
    ui.show()

    app.exec()


if __name__ == "__main__":
    main()
