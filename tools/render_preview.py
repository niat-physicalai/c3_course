#!/usr/bin/env python3
"""Step 5 — render a deck to PNGs + one contact sheet so Claude (and you) can eyeball it.

  python tools/render_preview.py 02                 # renders deck/build/02/*.pptx
  python tools/render_preview.py path/to/deck.pptx

Needs LibreOffice (soffice) + pdftoppm (poppler). LibreOffice is closer to Google Slides'
renderer than PowerPoint is, so overflow seen here is a real warning.
Output: deck/build/02/preview/slide-NN.png and contact-sheet.png
"""
from __future__ import annotations

import _venv  # noqa: F401  (re-runs under .venv if needed)

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw

from common import ROOT, load_config, module_info


def render(pptx: Path) -> Path:
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if not soffice or not shutil.which("pdftoppm"):
        sys.exit("Install LibreOffice and poppler (pdftoppm) to render previews.")
    out = pptx.parent / "preview"
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir(parents=True)
    # temp dir next to the output: snap-packaged LibreOffice cannot see the host /tmp
    with tempfile.TemporaryDirectory(dir=out) as td:
        subprocess.run([soffice, "--headless", "--convert-to", "pdf", "--outdir", td, str(pptx)],
                       check=True, capture_output=True)
        pdf = next(Path(td).glob("*.pdf"))
        shutil.copy(pdf, out / "deck.pdf")
        subprocess.run(["pdftoppm", "-png", "-r", "60", str(pdf), str(out / "slide")], check=True)
    pngs = sorted(out.glob("slide-*.png"))
    for i, p in enumerate(pngs, 1):
        p.rename(out / f"slide-{i:02d}.png")
    pngs = sorted(out.glob("slide-*.png"))
    if pngs:
        ims = [Image.open(p) for p in pngs]
        w, h = ims[0].size
        cols = 5
        rows = -(-len(ims) // cols)
        sheet = Image.new("RGB", (cols * (w + 10) + 10, rows * (h + 30) + 10), "white")
        d = ImageDraw.Draw(sheet)
        for i, im in enumerate(ims):
            x, y = 10 + (i % cols) * (w + 10), 10 + (i // cols) * (h + 30)
            sheet.paste(im, (x, y + 20))
            d.text((x, y + 4), f"{i + 1}", fill="black")
        sheet.save(out / "contact-sheet.png")
    print(f"✓ {len(pngs)} slides → {out.relative_to(ROOT) if out.is_relative_to(ROOT) else out}/ (contact-sheet.png, deck.pdf)")
    return out


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    arg = sys.argv[1]
    if arg.endswith(".pptx"):
        render(Path(arg).resolve())
    else:
        mod = module_info(load_config(), arg)
        decks = sorted(mod["work"].glob("*.pptx"))
        if not decks:
            sys.exit("No deck built yet — run tools/build_deck.py first")
        render(decks[-1])
