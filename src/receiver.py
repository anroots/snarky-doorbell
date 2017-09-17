import RPi.GPIO as GPIO

from pi_switch import RCSwitchReceiver


class Receiver:

    def __init__(self, data_pin):
        GPIO.setup(data_pin,GPIO.IN)
        self.data_pin = data_pin


    def test(self):

        receiver = RCSwitchReceiver()
        receiver.enableReceive(self.data_pin)

        num = 0
        print "Listening on pin %s" %self.data_pin
        while True:
            if receiver.available():
                print "Data available"
                received_value = receiver.getReceivedValue()
                if received_value:
                    num += 1
                    print("Received[%s]:" % num)
                    print(received_value)
                    print("%s / %s bit" % (received_value, receiver.getReceivedBitlength()))
                    print("Protocol: %s" % receiver.getReceivedProtocol())
                    print("")

                receiver.resetAvailable()