from PIL import Image, ImageDraw, ImageFont
import numpy as np

img = Image.new("RGB", (480, 320), "white")
draw = ImageDraw.Draw(img)
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)

# test markers
draw.text((10, 10),  "LEFT",  fill="black", font=font)
draw.text((150, 10), "MID",   fill="black", font=font)
draw.text((250, 10), "RIGHT", fill="black", font=font)
draw.text((300, 10), "X300",  fill="black", font=font)
draw.text((350, 10), "X350",  fill="black", font=font)
draw.text((400, 10), "X400",  fill="black", font=font)

arr = np.asarray(img, dtype=np.uint8)
r = (arr[:,:,0] >> 3).astype(np.uint16)
g = (arr[:,:,1] >> 2).astype(np.uint16)
b = (arr[:,:,2] >> 3).astype(np.uint16)
rgb565 = (r << 11) | (g << 5) | b
fb_data = rgb565.astype('<u2').tobytes()

with open("/dev/fb1", "wb") as f:
    f.write(fb_data)
