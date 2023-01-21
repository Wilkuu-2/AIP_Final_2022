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


# Riddle Dialogue
#   The a wrappper around the QT QMessageBox that can give a player a riddle
#   The correctness of the multiple choice answer given by the player
#   is reported in a event
#
class RiddleDialogue():
    # Constructor
    #
    #  main_text -> The riddle
    #  answers    -> Possible answers for the riddle
    #  corr_answer -> The index of the correct answer in the answers
    #  input_handler -> The input handler to send events to
    #
    def __init__(self, main_text: str, answers: list, corr_answer: int, input_handler: InHandler, bottom_text=None):

        assert len(answers) > 0

        # Initalize the QMessageBox
        self.message_box = QMessageBox()
        self.message_box.setText(main_text)

        # Optional text under the riddle
        if bottom_text is not None:
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

    # run
    #   Run opens the dialogue, since the constructor only opens it
    #
    def run(self):
        print("OPENING RIDDLE")
        self.message_box.exec()

    # handle_click
    #    A QT signal which handles the click of a answer
    #
    def handle_click(self, button):
        self.input_handler.handle_event("ReleaseHeld")
        self.input_handler.handle_event(
            "Popup_Finish", button == self.corr_ans_button)

    # TODO: Handle the user just killing the popup
