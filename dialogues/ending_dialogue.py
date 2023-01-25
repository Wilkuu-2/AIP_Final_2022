from PyQt5.QtWidgets import QMessageBox, QPushButton
from input_helpers import InHandler



class EndingDialogue():
    TOP_TEXT = "This is the end!"
    WON_TEXT = "You Won!\nCongratulations!" 
    LOST_TEXT = "You Lost!\nLMAO\nSkill Issue" 
    BUTTON_TEXT = "Exit"

    def __init__(self, input_handler: InHandler, won: bool):
        self.input_handler = input_handler
        self.ran = False 

        self.message_box = QMessageBox()
        self.message_box.setText(self.TOP_TEXT)

        bot_text = self.WON_TEXT if won else self.LOST_TEXT
        self.message_box.setInformativeText(bot_text)

        self.message_box.buttonClicked.connect(self.handle_button)

        button = QPushButton(self.BUTTON_TEXT)
        self.message_box.addButton(button, QMessageBox.AcceptRole)

    def run(self):
        if self.ran == True:
            return 

        print("running ending")

        self.ran = True

        self.input_handler.handle_event("Popup_Start")
        self.input_handler.handle_event("ReleaseHeld")

        self.input_handler.attach("CLICK", self.handle_button, None)

        self.message_box.show()

    def handle_button(self,button):
        print("Exiting!")
        exit()

        



