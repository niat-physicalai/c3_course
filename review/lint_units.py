#!/usr/bin/env python3
"""
lint_units.py - mechanical checks across every C3 unit file. No dependencies.

Run from the repo root:
    python review/lint_units.py              # all units -> review/lint-report.md
    python review/lint_units.py B1 C3        # only these unit IDs

What it measures (things a human finds tedious and an LLM reviewer counts badly):
  - words / characters against PROGRESS.md targets and the 50,000-char cap
  - sentence length, bullets, tables, MCQs, try-it boxes, media placeholders
  - filler and "LLM tic" phrases, consultant jargon, one-off acronyms
  - how often the same reference-product "stories" are retold across units
  - near-duplicate passages shared between units
"""
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPORT = ROOT / "review" / "lint-report.md"

# --- tune these lists as you review; they are the cheapest lever you have -----------

FILLER = [
    r"it is important to note", r"it is worth noting", r"note that", r"in other words",
    r"that is the whole point", r"here is the thing", r"this is not .{1,40}\. it is",
    r"not just .{1,40}, but", r"genuinely", r"deliberately", r"precisely", r"crucially",
    r"essentially", r"fundamentally", r"simply put", r"at the end of the day",
    r"the key (insight|point|idea) is", r"think about it", r"put differently",
    r"this matters because", r"which is exactly", r"and that is", r"the honest answer",
    r"in practice,", r"quietly", r"real engineering", r"the lesson (here )?is",
]
JARGON = [
    r"load-bearing", r"first-class", r"surface area", r"orthogonal", r"canonical",
    r"invariant", r"affordance", r"specimen", r"traceab\w+", r"provenance",
    r"discipline", r"artefact", r"artifact", r"heuristic", r"idempoten\w+",
    r"stakeholder", r"deliverable", r"non-functional", r"decompos\w+", r"allocat\w+",
    r"NRE", r"last-time-buy", r"PCN", r"NRND", r"granular\w*", r"leverage",
]
# Acronyms a Part 1 graduate already knows - not flagged.
KNOWN_ACRONYMS = set("""LED GPIO ADC PWM USB PCB CAD MCU IMU OLED I2C SPI UART WIFI
WiFi BLE HTTP MQTT JSON CSV API IDE IC IOT IoT VCC GND SDA SCL INT RAM ROM PPT MCQ BOM
LIPO LiPo STEP DRC ERC ESP C3 HR ID OK UI PC FAQ INR USD GST PDF SVG AI RF THT SMD
SW BT U1 U2 U3 U4 A0 A1 A2 B0 B1 B2 B3 B4 B5 C0 C1 C2 C4 C5 C5a C5b C6 C7 D0 D1 D2 D3
D4 D5 E0 E1 E2 F REF MEDIA FACT LINK VERIFY REFPRODUCT START END ASSET PLACEHOLDER
ASSIGNABLE TODO XIAO FDM PLA MAX MPU""".split())
# Reference-product anecdotes. Each should be told in full ONCE, then pointed to.
STORIES = {
    "green MAX / 1.82 V clamp": r"1\.82 ?V|green (MAX|module)",
    "clone WHO_AM_I 0x70": r"WHO_AM_I|0x70",
    "parallel pull-ups ~1.5 kΩ": r"1\.5 ?kΩ|three (sets|pairs) of (module )?pull-ups",
    "strapping pins GPIO2/8/9": r"strapping",
    "MPU-6050 obsolete / PCN": r"PCN-000614|obsolete|ICM-42670",
    "stack height 14.044 mm": r"14\.044",
    "AD0 floating": r"AD0",
    "OLED write never fails": r"never fails|nothing is read back",
    "sleep current dominates": r"sleep current dominat",
}
LONG_SENTENCE = 30  # words
SHINGLE = 8         # words per shingle for duplicate detection

# ------------------------------------------------------------------------------------

BOX = re.compile(r"[\u2500-\u257F\u25A0-\u25FF|]")


