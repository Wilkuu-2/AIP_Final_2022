# AI&P Final project [Create M6 2023]
# game/player.py
#
# Copyright 2023 Jakub Stachurski
# Copyright 2023 Natalia Bueno Donadeu
#

# Imports
from .game_object import GameObject
from input_helpers import InHandler
from common import ACCESS_FLAGS
from dialogues import BaseDialogue, EndingDialogue
from level import LevelTile


class Player(GameObject):
    """ The player entity, this is where the player logic lives
    tile -> see GameObject
    input_handler -> InHandler that will handle the movement and other actions
    """
    __name__ = "Player"
    blocking = True

    def __init__(self, tile: LevelTile, input_handler: InHandler, ):
        super().__init__(tile, (1, 1), input_handler, ACCESS_FLAGS.PLAYER)

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
        dialogue = BaseDialogue.getRandomDialogue(self.input_handler)
        dialogue.run()


        self.input_handler.attach(
            "Popup_Finish", self.handle_popup, enemy, oneshot=True)

    def handle_popup(self, ok, enemy):
        print(f"Popup finished: {ok}, {enemy}")
        self.beep_start([0,680,330])
        if ok:
            enemy.respawn()
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
        
