# AI&P Final project [Create M6 2022-2023]
# dialogues/base_dialogue.py
#
# Copyright 2023 Jakub Stachurski
# Copyright 2023 Natalia Bueno Donadeu
#

# Imports
from PyQt5.QtWidgets import QWidget, QPushButton
from input_helpers import InHandler, EventMethod
from PyQt5.QtCore import QObject 
from time import time
from random import choice

class BaseDialogue(QObject):
    """ BaseClass for popups and Dialogues,
    it handles controller input as well as mouse and keyboard"""
    FOCUS_COOLDOWN: float = 0.5
    RANDOM_DIALOGUES: list[type] = []

    @staticmethod 
    def getRandomDialogue(input_handler: InHandler) -> 'BaseDialogue':
        """Factory that creates a random subclass from 
        the RANDOM_DIALOGUES static variable """
        diag = choice(BaseDialogue.RANDOM_DIALOGUES)
        return diag(input_handler)

    def __init__(self, input_handler: InHandler) -> None:
        super().__init__(None)
        self.input_handler = input_handler
        self.last_focus = time()
        self.ran = False
        self.widget: QWidget
        self.evs: list[tuple[str, EventMethod]] = []

    def run(self):
        """Opens the dialogue"""
        if self.ran is True:
            return

        self.ran = True

        self.input_handler.handle_event("Popup_Start")
        self.input_handler.handle_event("ReleaseHeld")

        self.evs.append(self.input_handler.attach(
            "LEFT", self.handle_focus, False))
        self.evs.append(self.input_handler.attach(
            "RIGHT", self.handle_focus, True))
        self.evs.append(self.input_handler.attach("CLICK", self.handle_select))

        self.widget.show()
    
    def handle_click(self, button: QPushButton | None):
        """ A QT signal which handles the click of a answer"""

        self.input_handler.handle_event("ReleaseHeld")

        for ev in self.evs:
            self.input_handler.detach(*ev)

        self.input_handler.handle_event(
            "Popup_Finish", self.evaluate(button))

    def handle_focus(self, forward: bool):
        if self.last_focus + self.FOCUS_COOLDOWN < time():
            self.widget.focusNextPrevChild(forward)
            self.last_focus = time()

    def handle_select(self):
        self.handle_click(self.widget.focusWidget())
        self.widget.windowHandle().hide()

    def evaluate(self, button: QPushButton | None): # type: ignore 
        print("Warning, default evaluate method used.")
        return False    

    # TODO: Handle the user just killing the popup
