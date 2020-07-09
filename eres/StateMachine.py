from .states.State import State
from .states.State import IdleState
from .states.State import ErrorState

from .events.Event import Event
from .events.ErrorEvent import ErrorEvent


import logging


class StateMachine:

    def __init__(self, communicator, omit_welcome=False):

        super().__init__()
        self._comm = communicator
        self.is_running = False
        self.state = IdleState()

    @property
    def is_running(self):

        return self._is_running

    @is_running.setter
    def is_running(self, running):

        if not isinstance(running, bool):
            raise TypeError('is_running must be a bool')

        self._is_running = running

    @property
    def state(self):

        return self._state

    @state.setter
    def state(self, new_state):

        if not isinstance(new_state, State):
            raise TypeError('state must implement State')

        logging.debug('Context: New state is "{}"'.format(new_state))

        self._state = new_state
        self._comm.broadcast(self._state)

    def handleEvent(self, event):

        if not isinstance(event, Event):
            raise TypeError('event must implement Event')

        logging.debug('Context: Handling event "{}"'.format(event))

        if isinstance(event, ErrorEvent):
            self.state = ErrorState(event.origin, event.message, self.state,
                                    self.is_running)
        # elif isinstance(event, TeardownEvent):
        #     self.is_running = False
        #     self.state = TeardownState(event.target)
        #     if event.target == TeardownEvent.EXIT:
        #         self._comm.broadcast(None)
        #         return 0
        #     elif event.target == TeardownEvent.RESTART:
        #         self._comm.broadcast(None)
        #         return 123
        else:
            self.state.handleEvent(event, self)
