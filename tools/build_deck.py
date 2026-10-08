#!/usr/bin/env python3
"""Step 4 — render slides.yaml into a Google-Slides-safe .pptx using the template.

  python tools/build_deck.py 02            # validates first; refuses on errors
  python tools/build_deck.py 02 --force    # build anyway (draft review only)

Output: deck/build/02/<key>-<slug>.pptx  + manifest.json (hashes for change tracking)

Google Slides safety rules applied here (so the deck doesn't shift after import):
  • no SVG/EMF in the file — SVG rasterised to PNG, oversized images downscaled
  • text auto-fit OFF + explicit sizes (Slides ignores PowerPoint shrink-on-overflow)
  • bullets as plain buChar, no SmartArt, no charts, no grouped shapes created
  • images fitted inside boxes by aspect ratio (never stretched, never cropped)
  • unresolved assets become a visible dashed "ASSET TODO" box, never a silent gap
"""
from __future__ import annotations

import _venv  # noqa: F401  (re-runs under .venv if needed)

import copy
import io
import re
import shutil
import subprocess
import sys
from pathlib import Path

import yaml
from lxml import etree
from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_LINE_DASH_STYLE
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_AUTO_SIZE, PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches, Pt

from common import ROOT, load_config, module_info, read_json, write_json

R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"


# ─────────────────────────── template helpers ───────────────────────────
def layout_by_name(prs, name):
    for master in prs.slide_masters:      # Google Slides exports spread layouts over several masters
        for lay in master.slide_layouts:
            if lay.name == name:
                return lay
    raise SystemExit(f"Layout '{name}' not in template — check template.map.yaml (see template-inventory.md)")


def clone_slide(prs, src):
    """Duplicate a designed template slide (shapes, background, images)."""
    new = prs.slides.add_slide(src.slide_layout)
    for shp in list(new.shapes):
        shp._element.getparent().remove(shp._element)
    rid_map = {}
    for rel in src.part.rels.values():
        if "notesSlide" in rel.reltype or "slideLayout" in rel.reltype:
            continue
        if rel.is_external:
            nid = new.part.relate_to(rel.target_ref, rel.reltype, is_external=True)
        else:
            nid = new.part.relate_to(rel.target_part, rel.reltype)
        rid_map[rel.rId] = nid
    tree = new.shapes._spTree
    for el in src.shapes._spTree.iterchildren():
        if etree.QName(el).localname in ("nvGrpSpPr", "grpSpPr"):
            continue
        tree.append(copy.deepcopy(el))
    src_bg = src._element.cSld.find(qn("p:bg"))
    if src_bg is not None:
        new._element.cSld.insert(0, copy.deepcopy(src_bg))
    for el in new._element.iter():
        for attr in list(el.attrib):
            if attr.startswith("{%s}" % R_NS) and el.attrib[attr] in rid_map:
                el.attrib[attr] = rid_map[el.attrib[attr]]
    return new


def delete_slide(prs, slide):
    sldIdLst = prs.slides._sldIdLst
    for sldId in list(sldIdLst):
        if prs.part.related_part(sldId.rId) is slide.part:
            prs.part.drop_rel(sldId.rId)
            sldIdLst.remove(sldId)
            return


def find_target(slide, ref):
    """ref = placeholder idx (int) or shape name (str)."""
    if ref is None:
        return None
    if isinstance(ref, int):
        for ph in slide.placeholders:
            if ph.placeholder_format.idx == ref:
                return ph
        return None
    for sh in slide.shapes:
        if sh.name == ref:
            return sh
    return None


def box_of(shape):
    return [Emu(shape.left).inches, Emu(shape.top).inches, Emu(shape.width).inches, Emu(shape.height).inches]


def remove(shape):
    if shape is not None:
        shape._element.getparent().remove(shape._element)


# ─────────────────────────── text helpers ───────────────────────────
def set_bullet(p, on=True):
    pPr = p._p.get_or_add_pPr()
    for tag in ("a:buNone", "a:buChar", "a:buAutoNum"):
        for el in pPr.findall(qn(tag)):
            pPr.remove(el)
    if on:
        pPr.set("marL", str(Inches(0.3)))
        pPr.set("indent", str(-Inches(0.3)))
        bu = etree.SubElement(pPr, qn("a:buChar"))
        bu.set("char", "•")
    else:
        etree.SubElement(pPr, qn("a:buNone"))


