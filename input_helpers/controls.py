from PyQt5.QtCore import Qt


def getAxis():
    return 0, 0


# Key bindings for the physical controller using a custom class
# TODO: Write the controller class
other_events = {"Popup_Finish": "Popup_Finish"}

controller_keybinds = {"": "Test"}

# Key bindings for the keyboard using QT bindings
keyboard_keybinds = {f"{Qt.Key_Q}_KeyPress": "Test",
                     f"{Qt.Key_W}_KeyHold": "UP",
                     f"{Qt.Key_A}_KeyHold": "LEFT",
                     f"{Qt.Key_S}_KeyHold": "DOWN",
                     f"{Qt.Key_D}_KeyHold": "RIGHT",
                     }

# Combined keybinds
game_keybinds = controller_keybinds | keyboard_keybinds | other_events
