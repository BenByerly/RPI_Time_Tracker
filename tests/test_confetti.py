import time
import random
import numpy as np
from PIL import Image, ImageDraw
import os

FB = "/dev/fb1"
WIDTH = 480
HEIGHT = 320

# background used in main app (set to match yours)
BG_COLOR = "#303030"   # dark gray, change to whatever your main app uses


def push(img):
    """Push image to framebuffer"""
    arr = np.asarray(img, dtype=np.uint8)
    r = (arr[:, :, 0] >> 3).astype(np.uint16)
    g = (arr[:, :, 1] >> 2).astype(np.uint16)
    b = (arr[:, :, 2] >> 3).astype(np.uint16)
    rgb565 = (r << 11) | (g << 5) | b
    fb_data = rgb565.astype("<u2").tobytes()

    with open(FB, "wb") as f:
        f.write(fb_data)


def draw_confetti_frame():
    """Generate one confetti frame"""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # 80 colored squares dropped randomly
    for _ in range(80):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        size = random.randint(6, 16)

        color = random.choice([
            (255, 60, 60),
            (60, 255, 60),
            (60, 160, 255),
            (255, 200, 50),
            (200, 60, 255),
            (255, 120, 0)
        ])

        draw.rectangle((x, y, x + size, y + size), fill=color)

    return img


def main():
    print("🎉 Playing confetti animation...")

    for _ in range(30):     # 30 frames (~3 seconds)
        frame = draw_confetti_frame()
        push(frame)
        time.sleep(0.10)

    print("✨ Animation finished. Restoring blank screen.")

    # restore clean background when animation ends
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    push(img)


if __name__ == "__main__":
    main()
