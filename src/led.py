import RPi.GPIO as GPIO

class Led:

    def __init__(self, red_pin, green_pin, blue_pin):
        self.blue_pin = blue_pin
        self.green_pin = green_pin
        self.red_pin = red_pin

        GPIO.setup(self.red_pin, GPIO.OUT)
        GPIO.setup(self.green_pin, GPIO.OUT)
        GPIO.setup(self.blue_pin, GPIO.OUT)

        self.reset()

    def reset(self):
        GPIO.output(self.green_pin, GPIO.HIGH)
        GPIO.output(self.red_pin, GPIO.HIGH)
        GPIO.output(self.blue_pin, GPIO.HIGH)

    def red(self):
        self.reset()
        GPIO.output(self.red_pin, GPIO.LOW)

    def green(self):
        self.reset()
        GPIO.output(self.green_pin, GPIO.LOW)
    def blue(self):
        self.reset()
        GPIO.output(self.blue_pin,GPIO.LOW)

    def ready(self):
        self.green()

    def ringing(self):
        self.blue()