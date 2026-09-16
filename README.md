# 📈 mpy-stocks (MicroPython_Stocks)

A MicroPython project for the ESP32 that connects to Wi-Fi, pulls live stock/index quotes from Yahoo Finance, and displays a scrolling ticker with price, daily % change, and a sparkline on a 128x64 SSD1306 OLED.

<img width="4032" height="3024" alt="IMG_0610" src="https://github.com/user-attachments/assets/7bcabc51-3a87-4b21-b8ad-ea94f86cd1b2" />

## ✨ What it does

- Scans nearby Wi-Fi networks and connects using configured credentials
- Fetches quote data for a list of tickers from Yahoo Finance's chart API (`query1.finance.yahoo.com/v8/finance/chart/{symbol}`), including current price, previous close, % change, and a series of recent closing prices
- Cycles through the configured tickers automatically, updating every few seconds
- On the OLED, shows:
  - A continuously scrolling `mpy-stocks` title banner
  - The current ticker symbol and price, with an up/down/flat glyph (`^` / `v` / `-`) based on change from previous close
  - The selected time range and interval (e.g. `1d` / `5m`)
  - The percent change for the current ticker
  - A bordered sparkline chart of recent closing prices for the current ticker
- Uses delta-time (`time.ticks_ms`/`time.ticks_diff`) for the scrolling title so its speed is independent of loop timing

## 🔧 Hardware

- ESP32 dev board
- SSD1306 OLED display, 128x64, I2C
- Wiring (as configured in `stocks.py`):
  - SCL → GPIO 22
  - SDA → GPIO 21

## 📁 Files

| File | Purpose |
| --- | --- |
| `stocks.py` | Main application: Wi-Fi connect, Yahoo Finance data fetch, and the OLED ticker/sparkline loop |
| `ssd1306.py` | MicroPython SSD1306 display driver (I2C and SPI), subclasses `framebuf.FrameBuffer` for drawing primitives |
| `TERATERM.INI` | Tera Term terminal configuration, used for connecting to the ESP32's serial console over USB |

## 🚀 Setup

1. Flash MicroPython onto the ESP32 (via `esptool` or Thonny).
2. Copy `ssd1306.py` and `stocks.py` onto the device's filesystem.
3. In `stocks.py`, set your own Wi-Fi credentials:

   ```python
   SSID = "your-network-name"
   PASSWORD = "your-network-password"
   ```

4. (Optional) Edit the ticker list, range, and interval to taste:

   ```python
   range = "1d"
   interval = "5m"
   stock_tickers = ["^DJI", "NVDA", "TSM"]
   ```

   Any symbol Yahoo Finance's chart API recognizes will work, including indices (e.g. `^DJI`, `^GSPC`).

5. Wire the SSD1306 display's SCL/SDA to GPIO 22/21 (or update the pin numbers in `stocks.py` to match your wiring).
6. Reset the board. It will scan and connect to Wi-Fi, fetch data for each configured ticker, then continuously cycle through them on the display.

Serial output (Wi-Fi scan results, connection status, per-ticker fetch progress) can be viewed with Tera Term using the included `TERATERM.INI`, or any other serial terminal.

## 📝 Notes

- If Wi-Fi connection fails, the script prints `wlan.status()` after a 15-second timeout.
- Quote data is fetched once at boot for each ticker; the board does not currently re-fetch periodically, so prices reflect the values at power-on/reset.
- The sparkline auto-scales to the min/max of the fetched closing prices for the currently displayed ticker.