def fill_text(shape, lines, size=None, bullets=None, bold=None, align=None, color=None, font=None, cfg_compat=None,
              line_spacing=None, space_after=None):
    """Replace text, keeping the template's first-paragraph / first-run formatting."""
    tf = shape.text_frame
    if isinstance(lines, str):
        lines = [lines]
    p0 = tf.paragraphs[0]
    pPr = copy.deepcopy(p0._p.pPr) if p0._p.pPr is not None else None
    r0 = p0.runs[0] if p0.runs else None
    rPr = copy.deepcopy(r0._r.find(qn("a:rPr"))) if r0 is not None and r0._r.find(qn("a:rPr")) is not None else None
    for p in list(tf.paragraphs)[1:]:
        p._p.getparent().remove(p._p)
    for r in list(p0._p):
        if etree.QName(r).localname in ("r", "br", "fld"):
            p0._p.remove(r)
    for i, line in enumerate(lines):
        p = p0 if i == 0 else tf.add_paragraph()
        if i > 0 and pPr is not None:
            if p._p.pPr is not None:
                p._p.remove(p._p.pPr)
            p._p.insert(0, copy.deepcopy(pPr))
        run = p.add_run()
        run.text = line
        if rPr is not None:
            run._r.insert(0, copy.deepcopy(rPr))
            for extra in run._r.findall(qn("a:rPr"))[1:]:
                run._r.remove(extra)
        if size:
            run.font.size = Pt(size)
        if bold is not None:
            run.font.bold = bold
        if color:
            run.font.color.rgb = RGBColor.from_string(color)
        if font:
            run.font.name = font
        if bullets is not None:
            set_bullet(p, bullets)
        if align:
            p.alignment = align
        if line_spacing:
            p.line_spacing = line_spacing          # multiple of single spacing
        if space_after and i < len(lines) - 1:
            p.space_after = Pt(space_after)        # gap between bullets
    if (cfg_compat or {}).get("disable_autofit", True):
        tf.auto_size = MSO_AUTO_SIZE.NONE
        bp = tf._txBody.find(qn("a:bodyPr"))
        for el in list(bp):
            if etree.QName(el).localname in ("normAutofit", "spAutoFit"):
                bp.remove(el)
    tf.word_wrap = True


def textbox(slide, box, lines, **kw):
    tb = slide.shapes.add_textbox(*[Inches(v) for v in box])
    fill_text(tb, lines, **kw)
    return tb


