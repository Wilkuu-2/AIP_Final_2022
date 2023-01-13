from inspect import signature
DEBUG = False


class EventMethod:
    def __init__(self, method, *args, desired_arg_len=-1):
        self.__name__ = "EventMethod: " + getattr(method, "__name__")
        self.method = method
        self.args = args[0]
        if desired_arg_len == -1:
            try:
                self.desired_arg_len = len(signature(method).parameters)
            except ValueError:
                self.desired_arg_len = desired_arg_len
        else:
            self.desired_arg_len = desired_arg_len

    def invoke(self, *args):
        local_args = args
        local_args_len = len(args)

        if local_args_len > 0:
            new_args = []
            for arg in local_args:
                new_args.append(arg)

            if self.desired_arg_len > -1:
                for arg in self.args[len(args): self.desired_arg_len]:
                    new_args.append(arg)
            else:
                for arg in self.args[len(args):]:
                    new_args.append(arg)

            self.method(*new_args)

        elif len(self.args) > 0:
            self.method(*self.args)

        else:
            self.method()


class InputEvent:
    def __init__(self, key, name):
        self.name = name
        self.key = key
        self.methods = []

    def trigger(self, *args):
        for method in self.methods:
            if DEBUG:
                print(
                    f"[EV] {self.name}, {self.key}: method ({method.__name__}) executing")
            method.invoke(*args)

    def addMethod(self, method):
        if DEBUG:
            print(
                f"[EV] {self.name}, {self.key}: method ({method.__name__}) added")
        self.methods.append(method)


class InHandler:
    def __init__(self):
        pass

    def set_control_scheme(self, binds: dict, getAxis):
        self.axisMethod = getAxis
        self.control_scheme = binds
        self.events = {}
        self.held_keys = []
        self.popup_closed = False

        for key, name in self.control_scheme.items():
            try:
                ie = self.find_Event_by_name(name)
                self.events[key] = ie
            except KeyError:
                self.events[key] = InputEvent(key, name)

        print(self.events)

    def heldKeyUpdate(self):
        for key in self.held_keys:
            self.handle_key(key, "_KeyHold")

    def getAxis(self):
        return self.axisMethod()

    def handle_key(self, key, ev_type):
        if ev_type == "_KeyPress":
            self.held_keys.append(key)
        elif ev_type == "_KeyRelease":
            try:
                self.held_keys.remove(key)
            except ValueError:
                pass

        self.handle_event(str(key)+ev_type)

    def handle_event(self, ev_code, *args):
        if DEBUG:
            print(f"Event {ev_code}, handling START")
        if ev_code == "ReleaseHeld":
            self.held_keys = []
            return
        try:
            self.events[ev_code].trigger(*args)

        except KeyError:
            if DEBUG:
                print(f"Unhandled: {ev_code}")
        if DEBUG:
            print(f"Event {ev_code}, handling END")

    def find_Event_by_name(self, name):
        for event in self.events.values():
            if event.name == name:
                return event
        raise KeyError(f"[EV]: Event {name} not found")

    def attach(self, name, method, *args):
        self.find_Event_by_name(name).addMethod(EventMethod(method, args))
