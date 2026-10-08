"""claude-svg diagrams for module 02 (Sensing & Hardware Architecture).

Run from the repo root:  .venv/bin/python deck/asset-src/02/diagrams.py
Writes assets/slides/02/V-sNN-N.svg. Every label comes from the slide's cited sections.
Reuses the Svg helper and palette from module 01. Arrows meet a box at the centre of the side
they touch (several arrows into one side sit symmetric about its centre).
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location("d01", Path(__file__).resolve().parent.parent / "01" / "diagrams.py")
d01 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(d01)
d01.OUT = Path("assets/slides/02")          # Svg.save writes here

Svg, table = d01.Svg, d01.table
BLUE, LIGHT, INK, GREY = d01.BLUE, d01.LIGHT, d01.INK, d01.GREY
PALE, PALE2 = d01.PALE, d01.PALE2
GREEN, GREEN_BG, ORANGE, ORANGE_BG, RED, RED_BG = d01.GREEN, d01.GREEN_BG, d01.ORANGE, d01.ORANGE_BG, d01.RED, d01.RED_BG
NORM = (PALE2, "#C9DCEA", INK)


# ── B0 ───────────────────────────────────────────────────────────────────
def v_s04():
    s = Svg(1600, 720)
    rows = [("Presence and proximity", "Changing heat pattern, reflected light,\necho time, capacitance",
             "PIR misses a still person"),
            ("Position and motion", "Acceleration (including gravity), rotation\nrate, shaft position, magnetic field",
             "Accelerometers mix gravity with\nmotion; gyroscopes drift"),
            ("Optical and biometric", "Light reflected or transmitted\nthrough tissue or a surface",
             "Ambient light, poor contact, motion"),
            ("Environmental", "The conditions at the sensor itself", "Self-heating; reads the enclosure,\nnot the room"),
            ("Force and level", "Strain, resistance change,\nfloat position, distance",
             "Creep, temperature drift,\nmechanical wear"),
            ("Electrical", "Voltage across a resistance, magnetic\nfield around a conductor",
             "Offset and noise at small currents"),
            ("Identification", "Presence and code of a tag", "Range, orientation, metal nearby")]
    fills = [[(PALE, BLUE, BLUE), NORM, (ORANGE_BG, ORANGE, INK)] for _ in rows]
    table(s, 20, 10, [400, 620, 560], 76, ["Family", "What it actually measures", "How it typically fails"],
          rows, fills, size=24, head_size=28)
    s.save("V-s04-1")


def v_s07():
    s = Svg(1200, 900)
    cards = [("ECG electrodes", "Rejected: needs a\ndeliberate action", RED, RED_BG),
             ("Chest strap", "Rejected:\nuser tolerance", RED, RED_BG),
             ("Piezo pulse sensor", "Rejected: placement\ntoo fragile", RED, RED_BG),
             ("Optical PPG", "Kept: works passively\nfrom the wrist", GREEN, GREEN_BG)]
    for i, (name, verdict, c, bg) in enumerate(cards):
        x, y = 40 + (i % 2) * 570, 40 + (i // 2) * 430
        s.rect(x, y, 550, 390, fill=bg, stroke=c, sw=4)
        s.text(x + 275, y + 110, name, 42, c, 700)
        s.text(x + 275, y + 250, verdict, 36, INK, 600)
    s.save("V-s07-1")


# ── B1 ───────────────────────────────────────────────────────────────────
def v_s08():
    s = Svg(1600, 720)
    rows = [("I²C", "2, shared by all", "Many, by address", "100 or 400 kHz", "Yes"),
            ("SPI", "3 shared + 1 chip\nselect per device", "Many, by chip select", "Several MHz", "No"),
            ("UART", "2 per device (TX, RX)", "One", "9,600 to\n115,200 baud", "No"),
            ("Analog (ADC)", "1 per signal", "One", "Limited by ADC\nand filtering", "No"),
            ("Pulse / one-wire", "1 per device", "One (or a few)", "Depends on\nthe protocol", "Often")]
    first = (PALE, BLUE, BLUE)
    fills = [[first, NORM, NORM, NORM, NORM] for _ in rows]
    table(s, 20, 20, [300, 360, 340, 340, 240], 100, ["", "Wires (plus ground)", "Devices", "Typical speed",
                                                      "Pull-ups"], rows, fills, size=27, head_size=29)
    s.save("V-s08-1")


def v_s10():
    s = Svg(1200, 900)
    rows = [("Device missing from a scan,\nor coming and going", "Address pin floating,\nunpowered, or\nwrong address"),
            ("Two devices on one\naddress, garbled reads", "Address clash"),
            ("UART output is\nrandom characters", "Baud-rate mismatch"),
            ("Readings drift, everything\nbehaves oddly", "Missing common ground")]
    s.text(270, 45, "Symptom", 34, GREY, 700)
    s.text(950, 45, "Likely cause", 34, GREY, 700)
    for i, (sym, cause) in enumerate(rows):
        y = 90 + i * 200
        s.box(20, y, 500, 160, sym, fill=PALE2, stroke="#C9DCEA", size=30)
        s.box(720, y, 460, 160, cause, fill=ORANGE_BG, stroke=ORANGE, color=ORANGE, size=30, weight=700)
        s.line(525, y + 80, 714, y + 80, color=GREY)
    s.save("V-s10-1")


# ── B2 ───────────────────────────────────────────────────────────────────
def v_s12():
    s = Svg(1200, 900)
    mods = [("SSD1306\ndisplay\n0x3C", 250), ("MPU-6050\nmotion\n0x68", 600), ("MAX30102\nheart rate\n0x57", 950)]
    # 3.3 V rail: XIAO right side → up → across the module tops
    s.line(1050, 555, 1150, 555, color=ORANGE, head=False)
    s.line(1150, 555, 1150, 60, color=ORANGE, head=False)
    s.line(250, 60, 1150, 60, color=ORANGE, head=False)
    s.text(700, 30, "3.3 V rail (XIAO 3V3 pin)", 28, ORANGE, 700)
    for label, cx in mods:
        s.line(cx, 60, cx, 104, color=ORANGE)
        s.box(cx - 150, 110, 300, 180, label, size=32)
        s.line(cx, 292, cx, 370, color=BLUE, head=False)
    # one shared I²C bus, three taps
    s.line(250, 370, 950, 370, color=BLUE, sw=8, head=False)
    s.line(600, 370, 600, 464, color=BLUE, sw=8)
    s.text(780, 418, "I²C: SDA D4, SCL D5", 28, BLUE, 700, anchor="start")
    s.box(150, 470, 900, 170, "XIAO ESP32-C3 module\nUSB-C · charger · 3.3 V regulator", fill=BLUE, stroke=BLUE,
          color="white", size=34, weight=700)
    bottom = [("SW1 “next”", 300, "D10"), ("SW2 “previous”", 600, "D9"), ("SW3 → protected\nLiPo cell", 900, "BAT+ / BAT−")]
    for label, cx, pin in bottom:
        s.box(cx - 130, 760, 260, 120, label, size=28)
        s.line(cx, 755, cx, 646, color=GREY)
        s.text(cx + 14, 700, pin, 26, GREY, 600, anchor="start")
    s.save("V-s12-1")


def v_s13():
    s = Svg(1200, 900)
    rows = [("SDA, SCL", "I²C", "3.3 V", "Both", "100 or\n400 kHz", "0x3C, 0x68,\n0x57"),
            ("BTN_NEXT", "Digital", "3.3 V", "In", "Human\nspeed", "Internal\npull-up"),
            ("3V3", "Power", "3.3 V", "Out", "—", "XIAO\nregulator"),
            ("BAT+, BAT−", "Power", "3.7 V\nnominal", "In", "—", "3.7 V cell\nonly"),
            ("GND", "Ground", "0 V", "—", "—", "Shared\nreference")]
    volt = (ORANGE_BG, ORANGE, INK)
    fills = [[(PALE, BLUE, BLUE), NORM, volt, NORM, NORM, NORM] for _ in rows]
    table(s, 10, 40, [230, 165, 175, 150, 210, 250], 120, ["Signal", "Type", "Voltage", "Dir.", "Data rate", "Notes"],
          rows, fills, size=26, head_size=27)
    s.save("V-s13-1")


# ── B3 ───────────────────────────────────────────────────────────────────
def v_s15():
    s = Svg(1200, 900)
    # bare chip: the parts you add yourself
    s.text(290, 50, "Bare chip", 40, INK, 700)
    s.box(140, 110, 300, 150, "ESP32-C3", fill=BLUE, stroke=BLUE, color="white", size=38, weight=700)
    ext = ["External crystal", "External SPI flash", "Antenna input\n(LNA_IN)"]
    for i, e in enumerate(ext):
        y = 360 + i * 160
        s.box(90, y, 400, 120, e, fill="white", stroke=RED, color=RED, size=30, dash="12 8")
    s.line(290, 266, 290, 354, color=GREY, head=False)
    s.text(290, 860, "You design and certify these", 30, RED, 700)
    # module: all of it inside
    s.text(900, 50, "Module", 40, INK, 700)
    s.rect(640, 100, 520, 680, fill=GREEN_BG, stroke=GREEN, sw=4, r=26)
    inside = ["ESP32-C3", "Crystal", "Flash", "Regulator", "Antenna or\nconnector"]
    for i, e in enumerate(inside):
        y = 130 + i * 128
        s.box(700, y, 400, 104, e, fill="white", stroke=GREEN, color=GREEN if i else INK, size=30)
    s.text(900, 860, "Maker has often certified it", 30, GREEN, 700)
    s.save("V-s15-1")


def v_s16():
    s = Svg(1200, 900)
    s.box(60, 30, 320, 100, "USB-C 5 V", fill=PALE2, stroke=GREY, size=32)
    s.rect(30, 190, 730, 340, fill="white", stroke=BLUE, sw=3, r=24)
    s.text(395, 220, "XIAO ESP32-C3", 28, BLUE, 700)
    s.line(220, 134, 220, 254)
    s.box(70, 260, 300, 90, "Onboard charger", size=30)
    s.line(372, 305, 444, 305)
    s.box(450, 260, 270, 90, "3.3 V regulator", size=30)
    s.box(70, 410, 300, 90, "BAT+ / BAT− pads", size=28)
    s.line(220, 406, 220, 356)
    s.box(85, 590, 270, 90, "Slide switch SW3", fill=ORANGE_BG, stroke=ORANGE, color=ORANGE, size=28)
    s.box(85, 760, 270, 110, "Protected LiPo\ncell, 3.7 V", fill=PALE2, stroke=GREY, size=28)
    s.line(220, 756, 220, 686)
    s.line(220, 586, 220, 506)
    # 3.3 V rail to every load
    s.line(722, 305, 800, 305, color=ORANGE, head=False)
    s.line(800, 305, 800, 779, color=ORANGE, head=False)
    s.text(808, 240, "3.3 V rail", 28, ORANGE, 700, anchor="start")
    for i, load in enumerate(["ESP32-C3", "SSD1306 display", "MPU-6050", "MAX30102"]):
        cy = 305 + i * 158
        s.line(800, cy, 844, cy, color=ORANGE)
        s.box(850, cy - 40, 320, 80, load, size=28)
    s.save("V-s16-1")


def v_s19():
    s = Svg(1200, 900)
    s.rect(500, 60, 200, 60, fill="#B0BEC5", stroke=GREY, sw=3, r=10)
    s.text(600, 92, "USB-C", 26, INK, 700)
    s.rect(470, 110, 260, 690, fill="#2F4F4F", stroke="#2F4F4F", r=24)
    s.text(600, 455, "XIAO\nESP32-C3", 34, "white", 700)
    left = [("D0 · strapping, not connected", ORANGE), ("D1 · ADC1, free", GREY), ("D2 · ADC1, free", GREY),
            ("D3 · free", GREY), ("D4 · I²C SDA", BLUE), ("D5 · I²C SCL", BLUE), ("D6 · UART TX, left free", GREY)]
    right = [("5V", INK), ("GND", INK), ("3V3 · 3.3 V rail", INK), ("D10 · “next” button", GREEN),
             ("D9 · “previous”, strapping", ORANGE), ("D8 · strapping, not connected", ORANGE),
             ("D7 · UART RX, left free", GREY)]
    for i, ((lt, lc), (rt, rc)) in enumerate(zip(left, right)):
        y = 170 + i * 92
        s.parts.append(f'<circle cx="470" cy="{y}" r="16" fill="{lc}" stroke="white" stroke-width="3"/>')
        s.parts.append(f'<circle cx="730" cy="{y}" r="16" fill="{rc}" stroke="white" stroke-width="3"/>')
        s.text(440, y, lt, 25, lc if lc != GREY else INK, 700 if lc != GREY else 500, anchor="end")
        s.text(760, y, rt, 25, rc if rc != GREY else INK, 700 if rc != GREY else 500, anchor="start")
    legend = [("I²C bus", BLUE), ("Button to GND", GREEN), ("Strapping: high at reset", ORANGE), ("Free", GREY)]
    x = 40
    for t, c in legend:
        s.parts.append(f'<circle cx="{x + 14}" cy="855" r="14" fill="{c}"/>')
        s.text(x + 38, 855, t, 24, INK, 500, anchor="start")
        x += 140 + len(t) * 13
    s.save("V-s19-1")


# ── B4 ───────────────────────────────────────────────────────────────────
def v_s22():
    s = Svg(1200, 900)
    y = lambda v: 820 - v * 110                      # 0 V at the bottom, 6.5 V near the top
    cols = [("VDD (main)", 300, 1.7, 2.0, 2.2), ("VLED+ (LEDs)", 800, 3.1, 5.0, 6.0)]
    for name, x, lo, hi, amax in cols:
        s.text(x + 100, 60, name, 34, INK, 700)
        s.rect(x, y(6.5), 200, y(0) - y(6.5), fill=PALE2, stroke="#C9DCEA", r=8)
        s.rect(x, y(hi), 200, y(lo) - y(hi), fill=GREEN_BG, stroke=GREEN, sw=4, r=4)
        s.line(x - 10, y(amax), x + 210, y(amax), color=RED, sw=5, head=False)
        s.text(x - 14, (y(hi) + y(lo)) / 2, f"recommended\n{lo}–{hi} V", 26, GREEN, 700, anchor="end")
        s.text(x + 214, y(amax), f"absolute max\n{amax} V", 26, RED, 700, anchor="start")
        s.text(x + 100, 850, "0 V", 24, GREY, 600)
    s.line(290, y(3.3), 510, y(3.3), color=RED, sw=4, dash="12 8", head=False)
    s.text(514, y(3.3), "3.3 V would\nexceed it", 26, RED, 700, anchor="start")
    s.save("V-s22-1")


def v_s23():
    s = Svg(1200, 900)
    rows = [("Works on shared 3.3 V bus", "3", "0 → 0", "2 → 6", "2 → 6"),
            ("Hand solderable", "3", "2 → 6", "2 → 6", "0 → 0"),
            ("Height", "2", "1 → 2", "1 → 2", "2 → 4"),
            ("Price", "1", "1 → 1", "2 → 2", "0 → 0"),
            ("Stock", "2", "1 → 2", "1 → 2", "1 → 2"),
            ("Total", "", "11\ndisqualified", "18", "12")]
    zero = (RED_BG, RED, RED)
    win = (GREEN_BG, GREEN, GREEN)
    fills = [[NORM, NORM, zero, NORM, NORM], [NORM, NORM, NORM, NORM, zero], [NORM] * 5, [NORM] * 5, [NORM] * 5,
             [(PALE, BLUE, BLUE), (PALE, BLUE, BLUE), zero, win, (PALE, BLUE, BLUE)]]
    table(s, 10, 40, [400, 150, 210, 200, 220], 108, ["Criterion", "Weight", "Green", "Black", "Bare chip"],
          rows, fills, size=28, head_size=30)
    s.save("V-s23-1")


# ── B5 ───────────────────────────────────────────────────────────────────
def v_s25():
    s = Svg(1200, 900)
    y = lambda v: 820 - v * 220
    x, w = 300, 360
    bands = [(2.475, 3.3, GREEN_BG, GREEN, "HIGH\nguaranteed read as 1"),
             (0.825, 2.475, ORANGE_BG, ORANGE, "UNDEFINED\nmay read as 0 or 1"),
             (0.0, 0.825, PALE, BLUE, "LOW\nguaranteed read as 0")]
    for lo, hi, bg, c, lab in bands:
        s.rect(x, y(hi), w, y(lo) - y(hi), fill=bg, stroke=c, sw=3, r=4)
        s.text(x + w / 2, (y(hi) + y(lo)) / 2 + (40 if lo == 0.825 else 0), lab, 26, c, 700)
    for v, lab in [(3.3, "3.3 V"), (2.475, "2.475 V\n0.75 × VDD"), (0.825, "0.825 V\n0.25 × VDD"), (0, "0 V")]:
        s.text(x - 20, y(v), lab, 26, INK, 600, anchor="end")
    s.line(x - 10, y(1.82), x + w + 60, y(1.82), color=RED, sw=6, head=False)
    s.text(x + w + 75, y(1.82), "measured 1.82 V\nidle bus, green module", 30, RED, 700, anchor="start")
    s.save("V-s25-1")


def v_s27():
    s = Svg(1200, 900)
    s.box(250, 60, 700, 190, "Rest of the program\nheart.begin() · heart.readBpm()", fill=BLUE, stroke=BLUE,
          color="white", size=36, weight=700)
    s.line(500, 254, 300, 444)
    s.line(700, 254, 900, 444)
    s.box(60, 450, 480, 230, "In Wokwi\nMockHeartRate\nabout 66 to 78 bpm", fill=GREEN_BG, stroke=GREEN,
          color=GREEN, size=34)
    s.box(660, 450, 480, 230, "On the real watch\nMAX30102 class\nsame two functions", fill=PALE, stroke=BLUE, size=34)
    s.text(600, 800, "the program cannot tell the difference", 34, BLUE, 700)
    s.save("V-s27-1")


def v_s28():
    s = Svg(1600, 720)
    def seq(y, blocks):
        x = 30
        for label, w, kind, note in blocks:
            fill, stroke, color = {"edge": (INK, INK, "white"), "addr": (BLUE, BLUE, "white"),
                                   "ack": (GREEN_BG, GREEN, GREEN), "nack": (ORANGE_BG, ORANGE, ORANGE),
                                   "data": (PALE, BLUE, INK)}[kind]
            s.box(x, y, w, 110, label, fill=fill, stroke=stroke, color=color, size=28, weight=700, r=10)
            s.text(x + w / 2, y + 165, note, 25, GREY, 600)
            x += w + 14
    s.text(30, 50, "1 · Write the register number", 30, INK, 700, anchor="start")
    seq(80, [("START", 190, "edge", "SDA falls,\nSCL high"), ("0x68 + W", 270, "addr", "address,\nwrite bit 0"),
             ("ACK", 150, "ack", "sensor:\n“that's me”"), ("0x3B", 270, "data", "first acceleration\nregister"),
             ("ACK", 150, "ack", "")])
    s.text(30, 410, "2 · Read 14 bytes", 30, INK, 700, anchor="start")
    seq(440, [("Repeated\nSTART", 190, "edge", ""), ("0x68 + R", 270, "addr", "address,\nread bit 1"),
              ("ACK", 150, "ack", ""), ("data × 14", 380, "data", "each followed\nby an ACK"),
              ("NACK", 160, "nack", "“that's\nenough”"), ("STOP", 170, "edge", "SDA rises,\nSCL high")])
    s.save("V-s28-1")


if __name__ == "__main__":
    for fn in (v_s04, v_s07, v_s08, v_s10, v_s12, v_s13, v_s15, v_s16, v_s19, v_s22, v_s23, v_s25, v_s27, v_s28):
        fn()
