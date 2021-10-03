from PIL import Image, ImageOps
from PIL import ImageFont
from PIL import ImageDraw
import numpy as np
import math
import json


def lighten(color, factor):
    return tuple((255 - factor * (255 - np.array(color))).astype(int))


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


def pad_and_paste(img, pasted_img, box=(0, 0), align='center', vertical_align='top'):
    aw, ah = pasted_img.size
    iw, ih = img.size
    x, y = box

    if x < 0:
        img = ImageOps.pad(img, (iw - x, ih), centering=(1, 0))
        iw, ih = img.size
        x = 0
    if y < 0:
        img = ImageOps.pad(img, (iw, ih - y), color=(0, 0, 0), centering=(0, 1))
        iw, ih = img.size
        y = 0
    if x + aw > iw:
        img = ImageOps.pad(img, (x + aw, ih), centering=(0, 0))
        iw, ih = img.size
    if y + ah > ih:
        img = ImageOps.pad(img, (iw, y + ah), centering=(0, 0))
        iw, ih = img.size

    if align == 'center':
        x = int((iw - aw) / 2)
    if vertical_align == 'center':
        y = int((ih - ah) / 2)
    paste_mask = pasted_img.convert('RGBA').split()[3].point(lambda a: a * 1.0)

    img.paste(pasted_img, box=(x, y), mask=paste_mask)
    return img


def stack_image_xy(img, xy, spacer=0):
    x, y = xy
    w = img.width + spacer
    h = img.height + spacer
    new_img = Image.new('RGBA', (x*w - spacer, y*h - spacer))
    for i in range(x):
        for j in range(y):
            new_img.paste(img, (i*w, j*h))

    return new_img