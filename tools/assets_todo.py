#!/usr/bin/env python3
"""Step 6 — the asset to-do list, and syncing assets you've dropped in.

  python tools/assets_todo.py 02           # write deck/build/02/ASSETS-TODO.md
  python tools/assets_todo.py 02 --sync    # any todo whose file now exists → status: generated,
                                           # then validate → build the .pptx → render preview + PDF
  python tools/assets_todo.py 02 --sync --no-build   # sync only

Every visual in slides.yaml has an `id` and a `save_to` path. Drop the finished file at
that exact path (any of .png .jpg .gif .svg), run --sync. Nothing else to edit.
"""
from __future__ import annotations

import _venv  # noqa: F401  (re-runs under .venv if needed)

import subprocess
import sys
from pathlib import Path

import yaml

from common import ROOT, load_config, module_info

ROUTES = {
    "claude-svg": "Claude draws it (SVG diagram) — run /deck-assets",
    "claude-gif": "Claude animates it (Python → GIF) — run /deck-assets",
    "claude-chart": "Claude plots it (matplotlib → PNG) — run /deck-assets",
    "user-ai": "You generate it with a free image AI (prompt below)",
    "user-capture": "You capture it (screenshot / screen-recording GIF / photo)",
    "course": "Reuse an existing course asset (path given)",
}
EXTS = (".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp")


def visuals(spec):
    for n, s in enumerate(spec["slides"], 1):
        for k in ("visual", "visual2"):
            if s.get(k):
                yield n, s, k, s[k]


def resolve_drop(v):
    base = v.get("save_to")
    if not base:
        return None
    p = ROOT / base
    cands = [p] + [p.with_suffix(e) for e in EXTS]
    return next((c for c in cands if c.exists()), None)


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    cfg = load_config()
    mod = module_info(cfg, sys.argv[1])
    sp = mod["work"] / "slides.yaml"
    spec = yaml.safe_load(sp.read_text(encoding="utf-8"))

    if "--sync" in sys.argv:
        changed = 0
        for _, s, _, v in visuals(spec):
            if v.get("status") == "todo":
                f = resolve_drop(v)
                if f:
                    v["status"], v["path"] = "generated", str(f.relative_to(ROOT))
                    changed += 1
                    print(f"  ✓ {v['id']} ← {v['path']}")
        if changed:
            sp.write_text(yaml.safe_dump(spec, sort_keys=False, allow_unicode=True, width=110), encoding="utf-8")
        print(f"✓ synced {changed} asset(s)")

    todo = [(n, s, k, v) for n, s, k, v in visuals(spec) if v.get("status") == "todo"]
    done = [(n, s, k, v) for n, s, k, v in visuals(spec) if v.get("status") != "todo"]
    md = [f"# Assets TODO — module {mod['key']}: {mod['title']}", "",
          f"{len(todo)} to make · {len(done)} ready. Drop each file at its **Save to** path "
          f"(any of png/jpg/gif/svg), then run `python3 tools/assets_todo.py {mod['key']} --sync` "
          "(it rebuilds the .pptx, PDF and preview).", "",
          "Free image tools that work well for these prompts: Google Gemini / ImageFX, Microsoft Designer "
          "(Bing Image Creator), Ideogram, Leonardo.ai free tier, Canva free (Magic Media). "
          "Screen-recording GIFs: ScreenToGif (Windows), Kap (macOS), Peek (Linux); shrink with ezgif.com.", ""]
    for route, label in ROUTES.items():
        rows = [t for t in todo if t[3].get("route", "user-ai") == route]
        if not rows:
            continue
        md += [f"## {label}  ({len(rows)})", ""]
        for n, s, k, v in rows:
            md += [f"### ☐ Slide {n} · pic {1 if k == 'visual' else 2} · `{v['id']}` — {s.get('title', '')}",
                   f"- **Type:** {v.get('type', 'image')}   **Aspect:** {v.get('aspect', '16:9')}",
                   f"- **Save to:** `{v.get('save_to', '(missing save_to!)')}`",
                   f"- **Shows:** {v.get('brief') or v.get('alt') or ''}"]
            if v.get("prompt"):
                md += ["- **Prompt:**", "", "  ```", "  " + v["prompt"].strip().replace("\n", "\n  "), "  ```"]
            if v.get("source_ref"):
                md.append(f"- **Grounded in:** {v['source_ref']}")
            md.append("")
    if done:
        md += ["## ✓ Ready", ""] + [f"- Slide {n} `{v['id']}` → `{v.get('path')}`" for n, s, k, v in done]
    out = mod["work"] / "ASSETS-TODO.md"
    out.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"✓ {len(todo)} todo / {len(done)} ready → {out.relative_to(ROOT)}")

    if "--sync" in sys.argv and "--no-build" not in sys.argv:
        sys.stdout.flush()
        tools = Path(__file__).resolve().parent
        for step in ("validate_spec.py", "build_deck.py", "render_preview.py"):
            if subprocess.run([sys.executable, str(tools / step), mod["key"]]).returncode:
                sys.exit(f"✗ stopped: {step} failed — fix slides.yaml and run --sync again")


if __name__ == "__main__":
    main()
