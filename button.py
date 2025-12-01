# button.py

import time
import RPi.GPIO as GPIO

from times import crossed, ptr, col_1, col_2, times
from framebuffer import draw_screen

# BCM layout
BUTTON_PIN = 20

DEBOUNCE = 0.05
DOUBLE_CLICK_TIME = 0.50
LONG_PRESS_TIME = 1.2

last_press_time = 0
press_start_time = 0
click_count = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# ========================================
#     each function has a global ptr init
# ========================================


# cross out next time
def cross_next():
    global ptr
    if ptr < len(crossed):
        crossed[ptr] = True
        ptr += 1
        draw_screen()
        print(f"[CROSS] {times[ptr-1]}")
    else:
        print("[CROSS] All done")

# double click to undo
def undo_last():
    global ptr
    if ptr > 0:
        ptr -=1
        crossed[ptr] = False
        draw_screen()
        print(f"[UNDO] {times[ptr]}")
    else:
        print("[UNDO] Nothing to undo")

def reset_all():
    global ptr
    for i in range(len(crossed)):
        crossed[i] = False
    ptr = 0
    draw_screen()
    print("[RESET] All cleared")

def process_button_events():
    # detects the actual clicks: single click, double click, and long press
    global last_press_time, press_start_time, click_count

    state = GPIO.input(BUTTON_PIN)

    if state == 0:
        time.sleep(DEBOUNCE)
        if GPIO.input(BUTTON_PIN) == 0:
            press_start_time = time.time()

            # wait for the release
            while GPIO.input(BUTTON_PIN) == 0:
                time.sleep(0.01)

            press_time = time.time() - press_start_time

            # long press
            if press_time >= LONG_PRESS_TIME:
                reset_all()
                click_count = 0
                return

            # reg click
            now = time.time()
            if now - last_press_time <= DOUBLE_CLICK_TIME:
                click_count += 1
            else:
                click_count = 1

            last_press_time = now

            # double click
            if click_count == 2:
                undo_last()
                click_count = 0
            else:
                # delay to check it wasnt a double click
                time.sleep(DOUBLE_CLICK_TIME)
                if click_count == 1:
                    cross_next()
                    click_count = 0
