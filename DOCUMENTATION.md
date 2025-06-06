# Project Documentation

This document provides a more detailed explanation of the E-Paper Weather Clock project components, configuration, and customization options.

## 1. Core Scripts

### 1.1. `clock.py`
This is the main application script responsible for displaying the current time and weather forecast on the Waveshare 4.2-inch e-Paper display.

**Key Functionalities:**
- **Initialization**: Sets up logging and loads weather icons from the `pic/` directory. Icons are converted to monochrome for the e-paper display.
- **Weather Data Fetching**:
    - Uses the `fetch_json_data(url)` function to retrieve weather forecast data from the OpenWeatherMap API. The URL includes hardcoded latitude, longitude, units (metric), and your API key.
    - Handles potential HTTP errors during the API request.
- **Display Rendering**:
    - Initializes the e-paper display using the `waveshare_epd.EPD()` class.
    - Clears the display before each update.
    - Uses the Pillow (PIL) library (`Image`, `ImageDraw`, `ImageFont`) to create the layout.
    - **Fonts**: Loads custom fonts from the `pic/` directory:
        - `7segment.ttf` for time, date, and temperature.
        - `Font.ttc` (likely a more general-purpose font, usage can be expanded).
    - **Layout**:
        - Draws a timeline at the top showing weather forecasts for the next few 3-hour intervals (time, icon, temperature).
        - Displays the current time prominently in the center using a large 7-segment style font.
    - Pastes weather icons onto the display image.
    - The image is then converted to the appropriate format and sent to the e-paper display.
- **Update Cycle**:
    - The `update_screen()` function encapsulates the weather fetching and display rendering logic.
    - The `main()` function calls `update_screen()` and then sleeps for 60 seconds before repeating the process, ensuring the display is updated approximately every minute.
- **Error Handling**: Includes `try-except` blocks for `IOError` (e.g., display communication issues) and `KeyboardInterrupt` (to allow graceful exit using Ctrl+C, which calls `module_exit()` from `waveshare_epd`).

**API Key and Location:**
- The OpenWeatherMap API URL (containing the API key and location) is hardcoded:
  `url = 'https://api.openweathermap.org/data/2.5/forecast?lat=52.04&lon=5.67&units=metric&appid=YOUR_API_KEY'`
- **Security Note**: It is strongly recommended to externalize the API key (e.g., using a configuration file or environment variable) rather than keeping it directly in the script.
- **Location**: The latitude (`lat=52.04`) and longitude (`lon=5.67`) are also part of this URL.

### 1.2. `OpenWeather.py`
This is a simpler utility script primarily for testing the OpenWeatherMap API connection and fetching raw JSON data.

**Key Functionalities:**
- Defines `fetch_json_data(url)` which is identical to the one in `clock.py`.
- Contains the same hardcoded OpenWeatherMap API URL.
- When run directly (`if __name__ == "__main__":`), it fetches the weather data and prints the entire JSON response to the console. This is useful for inspecting the data structure provided by the API.

## 2. `waveshare_epd` Library
This directory contains the necessary drivers and configuration files for interacting with Waveshare e-Paper displays.

### 2.1. `epd4in2.py`
This is the Python driver specific to the 4.2-inch e-Paper display module.
- **Display Resolution**: `EPD_WIDTH = 400`, `EPD_HEIGHT = 300`.
- **Color**: Handles monochrome (black and white) display, with definitions for different gray levels (though the primary use in `clock.py` is 1-bit black/white).
- **Core Class `EPD`**:
    - `__init__()`: Initializes pins and display dimensions.
    - `init()`, `init_Partial()`, `Init_4Gray()`: Different initialization routines for the display. `clock.py` uses `init()`.
    - `reset()`: Performs a hardware reset of the display.
    - `send_command()`, `send_data()`, `send_data2()`: Low-level functions for SPI communication.
    - `ReadBusy()`: Waits for the display to finish its current operation.
    - `set_lut()`, `Partial_SetLut()`, `Gray_SetLut()`: Functions to set Look-Up Tables for different display modes.
    - `getbuffer()`: Converts a Pillow `Image` object into the byte buffer format required by the display. `clock.py` uses this.
    - `getbuffer_4Gray()`: Converts an image for 4-grayscale display.
    - `display()`: Sends the image buffer to the display for a full update.
    - `EPD_4IN2_PartialDisplay()`: For partial screen updates (not used by `clock.py`).
    - `display_4Gray()`: Displays an image using 4 grayscale levels.
    - `Clear()`: Clears the display (fills with white).
    - `sleep()`: Puts the display into a low-power deep sleep mode. Called by `clock.py` after each update.

