from machine import Pin, SoftI2C
import ssd1306

import time
import math

import urequests
import ujson
import network
import ntptime

i2c = SoftI2C(scl=Pin(22), sda=Pin(21))

oled_width = 128
oled_height = 64

oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

oled.text('Loading', 32, 28)

oled.show()

SSID = "XXXXXXXX"
PASSWORD = "XXXXXXXX"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.config(pm=wlan.PM_NONE)

print("Scanning for available Wi-Fi networks...")

networks = wlan.scan()

for net in networks:
    try:
        ssid = net[0].decode('utf-8')
    except UnicodeDecodeError:
        ssid = str(net[0])
        
    rssi = net[3]
    channel = net[2]
    
    if ssid.strip():
        print(f"{ssid:<25} | {rssi:<15} dBm | {channel:<7}")

print(f"\nFound {len(networks)} networks:")
print(f"{'SSID':<25} | {'Signal (RSSI)':<15} | {'Channel':<7}")
print("-" * 55)

print("Connecting to Wi-Fi...")
wlan.connect(SSID, PASSWORD)

timeout = 15
start = time.time()
while not wlan.isconnected():
    if time.time() - start > timeout:
        status = wlan.status()
        print(f"\nConnection failed. wlan.status() = {status}")
        break
    time.sleep(0.5)
    print(".", end="")

if wlan.isconnected():
    print("\nConnected! Network config:", wlan.ifconfig())

range = "1d"
interval = "5m"

stock_tickers = ["^DJI", "NVDA", "TSM"]

stock_data = []
stock_prices = []
stock_change = []
stock_pct = []
stock_closes = []

def get_stock_data(symbol, range_="1d", interval="5m"):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range={range_}&interval={interval}"
    r = urequests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        data = ujson.loads(r.text)
    finally:
        r.close()

    result = data["chart"]["result"][0]
    meta = result["meta"]
    price = meta["regularMarketPrice"]
    prev_close = meta["chartPreviousClose"]
    change = price - prev_close
    pct = change / prev_close * 100

    closes = result["indicators"]["quote"][0]["close"]
    closes = [c for c in closes if c is not None]
    
    return [data, price, change, pct, closes]
        
def draw_sparkline(oled, closes, x0, y0, x1, y1):
    if len(closes) < 2:
        return
    lo, hi = min(closes), max(closes)
    span = hi - lo if hi != lo else 1
    n = len(closes)
    px, py = x0, y1 - int((closes[0] - lo) / span * (y1 - y0))
    for i in range(1, n):
        x = x0 + int(i / (n - 1) * (x1 - x0))
        y = y1 - int((closes[i] - lo) / span * (y1 - y0))
        oled.line(px, py, x, y, 1)
        px, py = x, y

for i in range(len(stock_tickers)):
    print(f"Requesting data for ${stock_tickers[i]}")
    data = get_stock_data(stock_tickers[i], range, interval)
    print(f"Got data for ${stock_tickers[i]}")
    stock_data.append(data[0])
    stock_prices.append(data[1])
    stock_change.append(data[2])
    stock_pct.append(data[3])
    stock_closes.append(data[4])

current_stock = 0

bounds = [32, 16, 128, 64]

title_pos = 0
title = " mpy-stocks "

last_time = time.ticks_ms()

while True:
    now = time.ticks_ms()
    delta_ms = time.ticks_diff(now, last_time)
    last_time = now

    dt = delta_ms / 1000

    current_stock = math.floor((time.ticks_ms()/3000) % (len(stock_tickers)))
    
    title_pos += dt * 4
    
    if title_pos > 0:
        title_pos = -128 - (len(title) * 8 * 3)
    
    oled.fill(0)
    
    title_string = f"--------{title}--------{title}--------{title}--------"
    oled.text(title_string, int(title_pos), -2, 1)
    
    if stock_change[current_stock] > 0:
        stock_glyph = "^"
    elif stock_change[current_stock] < 0:
        stock_glyph = "v"
    else:
        stock_glyph = "-"

    oled.text(f"({stock_glyph}){stock_tickers[current_stock]}:{stock_prices[current_stock]:>{12 - len(stock_tickers[current_stock])}}", 0, 8, 1)
    
    oled.text("t:", 0, 16)
    
    oled.text(f"{range:>3}", 4, 24)
    
    oled.text("int:", 0, 32)
    
    oled.text(f"{interval:>3}", 4, 40)
    
    oled.text("pct:", 0, 48)
    if stock_pct[current_stock] > 0:
        if stock_pct[current_stock] >= 1:
            oled.text(f"+{str(stock_pct[current_stock])[0:3]}", 0, 56)
        else:
            oled.text(f"+{str(stock_pct[current_stock])[1:4]}", 0, 56)
    else:
        if stock_pct[current_stock] <= -1:
            oled.text(f"-{str(stock_pct[current_stock])[1:4]}", 0, 56)
        else:
            oled.text(f"-{str(stock_pct[current_stock])[2:5]}", 0, 56)
        
    oled.rect(int(bounds[0]), int(bounds[1]), int(bounds[2] - bounds[0]), int(bounds[3] - bounds[1]), 1)
    
    draw_sparkline(oled, stock_closes[current_stock], bounds[0], bounds[1], bounds[2], bounds[3])
    
    oled.show()