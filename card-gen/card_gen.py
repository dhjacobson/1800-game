from PIL import Image, ImageOps
from PIL import ImageFont
from PIL import ImageDraw
import numpy as np
import math
import json
import re
from utils import *


class Card:
    def __init__(self, title, flavor_image=None, corner_icon=None, margin=40, component_spacer=60, **excess_args):

        self.width = 825
        self.height = 1125
        self.component_spacer = component_spacer
        self.margin = margin
        self.border_color = (250, 250, 250)
        self.border_width = 40

        self.background_color = (250, 250, 250)

        self.title = title
        self.components = []
        self.component_layout = 'vertical_stack'

        self.flavor_image_component = None
        if flavor_image:
            self.flavor_image_component = FlavorImageComponent(**flavor_image)

        self.corner_icon_component = None
        if corner_icon:
            self.corner_icon_component = ImageComponent(**corner_icon)

    def add(self, component):
        self.components.append(component)

    def gen_card(self, fname, show=False):
        img = Image.new(mode='RGBA', size=(self.width - 2*self.border_width, self.height - 2*self.border_width), color=self.background_color)
        # interior = BoxComponent(self.background_color, outline_color=self.background_color, outline_width=1)
        # interior.build(self.width-self.border_width, self.height - self.border_width)
        # interior.draw(img, (self.border_width, self.border_width))
        draw = ImageDraw.Draw(img)

        # border = BoxComponent(self.background_color, outline_color=self.border_color, outline_width=self.border_width)
        # border.build(self.width-self.border_width, self.height - self.border_height)
        # border.draw(img, (0, 0))

        xcursor = self.margin
        ycursor = self.margin

        # flavor image
        if self.flavor_image_component is not None:
            img = self.flavor_image_component.draw(img)

        # corner icon
        if self.corner_icon_component is not None:
            img = self.corner_icon_component.draw(img, ())

        # title
        # font = ImageFont.truetype("fonts/Candarab.ttf", 56)
        # w, h = img.size
        # textw, texth = draw.textsize(self.title, font=font)
        # # draw.text((w/2 - textw/2, self.margin), self.title, fill=(0, 0, 0), font=font)
        # draw.text((self.margin, self.margin), self.title, fill=(0, 0, 0), font=font)
        # ycursor += self.margin + texth
        # ycursor += self.component_spacer

        # components
        for component in self.components:
            if isinstance(component, DevPaymentRewardComponent):
                img = component.draw(img, (self.margin, self.margin), align='left')
                xcursor += component.width
            else:
                img = component.draw(img, (xcursor, ycursor))
                cw, ch = component.cursor_shift()
                if self.component_layout == 'vertical_stack':
                    ycursor += ch + self.component_spacer

        new_size = (self.width, self.height)
        new_img = Image.new("RGB", new_size, color=self.border_color)
        new_img.paste(img, (self.border_width, self.border_width))

        # save
        if show:
            new_img.show()
        new_img.save(fname)


