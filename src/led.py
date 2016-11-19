import RPi.GPIO as GPIO
from time import sleep

class Led:

    def __init__(self, red_pin, green_pin, blue_pin):
        self.blue_pin = blue_pin
        self.green_pin = green_pin
        self.red_pin = red_pin

        GPIO.setup(self.red_pin, GPIO.OUT)
        GPIO.setup(self.green_pin, GPIO.OUT)
        GPIO.setup(self.blue_pin, GPIO.OUT)

        GPIO.output(self.green_pin, 1)
        GPIO.output(self.green_pin, 1)
        GPIO.output(self.green_pin, 1)
    def ready(self):
        sleep(2)
        GPIO.output(self.green_pin, 0)
        sleep(2)
        GPIO.output(self.green_pin, 1)
        GPIO.output(self.red_pin, 0)
        sleep(2)
        GPIO.output(self.red_pin, 1)
        GPIO.output(self.blue_pin, 0)
        sleep(2)
        GPIO.output(self.blue_pin, 1)
        return
