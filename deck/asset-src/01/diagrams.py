"""claude-svg diagrams for module 01 (System Architecture).

Run from the repo root:  .venv/bin/python deck/asset-src/01/diagrams.py
Writes assets/slides/01/V-sNN-N.svg. Every label comes from the slide's cited sections.
Palette and fonts follow the template (Montserrat titles, #006DAF blue, #3FB4E5 light blue).
Arrows meet a box at the centre of the side they touch (two arrows between one pair sit symmetric about it).
"""
from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path("assets/slides/01")
BLUE, LIGHT, INK, GREY = "#006DAF", "#3FB4E5", "#263238", "#6B7680"
PALE, PALE2 = "#E8F4FB", "#F4F8FB"
GREEN, GREEN_BG = "#2E9E5B", "#E7F6EC"
ORANGE, ORANGE_BG = "#E07B1A", "#FDF0E3"
RED, RED_BG = "#D64545", "#FBE9E9"
FONT = "Montserrat, Arial, sans-serif"


class Svg:
    def __init__(self, w=1200, h=900):
        self.w, self.h, self.parts = w, h, []
        self._markers = set()
        self.parts.append(f'<rect width="{w}" height="{h}" fill="white"/>')

    def rect(self, x, y, w, h, fill=PALE, stroke=BLUE, sw=3, r=18, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" '
                          f'stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def text(self, x, y, s, size=30, color=INK, weight=600, anchor="middle", family=FONT):
        lines = s.split("\n")
        y0 = y - (len(lines) - 1) * size * 0.6
        for i, ln in enumerate(lines):
            self.parts.append(f'<text x="{x}" y="{y0 + i * size * 1.2:.0f}" font-family="{family}" font-size="{size}" '
                              f'font-weight="{weight}" fill="{color}" text-anchor="{anchor}" '
                              f'dominant-baseline="middle">{escape(ln)}</text>')

    def box(self, x, y, w, h, label, fill=PALE, stroke=BLUE, size=32, color=INK, weight=600, dash=None, r=18):
        self.rect(x, y, w, h, fill, stroke, r=r, dash=dash)
        self.text(x + w / 2, y + h / 2, label, size, color, weight)

    def line(self, x1, y1, x2, y2, color=BLUE, sw=4, dash=None, head=True, both=False):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        mid = "arrow-" + color.strip("#")
        self._marker(color)
        me = f' marker-end="url(#{mid})"' if head else ""
        ms = f' marker-start="url(#{mid}s)"' if both else ""
        self.parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{sw}"{d}{me}{ms}/>')

    def _marker(self, color):
        mid = "arrow-" + color.strip("#")
        if mid in self._markers:
            return
        self._markers.add(mid)
        self.parts.insert(0, f'<defs><marker id="{mid}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" '
                             f'markerHeight="6" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{color}"/></marker>'
                             f'<marker id="{mid}s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="6" '
                             f'markerHeight="6" orient="auto"><path d="M10,0 L0,5 L10,10 z" fill="{color}"/></marker></defs>')

    def save(self, name):
        OUT.mkdir(parents=True, exist_ok=True)
        body = "\n".join(self.parts)
        (OUT / f"{name}.svg").write_text(
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" width="{self.w}" '
            f'height="{self.h}">\n{body}\n</svg>\n', encoding="utf-8")
        print("✓", name)


def table(s, x, y, col_w, row_h, header, rows, fills=None, size=28, head_size=28):
    """Simple rounded-card table: header row in blue, body rows in pale cards."""
    cx = x
    for i, hd in enumerate(header):
        s.box(cx, y, col_w[i] - 10, row_h, hd, fill=BLUE, stroke=BLUE, size=head_size, color="white", weight=700, r=12)
        cx += col_w[i]
    for r, row in enumerate(rows):
        cy = y + (r + 1) * (row_h + 12)
        cx = x
        for i, cell in enumerate(row):
            fill, stroke, color = (fills[r][i] if fills else (PALE2, "#C9DCEA", INK))
            s.box(cx, cy, col_w[i] - 10, row_h, cell, fill=fill, stroke=stroke, size=size, color=color, r=12)
            cx += col_w[i]


# ── A0 ───────────────────────────────────────────────────────────────────
def v_s04():
    s = Svg(1200, 900)
    steps = ["Problem statement", "User and their day", "Environment",
             "Requirements: what + how well", "How each is checked", "Not in version 1"]
    y = 40
    for i, st in enumerate(steps):
        last = i == len(steps) - 1
        s.box(220, y, 760, 100, st, fill=ORANGE_BG if last else PALE, stroke=ORANGE if last else BLUE, size=36)
        if not last:
            s.line(600, y + 102, 600, y + 140)
        y += 145
    s.save("V-s04-1")


def v_s05():
    s = Svg(1200, 900)
    cards = [("Accuracy", "±5 bpm, sitting still"), ("Response time", "within 15 s"),
             ("Battery life", "≥ 2 days, UP-1"), ("Cost", "≤ ₹2,500 at 10"),
             ("Size and weight", "≤ 45 × 45 × 16 mm"), ("Lifetime", "1 year of daily wear"),
             ("Serviceability", "battery replaceable")]
    w, h = 540, 190
    for i, (name, ex) in enumerate(cards):
        col, row = i % 2, i // 2
        x = 50 + col * 570 if i < 6 else 330
        y = 30 + row * 215
        s.rect(x, y, w, h, fill=PALE, stroke=BLUE)
        s.text(x + w / 2, y + 70, name, 38, BLUE, 700)
        s.text(x + w / 2, y + 135, ex, 30, INK, 500)
    s.save("V-s05-1")


def v_s06():
    s = Svg(1200, 900)
    s.box(80, 50, 1040, 150, "“The battery should last a long time.”", fill=RED_BG, stroke=RED, size=38)
    s.text(600, 245, "no number, no condition", 30, RED, 600)
    s.line(600, 280, 600, 350, color=GREY)
    parts = [("ID", "NFR-03"), ("shall", "shall run ≥ 2 days\nbetween charges"),
             ("number + condition", "with usage\npattern UP-1"), ("check", "analysis;\ntest after build")]
    x = 40
    for lab, val in parts:
        s.box(x, 380, 270, 250, val, fill=GREEN_BG, stroke=GREEN, size=26)
        s.text(x + 135, 680, lab, 30, GREEN, 700)
        x += 285
    s.text(600, 800, "a number, a condition, a check method", 32, BLUE, 700)
    s.save("V-s06-1")


def v_s09():
    s = Svg(1200, 900)
    rows = [("SpO2 readings", "Never, unless certified"), ("Phone app", "Version 2"),
            ("Waterproofing beyond splashes", "Version 2"), ("Continuous heart-rate logging", "After the power budget")]
    fills = [[(PALE2, "#C9DCEA", INK), (RED_BG, RED, RED)], [(PALE2, "#C9DCEA", INK), (ORANGE_BG, ORANGE, ORANGE)],
             [(PALE2, "#C9DCEA", INK), (ORANGE_BG, ORANGE, ORANGE)], [(PALE2, "#C9DCEA", INK), (PALE, BLUE, BLUE)]]
    table(s, 40, 70, [640, 480], 140, ["Not in version 1", "Where it goes"], rows, fills, size=32, head_size=34)
    s.save("V-s09-1")


# ── A1 ───────────────────────────────────────────────────────────────────
def v_s12():
    s = Svg(1600, 900)
    s.box(600, 350, 400, 180, "esp_watch", fill=BLUE, stroke=BLUE, size=48, color="white", weight=700, r=24)
    s.box(600, 40, 400, 110, "Wearer", size=36)
    s.line(700, 152, 700, 345)
    s.text(680, 250, "button presses", 30, GREY, 500, anchor="end")
    s.line(900, 348, 900, 157)
    s.text(920, 250, "time, weather,\nsteps, heart rate", 30, GREY, 500, anchor="start")
    s.box(30, 385, 290, 110, "USB charger", size=34)
    s.line(322, 440, 595, 440)
    s.text(458, 400, "charging power", 28, GREY, 500)
    s.box(600, 740, 400, 110, "Wrist / skin", size=36)
    s.line(800, 738, 800, 535)
    s.text(820, 640, "pulse, motion", 30, GREY, 500, anchor="start")
    s.box(1240, 385, 340, 110, "WiFi router", size=34)
    s.line(1005, 440, 1235, 440, both=True)
    s.text(1120, 495, "once, at\nfirst boot", 28, ORANGE, 700)
    s.box(1230, 700, 360, 140, "Time and weather\nservices", fill=PALE2, stroke=GREY, size=32)
    s.line(1410, 498, 1410, 695, color=GREY)
    s.text(1430, 600, "internet", 28, GREY, 500, anchor="start")
    s.save("V-s12-1")


def v_s13():
    s = Svg(1200, 900)
    s.rect(20, 20, 1160, 760, fill="white", stroke=GREY, sw=3, r=28)
    s.text(600, 60, "Enclosure: 3D-printed case", 30, GREY, 700)
    s.box(60, 110, 330, 200, "Sensing\nMAX30102\nMPU-6050", size=32)
    s.box(435, 110, 330, 200, "Processing\nXIAO ESP32-C3", fill=BLUE, stroke=BLUE, color="white", size=32)
    s.box(810, 110, 330, 200, "Local UI\nSSD1306\n2 buttons", size=32)
    s.line(392, 210, 430, 210)
    s.line(767, 210, 805, 210)
    s.box(60, 420, 500, 240, "Power\nLiPo cell, slide switch,\ncharger + 3.3 V regulator", size=30)
    s.box(640, 420, 500, 240, "Connectivity\nWiFi radio,\nexternal antenna", size=30)
    s.line(310, 418, 600, 312, color=GREY, head=False)
    s.line(890, 418, 600, 312, color=GREY, head=False)
    s.box(260, 805, 680, 80, "Backend: none of its own", fill=ORANGE_BG, stroke=ORANGE, size=32, color=ORANGE, dash="14 10")
    s.save("V-s13-1")


def v_s14():
    s = Svg(1200, 900)
    rows = [("FR-02 heart rate", "Sensing"), ("NFR-03 battery", "Power"),
            ("NFR-07 thickness", "Enclosure"), ("FR-04 semester trend", "none: orphan")]
    norm = (PALE2, "#C9DCEA", INK)
    fills = [[norm, (PALE, BLUE, BLUE)]] * 3 + [[(RED_BG, RED, RED), (RED_BG, RED, RED)]]
    table(s, 40, 80, [640, 480], 150, ["Requirement", "Owner"], rows, fills, size=34, head_size=36)
    s.save("V-s14-1")


def v_s15():
    s = Svg(1200, 900)
    s.box(300, 40, 600, 170, "FR-04 semester trend\norphan", fill=RED_BG, stroke=RED, size=36, color=RED)
    opts = ["Add a\nbackend", "Store on\nthe watch", "Move out\nof version 1"]
    for i, o in enumerate(opts):
        x = 40 + i * 390
        s.line(600, 212, x + 175, 440, color=GREY)
        s.box(x, 450, 350, 240, f"{i + 1}\n{o}", size=36, fill=PALE if i != 1 else GREEN_BG,
              stroke=BLUE if i != 1 else GREEN)
    s.text(600, 790, "the choice depends on how much data", 32, BLUE, 700)
    s.save("V-s15-1")


def v_s16():
    s = Svg(1200, 900)
    cols = [("Device", "Nothing changes", GREEN, GREEN_BG), ("Phone", "History stops\nupdating", ORANGE, ORANGE_BG),
            ("Server", "Buffer, or\ndata is lost", RED, RED_BG)]
    for i, (name, drop, c, bg) in enumerate(cols):
        x = 40 + i * 385
        s.box(x, 60, 350, 150, name, fill=BLUE, stroke=BLUE, color="white", size=44, weight=700)
        s.box(x, 420, 350, 260, drop, fill=bg, stroke=c, color=c, size=36)
        s.line(x + 175, 215, x + 175, 275, color=GREY, head=False)
        s.line(x + 175, 355, x + 175, 410, color=GREY)
    s.text(600, 315, "when the link drops", 34, GREY, 700)
    s.save("V-s16-1")


def v_s18():
    s = Svg(1200, 900)
    routes = [("No connection", PALE, BLUE), ("BLE to a phone", PALE, BLUE), ("WiFi direct", GREEN_BG, GREEN)]
    for i, (r, bg, c) in enumerate(routes):
        x = 40 + i * 385
        s.box(x, 150, 350, 330, r, fill=bg, stroke=c, size=38, weight=700, color=c if c == GREEN else INK)
    s.box(810, 560, 350, 170, "esp_watch:\nonce, at first boot", fill="white", stroke=GREEN, size=30, color=GREEN, dash="12 8")
    s.line(985, 485, 985, 555, color=GREEN)
    s.save("V-s18-1")


# ── A2 ───────────────────────────────────────────────────────────────────
def v_s20():
    s = Svg(1200, 900)
    s.box(80, 60, 320, 140, "BOOT", fill=BLUE, stroke=BLUE, color="white", size=44, weight=700)
    s.box(80, 400, 320, 140, "AWAKE", fill=BLUE, stroke=BLUE, color="white", size=44, weight=700)
    s.box(780, 400, 340, 140, "MEASURING", fill=BLUE, stroke=BLUE, color="white", size=40, weight=700)
    s.line(240, 205, 240, 395)
    s.text(290, 300, "done", 30, GREY, 600, anchor="start")
    s.line(405, 440, 775, 440)
    s.text(590, 405, "request HR", 28, GREY, 600)
    s.line(775, 500, 405, 500)
    s.text(590, 535, "result / abort", 28, GREY, 600)
    # gaps (dashed)
    s.box(780, 60, 340, 140, "WiFi fails?", fill="white", stroke=RED, color=RED, size=34, dash="14 10")
    s.line(405, 130, 775, 130, color=RED, dash="14 10")
    s.box(80, 700, 320, 140, "ASLEEP?", fill="white", stroke=RED, color=RED, size=36, dash="14 10")
    s.line(240, 545, 240, 695, color=RED, dash="14 10")
    s.box(560, 690, 600, 160, "Overlays: low battery,\ncharging, fault", fill=PALE2, stroke=GREY, size=32, color=GREY)
    s.save("V-s20-1")


def v_s21():
    s = Svg(1200, 900)
    rows = [("Taken off mid-reading", "No contact", "Degrade"), ("Sensor stops responding", "--", "Degrade"),
            ("No WiFi at first boot", "no time", "Degrade"), ("Battery reaches cut-off", "Screen goes dark", "Hard stop")]
    norm = (PALE2, "#C9DCEA", INK)
    deg = (GREEN_BG, GREEN, GREEN)
    fills = [[norm, norm, deg]] * 3 + [[norm, norm, (RED_BG, RED, RED)]]
    table(s, 20, 70, [520, 380, 280], 140, ["Failure", "Wearer sees", "Response"], rows, fills, size=30, head_size=32)
    s.save("V-s21-1")


def v_s24():
    s = Svg(1200, 900)
    rows = [("Decision", "WiFi only once, at first boot", BLUE),
            ("Options", "always on · BLE to a phone app · once at boot", GREY),
            ("Why", "battery is dominated by what runs all day", GREEN),
            ("Costs", "time never corrected, weather goes stale", ORANGE)]
    s.rect(30, 30, 1140, 840, fill=PALE2, stroke=BLUE, r=28)
    for i, (k, v, c) in enumerate(rows):
        y = 70 + i * 200
        s.box(70, y, 260, 160, k, fill=c, stroke=c, color="white", size=36, weight=700, r=14)
        s.box(350, y, 780, 160, v, fill="white", stroke="#C9DCEA", size=30, r=14)
    s.save("V-s24-1")


# ── REF ──────────────────────────────────────────────────────────────────
def v_s25():
    s = Svg(1200, 900)
    rows = [("Requirements checkable?", "Specification", "ID, number, test"),
            ("Architecture coherent?", "Allocation table", "all owned, all parts used"),
            ("Circuit logic works?", "Wokwi", "expected serial output"),
            ("Schematic consistent?", "KiCad ERC", "zero errors"),
            ("Board manufacturable?", "KiCad DRC + DFM", "zero DRC errors"),
            ("Firmware matches design?", "State diagram", "every arrow in code")]
    table(s, 10, 30, [420, 360, 410], 105, ["Question", "Tool", "Pass"], rows, size=26, head_size=30)
    s.save("V-s25-1")


def v_s27():
    s = Svg(1200, 900)
    s.box(60, 330, 400, 200, "Application\ncode", fill=BLUE, stroke=BLUE, color="white", size=40, weight=700)
    s.box(720, 90, 420, 200, "MAX30102\nnot in Wokwi", fill="white", stroke=RED, color=RED, size=36, dash="14 10")
    s.box(720, 570, 420, 200, "Mock sensor\nrealistic readings", fill=GREEN_BG, stroke=GREEN, color=GREEN, size=36)
    s.line(465, 430, 715, 190, color=RED, dash="14 10", head=False)
    s.line(465, 430, 715, 670, color=GREEN)
    s.text(600, 850, "the code cannot tell the difference", 32, BLUE, 700)
    s.save("V-s27-1")


def v_s28():
    s = Svg(1200, 900)
    tree = ["my-product/", "├── README.md", "├── .gitignore", "├── 01-spec-and-architecture/",
            "├── 04-schematic-and-pcb/", "├── 07-mechanical/", "└── 08-manufacturing/"]
    s.rect(30, 30, 1140, 470, fill=PALE2, stroke=BLUE, r=24)
    for i, t in enumerate(tree):
        s.text(80, 85 + i * 62, t, 34, INK if i else BLUE, 600 if i else 700, anchor="start",
               family="DejaVu Sans Mono, Courier New, monospace")
    s.box(30, 560, 380, 120, "pcb changes", fill=RED_BG, stroke=RED, color=RED, size=34)
    s.line(415, 620, 495, 620, color=GREY)
    s.box(500, 560, 670, 120, "Widen 3V3 track to 0.6 mm;\nDRC clean", fill=GREEN_BG, stroke=GREEN, color=GREEN, size=30)
    s.text(600, 760, "a message that says what changed", 32, BLUE, 700)
    s.save("V-s28-1")


def v_s29():
    s = Svg(1200, 900)
    items = [("Git tag", "v0.1.0"), ("Title block", "0.1.0"), ("Silkscreen", "0.1.0")]
    for i, (k, v) in enumerate(items):
        x = 40 + i * 395
        s.rect(x, 250, 330, 330, fill=PALE, stroke=BLUE)
        s.text(x + 165, 340, k, 38, BLUE, 700)
        s.text(x + 165, 470, v, 54, INK, 700)
        if i < 2:
            s.text(x + 362, 415, "=", 64, GREY, 700)
    s.text(600, 700, "one revision, three places", 34, GREY, 700)
    s.save("V-s29-1")


if __name__ == "__main__":
    for fn in (v_s04, v_s05, v_s06, v_s09, v_s12, v_s13, v_s14, v_s15, v_s16, v_s18,
               v_s20, v_s21, v_s24, v_s25, v_s27, v_s28, v_s29):
        fn()
