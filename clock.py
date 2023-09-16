#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import logging
from waveshare_epd import epd4in2
import time
from PIL import Image, ImageDraw, ImageFont


picdir = 'pic'

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("Starting the Clock")
    
    epd = epd4in2.EPD()
    logging.info("init and Clear")
    epd.init()
    epd.Clear()
    
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
    font35 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 35)
    
    ScreenImage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    
    draw = ImageDraw.Draw(ScreenImage)

    sunny = Image.open(os.path.join(picdir, 'sunny.bmp'))
    sunny.convert("1")
    ScreenImage.paste(sunny, (200, 150))

    draw.text((20, 0), u'Test Black', font=font35, fill=0)
    draw.line((10, 140, 60, 190), fill=0)
    draw.line((60, 140, 10, 190), fill=0)
    draw.rectangle((10, 140, 60, 190), outline=0)
    draw.line((95, 140, 95, 190), fill=0)
    draw.line((70, 165, 120, 165), fill=0)
    draw.arc((70, 140, 120, 190), 0, 360, fill=0)
    draw.rectangle((10, 200, 60, 250), fill=0)
    draw.chord((70, 200, 120, 250), 0, 360, fill=0)
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
