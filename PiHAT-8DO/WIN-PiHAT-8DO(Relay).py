import RPi.GPIO as GPIO
import time

# BCM GPIO numbers
DO_PINS = [17, 27, 22, 24, 25, 5, 6, 26]

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Setup pins
for pin in DO_PINS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)   # ensure OFF

try:
    while True:
        for pin in DO_PINS:
            GPIO.output(pin, GPIO.HIGH)
            time.sleep(1.0)
            GPIO.output(pin, GPIO.LOW)

        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()