def load_targets():
    targets = {}
    progress = ROOT / "PROGRESS.md"
    if not progress.exists():
        return targets
    for line in progress.read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 8 and cells[3].endswith(".md"):
            try:
                targets[cells[3]] = (int(cells[5]), int(cells[6]), cells[7])
            except ValueError:
                targets[cells[3]] = (None, None, cells[7])
    return targets


def split_parts(text):
    """Return (prose, code). Code lines and HTML comments are blanked in prose, but the
    line count is preserved so reported line numbers match the file."""
    code, prose, in_code = [], [], False
    for line in text.splitlines():
        fence = line.strip().startswith("```")
        if fence:
            in_code = not in_code
        if in_code or fence:
            code.append(line)
            prose.append("")
        else:
            prose.append(line)
    prose_text = re.sub(r"<!--.*?-->", lambda m: "\n" * m.group(0).count("\n"),
                        "\n".join(prose), flags=re.S)
    return prose_text, "\n".join(c for c in code if not c.strip().startswith("```"))


def words(s):
    return re.findall(r"[A-Za-z0-9µΩ°][\w'’.\-µΩ°/]*", BOX.sub(" ", s))


def hits(patterns, text, flags=re.I):
    out = {}
    lines = text.splitlines()
    for p in patterns:
        rx = re.compile(p, flags)
        where = [i + 1 for i, l in enumerate(lines) if rx.search(l)]
        if where:
            out[p] = where
    return out


def analyse(path):
    text = path.read_text(encoding="utf-8")
    prose, code = split_parts(text)
    plain = re.sub(r"<[^>]+>|[*_`#>\[\]()]", " ", prose)
    sentences = [s for s in re.split(r"(?<=[.!?])\s+", " ".join(plain.split())) if len(words(s)) > 2]
    slens = [len(words(s)) for s in sentences] or [0]
    lines = text.splitlines()
    return {
        "text": text,
        "prose": plain,
        "chars": len(text),
        "words_all": len(words(re.sub(r"<!--.*?-->", " ", text, flags=re.S))),
        "words_prose": len(words(plain)),
        "words_code": len(words(code)),
        "avg_sent": sum(slens) / len(slens),
        "long_sent_pct": 100 * sum(l > LONG_SENTENCE for l in slens) / max(len(slens), 1),
        "bullets": sum(bool(re.match(r"\s*([-*]|\d+\.)\s", l)) for l in lines),
        "tables": sum(1 for i, l in enumerate(lines) if re.match(r"\s*\|?\s*:?-{3,}", l)),
        "tryit": len(re.findall(r"\*\*Try it", text)),
        "mcq": len(re.findall(r"<details>", text)),
        "media": len(re.findall(r"<!--\s*MEDIA", text)),
        "fact_verify": len(re.findall(r"FACT:VERIFY", text)),
        "link_verify": len(re.findall(r"LINK:VERIFY", text)),
        "emdash_per_k": 1000 * text.count("—") / max(len(words(plain)), 1),
        "filler": hits(FILLER, prose),
        "jargon": hits(JARGON, prose),
        "acronyms": Counter(a for a in re.findall(r"\b[A-Z][A-Z0-9]{1,6}s?\b", plain)
                            if a.rstrip("s") not in KNOWN_ACRONYMS and a not in KNOWN_ACRONYMS),
        "stories": {k: len(re.findall(v, prose, re.I)) for k, v in STORIES.items()},
    }


def shingles(s):
    w = [x.lower() for x in words(s)]
    return {" ".join(w[i:i + SHINGLE]) for i in range(len(w) - SHINGLE + 1)}


