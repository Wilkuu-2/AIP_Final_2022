import socket
from controller_firmware import data
from enum import Enum
from PyQt5.QtWidgets import QInputDialog


class HARDWARE_INPUTS(Enum):
    SW1 = 1001
    SW2 = 1002


class HardwareEvent():
    MOVE_TRESHOLD: float = 0.1

    def __init__(self, inhandler):
        self.data: data.ControllerData = data.ControllerData()
        self.buzzerstate = 0
        self.inhandler = inhandler
        self.last_sw1 = 0
        self.last_sw2 = 0
        self.shakeEvents = []
        self.socket = None
        
        self.create_socket()

    def create_socket(self):
        dialog_text = "Give the IP of the controller. \nPress cancel to not use the controller."
        while True:
            ip, ok = QInputDialog().getText(None, "Connection", dialog_text)
            if not ok:
                self.socket = None
                return
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.settimeout(2)
                self.socket.connect((ip, 420))
                return
            except OSError as e:
                dialog_text = f"Error:\n{e}\n\nTry again.\nOr cancel to not use the controller."

    def handle(self):
        for ev in self.shakeEvents:
            if ev[1] < 0:
                ev[0].invoke()
                self.shakeEvents.remove(ev)
                continue
            ev[1] = ev[1] - 2

        if self.socket is None:
            return

        packet = data.readpacket(self.socket)
        message = packet.decode('utf-8')

        self.data.readMESSAGE(message)

        data_tuple = self.data.data_tuple()
        x, y, sw1, sw2, ax, ay, az, gx, gy, gz = data_tuple

        x -= 0.5
        y -= 0.5

        if abs(x) < self.MOVE_TRESHOLD:
            x = 0

        if abs(y) < self.MOVE_TRESHOLD:
            y = 0

        if x != 0 or y != 0:
            if abs(x) >= abs(y):
                direction = "HW_LEFT" if x > 0 else "HW_RIGHT"
                self.inhandler.handle_event(direction)
            else:
                direction = "HW_UP" if y > 0 else "HW_DOWN"
                self.inhandler.handle_event(direction)

        if self.last_sw1 != sw1:
            ev_type = "_KeyRelease" if sw1 != 0 else "_KeyPress"
            self.inhandler.handle_key(HARDWARE_INPUTS.SW1.value, ev_type)

        if self.last_sw2 != sw2:
            ev_type = "_KeyPress" if sw2 != 0 else "_KeyRelease"
            self.inhandler.handle_key(HARDWARE_INPUTS.SW2.value, ev_type)

        self.last_sw1 = sw1
        self.last_sw2 = sw2

        for ev in self.shakeEvents:
            if ev[1] < 0:
                ev[0].invoke()
                self.shakeEvents.remove(ev)
                continue
            ev[1] = ev[1] - (ax + ay + az) / 30.0

        self.socket.send(f"{self.buzzerstate}\n".encode("utf-8"))

    def startShakeEvent(self, callback, points: float):
        self.shakeEvents.append([callback, points])
