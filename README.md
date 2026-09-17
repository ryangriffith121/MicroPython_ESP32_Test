# 📈 MicroPython Stocks (mpy-stocks)

A simple stock market ticker made with **MicroPython**, an **ESP32**, and a **128×64 SSD1306 OLED display**.

The ESP32 connects to Wi-Fi and retrieves stock market data from the **Yahoo Finance Chart API**, then displays the current price, percentage change, and a sparkline of historical prices.

## ✨ Features

This project combines an ESP32, an OLED display, and online market data to create a small standalone stock ticker.

- 📡 Wi-Fi network scanning and connection
- 📊 Stock market data from Yahoo Finance
- 📈 Historical price sparklines
- 🔄 Automatic cycling through stocks
- ⏱️ Multiple time ranges and intervals
- 🔁 Automatic request retries
- 🖥️ 128×64 OLED display
- ⚡ Runs on an ESP32

## 📊 Stocks

The ticker can display multiple stocks and market indices. The current configuration includes seven securities:

```python
stock_tickers = [
    "^DJI",
    "NVDA",
    "TSM",
    "GOOG",
    "MSFT",
    "AMZN",
    "AVGO"
]
```

Additional Yahoo Finance ticker symbols can be added to the `stock_tickers` list.

## ⏱️ Time Ranges

The program retrieves different amounts of historical data depending on the selected range. Each range uses a different interval to provide an appropriate number of data points for the OLED graph.

| Range | Interval |
|---|---|
| `1d` | `5m` |
| `1mo` | `1d` |
| `ytd` | `1wk` |

## 🔌 Hardware

The project uses an ESP32 to handle the networking and data processing, along with a small SSD1306 OLED for displaying the information.

- ESP32
- 128×64 SSD1306 OLED
- USB cable

### OLED Wiring

The OLED communicates with the ESP32 over I2C using GPIO 22 for the clock signal and GPIO 21 for the data signal.

| OLED | ESP32 |
|---|---|
| SCL | GPIO 22 |
| SDA | GPIO 21 |
| VCC | 3.3V |
| GND | GND |

## 🚀 Setup

First, install MicroPython on the ESP32 and upload the required Python files. The Wi-Fi credentials also need to be configured before running the program.

Upload:

```text
stocks.py
ssd1306.py
```

Configure the Wi-Fi credentials in `stocks.py`:

```python
SSID = "your-network"
PASSWORD = "your-password"
```

Once configured, run `stocks.py` on the ESP32.

## 🔄 How It Works

When started, the ESP32 first scans for available Wi-Fi networks and connects to the configured network. It then requests stock data from Yahoo Finance for each ticker and time range.

The retrieved prices, percentage changes, and historical closing prices are stored in memory. The OLED then cycles through the stocks and displays the corresponding information and sparkline.

## 📁 Project Structure

The repository contains the main stock ticker program, the SSD1306 display driver, and the configuration used for serial communication.

```text
MicroPython_Stocks/
├── stocks.py
├── ssd1306.py
├── TERATERM.INI
└── README.md
```

## 🌐 API

Stock information is retrieved from the **Yahoo Finance Chart API**. The program sends a request for each ticker and extracts the current price, previous close, percentage change, and historical closing prices from the returned JSON data.

```text
https://query1.finance.yahoo.com/v8/finance/chart/
```
