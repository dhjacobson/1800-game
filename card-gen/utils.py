from PIL import Image, ImageOps
from PIL import ImageFont
from PIL import ImageDraw
import numpy as np
import math
import json


def wrap_text(text, width, font):
    text_lines = []
    text_line = []
    text = text.replace('\n', ' [br] ')
    words = text.split()

    for word in words:
        if word == '[br]':
            text_lines.append(' '.join(text_line))
            text_line = []
            continue
        text_line.append(word)
        w, h = font.getsize(' '.join(text_line))
        if w > width:
            text_line.pop()
            text_lines.append(' '.join(text_line))
            text_line = [word]

    if len(text_line) > 0:
        text_lines.append(' '.join(text_line))

    return text_lines


# w and h represent the *interior* width and height
def box(w, h, outline_color=(50, 50, 50), fill_color=(250, 250, 250), outline_width=13):
    img = Image.new("RGB", (w + 2*outline_width, h + 2*outline_width))
    draw = ImageDraw.Draw(img)

    outline_colors = np.linspace(outline_color, fill_color, outline_width)
    for i, color in enumerate(outline_colors):
        draw.rectangle([i, i, w + 2*outline_width - i, h + 2*outline_width - i],
                       fill=fill_color, outline=tuple(int(c) for c in color))
    return img


def img_in_box(img, margin=10, outline_width=13, **box_params):
    w, h = img.size
    bimg = box(w+margin*2, h+margin*2, outline_width=outline_width, **box_params)

    bimg.paste(img, box=(outline_width + margin, outline_width + margin), mask=img)
    return bimg


def crop_to_content(img):
    imageBox = img.getbbox()
    return img.crop(imageBox)