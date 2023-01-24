# AI&P Final project [Create M6 2022-2023]
# input_helpers/input_event.py
#
# Copyright 2022-2023 Jakub Stachurski
# Copyright 2022-2023 Natalia Bueno Donadeu
#

# Imports
from .event_method import EventMethod
DEBUG = False


class InputEvent:
    """An object that represents a single event in the application
    An event can be triggered by multiple keys and invoke multiple methods

    name -> The event name in the controls.py file
    """

    def __init__(self, name: str):
        self.name = name
        self.methods = []

    def trigger(self, *args):
        """Triggers the event by invoking all the attached EventMethods"""
        for method in self.methods:
            if DEBUG:
                print(
                    f"[EV] {self.name}: method ({method.__name__}) executing")
            method.invoke(*args)

    def addMethod(self, method: EventMethod):
        """Attaches a method to the event

        method -> the method to be attached
        """
        if DEBUG:
            print(
                f"[EV] {self.name}: method ({method.__name__}) added")
        self.methods.append(method)

    def removeMethod(self, method: EventMethod):
        self.methods.remove(method)

    def __repr__(self):
        return f"{self.name}:{type(self)}"
