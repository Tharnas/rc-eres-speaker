
import logging
import logging.handlers
import multiprocessing as mp

from .gpio import Gpio
from .sound import Sound
from .Communicator import Communicator
from .Workers import Workers
from .StateMachine import StateMachine
from .events.ErrorEvent import ErrorEvent
from .events.Event import Event
from .display import Display
from .countdown import Countdown


def main(argv):
    InitializeLogger()

    status_code = 1

    status_code = run()

    logging.info('Exiting with status code %d', status_code)

    return status_code


def InitializeLogger():
    log_level = logging.DEBUG
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # create console handler and set format
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)

    # create file handler and set format
    fh = logging.handlers.TimedRotatingFileHandler('eres.log', when='d',
                                                   interval=1, backupCount=10)
    fh.setFormatter(formatter)

    logging.basicConfig(level=log_level, handlers=(ch, fh))


def run():

    comm = Communicator()
    stateMachine = StateMachine(comm)

    # Initialize processes
    proc_classes = (GpioProcess, DisplayProcess, CountdownProcess, SoundProcess)
    # proc_classes = (GpioProcess, DisplayProcess, SoundProcess)
    procs = [P(comm, stateMachine) for P in proc_classes]

    for proc in procs:
        proc.start()

    # Enter main loop
    exit_code = mainloop(comm, stateMachine)

    # Wait for processes to finish
    for proc in procs:
        proc.join()

    logging.debug('All processes joined, returning code {}'. format(exit_code))

    return exit_code


def mainloop(comm, stateMachine):
    while True:
        try:
            for event in comm.iterate(Workers.MASTER):
                exit_code = stateMachine.handleEvent(event)
                if exit_code in (0, 123):
                    return exit_code
        except Exception as e:
            logging.exception('Main: Exception "{}"'.format(e))
            comm.send(Workers.MASTER, ErrorEvent('Gpio', str(e)))


class GpioProcess(mp.Process):
    def __init__(self, comm, stateMachine):
        super().__init__()
        self.daemon = True

        self._comm = comm
        self._stateMachine = stateMachine

    def run(self):

        logging.debug('GpioProcess: Initializing...')

        while True:
            try:
                if Gpio(self._comm).run():
                    break
            except Exception as e:
                logging.exception("GpioProcess: Exception \"{}\"".format(e))

        logging.debug('GpioProcess: Exit')

class SoundProcess(mp.Process):
    def __init__(self, comm, stateMachine):
        super().__init__()
        self.daemon = True

        self._comm = comm
        self._stateMachine = stateMachine

    def run(self):

        logging.debug('SoundProcess: Initializing...')

        while True:
            try:
                if Sound(self._comm, self._stateMachine).run():
                    break
            except Exception as e:
                logging.exception("SoundProcess: Exception \"{}\"".format(e))

        logging.debug('SoundProcess: Exit')

class DisplayProcess(mp.Process):
    def __init__(self, comm, stateMachine):
        super().__init__()
        self.daemon = True

        self._comm = comm
        self._stateMachine = stateMachine

    def run(self):

        logging.debug('DisplayProcess: Initializing...')

        while True:
            try:
                if Display(self._comm, self._stateMachine).run():
                    break
            except Exception as e:
                logging.exception("DisplayProcess: Exception \"{}\"".format(e))

        logging.debug('DisplayProcess: Exit')


class CountdownProcess(mp.Process):
    def __init__(self, comm, stateMachine):
        super().__init__()
        self.daemon = True

        self._comm = comm
        self._stateMachine = stateMachine

    def run(self):

        logging.debug('CountdownProcess: Initializing...')

        while True:
            try:
                if Countdown(self._comm, self._stateMachine).run():
                    break
            except Exception as e:
                logging.exception(
                    "CountdownProcess: Exception \"{}\"".format(e))

        logging.debug('CountdownProcess: Exit')
