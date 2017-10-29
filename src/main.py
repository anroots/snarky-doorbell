from time import sleep
import logging
import RPi.GPIO as GPIO
import redis

from doorbell import Doorbell


def main():

    GPIO.setwarnings(True)
    GPIO.setmode(GPIO.BCM)

    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    logger.info('Starting up...')

    logger.info('Connecting to Redis DB...')

    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    doorbell = Doorbell(logger, r)
    doorbell.init()

    try:
        while True:
            sleep(.1)

    except KeyboardInterrupt:
        logger.info('Got KeyboardInterrupt, cleaning up GPIO and exiting')
        GPIO.cleanup()
        logger.info('Cleanup done, bye!')


if __name__ == '__main__':
    main()