def main():
    want = set(a.upper() for a in sys.argv[1:])
    files = sorted(p for p in ROOT.glob("0*-*/*.md"))
    if want:
        files = [p for p in files if p.name.split("-")[0].upper() in want]
    if not files:
        sys.exit("No unit files found under 0*-*/ - run from the repo root.")
    targets = load_targets()
    data = {p: analyse(p) for p in files}
    uid = lambda p: p.name.split("-")[0]

    out = ["# Lint report\n",
           "Generated by `review/lint_units.py`. Numbers are signals for the reviewer, not verdicts.\n",
           "## Size and shape\n",
           "| Unit | Words (all) | Target | vs target | Prose | Code | Chars | Avg sent | >30w % | Bullets | Tables | Try-it | MCQ | Media | FACT? | LINK? | — /1k |",
           "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for p, d in data.items():
        tgt, cap, _ = targets.get(p.name, (None, 50000, ""))
        vs = f"{100 * d['words_all'] / tgt:.0f}%" if tgt else "—"
        cap_flag = " ⚠" if cap and d["chars"] > cap else ""
        out.append(f"| {uid(p)} | {d['words_all']} | {tgt or '—'} | {vs} | {d['words_prose']} | {d['words_code']} | "
                   f"{d['chars']}{cap_flag} | {d['avg_sent']:.1f} | {d['long_sent_pct']:.0f} | {d['bullets']} | "
                   f"{d['tables']} | {d['tryit']} | {d['mcq']} | {d['media']} | {d['fact_verify']} | "
                   f"{d['link_verify']} | {d['emdash_per_k']:.1f} |")
    tot = sum(d["words_all"] for d in data.values())
    out.append(f"\n**Total words:** {tot:,} across {len(data)} files.\n")

    out.append("## Filler / LLM tics (line numbers)\n")
    for p, d in data.items():
        if d["filler"]:
            items = "; ".join(f"`{k}` L{','.join(map(str, v[:6]))}{'…' if len(v) > 6 else ''}"
                              for k, v in sorted(d["filler"].items(), key=lambda kv: -len(kv[1])))
            out.append(f"- **{uid(p)}** ({sum(map(len, d['filler'].values()))}): {items}")

    out.append("\n## Consultant jargon (line numbers)\n")
    for p, d in data.items():
        if d["jargon"]:
            items = "; ".join(f"`{k}` L{','.join(map(str, v[:6]))}{'…' if len(v) > 6 else ''}"
                              for k, v in sorted(d["jargon"].items(), key=lambda kv: -len(kv[1])))
            out.append(f"- **{uid(p)}** ({sum(map(len, d['jargon'].values()))}): {items}")

    course_acr = Counter()
    for d in data.values():
        course_acr.update(d["acronyms"])
    oneoff = sorted(a for a, n in course_acr.items() if n <= 2)
    out.append("\n## Acronyms used ≤2 times in the whole course (likely unnecessary jargon)\n")
    out.append(", ".join(f"`{a}`" for a in oneoff) or "_none_")

    out.append("\n\n## Reference-product stories retold (mentions per unit)\n")
    out.append("Each story should be told fully once and pointed to elsewhere.\n")
    out.append("| Story | " + " | ".join(uid(p) for p in data) + " | Units |")
    out.append("|---|" + "---|" * (len(data) + 1))
    for k in STORIES:
        row = [data[p]["stories"][k] for p in data]
        out.append(f"| {k} | " + " | ".join(str(n or "") for n in row) + f" | **{sum(1 for n in row if n)}** |")

    # duplicate passages
    sh = {p: shingles(d["prose"]) for p, d in data.items()}
    freq = Counter(s for v in sh.values() for s in v)
    boiler = {s for s, n in freq.items() if n > max(3, len(data) // 2)}
    pairs = []
    ps = list(data)
    for i, a in enumerate(ps):
        for b in ps[i + 1:]:
            shared = (sh[a] & sh[b]) - boiler
            if len(shared) >= 5:
                pairs.append((len(shared), a, b, shared))
    pairs.sort(reverse=True, key=lambda t: t[0])
    out.append("\n## Near-duplicate passages between units\n")
    out.append("Shared 8-word runs, template boilerplate removed. High counts mean copied explanation.\n")
    for n, a, b, shared in pairs[:25]:
        sample = sorted(shared)[0]
        out.append(f"- **{uid(a)} ↔ {uid(b)}**: {n} shared runs — e.g. “{sample}…”")
    if not pairs:
        out.append("_none above threshold_")

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"Wrote {REPORT.relative_to(ROOT)} — {len(data)} units, {tot:,} words.")


if __name__ == "__main__":
    main()
