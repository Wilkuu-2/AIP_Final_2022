from PyQt5.QtCore import Qt


def getAxis():
    return 0, 0


# Key bindings for the physical controller using a custom class
# TODO: Write the controller class
controller_keybinds = {"": "Test"}

# Key bindings for the keyboard using QT bindings
keyboard_keybinds = {f"{Qt.Key_Q}_KeyPress": "Test",
                     f"{Qt.Key_W}_KeyPress": "UP",
                     f"{Qt.Key_A}_KeyPress": "LEFT",
                     f"{Qt.Key_S}_KeyPress": "DOWN",
                     f"{Qt.Key_D}_KeyPress": "RIGHT",
                     }

# Combined keybinds
game_keybinds = controller_keybinds | keyboard_keybinds
