# framebuffer.py

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from times import col_1, col_2, crossed

def draw_screen():
    img = Image.new("RGB", (480, 320), "#00FFFF")
    draw = ImageDraw.Draw(img)

    # small fonts for other times.
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
    # big font for 4 pm
    big_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 45)

    # column layout
    left_x = 40
    mid_x = 260
    big_x = 380

    y_start = 15
    spacing = 17

    # draw left column
    y = y_start
    for i, t in enumerate(col_1):
        draw.text((left_x, y), t, fill="black", font=font)
        if crossed[i]:
            draw.line((left_x, y+10, left_x+60, y+10), fill="red", width=2)
        y += spacing


    # draw mid column
    y = y_start
    for j, t in enumerate(col_2):
        idx = j + len(col_1)
        draw.text((mid_x, y), t, fill="black", font=font)
        if crossed[idx]:
            draw.line((mid_x, y+10, mid_x+60, y+10), fill="red", width=2)
        y += spacing

    # big font
    draw.text((big_x - 40, 120), "4:00!!", fill="black", font=big_font)


    # convert it to numpy
    arr = np.asarray(img, dtype=np.uint8)
    # Convert RGB888 → RGB565
    r = (arr[:,:,0] >> 3).astype(np.uint16)
    g = (arr[:,:,1] >> 2).astype(np.uint16)
    b = (arr[:,:,2] >> 3).astype(np.uint16)
    rgb565 = (r << 11) | (g << 5) | b

    # Convert to bytes (little endian)
    fb_data = rgb565.astype('<u2').tobytes()

    with open("/dev/fb1", "wb") as f:
        f.write(fb_data)
