# AI&P Final project [Create M6 2022-2023]
# UI/riddle_dialogue.py
#
# Copyright 2023 Jakub Stachurski
# Copyright 2023 Natalia Bueno Donadeu
#

# Imports
from random import shuffle
from PyQt5.QtWidgets import QMessageBox, QPushButton
from input_helpers.input_handler import InHandler
from input_helpers.event_method import EventMethod

from time import time


class RiddleDialogue():
    """This is a wrappper around the QT QMessageBox that can give a player a riddle
    The correctness of the multiple choice answer given by the player
    is reported in a event
    Constructor

    main_text -> The riddle
    answers    -> Possible answers for the riddle
    corr_answer -> The index of the correct answer in the answers
    input_handler -> The input handler to send events to
    bottom_text   -> Additional text under the riddle
    """

    def __init__(self, main_text: str, answers: list[str], corr_answer: int, input_handler: InHandler, bottom_text: str = ""):
        self.input_handler = input_handler
        self.last_focus = time()
        self.focus_cooldown = 0.5
        self.ran = False

        assert len(answers) > 0

        # Initalize the QMessageBox
        self.message_box = QMessageBox()
        self.message_box.setText(main_text)

        # Optional text under the riddle
        self.message_box.setInformativeText(bottom_text)

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
            self.message_box.addButton(button, QMessageBox.AcceptRole)

        # Attach the event of clicking
        self.message_box.buttonClicked.connect(self.handle_click)

    def run(self):
        """Opens the dialogue"""
        if self.ran is True:
            return

        self.ran = True

        self.input_handler.handle_event("Popup_Start")
        self.evs = []

        self.evs.append(self.input_handler.attach(
            "LEFT", self.handle_focus, False))
        self.evs.append(self.input_handler.attach(
            "RIGHT", self.handle_focus, True))
        self.evs.append(self.input_handler.attach("CLICK", self.handle_select))

        self.message_box.show()

    def handle_click(self, button: QPushButton):
        """ A QT signal which handles the click of a answer"""

        self.input_handler.handle_event("ReleaseHeld")

        self.input_handler.handle_event(
            "Popup_Finish", button == self.corr_ans_button)

        for ev in self.evs:
            self.input_handler.detach(*ev)

    def handle_focus(self, forward: bool):
        if self.last_focus + self.focus_cooldown < time():
            self.message_box.focusNextPrevChild(forward)
            self.last_focus = time()

    def handle_select(self):
        self.handle_click(self.message_box.focusWidget())
        self.message_box.windowHandle().hide()

    # TODO: Handle the user just killing the popup
