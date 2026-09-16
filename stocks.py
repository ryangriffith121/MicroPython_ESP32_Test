import time
import math

import urequests
import ujson
import network
import ntptime

SSID = "RyaniPhone"
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

i2c = SoftI2C(scl=Pin(22), sda=Pin(21))

oled_width = 128
oled_height = 64

oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

stock_ticker = "AAPL"

url = "https://query1.finance.yahoo.com/v8/finance/chart/" + stock_ticker
r = urequests.get(url, headers={"User-Agent": "Mozilla/5.0"})
data = ujson.loads(r.text)
price = data["chart"]["result"][0]["meta"]["regularMarketPrice"]
r.close()
print(price)

while True:
    oled.fill(0)

    oled.text("Stocks...........", 0, 0)

    oled.text(f"{stock_ticker}: price", 0, 0)
    oled.text(price)