import os
import random

from encoder import Encoder
from led import Led
from speaker import Speaker
from receiver import Receiver


class Doorbell:

    volume = 10
    voice = 0
    style = 0
    status = 0

    audio_path = '/opt/doorbell/wav/voices'
    status_led = None
    voices = []

    def __init__(self, logger):

        self.logger = logger

    def init(self):
        """
        Initialize the doorbell - set up I/O devices and start listening
        """

        self.logger.debug("Initializing the doorbell")

        # Setup rotary encoders - define which pins they are attached to
        # and set up callback functions that trigger on state changes

        # Volume
        Encoder(17, 4, self.change_volume, 2, self.mute)

        # Voice
        Encoder(22, 23, self.change_voice, 3, self.voice_button)

        # Style
        Encoder(24, 27, self.change_style, 15, self.style_button)

        # RGB PWM LED on those pins for status indication
        self.status_led = Led(12, 18, 13)
        self.status_led.ready()

        # 433 MHz receiver module attached to this pin
        Receiver(10, self.ring)

        # We have a speaker on the 3.5mm RPi audio jack
        self.speaker = Speaker(self.logger, self.volume)

        self.voices = self.list_voices()

    def mute(self, pin):
        self.logger.info("Mute pressed!")
        self.speaker.set_volume(0)
        self.volume = 0

    def change_style(self, direction):
        self.change('style', direction, min=0, max=100, amount=1)
        self.logger.info('Style set to %d', self.style)

    def style_button(self, value):
        self.logger.info("Style button pressed")

    def change_volume(self, direction):
        self.change('volume', direction, min=0, max=100, amount=5)
        self.speaker.set_volume(self.volume)
        self.speaker.say("%s/pluck.wav"%self.audio_path)
        self.logger.info('Volume set to %d', self.volume)

    def voice_button(self, value):
        self.logger.info("Voice button pressed")

    def change(self, attribute, direction, min=0, max=100, amount=1):
        value = getattr(self, attribute)
        newvalue = value + (amount * direction)

        if newvalue > max:

            # Wrap back to the beginning, except for the volume control
            if attribute == "volume":
                newvalue = max
            else:
                newvalue = min

        elif newvalue < min:
            if attribute == "volume":
                newvalue = min
            else:
                newvalue = max

        setattr(self, attribute, newvalue)

    def list_voices(self):
        voices = os.listdir(self.audio_path)
        self.logger.info("Found %d installed voices to use: %s" % (len(voices), voices))
        return voices

    def change_voice(self, direction):

        self.change('voice', direction, min=0, max=len(self.voices)-1, amount=1)

        self.speaker.say("%s/%s/name.wav" % (self.audio_path, self.get_voice_name()))
        self.logger.info('Voice set to %d', self.voice)

    def get_voice_path(self):
        return "%s/%s" % (self.audio_path,self.get_voice_name())

    def get_voice_name(self):
        return self.voices[self.voice]

    def ring(self):

        self.status_led.ringing()

        audio_files = os.listdir(self.get_voice_path())
        candidates = list(set(audio_files) - {"%s.wav" % self.get_voice_name()})

        self.speaker.say("%s/%s" % (self.get_voice_path(), random.choice(candidates)))
        self.status_led.ready()
