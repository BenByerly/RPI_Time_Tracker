from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os

times = [
    # first column
    "7:30",  "7:45",
    "8:00", "8:15", "8:30", "8:45",
    "9:00", "9:15", "9:30", "9:45",
    "10:00", "10:15","10:30", "10:45",
    "11:00", "11:15", "11:30",


    # second column
    "11:45",
    "12:00", "12:15", "12:30", "12:45",
    "1:00", "1:15", "1:30", "1:45",
    "2:00", "2:15", "2:30", "2:45",
    "3:00", "3:15", "3:30", "3:45",
]

mid = len(times)//2
col_1 = times[:mid]
col_2 = times[mid:]

crossed = [False] * len(times)



def draw_screen():
    img = Image.new("RGB", (480, 320), "white")
    draw = ImageDraw.Draw(img)

    # small fonts for other times.
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)

    # big font for 4 pm
    big_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 45)


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




draw_screen()
