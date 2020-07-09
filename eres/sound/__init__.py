import logging
import os
import time

import pygame

from ..Workers import Workers
from ..events.CountdownEvent import CountdownEvent
from ..states.State import IdleState
from ..states.State import State


class Sound:
    def __init__(self, comm, stateMachine):

        super().__init__()
        self._comm = comm
        self._state = stateMachine.state

        pygame.mixer.init()

        soundRootLocation = os.path.dirname(os.path.abspath(__file__))
        self._announcements = [
            Announcement(os.path.join(soundRootLocation, "sounds", "rahmenzeitBeginnt.ogg"), 540),
            Announcement(os.path.join(soundRootLocation, "sounds", "8minuten.ogg"), 480),
            Announcement(os.path.join(soundRootLocation, "sounds", "7minuten.ogg"), 420),
            Announcement(os.path.join(soundRootLocation, "sounds", "6minuten30sekunden.ogg"), 390),
            Announcement(os.path.join(soundRootLocation, "sounds", "6minuten.ogg"), 360),
            Announcement(os.path.join(soundRootLocation, "sounds", "5minuten.ogg"), 300),
            Announcement(os.path.join(soundRootLocation, "sounds", "4minuten.ogg"), 240),
            Announcement(os.path.join(soundRootLocation, "sounds", "3minuten.ogg"), 180),
            Announcement(os.path.join(soundRootLocation, "sounds", "2minuten.ogg"), 120),
            Announcement(os.path.join(soundRootLocation, "sounds", "1minute.ogg"), 60),
            Announcement(os.path.join(soundRootLocation, "sounds", "45sekunden.ogg"), 45),
            Announcement(os.path.join(soundRootLocation, "sounds", "30sekunden.ogg"), 30),
            Announcement(os.path.join(soundRootLocation, "sounds", "15sekunden.ogg"), 15),
            Announcement(os.path.join(soundRootLocation, "sounds", "rahmenzeitEndet.ogg"), 0),
            Announcement(os.path.join(soundRootLocation, "sounds", "ende15sekunden.ogg"), -15),
            Announcement(os.path.join(soundRootLocation, "sounds", "ende30sekunden.ogg"), -30),
            Announcement(os.path.join(soundRootLocation, "sounds", "ende45sekunden.ogg"), -45),
            Announcement(os.path.join(soundRootLocation, "sounds", "ende1minute.ogg"), -60)
        ]

        logging.debug("Initializing sound...")

    def run(self):
        logging.debug("Sound: RUN!!")

        for state in self._comm.iterate(Workers.SOUND):
            self.handleState(state)

        logging.debug("Sound: done")

        return True
 
    def handleState(self, state):
        if isinstance(state, State):
            self.handleStateChanged(state)
        if isinstance(state, CountdownEvent):
            self.handleCountdownEvent(state)
    
    def handleCountdownEvent(self, state):
        for announcement in self._announcements:
            if announcement.IsPlayed == False and announcement.ShouldTriggerAt > state.timeLeft:
                announcement.Play()
                break # shold only play once per event

    def handleStateChanged(self, state):
        if self._state != state:
            for announcement in self._announcements:
                announcement.ResetIsPlayed()
            self._state = state


class Announcement:
    def __init__(self, filename, shouldPlayAt):
        self._sound = pygame.mixer.Sound(filename)
        self._isPlayed = False
        self._shouldTriggerAt = shouldPlayAt + self._sound.get_length()


    @property
    def IsPlayed(self):
        return self._isPlayed

    @property
    def ShouldTriggerAt(self):
        return self._shouldTriggerAt

    def Play(self):
        if self._isPlayed == False:
            self._isPlayed = True
            self._sound.play()
    
    def ResetIsPlayed(self):
        if self._isPlayed:
            self._sound.stop()
            self._isPlayed = False

# class SoundAnnouncements(IntEnum):
#     START = 0
#     EIGHT_MIN_LEFT= 1
#     SEVEN_MIN_LEFT = 2
#     SIX_AND_A_HALF_MIN_LEFT = 3
#     SIX_MIN_LEFT = 4