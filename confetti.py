import numpy as np
from PIL import Image, ImageDraw
import time
import random



def confetti_frame():
    img = Image.new("RGB", (480, 320), "white")
    draw = ImageDraw.Draw(img)


    # any n of confetti 
    for _ in range(80):
        x = random.randint(0, 479)
        y = random.randint(0, 319)
        color = random.choice(["red", "blue", "green", "yellow", "purple", "orange"])
        draw.rectangle((x, y, x+5, y+5), fill=color)
    return img



def play_confetti_animation(write_fb_callback):
    for _ in range (20):
        img = confetti_frame()
        arr = np.asarray(img, dtype=np.uint8)

        # convert it to RGB 565 
        r = (arr[:,:,0] >> 3).astype(np.uint16)
        g = (arr[:,:,1] >> 2).astype(np.uint16)
        b = (arr[:,:,2] >> 3).astype(np.uint16)
        rgb565 = (r << 11) | (g << 5) | b
        fb_data = rgb565.astype('<u2').tobytes()

        write_fb_callback(fb_data)
        time.sleep(0.05)
