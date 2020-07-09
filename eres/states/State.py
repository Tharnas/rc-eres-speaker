from ..events.GpioEvent import GpioEvent
from ..events.CountdownEvent import CountdownEvent
from ..Communicator import Workers



class State:

    def __init__(self):

        super().__init__()
        self.update()

    def __str__(self):

        return type(self).__name__

    def update(self):

        pass

    def handleEvent(self, event, context):

        raise NotImplementedError()


class IdleState(State):

    def __init__(self):

        super().__init__()

    def handleEvent(self, event, context):
        if isinstance(event, GpioEvent):
            if event.message == 'LeftButton':
                context.state = CountdownState()
        # if isinstance(event, GuiEvent):
        #     if event.name == 'start':
        #         context.state = StartupState()
        #     elif event.name == 'exit':
        #         context.state = TeardownState(TeardownEvent.EXIT)
        # else:
        #     raise TypeError('Unknown Event type "{}"'.format(event))


class ErrorState(State):

    def __init__(self, origin, message, old_state, is_running):

        self.origin = origin
        self.message = message
        self.old_state = old_state
        self.is_running = is_running
        super().__init__()

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

    @property
    def old_state(self):

        return self._old_state

    @old_state.setter
    def old_state(self, old_state):

        if not isinstance(old_state, State):
            raise TypeError('old_state must be derived from State')

        self._old_state = old_state

    @property
    def is_running(self):

        return self._is_running

    @is_running.setter
    def is_running(self, running):

        if not isinstance(running, bool):
            raise TypeError('is_running must be a bool')

        self._is_running = running

    def handleEvent(self, event, context):

        pass
        # if isinstance(event, GuiEvent) and event.name == 'retry':
        #     context.state = self.old_state
        #     context.state.update()
        # elif isinstance(event, GuiEvent) and event.name == 'abort':
        #     if self.is_running:
        #         context.state = IdleState()
        #     else:
        #         context.state = TeardownState(TeardownEvent.WELCOME)
        # else:
        #     raise TypeError('Unknown Event type "{}"'.format(event))


class CountdownState(State):
    def __init__(self):

        super().__init__()


    def handleEvent(self, event, context):
        if isinstance(event, GpioEvent):
            if event.message == "RightButton":
                context.state = IdleState()
        else:
            raise TypeError('Unknown Event type "{}"'.format(event))
