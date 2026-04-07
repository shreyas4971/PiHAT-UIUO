import RPi.GPIO as	 GPIO
import time

import RPi.GPIO as GPIO
import time

# Your mapping from the photo
outputs = [17, 27, 22, 24, 25, 5, 6, 26]

GPIO.setmode(GPIO.BCM)

for pin in outputs:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

print("8 DO HAT Test Started")

try:
    while True:
        for i, pin in enumerate(outputs):
            print(f"DO{i+1} -> GPIO {pin} ON")
            GPIO.output(pin, GPIO.HIGH)
            time.sleep(1)

            print(f"DO{i+1} -> OFF")
            GPIO.output(pin, GPIO.LOW)
            time.sleep(0.5)

except KeyboardInterrupt:
    print("Stopping test")

finally:
    GPIO.cleanup()
