# 🔌 MicroPython_ESP32_Test

A MicroPython project for the ESP32 that connects to Wi-Fi, syncs the time over NTP, and drives a 128x64 SSD1306 OLED display showing a name/time header plus a small animated bouncing triangle.

## ✨ What it does

- Scans nearby Wi-Fi networks and prints their SSID, signal strength, and channel over serial
- Connects to a configured Wi-Fi network
- Syncs the system clock via NTP (`ntptime`)
- Applies a fixed UTC offset to compute and display local time
- Drives an SSD1306 OLED over I2C to show:
  - A name/header line
  - The current local date and time (`MM-DD H:MM:SS`)
  - A rotating triangle that bounces around inside a bordered box, animated using delta-time so its speed stays consistent regardless of loop timing

## 🔧 Hardware

- ESP32 dev board
- SSD1306 OLED display, 128x64, I2C
- Wiring (as configured in `program1.py`):
  - SCL → GPIO 22
  - SDA → GPIO 21

## 📁 Files

| File | Purpose |
|---|---|
| `program1.py` | Main application: Wi-Fi connect, NTP sync, and the OLED clock/animation loop |
| `ssd1306.py` | MicroPython SSD1306 display driver (I2C and SPI), subclasses `framebuf.FrameBuffer` for drawing primitives |
| `TERATERM.INI` | Tera Term terminal configuration, used for connecting to the ESP32's serial console over USB |

## 🚀 Setup

1. Flash MicroPython onto the ESP32 (via `esptool` or Thonny).
2. Copy `ssd1306.py` and `program1.py` onto the device's filesystem.
3. In `program1.py`, set your own Wi-Fi credentials:
   ```python
   SSID = "your-network-name"
   PASSWORD = "your-network-password"
   ```
4. Adjust `UTC_OFFSET` (in seconds) in `program1.py` to match your timezone.
5. Wire the SSD1306 display's SCL/SDA to GPIO 22/21 (or update the pin numbers in `program1.py` to match your wiring).
6. Reset the board. It will connect to Wi-Fi, sync time via NTP, then continuously update the display.

Serial output (Wi-Fi scan results, connection status, NTP sync result) can be viewed with Tera Term using the included `TERATERM.INI`, or any other serial terminal at the board's default baud rate.

## 📝 Notes

- If Wi-Fi connection fails, the script prints `wlan.status()` and continues to boot the display without a valid time sync.
- The bounce animation uses `time.ticks_ms()` / `time.ticks_diff()` for frame-rate-independent movement.