class CardComponent:

    def __init__(self, wmax=99999, hmax=99999, component_type=None, **generic):
        self.wmax = wmax
        self.hmax = hmax
        self.component_type = component_type
        self.generic = generic

        self.img = None

    @staticmethod
    def from_dict(d):
        if 'component_type' in d.keys():
            ctype = d['component_type']
            if ctype == 'payment-reward':
                return DevPaymentRewardComponent(**d)
            elif ctype == 'text-box':
                return TextBoxComponent(**d)
            elif ctype == 'image-box':
                return ImageBoxComponent(**d)
            elif ctype == 'flavor-image':
                return FlavorImageComponent(**d)
            elif ctype == 'resources':
                return ResourcesComponent(**d)
            else:
                raise ValueError(f'Invalid component_type: {ctype}')

        # if the type isn't given, infer it from the dict keys
        else:
            if 'resources' in d.keys():
                return ResourcesComponent(**d)
            elif 'text' in d.keys():
                return TextBoxComponent(**d)
            elif 'arrow' in d.keys():
                return ArrowImageComponent(**d)
            elif 'img_fpath' in d.keys():
                return ImageBoxComponent(**d)
            else:
                raise ValueError(f'Component type was not provided, and could not be inferred from keys: {d.keys()}')

    def build(self, wmax, hmax):
        pass

    def draw2(self, img, from_left=None, from_top=None, from_right=None, from_bottom=None):
        x, y = (0, 0)
        if from_left == 'center':
            x = img.width//2 - self.img.width//2
        elif from_left is not None:
            x = from_left
        elif from_right is not None:
            x = img.width - self.img.width - from_right
        if from_top == 'center':
            y = img.height//2 - self.img.height//2
        elif from_top is not None:
            y = from_top
        elif from_bottom is not None:
            y = img.height - self.img.height - from_bottom

        self.draw(img, xy=(x, y), align='left')

    def draw(self, img, xy=(0, 0), align='center', vertical_align='top', margin=0, rebuild=False):
        x, y = xy

        iw, ih = img.size
        if self.img is None or rebuild:
            wmax = min(self.wmax, iw - 2*x - 2*margin)
            hmax = min(self.hmax, ih - y - margin)
            self.build(wmax, hmax)
        self.img = crop_to_content(self.img)

        x_pcs, y_pcs = self.precursor_shift()
        x += x_pcs
        y += y_pcs

        aw, ah = self.img.size

        if x < 0:
            img = ImageOps.pad(img, (iw-x, ih), centering=(1, 0))
            iw, ih = img.size
            x = 0
        if y < 0:
            img = ImageOps.pad(img, (iw, ih-y), centering=(0, 1))
            iw, ih = img.size
            y = 0
        if x + aw > iw:
            img = ImageOps.pad(img, (x+aw, ih), centering=(0, 0))
            iw, ih = img.size
        if y + ah > ih:
            img = ImageOps.pad(img, (iw, y+ah), centering=(0, 0))
            iw, ih = img.size

        if align == 'center':
            x = int((iw - aw) / 2)
        if vertical_align == 'center':
            y = int((ih - ah) / 2)
        paste_mask = self.img.convert('RGBA').split()[3].point(lambda a: a * 1.0)

        # self.img = self.img.convert('RGBA')
        # data = self.img.load()
        # for i in range(self.img.width):
        #     for j in range(self.img.height):
        #         r, g, b, a = data[i, j]
        #         data[i, j] = (r, g, b, round(a*0.9))

        img.paste(self.img, box=(x, y), mask=paste_mask)

        return img

    def precursor_shift(self):
        return 0, 0

    def cursor_shift(self):
        return self.img.size


class TitleComponent:
    pass


class FlavorImageComponent(CardComponent):
    def __init__(self, fpath, shift_down=0, min_lightness=180, crop=True, scale_vert=None, overflow=False, **generic):
        CardComponent.__init__(self, **generic)
        self.fpath = fpath
        self.min_lightness = min_lightness
        self.crop = crop
        self.transparent_color = (255, 255, 255)
        self.shift_down = shift_down
        self.scale_vert = scale_vert
        self.overflow = overflow

    def build(self, wmax=99999, hmax=99999):
        self.img = Image.new('RGBA', (wmax, hmax), color=(255, 255, 255, 100))

        fimg = Image.open(self.fpath)
        fimg = ImageOps.grayscale(fimg).convert('RGBA')

        fw, fh = fimg.size
        if self.scale_vert:
            fh = int(fh * self.scale_vert)
            fimg = fimg.resize((fw, fh), Image.ANTIALIAS)
        fimg_data = fimg.load()

        lightening_factor = min(1, (255 - self.min_lightness) / (
                    255 - min([fimg_data[i, j][0] for j in range(fh) for i in range(fw)])))

        # convert transparent_color to transparent and lighten, if necessary
        for i in range(fw):
            for j in range(fh):
                r, g, b, a = fimg_data[i, j]
                if (r, g, b) == (255, 255, 255):
                    fimg_data[i, j] = (255, 255, 255, 0)
                else:
                    new_rgb = int(255 - lightening_factor * (255 - r))
                    fimg_data[i, j] = (new_rgb, new_rgb, new_rgb, a)

        # crop
        if self.crop:
            fimg = crop_to_content(fimg)

        # resize
        iw = wmax
        ih = hmax - self.shift_down
        if self.overflow:
            w = max(iw, math.floor(fw / fh * ih))
            h = max(ih, math.floor(fh / fw * iw))
        else:
            w = min(iw, math.floor(fw / fh * ih))
            h = min(ih, math.floor(fh / fw * iw))
        fimg = fimg.resize((w, h), Image.ANTIALIAS)

        # draw
        self.img.paste(fimg, (0, self.shift_down))


