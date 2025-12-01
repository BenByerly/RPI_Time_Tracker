# temp_mark_all.py
# Test script: hold button for 5 seconds → mark ALL entries as crossed.

import time
import RPi.GPIO as GPIO
import sys, os

# ----------------------------------------
# FIX MUST COME BEFORE ANY IMPORTS
# ----------------------------------------
sys.path.append(os.path.abspath(".."))
# Now we can import our modules
from times import crossed, ptr, times
from framebuffer import draw_screen

BUTTON_PIN = 20
DEBOUNCE = 0.05
SUPER_LONG_PRESS = 5.0   # <-- 5 second required hold

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def mark_all_crossed():
    """Mark every time slot as crossed out."""
    global ptr
    for i in range(len(crossed)):
        crossed[i] = True
    ptr = len(crossed)
    draw_screen()
    print("[MARK ALL] Entire schedule crossed out!")

print("Hold button 5 seconds to cross ALL times...")

try:
    while True:
        # Button pressed?
        if GPIO.input(BUTTON_PIN) == 0:
            time.sleep(DEBOUNCE)

            if GPIO.input(BUTTON_PIN) == 0:
                press_start = time.time()

                # Loop while still holding
                while GPIO.input(BUTTON_PIN) == 0:
                    time.sleep(0.05)

                    if time.time() - press_start >= SUPER_LONG_PRESS:
                        mark_all_crossed()
                        # Require button release
                        while GPIO.input(BUTTON_PIN) == 0:
                            time.sleep(0.05)
                        break

        time.sleep(0.01)

except KeyboardInterrupt:
    GPIO.cleanup()
    print("\nExiting temp test.")

