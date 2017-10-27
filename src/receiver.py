import RPi.GPIO as GPIO

class Receiver:

    data_pin = None
    trigger_callback = None

    def __init__(self, data_pin, trigger_callback):
        GPIO.setup(data_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        GPIO.add_event_detect(data_pin, GPIO.RISING, callback=self.on_receive, bouncetime=50)
        self.data_pin = data_pin
        self.trigger_callback = trigger_callback

    def on_receive(self, pin):
        print "Received from %s" %pin
        self.trigger_callback()