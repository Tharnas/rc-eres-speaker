# from .State import State
# from ..events.GpioEvent import GpioEvent
# from .CountdownState import CountdownState


# class IdleState(State):

#     def __init__(self):

#         super().__init__()

#     def handleEvent(self, event, context):
#         if isinstance(event, GpioEvent):
#             if event.message == 'LeftButton':
#                 context.state = CountdownState()
#         # if isinstance(event, GuiEvent):
#         #     if event.name == 'start':
#         #         context.state = StartupState()
#         #     elif event.name == 'exit':
#         #         context.state = TeardownState(TeardownEvent.EXIT)
#         # else:
#         #     raise TypeError('Unknown Event type "{}"'.format(event))
