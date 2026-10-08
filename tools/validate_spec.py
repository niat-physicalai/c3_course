#!/usr/bin/env python3
"""Step 3 — deterministic guard-rails on slides.yaml before anything is built.

  python tools/validate_spec.py 02            # exit 1 on any ERROR

Checks
  ERROR  slide count > max, duplicate ids, unknown kind
  ERROR  a `sources:` anchor that doesn't exist in digest.json  (no invented sources)
  ERROR  a number/figure on a slide that isn't in its cited sections  (no invented specs)
  ERROR  a unit of the module with no slide citing it            (coverage)
  ERROR  a curriculum outcome not covered by any slide           (curriculum match)
  ERROR  a locked slide whose content changed since last build   (no drastic edits)
  ERROR  visual with status existing/generated but file missing
  WARN   bullet whose key words are mostly absent from its sources (possible drift)
  WARN   word/bullet limits, visual ratio below target
"""
from __future__ import annotations

import _venv  # noqa: F401  (re-runs under .venv if needed)

import json
import re
import sys

import yaml

from common import ROOT, load_config, module_info, norm, numbers_in, read_json, sha

KINDS = {"title", "agenda", "section", "image-text", "image-full", "two-images", "bullets", "key-idea", "recap"}
NON_CONTENT = {"title", "agenda", "section", "recap"}
STOP = set("""this that with from into have will your they them their what when where which while also than then
there these those such each been being were very more most must should could would about over under only just
like make makes made using used uses use need needs between before after across every other same some many""".split())


def stem(w):
    for suf in ("ing", "ies", "es", "ed", "s"):
        if len(w) > 5 and w.endswith(suf):
            return w[: -len(suf)]
    return w


def key_words(t):
    return {stem(w) for w in re.findall(r"[a-z][a-z0-9+-]{3,}", t.lower()) if w not in STOP}


def slide_hash(s):
    keep = {k: s.get(k) for k in ("kind", "title", "subtitle", "bullets", "key_idea", "visual", "visual2", "notes")}
    return sha(json.dumps(keep, sort_keys=True, ensure_ascii=False))


def slide_texts(s):
    out = [s.get("title") or "", s.get("subtitle") or "", s.get("key_idea") or ""] + list(s.get("bullets") or [])
    for v in ("visual", "visual2"):
        if isinstance(s.get(v), dict):
            out.append(s[v].get("caption") or "")
    return [t for t in out if t]


