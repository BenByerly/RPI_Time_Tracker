# framebuffer.py

import numpy as np
import times
from PIL import Image, ImageDraw, ImageFont


def render_base(draw):
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
    big_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 45)

    left_x = 40
    mid_x = 260
    big_x = 380
    y_start = 15
    spacing = 17

    # left column
    y = y_start
    for i, t in enumerate(times.col_1):
        draw.text((left_x, y), t, fill="black", font=font)
        if times.crossed[i]:
            draw.line((left_x, y+10, left_x+60, y+10), fill="white", width=2)
        y += spacing

    # mid column
    y = y_start
    for j, t in enumerate(times.col_2):
        idx = j + len(times.col_1)
        draw.text((mid_x, y), t, fill="black", font=font)
        if times.crossed[idx]:
            draw.line((mid_x, y+10, mid_x+60, y+10), fill="white", width=2)
        y += spacing

    # 4 PM
    draw.text((big_x - 40, 120), "4:00!!", fill="black", font=big_font)
    if times.strike_fourpm:
        draw.line((big_x - 45, 150, big_x + 90, 150), fill="white", width=4)



def draw_screen():
    """Render & push UI to framebuffer."""
    img = render_to_image()
    arr = np.asarray(img, dtype=np.uint8)

    r = (arr[:, :, 0] >> 3).astype(np.uint16)
    g = (arr[:, :, 1] >> 2).astype(np.uint16)
    b = (arr[:, :, 2] >> 3).astype(np.uint16)
    rgb565 = (r << 11) | (g << 5) | b
    fb_data = rgb565.astype("<u2").tobytes()

    with open("/dev/fb1", "wb") as f:
        f.write(fb_data)

def render_to_image():
    """Return the current screen as a PIL image (NO framebuffer write)."""
    img = Image.new("RGB", (480, 320), "#00FFFF")
    draw = ImageDraw.Draw(img)
    render_base(draw)
    return img
