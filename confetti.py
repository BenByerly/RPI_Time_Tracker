import numpy as np
from PIL import Image, ImageDraw
from framebuffer import render_to_image
import time


def draw_confetti_frame(base_img):
    img = base_img.copy()
    draw = ImageDraw.Draw(img)

    # any n of confetti 
    for _ in range(200):
        x = np.random.randint(0, 480)
        y = np.random.randint(0, 320)
        color = tuple(np.random.randint(0, 255, 3))
        size = np.random.randint(4, 10)
        draw.rectangle((x, y, x+size, y+size), fill=color)

    return img

def run_confetti(duration=3.5, fps=20):
    base_image = render_to_image()
    frame_time = 1.0 / fps
    end_time = time.time() + duration

    while time.time() < end_time:
        frame = draw_confetti_frame(base_image)
        push_frame(frame)
        time.sleep(frame_time)


    with open("/dev/fb1", "wb") as f:
        f.write(fb_data)
