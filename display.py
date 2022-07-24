#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os

from cal import Calendar

fontdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts')


import logging
import time
from PIL import Image, ImageDraw, ImageFont
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

logging.basicConfig(level=logging.DEBUG)


def suffix(day):
    if 4 <= day <= 20 or 24 <= day <= 30:
        return "th"
    else:
        return ["st", "nd", "rd"][day % 10 - 1]

def time_format(event):
    return event.strftime("%H:%M")

def render(calendar: Calendar, debug=False, rotate=False):
    if not debug:
        from waveshare_epd import epd2in13b_V3
    try:
        logging.info("epd2in13b_V3 Demo")
        day_suffix = suffix(int(calendar.last_updated.strftime("%d")))
        title_part1 = f'{calendar.last_updated.strftime(f"%A %-d")}'
        title = f'{title_part1}    {calendar.last_updated.strftime("%B")}'

        if not debug:
            epd = epd2in13b_V3.EPD()
            logging.info("init and Clear")
            epd.init()
            epd.Clear()
            time.sleep(1)

        # Drawing on the image
        logging.info("Drawing")
        font_main = ImageFont.truetype(os.path.join(fontdir, 'Ubuntu-M.ttf'), 16)
        font_small = ImageFont.truetype(os.path.join(fontdir, 'Ubuntu-M.ttf'), 10)

        # Drawing on the Horizontal image
        logging.info("1.Drawing on the Horizontal image...")
        width = 212
        if debug:
            HBlackimage = Image.new('1', (width, 104), 255)
            HRYimage = Image.new('1', (width, 104), 255)
        else:
            HBlackimage = Image.new('1', (epd.height, epd.width), 255)
            HRYimage = Image.new('1', (epd.height, epd.width), 255)
        drawblack = ImageDraw.Draw(HBlackimage)
        drawry = ImageDraw.Draw(HRYimage)
        w, h = drawblack.textsize(title, font=font_main)
        w_p1, h = drawblack.textsize(title_part1, font=font_main)
        drawblack.text(((width - w) / 2, 0), title, font=font_main, fill=0)
        drawblack.text(((width - w) / 2 + w_p1 + 1, 0), day_suffix, font=font_small, fill=0)
        drawblack.line((52, 20, 52, epd.width), fill=0)
        y = 20
        line_height = 20
        different_day = False
        for event in calendar.events[:4]:
            if event.different_day and not different_day:
                different_day = True
                drawblack.rectangle((0, y - 3, epd.height, y - 1), outline=0, fill=0)
            drawblack.text((5, y), time_format(event.start), font=font_main, fill=0)
            for num_chars in range(14, 25):
                if drawry.textsize(f"{event.name[:num_chars]}", font=font_main)[0] > 118:
                    break
            drawry.text((59, y), f"{event.name[:num_chars]}", font=font_main, fill=0)
            num_blocks = round((event.end - event.start).total_seconds() // (60*30))
            block_width = (line_height // 2 - 1)
            for i in range(min(4, num_blocks)):
                x_top = 190 + (i // 2) * block_width
                y_top = y + (i % 2) * block_width
                draw = drawblack if i % 3 else drawry
                draw.rectangle((x_top, y_top, x_top + block_width, y_top + block_width), outline=0, fill=0)
            y += line_height
        if rotate:
            HBlackimage = HBlackimage.rotate(180, Image.NEAREST, expand = 1)
            HRYimage = HRYimage.rotate(180, Image.NEAREST, expand = 1)
        if not debug:
            epd.display(epd.getbuffer(HBlackimage), epd.getbuffer(HRYimage))
        else:
            HBlackimage.show()
            HRYimage.show()

        if not debug:
            epd.sleep()
            time.sleep(3)
            epd.Dev_exit()

    except IOError as e:
        logging.info(e)
