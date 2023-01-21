from random import shuffle
from PyQt5.QtWidgets import QMessageBox, QPushButton
from input_helpers.input_handler import InHandler


class RiddleDialogue():
    def __init__(self, main_text: str, answers: list, corr_answer: int, input_handler: InHandler, bottom_text=None):
        self.answers = answers
        self.main_text = main_text
        self.corr_ans_str = answers[corr_answer]
        self.corr_ans_button = None
        self.input_handler = input_handler
        self.bottom_text = bottom_text

        assert len(answers) > 0

        super().__init__()

    def run(self):
        self.message_box = QMessageBox()
        self.message_box.setText(self.main_text)

        if self.bottom_text is not None:
            self.message_box.setInformativeText(self.bottom_text)

        self.buttons = []
        for answer in self.answers:
            button = QPushButton(answer)
            if answer == self.corr_ans_str:
                self.corr_ans_button = button
            self.buttons.append(button)

        shuffle(self.buttons)

        for button in self.buttons:
            self.message_box.addButton(button, QMessageBox.AcceptRole)

        assert self.corr_ans_button is not None, "Correct answer not found"

        self.message_box.buttonClicked.connect(self.handle_click)
        print("OPENING RIDDLE")
        self.message_box.exec()

    async def exec(self):
        await self.message_box.exec()

    def handle_click(self, button):
        self.input_handler.handle_event("ReleaseHeld")
        self.input_handler.handle_event(
            "Popup_Finish", button == self.corr_ans_button)
