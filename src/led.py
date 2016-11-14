import RPi.GPIO as GPIO


class Led:

    def __init__(self, red_pin, green_pin, blue_pin):
        self.blue_pin = blue_pin
        self.green_pin = green_pin
        self.red_pin = red_pin

        GPIO.setup(self.red_pin, GPIO.IN)
        GPIO.setup(self.green_pin, GPIO.IN)
        GPIO.setup(self.blue_pin, GPIO.IN)

    def ready(self):
        return
