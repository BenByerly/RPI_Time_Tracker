# main.py

import time
import RPi.GPIO as GPIO
from framebuffer import draw_screen
from button import process_button_events

print("Rendering screen...")
draw_screen()

try:
    while True:
        process_button_events()
        time.sleep(0.01)
except KeyboardInterrupt:
    GPIO.cleanup()
    print("Done.")
