"""claude-chart plots for module 01. Run from repo root: .venv/bin/python deck/asset-src/01/charts.py
Numbers come only from the cited sections:
  V-s08-1  A0#worked-example-can-espwatch-last-two-days (estimates from a power model, planned pattern UP-1)
  V-s17-1  A1#how-much-data (example values)
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

OUT = Path("assets/slides/01")
BLUE, LIGHT, INK, GREY, ORANGE = "#006DAF", "#3FB4E5", "#263238", "#6B7680", "#E07B1A"
for _ttf in (Path.home() / ".local/share/fonts/montserrat").glob("Montserrat-*.ttf"):   # static weights
    font_manager.fontManager.addfont(str(_ttf))
FAMILY = "Montserrat" if any("Montserrat" in f.name for f in font_manager.fontManager.ttflist) else "DejaVu Sans"
plt.rcParams.update({"font.family": FAMILY, "font.size": 22, "font.weight": 500, "axes.edgecolor": GREY, "axes.labelcolor": INK,
                     "xtick.color": INK, "ytick.color": INK})


def clean(ax):
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)


def battery():
    cases = ["Best case\n(sleep 1 mA)", "Worst case\n(sleep 3 mA)"]
    screen, hr, sleep = [15.0, 15.0], [1.8, 1.8], [23.5, 70.6]
    totals, days = [40.3, 87.4], [6.0, 2.7]
    fig, ax = plt.subplots(figsize=(16, 9), dpi=100)
    y = [1, 0]
    ax.barh(y, screen, color=LIGHT, height=0.5, label="Screen on")
    ax.barh(y, hr, left=screen, color=ORANGE, height=0.5, label="Heart-rate reading")
    left = [a + b for a, b in zip(screen, hr)]
    ax.barh(y, sleep, left=left, color=BLUE, height=0.5, label="Sleep")
    for yi, t, d in zip(y, totals, days):
        ax.text(t + 1.5, yi, f"{t} mAh/day  →  {d} days", va="center", fontsize=26, fontweight="bold", color=INK)
    ax.set_yticks(y, cases, fontsize=24)
    ax.set_xlim(0, 125)
    ax.set_xlabel("Charge used per day (mAh), estimated", fontsize=22)
    ax.legend(loc="upper right", frameon=False, fontsize=22, ncol=3, bbox_to_anchor=(1, 1.12))
    clean(ax)
    fig.tight_layout()
    fig.savefig(OUT / "V-s08-1.png", facecolor="white")
    print("✓ V-s08-1")


def data_volume():
    labels = ["Option A\nraw optical signal", "Option B\nresults on the watch"]
    vals = [7_200_000, 20_280]
    text = ["7,200,000 bytes (7.2 MB)", "20,280 bytes (about 20 kB)"]
    fig, ax = plt.subplots(figsize=(16, 9), dpi=100)
    bars = ax.bar(labels, vals, color=[GREY, BLUE], width=0.5)
    ax.set_yscale("log")
    ax.set_ylim(1e3, 1e8)
    for b, t in zip(bars, text):
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() * 1.6, t, ha="center", fontsize=26,
                fontweight="bold", color=INK)
    ax.set_ylabel("Bytes per semester (log scale)", fontsize=22)
    ax.tick_params(axis="x", labelsize=24)
    ax.text(0.5, 3e6, "≈ 355×", ha="center", fontsize=40, fontweight="bold", color=ORANGE)
    clean(ax)
    fig.tight_layout()
    fig.savefig(OUT / "V-s17-1.png", facecolor="white")
    print("✓ V-s17-1")


if __name__ == "__main__":
    battery()
    data_volume()
