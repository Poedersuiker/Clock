#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import logging
from waveshare_epd import epd4in2
import time
from PIL import Image, ImageDraw, ImageFont, ImageOps


picdir = 'pic'

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("Starting the Clock")
    
    epd = epd4in2.EPD()
    logging.info("init and Clear")
    epd.init()
    epd.Clear()

    font18 = ImageFont.truetype(os.path.join(picdir, 'NixieOne.ttf'), 18)
    fontClock = ImageFont.truetype(os.path.join(picdir, '7segment.ttf'), 175)
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    font35 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 35)
    
    # Create a Black background (0 instead of 255)
    ScreenImage = Image.new('1', (epd.width, epd.height), 0)  # 255: clear the frame
    
    # initiate the Drawing tool
    draw = ImageDraw.Draw(ScreenImage)

    # load the sunny icon
    sunny = Image.open(os.path.join(picdir, 'sunny.bmp'))
    if sunny.mode != 'L':
        sunny = sunny.convert('L')
    sunny = ImageOps.invert(sunny)
    sunny = sunny.convert("1")

    # Draw the time line on top (with space for the times above
    draw.rectangle((0, 20, 400, 23), fill=255)
    draw.text((9, 2), u'9:00', font=font18, fill=255)
    draw.rectangle((5, 15, 8, 35), fill=255)
    ScreenImage.paste(sunny, (8, 24))

    draw.text((109, 2), u'12:00', font=font18, fill=255)
    draw.rectangle((105, 15, 108, 35), fill=255)
    ScreenImage.paste(sunny, (108, 24))

    draw.text((209, 2), u'15:00', font=font18, fill=255)
    draw.rectangle((205, 15, 208, 35), fill=255)
    ScreenImage.paste(sunny, (208, 24))

    draw.text((309, 2), u'18:00', font=font18, fill=255)
    draw.rectangle((305, 15, 308, 35), fill=255)
    ScreenImage.paste(sunny, (308, 24))

    draw.text((10, 100), u'24:00', font=fontClock, fill=255)
    draw.tex

    '''draw.text((20, 0), u'Test Black', font=font35, fill=0)
    draw.line((10, 140, 60, 190), fill=0)
    draw.line((60, 140, 10, 190), fill=0)
    draw.rectangle((10, 140, 60, 190), outline=0)
    draw.line((95, 140, 95, 190), fill=0)
    draw.line((70, 165, 120, 165), fill=0)
    draw.arc((70, 140, 120, 190), 0, 360, fill=0)
    draw.chord((70, 200, 120, 250), 0, 360, fill=0)'''

    epd.display(epd.getbuffer(ScreenImage))
    time.sleep(3)
    
    logging.info("Goto Sleep...")
    epd.sleep()
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd4in2.epdconfig.module_exit()
    exit()