def overflow_warning(lines, box, size_pt, line_spacing=1.0, space_after=0):
    if not box or not size_pt:
        return None
    w, h = box[2], box[3]
    cpl = max(1, int(w * 72 / (size_pt * 0.52)))
    need = (sum(max(1, -(-len(l) // cpl)) for l in lines) * size_pt * 1.25 * (line_spacing or 1.0)
            + max(0, len(lines) - 1) * (space_after or 0)) / 72
    return f"text may overflow ({need:.1f}in needed, {h:.1f}in box)" if need > h * 1.02 else None


# ─────────────────────────── image helpers ───────────────────────────
def prepare_image(path: Path, cache: Path, compat: dict):
    """Return a Slides-safe raster path (PNG/JPG/GIF) or None."""
    cache.mkdir(parents=True, exist_ok=True)
    ext = path.suffix.lower()
    maxpx = compat.get("max_image_px", 1920)
    if ext == ".svg":
        out = cache / (path.stem + ".png")
        if not out.exists() or out.stat().st_mtime < path.stat().st_mtime:
            scale = compat.get("svg_to_png_scale", 2)
            try:
                import cairosvg
                cairosvg.svg2png(url=str(path), write_to=str(out), scale=scale, background_color="white")
            except ImportError:
                exe = shutil.which("rsvg-convert") or shutil.which("inkscape")
                if not exe:
                    print(f"  ! cannot rasterise {path} — pip install cairosvg")
                    return None
                args = [exe, "-z", str(scale), "-b", "white", "-o", str(out), str(path)] if "rsvg" in exe \
                    else [exe, str(path), f"--export-filename={out}", f"--export-dpi={96 * scale}", "--export-background=white"]
                subprocess.run(args, check=True)
        path = out
    if ext in (".png", ".jpg", ".jpeg", ".svg"):
        im = Image.open(path)
        if max(im.size) > maxpx:
            out = cache / (path.stem + "_s" + (".png" if path.suffix.lower() == ".png" else ".jpg"))
            im.thumbnail((maxpx, maxpx))
            if out.suffix == ".jpg" and im.mode != "RGB":
                im = im.convert("RGB")
            im.save(out, quality=90)
            return out
        return path
    if ext == ".gif":
        mb = path.stat().st_size / 1e6
        if mb > compat.get("max_gif_mb", 8):
            print(f"  ! {path.name} is {mb:.1f} MB — Google Slides may reject it; shrink it (ezgif.com/optimize)")
        return path
    if ext in (".webp", ".bmp", ".tif", ".tiff"):
        out = cache / (path.stem + ".png")
        Image.open(path).save(out)
        return out
    print(f"  ! unsupported image type {path}")
    return None


def place_picture(slide, img: Path, box):
    x, y, w, h = box
    with Image.open(img) as im:
        iw, ih = im.size
    s = min(w / iw, h / ih)
    pw, ph = iw * s, ih * s
    return slide.shapes.add_picture(str(img), Inches(x + (w - pw) / 2), Inches(y + (h - ph) / 2), Inches(pw), Inches(ph))


def todo_box(slide, box, v):
    shp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, *[Inches(t) for t in box])
    shp.fill.solid()
    shp.fill.fore_color.rgb = RGBColor(0xFF, 0xF4, 0xE5)
    shp.line.color.rgb = RGBColor(0xE6, 0x7E, 0x22)
    shp.line.dash_style = MSO_LINE_DASH_STYLE.DASH
    brief = v.get("brief") or v.get("prompt") or v.get("alt") or ""
    fill_text(shp, [f"ASSET TODO · {v.get('id', '?')}", brief[:160]], size=12, color="A04000")
    shp.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    for p in shp.text_frame.paragraphs:
        p.alignment = PP_ALIGN.CENTER
    return shp


def put_visual(slide, v, box, cache, compat, fonts, warns, sid, caption_box=None):
    if not v or not box:
        return
    cap = v.get("caption")
    img_box = list(box)
    if cap and not caption_box:
        img_box[3] = max(0.5, box[3] - 0.45)
        caption_box = [box[0], box[1] + img_box[3] + 0.05, box[2], 0.4]
    path = ROOT / v["path"] if v.get("path") else None
    ready = v.get("status") in ("existing", "generated") and path and path.exists()
    img = prepare_image(path, cache, compat) if ready else None
    if img:
        place_picture(slide, img, img_box)
    else:
        todo_box(slide, img_box, v)
        warns.append(f"[{sid}] visual {v.get('id')} still TODO")
    if cap and caption_box:
        textbox(slide, caption_box, cap, size=fonts.get("caption_pt", 12), color=fonts.get("caption_color"),
                align=PP_ALIGN.CENTER, cfg_compat=compat)


# ─────────────────────────── build ───────────────────────────
def build(cfg, spec, out: Path, root: Path = ROOT):
    tmap = yaml.safe_load((root / cfg.get("template_map", "deck/template.map.yaml")).read_text(encoding="utf-8"))
    compat = cfg.get("compat", {})
    fonts = tmap.get("fonts", {})
    body_font = fonts.get("body_font")
    prs = Presentation(root / cfg["template"])
    originals = list(prs.slides)
    cache = out.parent / "_media"
    warns = []

    def bookend(which):                 # fixed template slides (e.g. WELCOME / THANK YOU), never in slides.yaml
        for n in (tmap.get("bookends") or {}).get(which) or []:
            clone_slide(prs, originals[int(n) - 1])

    bookend("start")
    for s in spec["slides"]:
        sid, kind = s["id"], s["kind"]
        m = tmap["kinds"].get(kind)
        if m is None:
            raise SystemExit(f"[{sid}] kind '{kind}' missing in template.map.yaml")
        if "prototype" in m:
            slide = clone_slide(prs, originals[int(m["prototype"]) - 1])
        else:
            slide = prs.slides.add_slide(layout_by_name(prs, m["layout"]))

        for name in m.get("drop") or []:     # reference-only decorations / content on the prototype
            remove(find_target(slide, name))
        for name, bx in (m.get("move") or {}).items():   # reposition a prototype shape, keeping its styling
            shp = find_target(slide, name)
            if shp is not None:
                shp.left, shp.top, shp.width, shp.height = [Inches(v) for v in bx]
        used = set()

        def region(role):
            """Return (shape-or-None, box) for a role, honouring *_box overrides."""
            if f"{role}_box" in m:
                return None, m[f"{role}_box"]
            shp = find_target(slide, m.get(role))
            return (shp, box_of(shp)) if shp is not None else (None, None)

        # title
        tshape, tbox = region("title")
        if s.get("title"):
            if tshape is not None:
                fill_text(tshape, s["title"], size=fonts.get("title_pt") if fonts.get("force_sizes") else None,
                          cfg_compat=compat)
                used.add(id(tshape))
            elif tbox:
                textbox(slide, tbox, s["title"], size=fonts.get("title_pt", 32), bold=True, cfg_compat=compat)

        # kicker: small running header above the title (prototype mode), filled with the deck title
        ksh = find_target(slide, m.get("kicker"))
        if ksh is not None:
            if spec.get("title"):
                fill_text(ksh, spec["title"], cfg_compat=compat)
                used.add(id(ksh))
            else:
                remove(ksh)

        # subtitle
        if s.get("subtitle"):
            sh, bx = region("subtitle")
            if sh is not None:
                fill_text(sh, s["subtitle"], cfg_compat=compat)
                used.add(id(sh))
            elif bx:
                textbox(slide, bx, s["subtitle"], size=fonts.get("body_pt", 20), cfg_compat=compat)

        # body: bullets or key idea
        lines, is_key = (s.get("bullets") or []), False
        if kind == "key-idea" and s.get("key_idea"):
            lines, is_key = [s["key_idea"]], True
        if lines:
            sh, bx = region("body")
            size = fonts.get("key_idea_pt", 32) if is_key else fonts.get("body_pt", 20)
            sh0 = find_target(slide, m.get("body")) if "body_box" not in m else None
            fit_box = box_of(sh0) if sh0 is not None else bx
            spacing = {} if is_key else dict(line_spacing=fonts.get("body_line_spacing"),
                                             space_after=fonts.get("body_space_after_pt"))
            if not is_key and fonts.get("body_min_pt") and overflow_warning(lines, fit_box, size, **spacing):
                size = fonts["body_min_pt"]     # text-heavy slide: step down instead of overflowing
            kw = dict(size=size, cfg_compat=compat, font=body_font, color=fonts.get("body_color"), **spacing)
            if is_key:
                kw.update(bullets=False, align=PP_ALIGN.CENTER, bold=True, color=fonts.get("key_idea_color"),
                          font=fonts.get("key_idea_font") or body_font)
            else:
                kw.update(bullets=True)
            if sh is not None:
                fill_text(sh, lines, **kw)
                used.add(id(sh))
            elif bx:
                tb = textbox(slide, bx, lines, **kw)
                if is_key:
                    tb.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
            w = overflow_warning(lines, bx, size, **spacing)
            if w:
                warns.append(f"[{sid}] {w}")

        # visuals
        cap_box = m.get("caption_box")
        for role in ("visual", "visual2"):
            if not s.get(role):
                if m.get(role) is not None:     # prototype's own picture must not leak into this slide
                    remove(find_target(slide, m.get(role)))
                continue
            sh, bx = region(role)
            if sh is not None:
                remove(sh)       # placeholder/proto image replaced by a fitted picture
                used.add(id(sh))
            put_visual(slide, s[role], bx, cache, compat, fonts, warns, sid,
                       caption_box=cap_box if role == "visual" and kind in ("image-full", "two-images") else None)
            if kind == "two-images":
                cap_box = None

        # drop unused empty placeholders (avoid "Click to add text" ghosts)
        for ph in list(slide.placeholders):
            if id(ph) not in used and ph.has_text_frame and not ph.text_frame.text.strip():
                remove(ph)

        # speaker notes: notes + sources + read-more pointer
        notes = (s.get("notes") or "").strip()
        srcs = s.get("sources") or []
        if srcs:
            notes += ("\n\n" if notes else "") + "Sources: " + ", ".join(srcs)
        if notes:
            slide.notes_slide.notes_text_frame.text = notes

    bookend("end")
    if not tmap.get("keep_template_slides"):
        for o in originals:
            delete_slide(prs, o)
    out.parent.mkdir(parents=True, exist_ok=True)
    prs.save(out)
    return warns


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    cfg = load_config()
    mod = module_info(cfg, sys.argv[1])
    work = mod["work"]
    from validate_spec import slide_hash, validate
    errs, _ = validate(cfg, mod["key"], quiet=True)
    if errs and "--force" not in sys.argv:
        print("\n".join("  ERROR " + e for e in errs))
        sys.exit("✗ slides.yaml has errors — fix them (or --force for a draft build)")
    spec = yaml.safe_load((work / "slides.yaml").read_text(encoding="utf-8"))
    slug = re.sub(r"[^a-z0-9]+", "-", mod["title"].lower()).strip("-")
    out = work / f"{mod['key']}-{slug}.pptx"
    warns = build(cfg, spec, out)
    for w in warns:
        print("  WARN ", w)

    digest = read_json(work / "digest.json")
    sec_hash = {f"{u['id']}#{s['anchor']}": s["hash"] for u in digest["units"] for s in u["sections"]}
    sec_hash.update({u["id"]: u["hash"] for u in digest["units"]})
    write_json(work / "manifest.json", {
        "pptx": out.name,
        "units": {u["id"]: u["hash"] for u in digest["units"]},
        "sections": sec_hash,
        "slides": {s["id"]: slide_hash(s) for s in spec["slides"]},
        "slide_sources": {s["id"]: s.get("sources") or [] for s in spec["slides"]},
    })
    print(f"✓ built {out.relative_to(ROOT)} ({len(spec['slides'])} slides, {len(warns)} warnings)")


if __name__ == "__main__":
    main()
