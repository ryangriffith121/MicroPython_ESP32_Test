from machine import Pin, SoftI2C
import ssd1306
import time
import math
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

try:
    ntptime.settime()
    print("NTP sync successful!")
except Exception as e:
    print("Error syncing time:", e)

UTC_OFFSET = -6 * 3600

def get_local_time():
    local_seconds = time.time() + UTC_OFFSET
    
    year, month, day, hour, minute, second, weekday, yearday = time.localtime(local_seconds)
        
    return f"{month:02d}-{day:02d} {(hour%12)}:{minute:02d}:{second:02d}"

last_time = time.ticks_ms()
    

bounds = [0, 16, 127, 64]
    
tri_pos = [40, 40]
    
tri_vel = [2.1,1.1]
    
tri_rad = 12

while True:
    now = time.ticks_ms()
    delta_ms = time.ticks_diff(now, last_time)
    last_time = now

    dt = delta_ms / 1000
    
    oled.fill(0)
    
    oled.text('Ryan L. Griffith', 0, 0)
    oled.text(get_local_time(), 0, 8)

    angle = math.radians((time.ticks_ms()/20) % 360)

    tri = [
        int(tri_pos[0] + math.cos(angle) * tri_rad),
        int(tri_pos[1] + math.sin(angle) * tri_rad),
        int(tri_pos[0] + math.cos(angle + (2 * math.pi) / 3) * tri_rad),
        int(tri_pos[1] + math.sin(angle + (2 * math.pi) / 3) * tri_rad),
        int(tri_pos[0] + math.cos(angle + (4 * math.pi) / 3) * tri_rad),
        int(tri_pos[1] + math.sin(angle + (4 * math.pi) / 3) * tri_rad),
    ]
    
    speed_mult = dt * 5
    
    if tri_pos[0] - tri_rad + tri_vel[0] * speed_mult < bounds[0] or tri_pos[0] + tri_rad + tri_vel[0] * speed_mult > bounds[2]:
        tri_vel[0] *= -1
        
    if tri_pos[1] - tri_rad + tri_vel[1] * speed_mult < bounds[1] or tri_pos[1] + tri_rad + tri_vel[1] * speed_mult > bounds[3]:
        tri_vel[1] *= -1
    
    tri_pos[0] += tri_vel[0] * speed_mult
    tri_pos[1] += tri_vel[1] * speed_mult
    

    oled.line(tri[0], tri[1], tri[2], tri[3], 1)
    oled.line(tri[2], tri[3], tri[4], tri[5], 1)
    oled.line(tri[4], tri[5], tri[0], tri[1], 1)
    
    #print(f"x: {tri_pos[0]}, y: {tri_pos[1]}")
    
    oled.rect(int(bounds[0]), int(bounds[1]), int(bounds[2] - bounds[0]), int(bounds[3] - bounds[1]), 1)
    
    oled.show()