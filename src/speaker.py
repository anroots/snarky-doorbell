from time import sleep

import os
import pygame.mixer
from pygame.mixer import Sound

class Speaker:

    volume = 0

    def __init__(self, logger, volume):
        self.logger = logger
        self.volume = volume

        pygame.mixer.init()

        self.channel = pygame.mixer.Channel(0)
        self.channel.set_volume(0)

    def say(self, file):

        if not os.path.exists(file):
            self.logger.error("Sound file %s does not exist!" % file)

        self.logger.debug("Playing %s", file)

        # Volume is in range 0 .. 1.0, but we represent it in 0 .. 100 internally
        volume = round(self.volume/100.0,2)
        self.channel.set_volume(volume)
        self.logger.debug("Volume is %s"%volume)

        sound = Sound(file)
        sound.set_volume(1.0)

        self.channel.play(sound)

        #while self.channel.get_busy() == True:
        #    sleep(1)

        #self.logger.debug("Sound ended")
        #self.channel.set_volume(0)



    def set_volume(self, volume):
        self.volume = volume
        self.logger.info("Set volume to %f" % volume)


    def mute(self):
        self.logger.info("Muting")
        self.set_volume(0)