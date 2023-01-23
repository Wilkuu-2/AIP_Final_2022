# AI&P Final project [Create M6 2022-2023]
# input_helpers/controls.py
#
# Copyright 2022-2023 Jakub Stachurski
# Copyright 2022-2023 Natalia Bueno Donadeu
#

# Imports
from PyQt5.QtCore import Qt

# A fake getAxis method
def getAxis():
    return 0, 0


# Key bindings for the physical controller using a custom class

# Events that have no regular key input
other_events = {"Popup_Finish": "Popup_Finish",
                "TF-015": "Timed_Move"}

# TODO: Write the controller class/driver
controller_keybinds = {"": "Test"}

# Key bindings for the keyboard using QT bindings
keyboard_keybinds = {f"{Qt.Key_Q}_KeyHold": "Test",
                     f"{Qt.Key_W}_KeyHold": "UP",
                     f"{Qt.Key_A}_KeyHold": "LEFT",
                     f"{Qt.Key_S}_KeyHold": "DOWN",
                     f"{Qt.Key_D}_KeyHold": "RIGHT",
                     }

# Combined keybinds
game_keybinds = controller_keybinds | keyboard_keybinds | other_events
