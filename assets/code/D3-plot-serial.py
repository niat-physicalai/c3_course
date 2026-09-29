#!/usr/bin/env python3
"""D3 — Read the esp_watch_stream CSV, save it to a file, and plot it live.

Usage:
  python3 D3-plot-serial.py COM5                      # Windows serial port
  python3 D3-plot-serial.py /dev/ttyUSB0              # Linux / macOS
  python3 D3-plot-serial.py rfc2217://localhost:4000  # Wokwi for VS Code
  python3 D3-plot-serial.py --replay session.csv      # replay a saved file
Needs: pip install pyserial matplotlib
"""
import sys, time, collections
import matplotlib.pyplot as plt
import matplotlib.animation as animation

WINDOW = 500      # samples shown (10 s at 50 per second)
SMOOTH = 25       # moving-average length for the baseline (0.5 s)

def lines_from_serial(port):
    import serial
    ser = serial.serial_for_url(port, baudrate=115200, timeout=1)
    log = open(time.strftime("session_%Y%m%d_%H%M%S.csv"), "w")
    while True:
        line = ser.readline().decode(errors="ignore").strip()
        if line:
            log.write(line + "\n"); log.flush()
            yield line

def lines_from_file(path):
    for line in open(path):
        time.sleep(0.02)                       # replay at about 50 per second
        yield line.strip()

source = lines_from_file(sys.argv[2]) if sys.argv[1] == "--replay" else lines_from_serial(sys.argv[1])
raw = collections.deque(maxlen=WINDOW)
filtered = collections.deque(maxlen=WINDOW)
recent = collections.deque(maxlen=SMOOTH)

fig, (ax_raw, ax_f) = plt.subplots(2, 1, sharex=True)
line_raw, = ax_raw.plot([], []); ax_raw.set_ylabel("raw PPG (counts)")
line_f, = ax_f.plot([], []); ax_f.set_ylabel("raw minus baseline"); ax_f.set_xlabel("sample")

def update(_):
    for _ in range(10):                        # take up to 10 new lines per frame
        line = next(source, None)
        if line is None or line.startswith("#") or line.startswith("t_ms"):
            continue
        try:
            t_ms, ppg, steps = line.split(",")
            value = int(ppg)
        except ValueError:
            continue                           # skip a damaged line, keep going
        recent.append(value)
        raw.append(value)
        filtered.append(value - sum(recent) / len(recent))
    for ln, data, ax in ((line_raw, raw, ax_raw), (line_f, filtered, ax_f)):
        ln.set_data(range(len(data)), list(data))
        ax.relim(); ax.autoscale_view()
    return line_raw, line_f

anim = animation.FuncAnimation(fig, update, interval=200, cache_frame_data=False)
plt.show()
