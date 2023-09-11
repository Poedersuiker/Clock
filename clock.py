#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = 'pic'

import logging
from waveshare_epd import epd4in2
import time
from PIL import Image,ImageDraw,ImageFont
from svglib.svglib import svg2rlg
import traceback

logging.basicConfig(level=logging.DEBUG)

# Load the SVG images using the 'svglib.svg2rlg()' function
sunny = svg2rlg(os.path.join(picdir, 'wi-day-sunny.svg'))
sunny.scale(1/8,1/8)
sunny.width=200
sunny.height=200

try:
    logging.info("Starting the Clock")
    
    epd = epd4in2.EPD()
    logging.info("init and Clear")
    epd.init()
    epd.Clear()
    
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
    font35 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 35)
    
    logging.info("Init Grayscale")
    epd.Init_4Gray()
    
    Limage = Image.new('L', (epd.width, epd.height), 0)  # 255: clear the frame
    draw = ImageDraw.Draw(Limage)
    Limage.paste(sunny, (300, 150))
    draw.text((20, 0), u'Test Gray1', font = font35, fill = epd.GRAY1)
    draw.text((20, 35), u'Test Gray2', font = font35, fill = epd.GRAY2)
    draw.text((20, 70), u'Test Gray3', font = font35, fill = epd.GRAY3)
    draw.line((10, 140, 60, 190), fill = epd.GRAY1)
    draw.line((60, 140, 10, 190), fill = epd.GRAY1)
    draw.rectangle((10, 140, 60, 190), outline = epd.GRAY1)
    draw.line((95, 140, 95, 190), fill = epd.GRAY1)
    draw.line((70, 165, 120, 165), fill = epd.GRAY1)
    draw.arc((70, 140, 120, 190), 0, 360, fill = epd.GRAY1)
    draw.rectangle((10, 200, 60, 250), fill = epd.GRAY1)
    draw.chord((70, 200, 120, 250), 0, 360, fill = epd.GRAY1)
    epd.display_4Gray(epd.getbuffer_4Gray(Limage))
    time.sleep(3)
    
    logging.info("Goto Sleep...")
    epd.sleep()
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd4in2.epdconfig.module_exit()
    exit()
