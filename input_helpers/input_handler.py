# AI&P Final project [Create M6 2022-2023]
# input_helpers/input_handler.py
#
# Copyright 2022-2023 Jakub Stachurski
# Copyright 2022-2023 Natalia Bueno Donadeu
#
# TODO: Maybe we should split this file a bit

# Imports
from inspect import signature

# Debug flag
DEBUG = False

#
# Event Method
# A wrapper around a method that handles constant and non-constant arguments


class EventMethod:

    # Constructor
    #   method -> a method that is to be called
    #   args   -> any amount of constant arguments
    #   desired_arg_len -> the amount of arguments the method has,
    #                   if left on -1, the amount will be determined automatically
    #                   for most cases
    #
    def __init__(self, method, *args, desired_arg_len=-1):
        self.__name__ = "EventMethod: " + getattr(method, "__name__")
        self.method = method
        self.args = args[0]

        # Determine the amount of arguments automatically
        if desired_arg_len == -1:
            try:
                self.desired_arg_len = len(signature(method).parameters)
            except ValueError:
                self.desired_arg_len = desired_arg_len
        # Set to the given value
        else:
            self.desired_arg_len = desired_arg_len

    # invoke
    #   Calls the method
    #
    #   args -> any amount of non-constant arguments
    #
    def invoke(self, *args):
        local_args = args
        local_args_len = len(args)

        # Create an array that is either the local_args or a mix of
        # local_args and self.args in that order
        if local_args_len > 0:
            # Fill in all the local_args
            new_args = list(local_args)

            # If we know how much parameters the method has
            # We can fill it up to that amount
            if self.desired_arg_len > -1:
                for arg in self.args[:self.desired_arg_len - local_args_len]:
                    new_args.append(arg)

            # Otherwise just put in all we have
            else:
                for arg in self.args:
                    new_args.append(arg)

            # Call the method with all the args we accumulated
            self.method(*new_args)

        # Fill the method with the constant arguments only
        elif len(self.args) > 0:
            self.method(*self.args)

        # A method with no parameters (hopefully) will be called
        else:
            self.method()

#
# Input Event
#   A object that represents a single event in the application
#   An event can be triggered by multiple keys and invoke multiple methods
#


class InputEvent:
    # Constructor
    #
    # name -> The event name in the controls.py file
    #
    def __init__(self, name):
        self.name = name
        self.methods = []

    # trigger
    #  Triggers the event by invoking all the attached EventMethods
    #
    #  args -> any amount on arguments to be given to the EventMethods
    #
    def trigger(self, *args):
        for method in self.methods:
            if DEBUG:
                print(
                    f"[EV] {self.name}: method ({method.__name__}) executing")
            method.invoke(*args)

    # addMethod
    #   Attaches a method to the event
    #
    #   method -> the method to be attached
    #
    def addMethod(self, method: EventMethod):
        if DEBUG:
            print(
                f"[EV] {self.name}: method ({method.__name__}) added")
        self.methods.append(method)


# InHandler
#   The handler for all inputs and events.
class InHandler:
    # Constructor
    # TODO: Figure out why everything has to be done in set_control_scheme
    def __init__(self):
        self.events = {}
        self.held_keys = []

    # set_control_scheme
    #   A method that initalizes the control scheme
    #
    #   binds -> key/event binds a dict of format {"EVENT_CODE":"EVENT_NAME"}
    #   getAxis -> temporarily non-functional movement axis getter method
    #   TODO: reevaluate the existance of getAxis
    #
    def set_control_scheme(self, binds: dict, getAxis):
        self.axisMethod = getAxis
        self.control_scheme = binds

        # Go over all the binds
        for key, name in self.control_scheme.items():
            try:
                # Find a InputEvent with that name and assign it
                ie = self.find_Event_by_name(name)
                self.events[key] = ie
            except KeyError:
                # If the event does not exist yet, create one
                self.events[key] = InputEvent(name)

    # heldKeyUpdate
    #   A method to be called each frame to generate KeyHold events
    #
    def heldKeyUpdate(self):
        for key in self.held_keys:
            self.handle_key(key, "_KeyHold")

    # getAxis
    #   Wrapper around the getAxis method passed in the constructor
    #
    def getAxis(self):
        return self.axisMethod()

    # handle_key
    #   A handler for key events
    #
    #   key -> keycode of the input
    #   ev_type -> string with the type of key event
    #           (_KeyPress, _KeyRelease, or _KeyHold)
    #
    def handle_key(self, key, ev_type):
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
    #   A method that handles event_codes and starts events
    #
    #   ev_code -> event code to be handled
    #   args    -> any amount of arguments to be passed to the event
    #
    def handle_event(self, ev_code, *args):
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

    # find_Event_by_name
    #   Finds the event by its name instead of the event code
    #   (AKA searches the dict by value instead of the key)
    #   Raises a KeyError when not successfull
    #
    #   name -> the
    #
    def find_Event_by_name(self, name):
        for event in self.events.values():
            if event.name == name:
                return event
        raise KeyError(f"[EV]: Event {name} not found")

    # attach
    #   Wrapper for attaching regular python methods to InputEvents
    #
    #   name -> "Name of the event"
    #   method -> method to be called
    #   args   -> any amount of constant arguments
    #
    def attach(self, name, method, *args):
        self.find_Event_by_name(name).addMethod(EventMethod(method, args))
