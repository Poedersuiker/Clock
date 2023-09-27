#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import logging
from waveshare_epd import epd4in2
import time
from PIL import Image, ImageDraw, ImageFont, ImageOps
import requests


picdir = 'pic'
url = 'https://api.openweathermap.org/data/2.5/forecast?lat=52.04&lon=5.67&units=metric&appid=b959aff47fc0058e7d8e3a6b3c0b558e'

logging.basicConfig(level=logging.DEBUG)
logging.info("Starting the Clock")

# load icons
icons = {'01n': Image.open(os.path.join(picdir, '01.bmp')), '01b': Image.open(os.path.join(picdir, '01.bmp')),
         '02n': Image.open(os.path.join(picdir, '02.bmp')), '02b': Image.open(os.path.join(picdir, '02.bmp')),
         '03n': Image.open(os.path.join(picdir, '03.bmp')), '03b': Image.open(os.path.join(picdir, '03.bmp')),
         '04n': Image.open(os.path.join(picdir, '04.bmp')), '04b': Image.open(os.path.join(picdir, '04.bmp')),
         '09n': Image.open(os.path.join(picdir, '09.bmp')), '09b': Image.open(os.path.join(picdir, '09.bmp')),
         '10n': Image.open(os.path.join(picdir, '10.bmp')), '10b': Image.open(os.path.join(picdir, '10.bmp')),
         '11n': Image.open(os.path.join(picdir, '11.bmp')), '11b': Image.open(os.path.join(picdir, '11.bmp')),
         '13n': Image.open(os.path.join(picdir, '13.bmp')), '13b': Image.open(os.path.join(picdir, '13.bmp')),
         '50n': Image.open(os.path.join(picdir, '50.bmp')), '50b': Image.open(os.path.join(picdir, '50.bmp'))}

for key in icons:
    if icons[key].mode != 'L':
        icons[key] = icons[key].convert('L')
        icons[key] = ImageOps.invert(icons[key])
        icons[key] = icons[key].convert("1")


def fetch_json_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        return response.json()  # Parse JSON response
    except requests.exceptions.HTTPError as errh:
        print("HTTP Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("Something went wrong:", err)


def update_screen():
    weather_data = fetch_json_data(url)
    timestamp = time.strftime('%H:%M')

    try:
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

        # Draw the time line on top (with space for the times above
        draw.rectangle((0, 20, 400, 23), fill=255)
        draw.text((9, 2), weather_data['list'][0]['dt_txt'][11:], font=font18, fill=255)
        draw.rectangle((5, 15, 8, 35), fill=255)
        ScreenImage.paste(icons[weather_data['list'][0]['weather'][0]['icon']], (8, 24))

        draw.text((109, 2), weather_data['list'][1]['dt_txt'][11:], font=font18, fill=255)
        draw.rectangle((105, 15, 108, 35), fill=255)
        ScreenImage.paste(icons[weather_data['list'][1]['weather'][0]['icon']], (108, 24))

        draw.text((209, 2), weather_data['list'][2]['dt_txt'][11:], font=font18, fill=255)
        draw.rectangle((205, 15, 208, 35), fill=255)
        ScreenImage.paste(icons[weather_data['list'][2]['weather'][0]['icon']], (208, 24))

        draw.text((309, 2), weather_data['list'][3]['dt_txt'][11:], font=font18, fill=255)
        draw.rectangle((305, 15, 308, 35), fill=255)
        ScreenImage.paste(icons[weather_data['list'][3]['weather'][0]['icon']], (308, 24))

        draw.text((10, 100), timestamp, font=fontClock, fill=255)

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


def main():
    while True:
        update_screen()
        time.sleep(60)


if __name__ == "__main__":
    main()
