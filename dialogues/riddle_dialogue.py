# AI&P Final project [Create M6 2022-2023]
# dialogues/riddle_dialogue.py
#
# Copyright 2023 Jakub Stachurski
# Copyright 2023 Natalia Bueno Donadeu
#

# Imports
from random import shuffle, choice
from PyQt5.QtWidgets import QMessageBox, QPushButton
from input_helpers import InHandler
from .riddles import riddles
from .base_dialogue import BaseDialogue

from time import time


class RiddleDialogue(BaseDialogue):
    """This is a wrappper around the QT QMessageBox that can give a player a riddle
    The correctness of the multiple choice answer given by the player
    is reported in a event
    """

    def __init__(self, input_handler: InHandler):
        super().__init__(input_handler)
        riddle = choice(riddles)

        main_text = riddle[0]
        answers = riddle[1]
        corr_answer = riddle[2]

        assert len(answers) > 0

        # Initalize the QMessageBox
        self.widget = QMessageBox()
        self.widget.setText(main_text)

        # Optional text under the riddle
        #self.widget.setInformativeText(bottom_text)

        # Buttons held by the class
        self.buttons = []

        self.corr_ans_button = None
        for i in range(0, len(answers)):
            answer = answers[i]

            # Initalize the button and add it into buttons
            button = QPushButton(answer)
            self.buttons.append(button)

            # Save the button that holds the correct answer
            if i == corr_answer:
                self.corr_ans_button = button

        assert self.corr_ans_button is not None, "Correct answer not found"

        # Attach the buttons to the message box in a random order
        shuffle(self.buttons)
        for button in self.buttons:
            self.widget.addButton(button, QMessageBox.AcceptRole)

        # Attach the event of clicking
        self.widget.buttonClicked.connect(self.handle_click)

    def evaluate(self, button: QPushButton):
        return button == self.corr_ans_button
         

BaseDialogue.RANDOM_DIALOGUES.append(RiddleDialogue)
