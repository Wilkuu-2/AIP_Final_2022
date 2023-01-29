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
                "Popup_Start": "Popup_Start",
                "TF-020": "Timed_Move",
                "TF-001": "FRAME",
                "TF-015": "BUZZ_TIME"} # typing: none

# TODO: Write the controller class/driver
controller_keybinds = {"": "Test",
                       "HW_UP": "UP",
                       "HW_LEFT": "LEFT",
                       "HW_DOWN": "DOWN",
                       "HW_RIGHT": "RIGHT",
                       "1001_KeyPress": "CLICK",
                       "1002_KeyPress": "NONE"}


# Key bindings for the keyboard using QT bindings
# type: ignore
keyboard_keybinds = {f"{Qt.Key_Q}_KeyHold": "Test", # type: ignore 
                     f"{Qt.Key_W}_KeyHold": "UP", # type: ignore 
                     f"{Qt.Key_A}_KeyHold": "LEFT", # type: ignore 
                     f"{Qt.Key_S}_KeyHold": "DOWN", # type: ignore 
                     f"{Qt.Key_D}_KeyHold": "RIGHT", # type: ignore 
                     } 

# Combined keybinds
game_keybinds = controller_keybinds | keyboard_keybinds | other_events