### 2.2. `epdconfig.py`
This script handles the hardware abstraction layer, allowing the EPD library to work on different platforms like Raspberry Pi, Jetson Nano, and SunriseX3.
- **Platform Detection**: Attempts to detect the platform (e.g., by checking for `/sys/bus/platform/drivers/gpiomem-bcm2835` for Raspberry Pi).
- **Pin Definitions**: Defines GPIO pin numbers (BCM mode) for `RST`, `DC`, `CS`, `BUSY`, and `PWR`.
- **GPIO and SPI Initialization**:
    - Imports the appropriate GPIO library (`RPi.GPIO`, `Jetson.GPIO`, `Hobot.GPIO`).
    - Imports `spidev` for SPI communication on Raspberry Pi or uses a custom software SPI implementation (`sysfs_software_spi.so`) for Jetson Nano if hardware SPI is not directly used by the Python `spidev` library there.
    - `module_init()`: Sets up GPIO pins (mode, direction) and initializes the SPI interface.
    - `module_exit()`: Cleans up GPIO settings and closes the SPI connection. Also powers down the EPD module.
- **Wrapper Functions**: Provides common functions like `digital_write()`, `digital_read()`, `delay_ms()`, `spi_writebyte()`, `spi_writebyte2()` that call the platform-specific implementations.

## 3. Configuration Details

### 3.1. OpenWeatherMap API
- **API Key**: As mentioned, the API key `b959aff47fc0058e7d8e3a6b3c0b558e` is a placeholder in both `clock.py` and `OpenWeather.py`. You **must** replace this with your own valid API key from [OpenWeatherMap](https://openweathermap.org/).
- **URL Structure**: `https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units=metric&appid={API_key}`
    - `lat`: Latitude
    - `lon`: Longitude
    - `units=metric`: For temperature in Celsius. Change to `imperial` for Fahrenheit.
    - `appid`: Your API key.

### 3.2. Location
- Latitude and Longitude are hardcoded in the API URL in `clock.py` and `OpenWeather.py`.
- To change the location, modify the `lat=` and `lon=` values in the `url` variable in both files. For example, for New York: `lat=40.7128&lon=-74.0060`.

## 4. Customization

### 4.1. Weather Icons
- Weather icons are stored in the `pic/` directory as BMP files.
- The `clock.py` script maps OpenWeatherMap icon codes (e.g., "01d", "01n", "02d") to these BMP files.
  ```python
  icons = {'01n': Image.open(os.path.join(picdir, '01.bmp')), ...}
  ```
- **Adding/Changing Icons**:
    1. Create your new icon as a BMP file. For best results on a monochrome display, use a simple black and white design. The current icons appear to be white on a black background after processing.
    2. The script processes these icons:
       ```python
       if icons[key].mode != 'L': # If not grayscale
           icons[key] = icons[key].convert('L') # Convert to grayscale
           icons[key] = ImageOps.invert(icons[key]) # Invert colors
           icons[key] = icons[key].convert("1") # Convert to 1-bit monochrome
       ```
       This means if your source BMP is black on white, it will become white on black, which is then drawn on a black background in `clock.py` (effectively making the icon appear white).
    3. Place the new BMP in the `pic/` directory.
    4. Update the `icons` dictionary in `clock.py` if you change filenames or add new icon codes.

### 4.2. Fonts
- Fonts are stored in the `pic/` directory (e.g., `7segment.ttf`, `Font.ttc`).
- `clock.py` loads these fonts using `ImageFont.truetype()`:
  ```python
  font18 = ImageFont.truetype(os.path.join(picdir, '7segment.ttf'), 18)
  fontClock = ImageFont.truetype(os.path.join(picdir, '7segment.ttf'), 175)
  # ... and so on for other font sizes/styles.
  ```
- **Changing Fonts**:
    1. Place your new `.ttf` or `.ttc` font file in the `pic/` directory.
    2. Update the `ImageFont.truetype()` calls in `clock.py` to point to your new font file and adjust the size as needed.

## 5. Running the Project
1.  Ensure all hardware is connected correctly (EPD to Raspberry Pi/Jetson).
2.  Ensure SPI is enabled on your Raspberry Pi (`sudo raspi-config`).
3.  Install dependencies: `pip install -r requirements.txt`.
4.  Configure your OpenWeatherMap API key and location in `clock.py` (and `OpenWeather.py` if you use it).
5.  Run the main script: `python clock.py`.

The display should update with the current time and weather forecast. It will then enter a loop, refreshing approximately every minute. To stop the script, press Ctrl+C.