class FullDevCardComponent(CardComponent):

    def __init__(self, title, icon, text=None, paymentreward=None, spacer=60, title_height=160, color1=(255, 255, 255), color2=(0, 0, 0), **generic):
        CardComponent.__init__(self, **generic)
        self.title = DevTitleComponent(title, icon, fill_color=color2, outline_color=lighten(color2, 0.60), **generic)
        self.paymentreward = DevPaymentRewardComponent(**paymentreward)
        self.spacer = spacer
        self.title_height = title_height
        self.textbox = TextBoxComponent(text, fill_color=lighten(color2, 0.15) + (170, ), outline_color=color2 + (170, ), text_color=color2, default_font_size=42, margin=22, shrink_to_fit=False) if text is not None else None

    def build(self, wmax=99999, hmax=99999):
        self.img = Image.new("RGBA", (wmax, hmax))

        self.paymentreward.build(wmax, hmax)
        self.paymentreward.draw(self.img, (0, 0), align='left')

        self.title.build(wmax - self.paymentreward.width - self.spacer - 2*self.title.outline_width, self.title_height)
        self.title.draw(self.img, (self.paymentreward.width + self.spacer, 0), align='left')

        if self.textbox is not None:
            self.textbox.build(wmax - self.paymentreward.width - self.spacer - 2*self.textbox.outline_width, hmax - self.title.img.height - self.paymentreward.width - 2 * self.spacer - 2*self.textbox.outline_width)
            self.textbox.draw2(self.img, from_left=self.paymentreward.width + self.spacer, from_top=self.title.img.height + self.spacer)


