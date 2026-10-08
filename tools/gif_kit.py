"""Tiny helpers Claude uses when it writes an animated-GIF asset script.

Each GIF asset gets its own script in deck/asset-src/<module>/<asset-id>.py so it can be
re-run after content changes. Pattern:

    import sys; sys.path.insert(0, "tools")
    from gif_kit import Canvas, save_gif
    frames = []
    for t in range(24):
        c = Canvas(960, 540)                  # 16:9, white background
        c.box(80, 200, 220, 120, "Sensor", fill="#E8F1FF")
        c.arrow(300, 260, 300 + t * 10, 260)
        frames.append(c.img)
    save_gif(frames, "assets/slides/02/V-s07-1.gif", ms=80)

Keep GIFs short (≤ 4 s loop, ≤ 40 frames, ≤ 960 px wide) so they stay small and
Google Slides plays them smoothly.
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def _font(size):
    for name in ("DejaVuSans.ttf", "Arial.ttf", "LiberationSans-Regular.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


class Canvas:
    def __init__(self, w=960, h=540, bg="white"):
        self.img = Image.new("RGB", (w, h), bg)
        self.d = ImageDraw.Draw(self.img)

    def box(self, x, y, w, h, label="", fill="#E8F1FF", outline="#1F4E9E", size=26, radius=14):
        self.d.rounded_rectangle([x, y, x + w, y + h], radius=radius, fill=fill, outline=outline, width=3)
        if label:
            f = _font(size)
            tw, th = self.d.textbbox((0, 0), label, font=f)[2:]
            self.d.text((x + (w - tw) / 2, y + (h - th) / 2), label, fill="#1A1A1A", font=f)

    def text(self, x, y, s, size=24, color="#1A1A1A"):
        self.d.text((x, y), s, fill=color, font=_font(size))

    def arrow(self, x1, y1, x2, y2, color="#1F4E9E", width=5):
        import math
        self.d.line([x1, y1, x2, y2], fill=color, width=width)
        a = math.atan2(y2 - y1, x2 - x1)
        for s in (2.6, -2.6):
            self.d.line([x2, y2, x2 - 16 * math.cos(a + s / 6), y2 - 16 * math.sin(a + s / 6)], fill=color, width=width)

    def dot(self, x, y, r=10, color="#E67E22"):
        self.d.ellipse([x - r, y - r, x + r, y + r], fill=color)


def save_gif(frames, path, ms=80, loop=0, hold_last=10):
    """Save frames as an optimised, looping GIF (last frame held a little longer)."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    frames = list(frames) + [frames[-1]] * hold_last
    pal = [f.convert("P", palette=Image.ADAPTIVE, colors=128) for f in frames]
    pal[0].save(p, save_all=True, append_images=pal[1:], duration=ms, loop=loop, optimize=True, disposal=2)
    print(f"✓ {p} ({len(frames)} frames, {p.stat().st_size / 1e6:.2f} MB)")
