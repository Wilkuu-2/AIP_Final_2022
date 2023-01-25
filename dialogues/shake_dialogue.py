# AI&P Final project [Create M6 2022-2023]
# dialogues/shake_dialogue.py
#
# Copyright 2023 Jakub Stachurski
# Copyright 2023 Natalia Bueno Donadeu
#
# Imports
from PyQt5.QtWidgets import QProgressDialog
from PyQt5.QtCore import QObject, Qt
from random import random


class ShakeDialogue(QObject):
    def __init__(self, input_handler):
        super().__init__(None)
        self.progress = QProgressDialog(
            "The ghost is on you! Shake the controller to get rid of it", "Die", 0, 1000)
        self.progress.setWindowModality(Qt.WindowModality.WindowModal)
        self.progress.setAutoReset(False)
        self.state = 100.0

        self.input_handler = input_handler
        self.ran = False

    def run(self):
        if self.ran is True:
            return
        self.ran = True

        self.input_handler.handle_event("Popup_Start")
        self.input_handler.handle_event("ReleaseHeld")

        self.evs = []
        self.evs.append(self.input_handler.attach("CLICK", self.handle_cancel))
        self.evs.append(self.input_handler.attach(
            "FRAME", self.handle_increment))
        self.progress.canceled.connect(self.handle_cancel)

        self.progress.show()

    def handle_increment(self):
        shake = self.input_handler.get_shake()
        self.state += shake * 30.0
        self.state -= (random() + 0.3) * 12
        print(self.state)
        self.progress.setValue(int(self.state))
        if self.state >= 1000:
            self.end(True)

    def handle_cancel(self):
        self.end(False)

    def end(self, ok):
        for ev in self.evs:
            self.input_handler.detach(*ev)

        self.input_handler.handle_event("ReleaseHeld")
        self.input_handler.handle_event("Popup_Finish", ok)
        self.progress.hide()
