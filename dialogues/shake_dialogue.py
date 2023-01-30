# AI&P Final project [Create M6 2022-2023]
# dialogues/shake_dialogue.py
#
# Copyright 2023 Jakub Stachurski
# Copyright 2023 Natalia Bueno Donadeu
#
# Imports
from PyQt5.QtWidgets import QProgressDialog, QPushButton
from PyQt5.QtCore import Qt
from .base_dialogue import BaseDialogue
from random import random

class ShakeDialogue(BaseDialogue):
    STATE_MAX = 1000

    def __init__(self, input_handler):
        super().__init__(input_handler)

        self.widget = QProgressDialog(
            "The ghost is on you! Shake the controller to get rid of it", "Die", 0, 1000)
        self.widget.setWindowModality(Qt.WindowModality.WindowModal)
        self.widget.setAutoReset(False)
        self.state = 100.0

    def run(self):
        super().run()
        self.evs.append(self.input_handler.attach(
            "FRAME", self.handle_increment))
        self.widget.canceled.connect(self.handle_select)

    def handle_increment(self):
        shake = self.input_handler.get_shake()
        self.state += shake * 30.0
        self.state -= (random() + 0.3) * 12
        print(self.state)
        self.widget.setValue(int(self.state))
        if self.state >= self.STATE_MAX:
            self.handle_select()

    def evaluate(self, button: QPushButton | None ):
        return self.state >= self.STATE_MAX 

# Add the shake dialogue to random dialogues
BaseDialogue.RANDOM_DIALOGUES.append(ShakeDialogue)
