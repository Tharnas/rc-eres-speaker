import logging

import threading

from ..Workers import Workers
from ..events.GpioEvent import GpioEvent
from ..events.CountdownEvent import CountdownEvent
from ..states.State import IdleState
from ..states.State import State
from ..states.State import CountdownState


class Countdown:
    def __init__(self, comm, stateMachine):

        super().__init__()
        self._comm = comm

        logging.debug("Initializing countdown...")

        self.TIMERINTERVAL = 0.1 # seconds
        self._timeLeft = 0 
        self._timer = None

        logging.debug("Countdown initialized!")

    def run(self):
        logging.debug("Countdown: RUN!!")

        for state in self._comm.iterate(Workers.COUNTDOWN):
            self.handleState(state)

        logging.debug("Countdown: done")

        return True

    def timerCallback(self):
        self._timeLeft -= self.TIMERINTERVAL
        self._comm.broadcast(CountdownEvent(self._timeLeft))
        self.runTimer()

    def runTimer(self):
        self._timer = threading.Timer(self.TIMERINTERVAL, self.timerCallback)
        self._timer.start()

    def stopTimer(self):
        if self._timer is not None:
            self._timer.cancel()
            
    def handleState(self, state):
        if isinstance(state, CountdownState):
            # start timer
            self.stopTimer() # make sure timer is not running
            self._timeLeft = 540 + 6  # 9 min + 5s
            self.runTimer()
        elif isinstance(state, State):
            # stop timer
            self.stopTimer()
