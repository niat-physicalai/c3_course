#!/usr/bin/env python3
"""Step 1 — split a module's unit markdown into addressable, hashed sections.

  python tools/digest_module.py 02

Writes deck/build/02/:
  digest.json     every section: anchor, text, hash, images  (the ONLY source of truth)
  outline.md      compact anchor list Claude reads first (cheap on tokens)
  curriculum.md   the module's slice of CURRICULUM.md (best-effort match)
"""
from __future__ import annotations

import _venv  # noqa: F401  (re-runs under .venv if needed)

import re
import sys
from pathlib import Path

from common import ROOT, load_config, module_info, norm, sha, slugify, unit_files, unit_id, write_json

IMG_RE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)[^)]*\)|<img[^>]+src=[\"']([^\"']+)[\"']", re.I)
HEAD_RE = re.compile(r"^(#{1,4})\s+(.*?)\s*#*\s*$")


def parse_unit(path: Path) -> dict:
    lines = path.read_text(encoding="utf-8").splitlines()
    sections, cur, in_code, used = [], None, False, {}

    def start(level, heading):
        base = slugify(heading) or "section"
        n = used.get(base, 0)
        used[base] = n + 1
        return {"anchor": base if n == 0 else f"{base}-{n}", "heading": heading,
                "level": level, "lines": []}

    cur = start(0, "(intro)")
    for ln in lines:
        if ln.strip().startswith(("```", "~~~")):
            in_code = not in_code
        m = None if in_code else HEAD_RE.match(ln)
        if m:
            sections.append(cur)
            cur = start(len(m.group(1)), m.group(2).strip())
        else:
            cur["lines"].append(ln)
    sections.append(cur)

    out = []
    for s in sections:
        text = "\n".join(s.pop("lines")).strip()
        if not text and s["heading"] == "(intro)":
            continue
        imgs = []
        for alt, p1, p2 in IMG_RE.findall(text):
            src = p1 or p2
            resolved = (path.parent / src).resolve()
            try:
                rel = str(resolved.relative_to(ROOT))
            except ValueError:
                rel = src
            imgs.append({"alt": alt, "src": src, "path": rel,
                         "exists": resolved.exists() or src.startswith("http")})
        s.update(text=text, hash=sha(norm(text)), words=len(text.split()), images=imgs)
        out.append(s)
    title = next((s["heading"] for s in out if s["level"] == 1), path.stem)
    return {"id": unit_id(path), "file": str(path.relative_to(ROOT)), "title": title,
            "hash": sha(norm(path.read_text(encoding="utf-8"))),
            "words": sum(s["words"] for s in out), "sections": out}


def curriculum_slice(cfg: dict, mod: dict, unit_ids: list[str]) -> str:
    cpath = ROOT / cfg.get("curriculum", "CURRICULUM.md")
    if not cpath.exists():
        return "(CURRICULUM.md not found)"
    lines = cpath.read_text(encoding="utf-8").splitlines()
    keys = [mod["title"].lower(), mod["dir"].lower(), f"module {int(mod['key'])}" if mod["key"].isdigit() else mod["key"]]
    start, level = None, None
    for i, ln in enumerate(lines):
        m = HEAD_RE.match(ln)
        if m and any(k and k in ln.lower() for k in keys):
            start, level = i, len(m.group(1))
            break
    if start is None:   # fall back: every line mentioning a unit id
        hits = [ln for ln in lines if any(re.search(rf"\b{re.escape(u)}\b", ln) for u in unit_ids)]
        return ("(No module heading matched — lines mentioning this module's units:)\n\n" + "\n".join(hits)) if hits \
            else "(No curriculum match found — read CURRICULUM.md manually.)"
    end = len(lines)
    for j in range(start + 1, len(lines)):
        m = HEAD_RE.match(lines[j])
        if m and len(m.group(1)) <= level:
            end = j
            break
    return "\n".join(lines[start:end])


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    cfg = load_config()
    mod = module_info(cfg, sys.argv[1])
    units = [parse_unit(p) for p in unit_files(cfg, mod["dir"])]
    if not units:
        sys.exit(f"No unit .md files in {mod['dir']}")
    digest = {"module": mod["key"], "dir": mod["dir"], "title": mod["title"],
              "total_words": sum(u["words"] for u in units), "units": units}
    write_json(mod["work"] / "digest.json", digest)

    o = [f"# Outline — module {mod['key']}: {mod['title']}",
         f"{len(units)} units, {digest['total_words']} words. Cite sources as `UNIT#anchor`.", ""]
    for u in units:
        o.append(f"## {u['title']}  ({u['words']} words)  `{u['file']}`")
        for s in u["sections"]:
            ind = "  " * max(s["level"] - 1, 0)
            imgs = ", ".join(i["path"] + ("" if i["exists"] else " [MISSING]") for i in s["images"])
            o.append(f"{ind}- `{u['id']}#{s['anchor']}` {s['heading']} ({s['words']}w)" + (f" — imgs: {imgs}" if imgs else ""))
        o.append("")
    (mod["work"] / "outline.md").write_text("\n".join(o), encoding="utf-8")
    (mod["work"] / "curriculum.md").write_text(curriculum_slice(cfg, mod, [u["id"] for u in units]), encoding="utf-8")
    print(f"✓ digest: {len(units)} units, {sum(len(u['sections']) for u in units)} sections, "
          f"{digest['total_words']} words → {mod['work'].relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
