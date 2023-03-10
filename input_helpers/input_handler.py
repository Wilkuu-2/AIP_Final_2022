# AI&P Final project [Create M6 2022-2023]
# input_helpers/input_handler.py
#
# Copyright 2022-2023 Jakub Stachurski
# Copyright 2022-2023 Natalia Bueno Donadeu
#
# TODO: Maybe we should split this file a bit

# Imports
from typing import Callable, Union
from .input_event import InputEvent
from .event_method import EventMethod
from .hardware_event import HardwareEvent
from .timed_event import TimedEvent
import re

# Debug flag
DEBUG = False

#
# Event Method


class InHandler:
    """The handler for all inputs and events.
    """

    # TODO: Figure out why everything has to be done in set_control_scheme
    def __init__(self):
        self.events: dict[str, Union[InputEvent, TimedEvent]] = {}
        self.held_keys: list[int] = []
        self.timed_events: list[TimedEvent] = []
        self.hardware_event = HardwareEvent(self)

    # set_control_scheme
    #
    def set_control_scheme(self, binds: dict):
        """A method that initalizes the control scheme
        binds -> key/event binds a dict of format {"EVENT_CODE":"EVENT_NAME"}
        getAxis -> temporarily non-functional movement axis getter method
        TODO: reevaluate the existance of getAxis
        """
        self.control_scheme = binds

        # Go over all the binds
        for key, name in self.control_scheme.items():
            try:
                # Find a InputEvent with that name and assign it
                ie = self.find_Event_by_name(name)
                self.events[key] = ie
            except KeyError:
                # If the event does not exist yet, create one

                # Match for TimedEvent syntax in the key
                if re.match(r"TF-\d{3}", key):
                    ev = TimedEvent(name, int(key[3:6]))
                    self.events[key] = ev
                    self.timed_events.append(ev)

                else:
                    self.events[key] = InputEvent(name)

    def heldKeyUpdate(self):
        """A method to be called each frame to generate KeyHold events and coordinate timed events"""
        for key in self.held_keys:
            self.handle_key(key, "_KeyHold")

        TimedEvent.increment()
        for ev in self.timed_events:
            ev.refresh()

        self.hardware_event.handle()

    def handle_key(self, key: int, ev_type: str):
        """A handler for key events

        key -> keycode of the input
        ev_type -> string with the type of key event
                   (_KeyPress, _KeyRelease, or _KeyHold)
        """

        # Check if he Key has to be held
        if ev_type == "_KeyPress":
            self.held_keys.append(key)
        elif ev_type == "_KeyRelease":
            try:
                self.held_keys.remove(key)
            except ValueError:
                pass

        # Handle the input event like normal
        self.handle_event(str(key)+ev_type)

    # handle_event
    #
    def handle_event(self, ev_code: str, *args):
        """A method that handles event_codes and starts events

           ev_code -> event code to be handled
           args    -> any amount of arguments to be passed to the event
        """
        if DEBUG:
            print(f"Event {ev_code}, handling START")

        # ReleaseHeld
        # Special event code that releases the held keys
        # Usefull for when the player loses control of the game
        if ev_code == "ReleaseHeld":
            self.held_keys = []
            return

        # Try to find a event for the event code
        try:
            self.events[ev_code].trigger(*args)

        # Discard events codes without corresponding events
        except KeyError:
            if DEBUG:
                print(f"Unhandled: {ev_code}")

        if DEBUG:
            print(f"Event {ev_code}, handling END")

    def find_Event_by_name(self, name: str) -> InputEvent:
        """Finds the event by its name instead of the event code
        (AKA searches the dict by value instead of the key)
        Raises a KeyError when not successful
        """
        for event in self.events.values():
            if event.name == name:
                return event
        raise KeyError(f"[EV]: Event {name} not found")

    def attach(self, name: str, method: Callable, *args, oneshot=False):
        """Wrapper for attaching regular python methods to InputEvents

        name -> Name of the event
        method -> method to be called
        args   -> any amount of constant arguments
        """
        e_method = EventMethod(method, args, oneshot=oneshot)
        self.find_Event_by_name(name).addMethod(e_method)
        return (name, e_method)

    def detach(self, name: str, method: EventMethod):
        self.find_Event_by_name(name).removeMethod(method)

    def get_shake(self):
        return self.hardware_event.shake
