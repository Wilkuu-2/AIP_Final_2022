DEBUG = False

class InputEvent:
    def __init__(self, key, name):
        self.name = name
        self.key = key
        self.methods = []

    def trigger(self):
        for method in self.methods:
            method()

    def addMethod(self, method):
        if DEBUG:
            print(f"[EV] {self.name}, {self.key}: method {method} added")
        self.methods.append(method)


class InHandler:
    def __init__(self):
        pass

    def set_control_scheme(self, binds: dict, getAxis):
        self.axisMethod = getAxis
        self.control_scheme = binds
        self.events = {}

        for key, name in self.control_scheme.items():
            self.events[key] = InputEvent(key, name)

    def getAxis(self):
        return self.axisMethod()

    def handle(self, key, ev_type):
        try:
            self.events[str(key)+ev_type].trigger()
        except KeyError:
            pass
            # print(f"Unhandled: {key}, {ev_type}")

    def find_Event_by_name(self, name):
        for event in self.events.values():
            if event.name == name:
                return event
        raise KeyError("[EV]: Event {name} not found")

    def attach(self, name, method):
        self.find_Event_by_name(name).addMethod(method)
