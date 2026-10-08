"""claude-chart plots for module 02. Run from repo root: .venv/bin/python deck/asset-src/02/charts.py
Numbers come only from the cited sections:
  V-s14-1  B2#worked-example-predicting-a-display-update
  V-s17-1  B3#worked-example-hours-or-days-duty-cycling-the-heart-rate-sensor (modelled figures)
  V-s18-1  B3#worked-example-how-many-pull-ups-is-too-many
  V-s24-1  B5#worked-example-three-pull-up-values
  V-s26-1  B5#a-battery-dividers-settling-time (example values)
Every bar is direct-labelled in ink colour; grey marks "the rest", red marks only "over the limit".
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager

OUT = Path("assets/slides/02")
BLUE, LIGHT, INK, GREY, ORANGE, RED = "#006DAF", "#3FB4E5", "#263238", "#6B7680", "#E07B1A", "#D64545"
PALE_GREY = "#DCE3E8"
for _ttf in (Path.home() / ".local/share/fonts/montserrat").glob("Montserrat-*.ttf"):   # static weights
    font_manager.fontManager.addfont(str(_ttf))
FAMILY = "Montserrat" if any("Montserrat" in f.name for f in font_manager.fontManager.ttflist) else "DejaVu Sans"
plt.rcParams.update({"font.family": [FAMILY, "DejaVu Sans"],   # DejaVu fills glyphs Montserrat lacks (τ)
                     "font.size": 22, "font.weight": 600, "axes.edgecolor": GREY,
                     "axes.labelcolor": INK, "xtick.color": INK, "ytick.color": INK})


def clean(ax):
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)


def save(fig, name):
    OUT.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(OUT / f"{name}.png", facecolor="white")
    plt.close(fig)
    print("✓", name)


def bus_time():
    fig, ax = plt.subplots(figsize=(12, 9), dpi=100)
    rows = ["Display\n30 redraws a second", "Two sensors"]
    ax.barh(1, 750, color=BLUE, height=0.5)
    ax.barh(1, 250, left=752, color=PALE_GREY, height=0.5)
    ax.barh(0, 20, color=ORANGE, height=0.5)
    ax.text(375, 1, "750 ms (75%)", ha="center", va="center", fontsize=28, fontweight="bold", color="white")
    ax.text(877, 1.38, "250 ms left", ha="center", va="center", fontsize=22, color=INK)
    ax.text(40, 0, "about 2%", ha="left", va="center", fontsize=28, fontweight="bold", color=INK)
    ax.set_yticks([1, 0], rows, fontsize=24)
    ax.set_xlim(0, 1000)
    ax.set_xlabel("ms of every second on the shared 400 kHz bus", fontsize=22)
    clean(ax)
    save(fig, "V-s14-1")


def runtime():
    fig, ax = plt.subplots(figsize=(16, 7), dpi=100)
    rows = ["Measure continuously", "30 s every 10 minutes", "Only when asked (UP-1)"]
    y = [2, 1, 0]
    ax.barh(2, 5.5 / 24, color=GREY, height=0.5)
    ax.barh(1, 1.8, color=BLUE, height=0.5)
    ax.barh(1, 0.9, left=1.8, color=LIGHT, height=0.5)
    ax.barh(0, 2.7, color=BLUE, height=0.5)
    ax.barh(0, 3.3, left=2.7, color=LIGHT, height=0.5)
    for yi, x, t in [(2, 0.4, "5.5 hours"), (1, 2.85, "1.8 to 2.7 days"), (0, 6.15, "2.7 to 6.0 days")]:
        ax.text(x, yi, t, va="center", fontsize=28, fontweight="bold", color=INK)
    ax.set_yticks(y, rows, fontsize=24)
    ax.set_xlim(0, 7.6)
    ax.set_xlabel("Runtime from 240 mAh usable (days), modelled: worst case to best case", fontsize=21)
    clean(ax)
    save(fig, "V-s17-1")


def pullups():
    fig, ax = plt.subplots(figsize=(12, 9), dpi=100)
    labels = ["One pair\n4.7 kΩ", "Three pairs\n1.57 kΩ", "Four pairs\n1.18 kΩ"]
    vals = [0.7, 2.1, 2.8]
    bars = ax.bar(labels, vals, color=[LIGHT, BLUE, ORANGE], width=0.55)
    for b, v in zip(bars, vals):              # tall bars carry their value inside, clear of the 3 mA line
        inside = v > 1
        ax.text(b.get_x() + b.get_width() / 2, v - 0.28 if inside else v + 0.08, f"{v} mA", ha="center",
                fontsize=28, fontweight="bold", color="white" if inside else INK)
    ax.axhline(3, color=RED, lw=3, ls="--")
    ax.text(-0.3, 3.1, "every device must be able to sink 3 mA", fontsize=22, color=INK, va="bottom")
    ax.set_ylim(0, 3.6)
    ax.set_ylabel("Current to pull the line LOW (mA)", fontsize=22)
    ax.tick_params(axis="x", labelsize=24)
    clean(ax)
    save(fig, "V-s18-1")


def rise_time():
    fig, ax = plt.subplots(figsize=(12, 9), dpi=100)
    labels = ["1.57 kΩ\n(three pairs)", "4.7 kΩ", "10 kΩ"]
    vals = [67, 199, 424]
    bars = ax.bar(labels, vals, color=[LIGHT, BLUE, RED], width=0.55)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 8, f"{v} ns", ha="center", fontsize=28, fontweight="bold",
                color=INK)
    ax.axhline(300, color=INK, lw=3, ls="--")
    ax.text(-0.3, 308, "400 kHz limit: 300 ns", fontsize=22, color=INK, va="bottom")
    ax.set_ylim(0, 480)
    ax.set_ylabel("Rise time, 30% to 70% (ns)", fontsize=22)
    ax.tick_params(axis="x", labelsize=24)
    clean(ax)
    save(fig, "V-s24-1")


def settling():
    fig, ax = plt.subplots(figsize=(12, 9), dpi=100)
    t = np.linspace(0, 320, 400)
    ax.plot(t, 100 * (1 - np.exp(-t / 50)), color=BLUE, lw=4)
    ax.axvline(50, color=GREY, lw=2, ls=":")
    ax.axvline(250, color=ORANGE, lw=3, ls="--")
    ax.text(56, 12, "τ = 50 ms", fontsize=24, color=INK)
    ax.text(244, 40, "settled (about 99%)\nafter 5τ = 250 ms", fontsize=24, fontweight="bold", color=INK, ha="right")
    ax.set_xlim(0, 320)
    ax.set_ylim(0, 108)
    ax.set_xlabel("Time after power-up (ms)", fontsize=22)
    ax.set_ylabel("ADC pin voltage (% of final)", fontsize=22)
    clean(ax)
    save(fig, "V-s26-1")


if __name__ == "__main__":
    bus_time()
    runtime()
    pullups()
    rise_time()
    settling()
