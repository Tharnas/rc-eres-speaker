import logging
import os
import time

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106
from PIL import ImageFont

from ..Workers import Workers
from ..events.GpioEvent import GpioEvent
from ..events.CountdownEvent import CountdownEvent
from ..states.State import IdleState
from ..states.State import State
from ..states.State import CountdownState


class Display:
    def __init__(self, comm, stateMachine):

        super().__init__()
        self._comm = comm
        self._state = stateMachine.state
        self._timeLeft = "00:00"

        logging.debug("Initializing display...")

        interface = i2c(port=1, address=0x3C)
        currentPath = os.path.dirname(os.path.abspath(__file__))
        self._font = os.path.join(currentPath, "arial.ttf")
        self._device = sh1106(interface, rotate=0)

        logging.debug("Display initialized!")

    def run(self):
        logging.debug("Display: RUN!!")

        for state in self._comm.iterate(Workers.DISPLAY):
            self.handleState(state)

        logging.debug("Display: done")

        return True

    def print(self):
        # Box and text rendered in portrait mode
        with canvas(self._device) as draw:
            showStart = False
            showStop = False
            showCountdown = False
            font = ImageFont.truetype(self._font, 12)

            if isinstance(self._state, CountdownState):
                stateText = "countdown"
                showStop = True
                showCountdown = True
            elif isinstance(self._state, IdleState):
                stateText = "idle"
                showStart = True

            if showStop:
                self.drawStop(draw, font)
            if showStart:
                self.drawStart(draw, font)

            if showCountdown:
                self.drawCountdown(self._timeLeft, draw, ImageFont.truetype(self._font, 40))

            self.drawTitle(stateText, draw, ImageFont.truetype(self._font, 10))

    def drawCountdown(self, text, draw, font):
        w, h = draw.textsize(text, font=font)

        position = (self._device.bounding_box[2]/2 - w/2, 10)

        draw.text(position, text, font=font,  fill="white")


    def drawTitle(self, text, draw, font):
        w, h = draw.textsize(text, font=font)

        position = (self._device.bounding_box[2]/2 - w/2, -1)

        draw.text(position, text, font=font,  fill="white")

    def drawStart(self, draw, font):
        text = "Start ->"
        w, h = draw.textsize(text, font=font)

        position = (
            (self._device.bounding_box[2] - w), (self._device.bounding_box[3] - h))

        draw.text(position, text, font=font,  fill="white")

    def drawStop(self, draw, font):
        text = "<- Stop"
        w, h = draw.textsize(text, font=font)

        position = (0, (self._device.bounding_box[3] - h))

        draw.text(position, text, font=font,  fill="white")

    def handleState(self, state):
        reprint = False
        if isinstance(state, State):
            self._state = state
            reprint = True
        if isinstance(state, CountdownEvent):
            if state.timeLeft > 0:
                timeString = time.strftime("%M:%S", time.gmtime(state.timeLeft))
            else:
                timeString = time.strftime("-%M:%S", time.gmtime(state.timeLeft*(-1)))

            if self._timeLeft != timeString:
                self._timeLeft = timeString
                reprint = True

        if reprint:
            self.print()
