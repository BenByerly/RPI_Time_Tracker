# button_test.py
# Simple test to verify wiring on GPIO20

import RPi.GPIO as GPIO
import time

BUTTON_PIN = 20  # BCM numbering

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("Button test started.")
print("Press the button to see output. Ctrl+C to exit.\n")

last_state = GPIO.input(BUTTON_PIN)

try:
    while True:
        state = GPIO.input(BUTTON_PIN)

        if state != last_state:
            if state == 0:
                print("PRESSED (GPIO = LOW)")
            else:
                print("RELEASED (GPIO = HIGH)")

            last_state = state

        time.sleep(0.02)  # debounce sample

except KeyboardInterrupt:
    GPIO.cleanup()
    print("\nExiting test.")
