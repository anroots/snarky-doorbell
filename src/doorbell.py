from encoder import Encoder
from led import Led
from speaker import Speaker
from receiver import Receiver


class Doorbell:
    volume = 100
    voice = 1
    style = 1
    status = 1

    def __init__(self, logger):

        self.logger = logger

    def startup(self):
        volume_encoder = Encoder(17, 4, self.change_volume, 2, self.mute)
        voice_encoder = Encoder(22, 23, self.change_voice, 3, self.voice_button)
        style_encoder = Encoder(15, 27, self.change_style, 14, self.style_button)

        status_led = Led(12, 13, 18)

        receiver = Receiver(10)
        receiver.test()

        self.speaker = Speaker(self.logger)
        self.speaker.volume(self.volume)
        #self.speaker.say('/opt/doorbell/wav/test2.wav')

    def mute(self, button):
        self.logger.info("Mute pressed!")
        self.speaker.mute()

    def change_style(self, direction):
        self.change('style', direction, min=0, max=100, amount=1)

        self.logger.info('Style set to %d', self.style)


    def style_button(self, value):
        self.logger.info("Style button pressed")

    def change_volume(self, direction):
        self.change('volume', direction, min=0, max=100, amount=5)
        self.speaker.volume(self.volume)
        self.logger.info('Volume set to %d', self.volume)

    def voice_button(self, value):
        self.logger.info("Voice button pressed")


    def change(self, attribute, direction, min=0, max=100, amount=1):
        value = getattr(self, attribute)
        newvalue = value + (amount * direction)

        if (newvalue > max):
            newvalue = max
        elif (newvalue < min):
            newvalue = min

        setattr(self, attribute, newvalue)

    def change_voice(self, direction):

        self.change('voice', direction, min=0, max=100, amount=1)
        self.speaker.say('example.wav')

        self.logger.info('Voice set to %d', self.voice)

