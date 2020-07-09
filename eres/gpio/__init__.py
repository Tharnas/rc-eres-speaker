import logging
import gpiozero

from ..Workers import Workers
from ..events.GpioEvent import GpioEvent


class Gpio:
    def __init__(self, comm):

        super().__init__()
        self._comm = comm

        logging.debug("Initializing buttons...")

        pin_left_button = 24
        pin_right_button = 27

        self._left_button = gpiozero.Button(pin_left_button)
        self._left_button.when_pressed = self.leftButtonPressed

        self._right_button = gpiozero.Button(pin_right_button)
        self._right_button.when_pressed = self.rightButtonPressed

        logging.debug("Buttons initialized!")

    def leftButtonPressed(self):
        logging.debug("left button pressed")
        self._comm.send(Workers.MASTER, GpioEvent("Gpio", "LeftButton"))

    def rightButtonPressed(self):
        logging.debug("right button pressed")
        self._comm.send(Workers.MASTER, GpioEvent("Gpio", "RightButton"))


    def run(self):
        logging.debug("Gpio: RUN!!")

        for state in self._comm.iterate(Workers.GPIO):
            self.handleState(state)

        logging.debug("Gpio: done")

        return True

    def handleState(self, state):

        pass

