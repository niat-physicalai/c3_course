"""Shared helpers for deck-kit tools. Run every tool from the course repo root."""
from __future__ import annotations

import fnmatch
import hashlib
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path.cwd()
CONFIG_PATH = ROOT / "deck.config.yaml"


def load_config() -> dict:
    if not CONFIG_PATH.exists():
        sys.exit("deck.config.yaml not found — run tools from the course repo root.")
    return yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))


def module_info(cfg: dict, key: str) -> dict:
    key = str(key).zfill(2) if str(key).isdigit() else str(key)
    mods = cfg["modules"]
    if key not in mods:
        sys.exit(f"Module '{key}' not in deck.config.yaml → modules. Known: {', '.join(mods)}")
    info = dict(mods[key])
    info["key"] = key
    info["work"] = ROOT / cfg.get("output_dir", "deck/build") / key
    info["work"].mkdir(parents=True, exist_ok=True)
    return info


def unit_files(cfg: dict, module_dir: str) -> list[Path]:
    d = ROOT / module_dir
    if not d.is_dir():
        sys.exit(f"Module folder not found: {d}")
    files = sorted(p for p in d.glob("*.md"))
    excl = cfg.get("exclude_units") or []
    return [p for p in files if not any(fnmatch.fnmatch(p.name, pat) for pat in excl)]


def unit_id(path: Path) -> str:
    """'B0-choosing-sensors.md' -> 'B0'; 'REF-version-control.md' -> 'REF-version-control'."""
    stem = path.stem
    m = re.match(r"^([A-Z]\d+|[A-Z])-", stem)
    return m.group(1) if m else stem


def slugify(text: str) -> str:
    """GitHub-style heading anchor."""
    t = text.strip().lower()
    t = re.sub(r"[`*_~\[\]()<>]", "", t)
    t = re.sub(r"[^\w\s-]", "", t)
    return re.sub(r"\s+", "-", t).strip("-")


def sha(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:12]


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[`*_>#|]", " ", text)).strip().lower()


def read_json(p: Path, default=None):
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else default


def write_json(p: Path, data) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


NUM_RE = re.compile(r"(?<![\w.])(\d+(?:[.,]\d+)?)\s*(%|[a-zA-Zµμ°Ω]{0,4})")


def numbers_in(text: str) -> set[str]:
    """Numeric facts (value+unit) — used to catch invented figures."""
    out = set()
    for val, unit in NUM_RE.findall(text):
        val = val.replace(",", ".")
        out.add((val + unit.lower()).strip())
        out.add(val)
    return out
