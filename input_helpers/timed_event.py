from .input_handler import InputEvent


class TimedEvent(InputEvent):
    """ A InputEvent that fires once every x frames

        name -> name of the event
        n_frames -> amount of frames of delay per trigger of the event

    """
    current_frame = 0

    @staticmethod
    def increment():
        TimedEvent.current_frame += 1

    def __init__(self, name: str, n_frames: int):
        super().__init__(name)
        self.n_frames = n_frames
        self.activate_at = TimedEvent.current_frame + n_frames

    def refresh(self):
        """ Increments the frame counter and checks if the event should be triggered.
        """
        if TimedEvent.current_frame > self.activate_at:
            self.activate_at = TimedEvent.current_frame + self.n_frames
            self.trigger()
