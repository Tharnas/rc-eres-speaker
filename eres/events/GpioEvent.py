from .Event import Event


class GpioEvent(Event):

    def __init__(self, origin, message):

        super().__init__('Gpio')
        self.origin = origin
        self.message = message

    def __str__(self):

        return self.origin + ': ' + self.message

    @property
    def origin(self):

        return self._origin

    @origin.setter
    def origin(self, origin):

        if not isinstance(origin, str):
            raise TypeError('origin must be a string')

        self._origin = origin

    @property
    def message(self):

        return self._message

    @message.setter
    def message(self, message):

        if not isinstance(message, str):
            raise TypeError('message must be a string')

        self._message = message
