# AI&P Final project [Create M6 2022-2023]
# ui_main.py
#
# Copyright 2022-2023 Jakub Stachurski
# Copyright 2022-2023 Natalia Bueno Donadeu
#
# Imports
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QMainWindow

from sys import argv
from game_main import GameWidget

class UI(QMainWindow):
    """The main UI Window"""
    def __init__(self):
        super().__init__()

        # Create the game widget
        self.pygame = GameWidget()

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


def main():
    """The entry point of the UI application"""
    app = QApplication(argv)

    ui = UI()
    ui.show()

    app.exec()


if __name__ == "__main__":
    main()

