import logging
import os
import time

import threading

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

        self._displayInformation = DisplayInformation()

        logging.debug("Initializing display...")

        # initialize display
        interface = i2c(port=1, address=0x3C)
        self._device = sh1106(interface, rotate=0)

        # initialize fonts
        currentPath = os.path.dirname(os.path.abspath(__file__))
        font = os.path.join(currentPath, "arial.ttf")
        self._smallFont = ImageFont.truetype(font, 10)
        self._regularFont = ImageFont.truetype(font, 12)
        self._bigFont = ImageFont.truetype(font, 40)

        # start drawing timer        
        self.runDrawTimer()

        self._statusPixelToggleCounter = time.perf_counter()

        logging.debug("Display initialized!")

    def runDrawTimer(self):
        self._drawTimer = threading.Timer(0.1, self.timerCallback)
        self._drawTimer.start()

    def timerCallback(self):

        # toggle status pixel if redraw is required or not later than 1.5s
        currentCounter = time.perf_counter()
        sinceLastToggle = currentCounter - self._statusPixelToggleCounter
        if self._displayInformation.shouldRedraw or sinceLastToggle >= 1.5:
            self._displayInformation.statusPixel = not self._displayInformation.statusPixel
            self._statusPixelToggleCounter = currentCounter

        if self._displayInformation.shouldRedraw:
            self.draw()
            self._displayInformation.markDrawn()

        self.runDrawTimer()


    def run(self):
        logging.debug("Display: RUN!!")

        for state in self._comm.iterate(Workers.DISPLAY):
            self.handleState(state)

        logging.debug("Display: done")

        return True

    def draw(self):
        # startTime= time.perf_counter()

        # Box and text rendered in portrait mode
        with canvas(self._device) as draw:
            try:
                # stop button
                if self._displayInformation.showStopButton:
                    self.drawStop(draw, self._regularFont)

                # start button
                if self._displayInformation.showStartButton:
                    self.drawStart(draw, self._regularFont)

                # time left
                if self._displayInformation.timeLeft:
                    self.drawCountdown(self._displayInformation.timeLeft, draw, self._bigFont)
                
                # status text
                self.drawTitle(self._displayInformation.statusText, draw, self._smallFont)

                # status pixel
                if self._displayInformation.statusPixel:
                    draw.rectangle((0,0,1,1), fill="white")
            except:
                logging.exception("Display: error during drawing.")


        # endTime = time.perf_counter()
        # logging.debug("took {} to draw".format(endTime - startTime))

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
        if isinstance(state, State):
            if isinstance(state, CountdownState):
                self._displayInformation.statusText = "countdown"
                self._displayInformation.showStartButton = False
                self._displayInformation.showStopButton = True
            elif isinstance(state, IdleState):
                self._displayInformation.statusText = "idle"
                self._displayInformation.showStartButton = True
                self._displayInformation.showStopButton = False
                self._displayInformation.timeLeft = ""

        if isinstance(state, CountdownEvent):
            if state.timeLeft > 0:
                self._displayInformation.timeLeft = time.strftime("%M:%S", time.gmtime(state.timeLeft))
            else:
                self._displayInformation.timeLeft = time.strftime("-%M:%S", time.gmtime(state.timeLeft*(-1)))


class DisplayInformation:
    def __init__(self):
        super().__init__()

        self._statusText = "Starting..."
        self._timeLeft = ""
        self._showStartButton = False
        self._showStopButton = False
        self._statusPixel = False
        self._shouldRedraw = True

    @property
    def statusText(self):
        return self._statusText

    @statusText.setter
    def statusText(self, value):
        if value != self._statusText:
            self._statusText = value
            self._shouldRedraw = True

    @property
    def statusPixel(self):
        return self._statusPixel

    @statusPixel.setter
    def statusPixel(self, value):
        if value != self._statusPixel:
            self._statusPixel = value
            self._shouldRedraw = True

    @property
    def timeLeft(self):
        return self._timeLeft

    @timeLeft.setter
    def timeLeft(self, value):
        if value != self._timeLeft:
            self._timeLeft = value
            self._shouldRedraw = True
            
    @property
    def showStartButton(self):
        return self._showStartButton

    @showStartButton.setter
    def showStartButton(self, value):
        if value != self._showStartButton:
            self._showStartButton = value
            self._shouldRedraw = True

    @property
    def showStopButton(self):
        return self._showStopButton

    @showStopButton.setter
    def showStopButton(self, value):
        if value != self._showStopButton:
            self._showStopButton = value
            self._shouldRedraw = True

    @property
    def shouldRedraw(self):
        return self._shouldRedraw
    
    def markDrawn(self):
        self._shouldRedraw = False

