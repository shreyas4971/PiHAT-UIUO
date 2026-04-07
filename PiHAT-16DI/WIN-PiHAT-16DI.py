import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

di_pins = {
    "DI1": 17,
    "DI2": 27,
    "DI3": 23,
    "DI4": 22,
    "DI5": 24,
    "DI6": 25,
    "DI7": 7,
    "DI8": 5,
    "DI9": 12,
    "DI10": 6,
    "DI11": 13,
    "DI12": 16,
    "DI13": 19,
    "DI14": 26,
    "DI15": 20,
    "DI16": 21
}

# Setup GPIOs as INPUT with pull-up (important for active-LOW)
for pin in di_pins.values():
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("DI input monitoring started (12V = ON)")
print("------------------------------------")

try:
    while True:
        any_on = False

        for di, pin in di_pins.items():
            state = GPIO.input(pin)

            if state == GPIO.LOW:   # 12V applied
                print(f"{di} is ON")
                any_on = True
            else:
                print(f"{di} is OFF")

        if not any_on:
            print("No DI is ON")

        print("------------------------------------")
        time.sleep(0.5)

except KeyboardInterrupt:
    print("Stopped by user")

finally:
    GPIO.cleanup()