class DevPaymentRewardComponent(CardComponent):

    def __init__(self, payment, reward, activation=None, location=0, width=125, arrow_width=50, arrow_head_width=120, elbow_radius=90, spacer=30, arrow_color=(20, 20, 20, 220), activation_size=120, **generic):
        CardComponent.__init__(self, **generic)
        # self.payment = payment

        if isinstance(payment, str):
            self.payment = ResourcesComponent(payment, **self.generic, resource_max_rows=len(payment))
        else:
            self.payment = CardComponent.from_dict({**self.generic, **payment})

        if isinstance(reward, str):
            self.reward = ImageComponent(reward, **{'margin': 10, 'monochrome': (50, 50, 50), **self.generic})
        else:
            self.reward = CardComponent.from_dict({**self.generic, **reward})

        self.activation = ImageBoxComponent(f'icons/{activation}.png', shape='circle', margin=4, outline_width=9, **self.generic) if activation else None
        self.activation_size = activation_size

        self.location = location
        self.width = width
        self.arrow_width = arrow_width
        self.arrow_head_width = arrow_head_width
        self.elbow_radius = elbow_radius
        self.arrow_color = arrow_color
        self.spacer = spacer

    def build(self, wmax=99999, hmax=99999):
        self.img = Image.new("RGBA", (wmax, hmax))
        draw = ImageDraw.Draw(self.img)

        # draw reward
        self.reward.build(wmax//2, self.width)
        self.reward.draw2(self.img, from_bottom=0, from_right=0)

        # draw arrow
        arrow_head_base = (wmax - self.reward.img.width - self.spacer - self.arrow_head_width*2//3, hmax-self.width//2)
        arrow_head_tip = (wmax - self.reward.img.width - self.spacer, hmax-self.width//2)
        draw.line([(self.width//2, 0), (self.width//2, hmax-self.width//2-self.elbow_radius+self.arrow_width//2)], fill=self.arrow_color, width=self.arrow_width)
        draw.arc([(self.width//2-self.arrow_width//2, hmax-self.width//2-2*self.elbow_radius), (self.width//2+2*self.elbow_radius, hmax-self.width//2+self.arrow_width//2)], start=90, end=180, fill=self.arrow_color, width=self.arrow_width)
        draw.line([(self.width//2+self.elbow_radius-self.arrow_width//2, hmax-self.width//2), arrow_head_base], fill=self.arrow_color, width=self.arrow_width)
        draw.polygon([(arrow_head_base[0], arrow_head_base[1] - self.arrow_head_width//2), (arrow_head_base[0], arrow_head_base[1] + self.arrow_head_width//2), (arrow_head_tip)], fill=self.arrow_color)

        # draw payment
        self.payment.build(wmax, hmax)
        self.payment.draw(self.img, (self.width//2 - self.payment.img.width//2, 0), align='left')

        # draw activation
        if self.activation is not None:
            self.activation.build(int(self.width*2/np.sqrt(2)), int(self.width*2//np.sqrt(2)))
            self.activation.draw2(self.img, from_bottom=0)


class BoxComponent(CardComponent):

    def __init__(self, fill_color=(250, 250, 250), outline_color=(50, 50, 50), outline_width=13, shape='rectangle', border_fade=True, **generic):
        CardComponent.__init__(self, **generic)
        self.fill_color = fill_color
        self.outline_width = outline_width
        self.outline_color = outline_color
        self.border_fade = border_fade
        self.shape = shape

    def build(self, wmax=99999, hmax=99999):
        img = Image.new("RGBA", (wmax + 2*self.outline_width, hmax + 2*self.outline_width))
        draw = ImageDraw.Draw(img)

        if len(self.fill_color) == 4 and len(self.outline_color) == 3:
            self.outline_color += (self.fill_color[3], )
        outline_colors = np.linspace(self.outline_color, self.fill_color, self.outline_width)
        if not self.border_fade:
            outline_colors = [self.outline_color]*self.outline_width
        for i, color in enumerate(outline_colors):
            bbox = [i, i, wmax + 2*self.outline_width - i, hmax + 2*self.outline_width - i]
            if self.shape in ('circle', 'ellipse'):
                draw.ellipse(bbox, fill=self.fill_color, outline=tuple(int(c) for c in color))
                # draw some more ellipses, slightly adjusted to avoid missing pixels
                if i > 0:
                    for j in range(4):
                        adjusted_bbox = bbox.copy()
                        adjusted_bbox[j] -= 1
                        draw.ellipse(adjusted_bbox, fill=self.fill_color, outline=tuple(int(c) for c in color))
            else:
                draw.rectangle(bbox, fill=self.fill_color, outline=tuple(int(c) for c in color))
        self.img = img


class ImageComponent(CardComponent):
    def __init__(self, img_fpath, monochrome=None, **generic):
        CardComponent.__init__(self, **generic)
        self.img_fpath = img_fpath
        self.monochrome = monochrome
        if type(self.monochrome) == str:
            self.monochrome = tuple(int(self.monochrome[i:i+2], 16) for i in (0, 2, 4))

    def build(self, wmax=9999, hmax=9999):
        self.img = crop_to_content(Image.open(self.img_fpath).convert('RGBA'))

        if self.monochrome:
            data = self.img.load()
            for i in range(self.img.width):
                for j in range(self.img.height):
                    r, g, b, a = data[i, j]
                    if a != 0:
                        data[i, j] = self.monochrome + (a, )

        w, h = self.img.size
        if wmax < w:
            self.img = self.img.resize((wmax, round(h * wmax / w)), Image.ANTIALIAS)
            w, h = self.img.size
        if hmax < h:
            self.img = self.img.resize((round(w * hmax / h), hmax), Image.ANTIALIAS)


class CornerIconComponent(ImageComponent):

    def __init__(self, img_fpath, icon_size=(100, 100), margin=12, **generic):
        ImageComponent.__init__(self, img_fpath, **generic)
        self.img_fpath = img_fpath
        self.icon_size = icon_size
        self.margin = margin

    def build(self, wmax=9999, hmax=9999):
        super().build(self.icon_size[0], self.icon_size[1])

    def draw(self, img, xy=(0, 0), **kwargs):
        x = img.width - self.margin - self.icon_size[0]
        y = self.margin
        # y = img.height - self.margin - self.icon_size[1]
        return super().draw(img, xy=(x, y), align='left', **kwargs)

    def cursor_shift(self):
        return 0, 0


class ImageBoxComponent(BoxComponent):

    def __init__(self, img_fpath, margin=20, **generic):
        BoxComponent.__init__(self, **generic)
        self.img_fpath = img_fpath
        self.margin = margin

    @property
    def full_margin(self):
        return self.margin + self.outline_width

    def build(self, wmax=99999, hmax=99999):
        ic = ImageComponent(self.img_fpath, **self.generic)
        iwmax = wmax - 2*self.full_margin
        ihmax = hmax - 2*self.full_margin

        ic.build(iwmax, ihmax)
        w, h = ic.img.size
        super().build(w+self.margin*2, h+self.margin*2)
        self.img = ic.draw(self.img, (self.full_margin, self.full_margin))


class TextBoxComponent(BoxComponent):

    def __init__(self, text, margin=20, default_font_size=48, spacing=12, font='Merriweather-Bold.ttf', text_color=(0, 0, 0), extra_right_margin=0, shrink_to_fit=True, align='left', vertical_align='top', **generic):
        BoxComponent.__init__(self, **generic)
        self.text = text
        self.margin = margin
        self.extra_right_margin = extra_right_margin
        self.default_font_size = default_font_size
        self.spacing = spacing
        self.font = font
        self.text_color = text_color
        self.shrink_to_fit = shrink_to_fit
        self.align = align
        self.vertical_align = vertical_align

        self.font_size = None

    def adjust_font_size(self):
        if self.font_size is None:
            self.font_size = self.default_font_size
        if self.font_size >= 24:
            self.font_size -= 2
        # elif self.font_size >= 12:
        #     self.font_size -= 2
        else:
            raise ValueError(f'Not enough space on card to print with font size >= 24 for {type(self)}.')

    def build(self, wmax=9999, hmax=9999):
        junk_img = Image.new('RGBA', (wmax, hmax))
        draw = ImageDraw.Draw(junk_img)
        filler = '-----'

        text_to_write = re.sub(r'\[\[\w+\]\]', filler, self.text)

        # determine the correct font size
        wmax = min(self.wmax, wmax)
        hmax = min(self.hmax, hmax)
        tw, th = 99999999, 99999999
        while th > hmax - 2*self.margin or tw > wmax - 2*self.margin - self.extra_right_margin:
            self.adjust_font_size()
            font = ImageFont.truetype(f'fonts/{self.font}', self.font_size)
            text_lines = wrap_text(text_to_write, wmax - 2*self.margin - self.extra_right_margin, font)

            tw, th = draw.textsize('\n'.join(text_lines), font=font, spacing=self.spacing)

        super().build(tw + 2*self.margin if self.shrink_to_fit else wmax, th+2*self.margin if self.shrink_to_fit else hmax)
        draw = ImageDraw.Draw(self.img)

        icons = re.findall(r'\[\[(\w+)\]\]', self.text)

        i = 0
        for line_n, line in enumerate(text_lines):
            line_parts = re.split(filler, line)
            x = self.outline_width + self.margin
            for line_part in line_parts[:-1]:
                lw = draw.textsize(line_part, font=font, spacing=self.spacing)[0]
                lh = draw.textsize(' ', font=font, spacing=self.spacing)[1]
                if icons[i] == '1Y':
                    fill_color = self.fill_color
                else:
                    fill_color = (255, 255, 255)
                icon = ImageBoxComponent(f'icons/{icons[i]}.png', margin=0, outline_width=1, outline_color=self.fill_color[:3], fill_color=fill_color)
                icon.build(lh+self.spacing, lh+self.spacing)
                iimg = icon.img
                x += lw + int(draw.textsize(' ', font=font)[0] / 2)
                self.img.paste(iimg, box=(x, self.outline_width + self.margin + line_n*(lh+self.spacing)), mask=iimg.convert('RGBA'))
                x += int(draw.textsize(filler + ' ', font=font)[0])
                i += 1

        x = self.outline_width + self.margin
        y = self.outline_width + self.margin
        if self.align == 'center':
            x = wmax//2 - tw//2
        elif self.align == 'right':
            x = wmax - tw - self.margin
        if self.vertical_align == 'center':
            y = hmax//2 - th//2
        elif self.vertical_align == 'bottom':
            y = hmax - th - self.margin
        draw.text((x, y), '\n'.join(text_lines).replace(filler, '      '), fill=self.text_color, font=font,
                  spacing=self.spacing)


class DevTitleComponent(TextBoxComponent):

    def __init__(self, title, icon, icon_size=(90, 90), margin=25, **generic):
        TextBoxComponent.__init__(self, title, default_font_size=64, shrink_to_fit=False, margin=margin, extra_right_margin=icon_size[0] + 2*margin
                                  , text_color=(255, 255, 255), outline_width=10, border_fade=False, vertical_align='bottom', **generic)
        self.title = title
        self.icon = ImageComponent(icon, monochrome=(255, 255, 255))
        self.icon_size = icon_size
        self.fill_color += (187, )

    def build(self, wmax=99999, hmax=99999):
        super().build(wmax, hmax)
        self.icon.build(*self.icon_size)
        self.icon.draw2(self.img, from_top='center', from_right=self.margin+self.outline_width)


class ArrowImageComponent(CardComponent):
    def __init__(self, arrow, arrow_width=28, activation=None, activation_loc=(0, 60), activation_size=(124, 124), **generic):
        CardComponent.__init__(self, **generic)
        self.arrow = arrow
        self.arrow_width = arrow_width

        self.activation = activation
        self.activation_loc = activation_loc
        self.activation_size = activation_size

    def build(self, wmax=99999, hmax=99999):
        arrow = ImageComponent(f'arrows/{self.arrow}.png', monochrome=(50, 50, 50))
        arrow.build(wmax, hmax)
        self.img = arrow.img
        if self.activation:
            actv = ImageBoxComponent(f'icons/{self.activation}.png', shape='circle', margin=4, outline_width=9, **self.generic)
            actv.build(self.activation_size[0], self.activation_size[1])
            if self.arrow == 'S':
                x = round(self.img.size[0] / 2 - actv.img.size[0] / 2)
                y = round(self.img.size[1] / 3 - actv.img.size[1] / 2)
            else:
                x, y = self.activation_loc
            self.img = actv.draw(self.img, (x, y), align='')

    def precursor_shift(self):
        aw, ah = self.img.size
        aimg_data = self.img.load()
        if self.arrow in ['E']:
            return (0, -1*int(np.median([j for j in range(ah) if aimg_data[0, j][3] > 0])))
        elif self.arrow in ['S', 'SE']:
            return (-1*int(np.median([i for i in range(aw) if aimg_data[i, 0][3] > 0])), 0)
        else:
            return 0, 0

    def cursor_shift(self):
        aw, ah = self.img.size
        aimg_data = self.img.load()
        if self.arrow in ['SE']:
            return (aw, int(np.median([j for j in range(ah) if aimg_data[aw - 1, j][3] > 0])))
        elif self.arrow in ['S']:
            return (int(np.median([i for i in range(aw) if aimg_data[i, ah - 1][3] > 0])), ah)
        elif self.arrow in ['E']:
            return (aw, 0)
        else:
            return aw, ah


class ResourcesComponent(CardComponent):
    def __init__(self, resources, resource_spacer=10, resource_size=(118, 118), resource_max_rows=2, **generic):
        CardComponent.__init__(self, **generic)
        self.resources = resources
        self.resource_spacer = resource_spacer
        self.resource_size = resource_size
        self.resource_max_rows = resource_max_rows

    def build(self, wmax=99999, hmax=99999):
        self.img = Image.new("RGBA", (wmax, hmax))

        rw, rh = self.resource_size
        for i, resource in enumerate(self.resources):
            row, col = (i % self.resource_max_rows, int(i/self.resource_max_rows))
            rimg = Image.open(f'resources/{resource}.png')
            loc = (col * (rw + self.resource_spacer), row * (rh + self.resource_spacer))
            self.img.paste(rimg, box=loc)

        self.img = crop_to_content(self.img)


class PaymentRewardComponent(CardComponent):
    def __init__(self, payment, reward, arrow='SE', activation=None, align='left', **generic):
        CardComponent.__init__(self, **generic)

        self.sub_component_spacer = 20
        self.align = align
        if arrow == 'S':
            self.align = 'center'

        if isinstance(payment, str):
            self.payment = ResourcesComponent(payment, **self.generic)
        else:
            self.payment = CardComponent.from_dict({**self.generic, **payment})

        self.arrow = arrow
        self.activation = activation

        if isinstance(reward, str):
            self.reward = ImageBoxComponent(reward, **{'margin': 10, 'monochrome': (50, 50, 50), **self.generic})
        else:
            self.reward = CardComponent.from_dict({**self.generic, **reward})

    def build(self, wmax=99999, hmax=99999):
        self.img = Image.new("RGBA", (wmax, hmax))
        ycursor = 0
        xcursor = 0
        if self.arrow == 'E':
            hmax = min(hmax, 400)
            ycursor += 40

        # resources
        self.img = self.payment.draw(self.img, (xcursor, ycursor), align=self.align)
        xshift, yshift = self.payment.cursor_shift()

        # arrow
        if self.arrow in ['S', 'SE']:
            xcursor += xshift//2
            ycursor += yshift + self.sub_component_spacer
        elif self.arrow in ['E']:
            xcursor += xshift + self.sub_component_spacer
            ycursor += yshift//2

        # arrow
        if self.arrow == 'SE':
            activation_loc = (0, 60)
        elif self.arrow == 'E':
            activation_loc = (30, 0)
        else:
            activation_loc = None
        arrow = ArrowImageComponent(self.arrow, activation=self.activation, activation_loc=activation_loc, **self.generic)
        arrow.build(300, 300)
        self.img = arrow.draw(self.img, (xcursor, ycursor), align=self.align)
        xshift, yshift = arrow.cursor_shift()
        xcursor += xshift
        ycursor += yshift
        if self.arrow in ['E', 'SE']:
            xcursor += self.sub_component_spacer
        elif self.arrow in ['S']:
            ycursor += self.sub_component_spacer

        # reward
        rwmax = min(wmax - xcursor, self.reward.wmax)
        rhmax = min(hmax - ycursor, self.reward.hmax)
        if self.arrow == 'E':
            rhmax = max(rhmax, self.payment.img.size[1])
        self.reward.build(rwmax, rhmax)
        if self.arrow in ['E', 'SE']:
            ycursor -= self.reward.img.height // 2
        else:
            xcursor -= self.reward.img.width // 2

        self.img = self.reward.draw(self.img, (xcursor, ycursor), align='center' if self.arrow == 'S' else 'left')




