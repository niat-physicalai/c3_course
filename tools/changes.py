#!/usr/bin/env python3
"""Update mode — what changed in the reading material since the deck was last built?

  python tools/changes.py 02        # re-digests, compares with manifest.json

Writes deck/build/02/changes.md:
  • changed sections  → the slides that cite them (ONLY these may be edited)
  • new sections      → candidates for a new/extended slide
  • removed sections  → slides citing them must be fixed (validator will fail)
  • unchanged slides  → must stay byte-identical (lock them if you like)
"""
from __future__ import annotations

import _venv  # noqa: F401  (re-runs under .venv if needed)

import subprocess
import sys
from pathlib import Path

from common import ROOT, load_config, module_info, read_json


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    cfg = load_config()
    mod = module_info(cfg, sys.argv[1])
    work = mod["work"]
    man = read_json(work / "manifest.json")
    if not man:
        sys.exit("No manifest.json — this module was never built. Use /deck-build instead.")
    subprocess.run([sys.executable, str(Path(__file__).parent / "digest_module.py"), mod["key"]], check=True)
    digest = read_json(work / "digest.json")
    now = {f"{u['id']}#{s['anchor']}": s["hash"] for u in digest["units"] for s in u["sections"]}
    now_units = {u["id"]: u["hash"] for u in digest["units"]}
    old = {k: v for k, v in man["sections"].items() if "#" in k}

    changed = sorted(k for k in now if k in old and now[k] != old[k])
    added = sorted(k for k in now if k not in old)
    removed = sorted(k for k in old if k not in now)
    new_units = sorted(u for u in now_units if u not in man["units"])
    gone_units = sorted(u for u in man["units"] if u not in now_units)
    changed_units = {u for u in now_units if u in man["units"] and now_units[u] != man["units"][u]}

    hit = set(changed) | set(removed)
    affected = {}
    for sid, srcs in man["slide_sources"].items():
        why = [s for s in srcs if s in hit or ("#" not in s and s in changed_units)]
        if why:
            affected[sid] = why

    md = [f"# Changes since last build — module {mod['key']}", ""]
    if not (changed or added or removed or new_units or gone_units):
        md.append("Nothing changed. The deck is current — do not edit slides.yaml.")
    else:
        md += ["## Slides you MAY edit (and only the bullets tied to the changed source)", ""]
        md += [f"- `{sid}` ← {', '.join(w)}" for sid, w in sorted(affected.items())] or ["- none"]
        md += ["", "## Changed sections", ""] + ([f"- `{k}`" for k in changed] or ["- none"])
        md += ["", "## New sections (consider adding to an existing slide before adding a new one)", ""]
        md += [f"- `{k}`" for k in added] or ["- none"]
        md += ["", "## Removed sections (slides citing these must be repaired)", ""]
        md += [f"- `{k}`" for k in removed] or ["- none"]
        if new_units:
            md += ["", "## New units (need at least one slide each)", ""] + [f"- {u}" for u in new_units]
        if gone_units:
            md += ["", "## Units removed (delete or re-source their slides)", ""] + [f"- {u}" for u in gone_units]
        md += ["", "## Everything else", "", f"{len(man['slides']) - len(affected)} slides are untouched by these "
               "changes and must stay exactly as they are."]
    (work / "changes.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"✓ {len(changed)} changed, {len(added)} new, {len(removed)} removed sections; "
          f"{len(affected)} slide(s) affected → {(work / 'changes.md').relative_to(ROOT)}")


if __name__ == "__main__":
    main()
