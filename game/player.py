# AI&P Final project [Create M6 2023]
# game/player.py
#
# Copyright 2023 Jakub Stachurski
# Copyright 2023 Natalia Bueno Donadeu
#

# Imports
from .game_object import GameObject
from input_helpers.input_handler import InHandler
from common import ACCESS_FLAGS
from dialogues import RiddleDialogue, ShakeDialogue, EndingDialogue
from random import random
from level import Level


class Player(GameObject):
    """ The player entity, this is where the player logic lives
    pos -> see GameObject
    level -> see GameObject
    input_handler -> InHandler that will handle the movement and other actions
    """
    __name__ = "Player"
    blocking = True

    def __init__(self, pos, input_handler: InHandler, level: Level):
        super().__init__(level.get_tile(*pos), (1, 1), input_handler, ACCESS_FLAGS.PLAYER)
        self.level = level

        self.handling_enemy = False

        input_handler.attach("UP",   self.timed_move, (0, -1))
        input_handler.attach("DOWN", self.timed_move, (0, 1))
        input_handler.attach("LEFT", self.timed_move, (-1, 0))
        input_handler.attach("RIGHT", self.timed_move, (1, 0))

    def handle_enemy(self, enemy):
        if self.handling_enemy:
            return

        self.beep_start([0,440,880,550])

        self.handling_enemy = True
        if  random() < 0.5:
            r = RiddleDialogue(self.input_handler)
            r.run()
        else:
            s = ShakeDialogue(self.input_handler)
            s.run()

        self.input_handler.attach(
            "Popup_Finish", self.handle_popup, enemy, oneshot=True)

    def handle_popup(self, ok, enemy):
        print(f"Popup finished: {ok}, {enemy}")
        self.beep_start([0,680,330])
        if ok:
            enemy.tile = self.level.get_tile(16,16)
            self.handling_enemy = False
        else:
            self.handle_end(False)

    def handle_end(self, won):
        e = EndingDialogue(self.input_handler, won)
        e.run()

    def beep_start(self, freqs):
        self.input_handler.hardware_event.buzzerstate = freqs[0]
        if len(freqs) > 1:
            # Start a new beep when 
            self.input_handler.attach("BUZZ_TIME",self.beep_start,freqs[1:],oneshot=True)
        else: 
            self.input_handler.attach("BUZZ_TIME",self.beep_end, oneshot=True)

    def beep_end(self):
        self.input_handler.hardware_event.buzzerstate = 0
        
