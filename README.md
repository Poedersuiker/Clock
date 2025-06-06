## Project Overview
A brief description of the project: An e-paper display that shows the current time and a 5-day weather forecast from OpenWeatherMap.

## Features
- Displays current time.
- Shows a 5-day weather forecast including temperature and weather icons.
- Utilizes a Waveshare 4.2inch e-Paper display.
- Weather data fetched from OpenWeatherMap API.

## Hardware Requirements
- Raspberry Pi (or Jetson Nano/SunriseX3 - support for these is included in the `waveshare_epd` library)
- Waveshare 4.2inch e-Paper Display (ensure it's compatible with the `epd4in2.py` driver)
- Connecting wires

## Software Requirements
- Python 3
- Dependencies listed in `requirements.txt`. These can be installed by running:
  ```bash
  pip install -r requirements.txt
  ```
  Note: `RPi.GPIO` is for Raspberry Pi. If using a Jetson Nano, you might need `Jetson.GPIO`. The `waveshare_epd` library attempts to use the appropriate GPIO library for your detected hardware.

## Setup Instructions
1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configure OpenWeatherMap API Key:**
    - Sign up for a free API key at [OpenWeatherMap](https://openweathermap.org/forecast5).
    - Currently, the API key is hardcoded in `OpenWeather.py` and `clock.py`. You need to replace the placeholder `'b959aff47fc0058e7d8e3a6b3c0b558e'` with your actual API key in these files.
    - **Important:** For better security, it's recommended to move the API key to a configuration file (e.g., `config.ini`) or an environment variable instead of keeping it directly in the code.
4.  **Configure Location (Latitude and Longitude):**
    - The latitude and longitude for the weather forecast are also hardcoded in `OpenWeather.py` and `clock.py`. Update the `lat` and `lon` variables in these files to your desired location.
    - Example: `url = 'https://api.openweathermap.org/data/2.5/forecast?lat=YOUR_LAT&lon=YOUR_LON&units=metric&appid=YOUR_API_KEY'`
5.  **Enable SPI Interface:**
    - For Raspberry Pi, ensure the SPI interface is enabled. You can do this using `raspi-config`:
      `Interfacing Options` -> `SPI` -> `Yes`.
6.  **Run the application:**
    ```bash
    python clock.py
    ```
    The script will fetch the latest weather data and update the e-paper display. It then refreshes every minute.

## Directory Structure
```
.
├── OpenWeather.py        # Script to fetch and print weather data from OpenWeatherMap.
├── README.md             # This file.
├── clock.py              # Main application to display time and weather on e-paper.
├── requirements.txt      # Python package dependencies.
├── pic/                  # Contains weather icons (BMP) and font files (TTF, TTC).
│   ├── 01.bmp, ...       # Weather condition icons.
│   └── 7segment.ttf, ... # Font files.
└── waveshare_epd/        # Library for Waveshare e-Paper display.
    ├── epd4in2.py        # Driver for the 4.2inch e-Paper module.
    ├── epdconfig.py      # Hardware configuration for different platforms (RPi, Jetson).
    └── ...
```

## Customization
- **Location**: Change `lat` and `lon` variables in `clock.py` and `OpenWeather.py`.
- **Weather Icons**: Modify or replace BMP images in the `pic/` directory. Ensure new icons match the naming convention used in `clock.py` (e.g., '01d.bmp', '02n.bmp').
- **Fonts**: Change font files (`.ttf`, `.ttc`) in `pic/` and update font paths and sizes in `clock.py`.

## License
This project does not currently specify a license. Please be mindful of the licenses of the included libraries and resources (e.g., Waveshare EPD library, OpenWeatherMap terms of service, fonts).
