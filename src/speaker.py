import pygame.mixer
from pygame.mixer import Sound

class Speaker:


    def __init__(self, logger):
        self.logger = logger
        pygame.mixer.init()
        self.channel = pygame.mixer.Channel(0)


    def say(self, file):

        self.logger.info("Playing %s", file)
        sound = Sound(file)

        self.channel.play(sound)


    def volume(self, volume):
        self.logger.info("Set volume to %f" % volume)
        self.channel.set_volume(volume)

    def mute(self):
        self.logger.info("Muting")
        self.volume(0)