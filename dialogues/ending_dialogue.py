# AI&P Final project [Create M6 2022-2023]
# dialogues/ending_dialoge.py
#
# Copyright 2023 Jakub Stachurski
# Copyright 2023 Natalia Bueno Donadeu
#
# Imports
from PyQt5.QtWidgets import QMessageBox, QPushButton
from input_helpers import InHandler
from .base_dialogue import BaseDialogue 

class EndingDialogue(BaseDialogue):
    TOP_TEXT = "This is the end!"
    WON_TEXT = "You Won!\nCongratulations!" 
    LOST_TEXT = "You Lost!\nLMAO\nSkill Issue" 
    BUTTON_TEXT = "Exit"

    def __init__(self, input_handler: InHandler, won: bool):
        super().__init__(input_handler)

        self.widget = QMessageBox()
        self.widget.setText(self.TOP_TEXT)

        bot_text = self.WON_TEXT if won else self.LOST_TEXT
        self.widget.setInformativeText(bot_text)

        self.widget.buttonClicked.connect(self.handle_click)

        button = QPushButton(self.BUTTON_TEXT)
        self.widget.addButton(button, QMessageBox.AcceptRole)

    def evaluate(self, button: QPushButton):
        exit()
    

        



