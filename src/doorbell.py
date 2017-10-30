import json
import os
import random
from time import sleep, strftime, time

from encoder import Encoder
from led import Led
from speaker import Speaker
from receiver import Receiver


class Doorbell:

    initial_delay = 1

    audio_path = '/opt/doorbell/wav/voices'
    log_path = '/opt/doorbell/logs'

    status_led = None
    voices = []
    settings = [
        {'key': 'language', 'min':0, 'max':1},
        {'key': 'switch_voice_randomly', 'min': 0, 'max': 1}
    ]

    redis = None  # type: redis

    def __init__(self, logger, redis):

        self.logger = logger
        self.redis = redis

    def init(self):
        """
        Initialize the doorbell - set up I/O devices and start listening
        """

        self.logger.debug("Initializing the doorbell")

        # Setup rotary encoders - define which pins they are attached to
        # and set up callback functions that trigger on state changes

        # Volume
        Encoder(24, 27, self.change_volume, 15, self.mute)

        # Voice
        Encoder(22, 23, self.change_voice, 3, self.voice_button)

        # Setting
        Encoder(17, 4, self.change_setting, 2, self.setting_button)

        # RGB PWM LED on those pins for status indication
        self.status_led = Led(12, 18, 13)
        self.status_led.ready()

        # 433 MHz receiver module attached to this pin
        Receiver(10, self.ring)

        # We have a speaker on the 3.5mm RPi audio jack
        self.speaker = Speaker(self.logger)

        self.voices = self.list_voices()

        self.init_config()

        self.logger.debug("Init done, will wait for I/O interrupts...")

    def mute(self, pin):
        self.logger.debug("Mute pressed!")
        self.redis.set('volume', 0)

    def get_setting_index(self):
        return int(self.redis.get('setting_index'))

    def get_voice(self):
        return int(self.redis.get('voice'))

    def get_volume(self):
        return int(self.redis.get('volume'))

    def change_setting(self, direction):
        self.change('setting_index', direction, min=0, max=len(self.settings)-1, amount=1)

    def setting_button(self, value):
        setting = self.settings[self.get_setting_index()]
        self.change(setting['key'], 1, setting['min'], setting['max'])

    def change_volume(self, direction):
        self.change('volume', direction, min=0, max=100, amount=5)
        self.speaker.say("%s/volume.wav" % self.audio_path, self.get_volume())

    def voice_button(self, value):
        self.status_led.red()
        self.logger.info("Shutdown button pressed, shutting down...")
        os.system("sudo shutdown -h now")

    def change(self, attribute, direction, min=0, max=100, amount=1):
        value = int(self.redis.get(attribute))
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

        self.logger.debug('%s set to %d', attribute, newvalue)
        self.redis.set(attribute, newvalue)

    def list_voices(self):
        voices = [name for name in os.listdir(self.audio_path) if os.path.isdir(os.path.join(self.audio_path, name))]
        self.logger.info("Found %d installed voices to use: %s" % (len(voices), voices))
        return voices

    def change_voice(self, direction):
        self.change('voice', direction, min=0, max=len(self.voices)-1, amount=1)
        self.speaker.say("%s/%s/name.wav" % (self.audio_path, self.get_voice_name()), self.get_volume())

    def get_voice_path(self):
        return "%s/%s" % (self.audio_path,self.get_voice_name())

    def get_voice_name(self):
        return self.voices[self.get_voice()]

    def log_ring(self, audio_file, volume):
        """
        Save log about the ring event to the JSON log file
        :param audio_file: Full path to an audio file that was played
        :param volume: Volume of the ring
        :return:
        """

        # Log files are rotated on a monthly basis
        log_file = "%s/%s.json" % (self.log_path, strftime("%Y-%m"))

        # Create the log file if it doesn't exist
        if not os.path.isfile(log_file):
            with open(log_file, mode='w') as f:
                json.dump([], f)

        # Append a new entry to the log file-s JSON array
        with open(log_file, mode='r') as ring_logs:
            feeds = json.load(ring_logs)

        with open(log_file, mode='w') as ring_logs:
            entry = {'time': time(), 'audio_file': audio_file, 'volume': volume}
            feeds.append(entry)
            json.dump(feeds, ring_logs)

        # Increment stats counters in Redis
        self.redis.set('total_rings', int(self.redis.get('total_rings'))+1)
        self.redis.set('rings_since_boot', int(self.redis.get('rings_since_boot'))+1)
        self.redis.set('last_ring', time())

    def ring(self):
        """
        Ring the doorbell

        Triggered when the "test" button is pressed or if the Receiver picks up
        an actual radio transmission from the real doorbell button
        :return:
        """
        self.status_led.ringing()

        # Wait for the "real" doorbell to do it's "ding-dong" sound
        sleep(self.initial_delay)

        # Select an audio file to play
        audio_files = os.listdir(self.get_voice_path())
        candidates = list(set(audio_files) - {"%s.wav" % self.get_voice_name()})
        audio_file = "%s/%s" % (self.get_voice_path(), random.choice(candidates))

        self.speaker.say(audio_file, self.get_volume())
        self.log_ring(audio_file, self.get_volume())

        # Pseudo polling: keep the status light active for some seconds after
        # the doorbell has rung. A better implementation would hook into
        # pygame's event system and trigger LED change when the sound actually finishes
        # playing (and would be non-blocking)
        sleep(2)

        self.status_led.ready()

    def init_config(self):
        """
        Set configuration keys to default values in Redis, if they do not exist
        :return:
        """
        self.redis.set('rings_since_boot', 0)

        for key in ['volume', 'setting_index', 'voice', 'total_rings', 'last_ring']:
            if self.redis.get(key) is None:
                self.redis.set(key, 0)

        for setting in self.settings:
            if self.redis.get(setting['key']) is None:
                self.redis.set(setting['key'], 0)