# AI&P Final project [Create M6 2022-2023]
# input_helpers/event_method.py
#
# Copyright 2022-2023 Jakub Stachurski
# Copyright 2022-2023 Natalia Bueno Donadeu
#
# TODO: Maybe we should split this file a bit

# Imports
from inspect import signature
from typing import Callable


class EventMethod:
    """ A wrapper around a method that handles constant and non-constant arguments

    method -> a method that is to be called
    args   -> any amount of constant arguments
    desired_arg_len -> the amount of arguments the method has,
                    if left on -1, the amount will be determined automatically
                    for most cases
    """

    def __init__(self, method: Callable, *args, desired_arg_len: int=-1):
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

    def invoke(self, *args):
        """Calls the method

        args -> any amount of non-constant arguments
        """
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
