from .Event import Event
import numbers

class CountdownEvent(Event):

    def __init__(self, timeLeft):

        super().__init__('Countdown')
        self.timeLeft = timeLeft

    def __str__(self):

        return self.timeLeft

    @property
    def timeLeft(self):

        return self._timeLeft

    @timeLeft.setter
    def timeLeft(self, timeLeft):

        if not isinstance(timeLeft, (numbers.Number)):
            raise TypeError('TimeLeft has to be a number')

        self._timeLeft = timeLeft
