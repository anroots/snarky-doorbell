from time import sleep

import os
import pygame.mixer
from pygame.mixer import Sound

class Speaker:

    def __init__(self, logger):
        self.logger = logger

        pygame.mixer.init()

        self.channel = pygame.mixer.Channel(0)
        self.channel.set_volume(0)

    def say(self, file, volume = 0.1):

        if not os.path.exists(file):
            self.logger.error("Sound file %s does not exist!" % file)

        self.logger.debug("Playing %s", file)

        # Volume is in range 0 .. 1.0, but we represent it in 0 .. 100 internally
        volume = round(volume/100.0,2)
        self.channel.set_volume(volume)
        self.logger.debug("Volume is %s"%volume)

        sound = Sound(file)
        sound.set_volume(1.0)

        self.channel.play(sound)