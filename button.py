# button.py
''' Handles all the button logic for 
        - single click -> cross out next line
        - double click -> undo last crossed line
        - long press   -> undo all 
    Uses a state machine to prevent oopsies

'''

import time
import RPi.GPIO as GPIO

# shared states from all modules
from times import crossed, ptr, col_1, col_2, times
from framebuffer import draw_screen

# BCM layout
BUTTON_PIN = 20

# ==============================
# GPIO + timing configs
# ==============================

DEBOUNCE = 0.05               # delay to avoid singal noise
DOUBLE_CLICK_TIME = 0.50      # max time between clicks to count as a double
LONG_PRESS_TIME = 1.2         # minimum time I found to be the best to reset all strikes

# state vars
click_pending = False         # true when the sys is waiting for a second click
first_click_time= 0           # time stamp of first click
press_start_time = 0          # when the button was pressed first this is used in long press detection
ignore_until_release = False  # blocks all click login after a long press, fixes the clear into immediate strike bug


# wired to pull low when pressed so need to enable the pull up register
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) 



# ========================================
#     each function has a global ptr init
# ========================================

# cross out next time
def cross_next():
    global ptr
    if ptr < len(crossed):
        crossed[ptr] = True               # mark the time as crossed out
        ptr += 1                          # move ptr forwards
        draw_screen()                     # update the display
        print(f"[CROSS] {times[ptr-1]}")
    else:
        print("[CROSS] All done")



# double click to undo
def undo_last():
    global ptr
    if ptr > 0:
        ptr -=1                           # move ptr backwards
        crossed[ptr] = False              # un cross the line 
        draw_screen()                     # update display
        print(f"[UNDO] {times[ptr]}")
    else:
        print("[UNDO] Nothing to undo")



def reset_all():
    global ptr
    for i in range(len(crossed)):
        crossed[i] = False                # uncross all times
    ptr = 0                               # reset ptr to first value
    draw_screen()                         # update display
    print("[RESET] All cleared")



# ===================================
#      processess the buttons events
#      ( hurt my brain )
# ===================================

# this function runs constantly inside the main loop it will detect: singe, double and long clicks
def process_button_events():
    # detects the actual clicks: single click, double click, and long press
    global click_pending, first_click_time, press_start_time
    global ignore_until_release, ptr

    # is button released
    if ignore_until_release:
        if GPIO.input(BUTTON_PIN) == 1:
            ignore_until_release = False         # enables logic again
        return


    now = time.time()                            # sets current time for calc later
    state = GPIO.input(BUTTON_PIN)

    
    # safetey check to prevent edge cases
    if click_pending and first_click_time == 0:
        click_pending = False

    # if button is pressed (low)
    if state == 0:
        time.sleep(DEBOUNCE)                     # stabilize 

    
    ''' button pressed logic starts here '''

    if GPIO.input(BUTTON_PIN) == 0:
        press_start_time = now                   # start timing the press

        while GPIO.input(BUTTON_PIN) == 0:       # keep looping while the button is being help
            time.sleep(0.01)

            # long press is detected
            if time.time() - press_start_time >= LONG_PRESS_TIME:
                reset_all()
                click_pending = False            # clear any click waiting state
                first_click_time = 0
                ignore_until_release = True      # block all actions until it is released
                return

        # short press check on button release
        if not click_pending:
            click_pending = True                 # this is first click then start timer for possible double click
            first_click_time = time.time()
        else:
            undo_last()                          # this is second click 
            click_pending = False
            return

    # handle single click after a timeout
    if click_pending and (now - first_click_time >= DOUBLE_CLICK_TIME):
        cross_next()            # single click confirmed
        click_pending = False
        first_click_time = 0