def validate(cfg, key, quiet=False):
    mod = module_info(cfg, key)
    work = mod["work"]
    digest = read_json(work / "digest.json")
    if not digest:
        sys.exit("digest.json missing — run tools/digest_module.py first")
    spec = yaml.safe_load((work / "slides.yaml").read_text(encoding="utf-8"))
    lim = cfg.get("limits", {})
    manifest = read_json(work / "manifest.json", {}) or {}

    sec = {f"{u['id']}#{s['anchor']}": s for u in digest["units"] for s in u["sections"]}
    unit_text = {u["id"]: "\n".join(s["heading"] + "\n" + s["text"] for s in u["sections"]) for u in digest["units"]}
    errs, warns = [], []
    slides = spec.get("slides") or []

    if len(slides) > lim.get("max_slides", 30):
        errs.append(f"{len(slides)} slides > max {lim.get('max_slides', 30)}")
    if len(slides) < lim.get("min_slides", 0):
        warns.append(f"only {len(slides)} slides (min {lim.get('min_slides')})")

    seen, cited_units, covered = set(), set(), set()
    content, with_visual = 0, 0
    for s in slides:
        sid = s.get("id", "?")
        tag = f"[{sid}]"
        if sid in seen:
            errs.append(f"{tag} duplicate id")
        seen.add(sid)
        kind = s.get("kind")
        if kind not in KINDS:
            errs.append(f"{tag} unknown kind '{kind}' (use: {', '.join(sorted(KINDS))})")
        covered.update(s.get("covers") or [])

        # ── sources resolve ────────────────────────────────
        srcs = s.get("sources") or []
        src_text = ""
        for a in srcs:
            if a in sec:
                src_text += "\n" + sec[a]["heading"] + "\n" + sec[a]["text"]
                cited_units.add(a.split("#")[0])
            elif a in unit_text:            # whole-unit citation allowed (section/recap slides)
                src_text += "\n" + unit_text[a]
                cited_units.add(a)
            else:
                errs.append(f"{tag} source '{a}' not found in digest (see outline.md for valid anchors)")
        if kind not in NON_CONTENT and not srcs:
            errs.append(f"{tag} content slide without sources")

        # ── grounding: numbers + key words ─────────────────
        if src_text:
            src_nums = numbers_in(src_text)
            src_words = key_words(src_text)
            src_vals = {n for n in src_nums if re.fullmatch(r"[\d.]+", n)}
            for t in slide_texts(s):
                for n in sorted({n for n in numbers_in(t) if re.fullmatch(r"[\d.]+", n)} - src_vals):
                    if re.fullmatch(r"\d", n):      # single digits ("3 steps") are usually structural
                        continue
                    errs.append(f"{tag} figure '{n}' not in cited sources → \"{t[:60]}\"")
            for b in (s.get("bullets") or []) + ([s["key_idea"]] if s.get("key_idea") else []):
                kw = key_words(b)
                if len(kw) >= 3:
                    hit = len(kw & src_words) / len(kw)
                    if hit < 0.5:
                        warns.append(f"{tag} low grounding {hit:.0%} → \"{b[:70]}\" (check wording vs source)")

        # ── limits ─────────────────────────────────────────
        bullets = s.get("bullets") or []
        if len(bullets) > lim.get("max_bullets_per_slide", 4):
            warns.append(f"{tag} {len(bullets)} bullets (max {lim.get('max_bullets_per_slide')})")
        for b in bullets:
            if len(b.split()) > lim.get("max_words_per_bullet", 14):
                warns.append(f"{tag} long bullet ({len(b.split())}w): \"{b[:50]}…\"")
        body_words = sum(len(b.split()) for b in bullets) + len((s.get("key_idea") or "").split())
        if body_words > lim.get("max_words_per_slide", 45):
            warns.append(f"{tag} {body_words} body words (max {lim.get('max_words_per_slide')})")

        # ── visuals ────────────────────────────────────────
        if kind not in NON_CONTENT:
            content += 1
        for vk in ("visual", "visual2"):
            v = s.get(vk)
            if not v:
                continue
            if kind not in NON_CONTENT and vk == "visual":
                with_visual += 1
            st = v.get("status", "todo")
            if st in ("existing", "generated"):
                if not v.get("path") or not (ROOT / v["path"]).exists():
                    errs.append(f"{tag} {vk} status={st} but file missing: {v.get('path')}")
            elif st == "todo" and not (v.get("prompt") or v.get("brief")):
                warns.append(f"{tag} {vk} is todo without prompt/brief")
        if kind in ("image-text", "image-full", "two-images") and not s.get("visual"):
            errs.append(f"{tag} kind {kind} needs a visual")

        # ── locked slides untouched ───────────────────────
        if s.get("locked"):
            old = (manifest.get("slides") or {}).get(sid)
            if old and old != slide_hash(s):
                errs.append(f"{tag} is locked but its content changed since last build — revert or unlock")

    for u in digest["units"]:
        if u["id"] not in cited_units:
            errs.append(f"unit {u['id']} ({u['title']}) is not cited by any slide")
    for o in spec.get("outcomes") or []:
        if o["id"] not in covered:
            errs.append(f"curriculum outcome {o['id']} not covered: {o['text'][:70]}")
    ratio = with_visual / content if content else 1
    if ratio < lim.get("min_visual_ratio", 0):
        warns.append(f"visual ratio {ratio:.0%} < target {lim['min_visual_ratio']:.0%}")

    if not quiet:
        print(f"Module {mod['key']}: {len(slides)} slides, {content} content, visual ratio {ratio:.0%}")
        for e in errs:
            print("  ERROR", e)
        for w in warns:
            print("  WARN ", w)
        print("✓ PASS" if not errs else f"✗ {len(errs)} error(s)")
    return errs, warns


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    e, _ = validate(load_config(), sys.argv[1])
    sys.exit(1 if e else 0)
