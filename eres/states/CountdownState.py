# from .State import State
# from .IdleState import IdleState

# from ..events.GpioEvent import GpioEvent


# class CountdownState(State):

#     def __init__(self):

#         super().__init__()

#     def handleEvent(self, event, context):
#         if isinstance(event, GpioEvent):
#             if event.message == "RightButton":
#                 context.state = IdleState()
#         else:
#             raise TypeError('Unknown Event type "{}"'.format(event))
