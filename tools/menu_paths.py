#!/usr/bin/env python
"""
Build the camera's full menu address book from the manual's own tab indexes.

Canon's vocabulary, from the manual's labeled menu screen: a MAIN TAB
(Shooting, Autofocus, Playback, Communication functions, Set-up, Control
customization, Custom Functions, My Menu), a numbered SECONDARY TAB that
carries a name, and the ITEMS on it. The camera prints the number as "6/9"
in the top right corner of the screen.

The "Tab Menus: ..." pages near the start of each manual chapter reproduce
every secondary tab in order: a bold heading (the secondary tab name), a
screenshot, then the numbered item list. Parsing those gives the complete
address of every setting in the camera, which is the one thing the menu
screenshots themselves never show.

Writes working/menu-paths.json and working/menu-paths.txt.

    python tools/menu_paths.py                 # rebuild both files
    python tools/menu_paths.py "shutter mode"  # look an address up

Deterministic. Makes no model calls.
"""

import json
import os
import re
import sys

import fitz

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF = os.path.join(ROOT, "Canon.EOS.R5.MarkII.pdf")
OUT_JSON = os.path.join(ROOT, "working", "menu-paths.json")
OUT_TXT = os.path.join(ROOT, "working", "menu-paths.txt")

# Each section is (main tab label, first pdf page, last pdf page). The ranges
# were found by scanning for pages carrying bold 7.2pt headings and 6.0pt
# "(n)" item rows, the signature of an index page.
SECTIONS = [
    ("Shooting",                160, 164),
    ("Shooting (movie)",        345, 349),
    ("Autofocus",               484, 487),
    ("Autofocus (movie)",       488, 489),
    ("Playback",                591, 593),
    ("Communication functions", 707, 708),
    ("Set-up",                  956, 959),
    ("Control customization",  1049, 1051),
    ("Custom Functions",       1084, 1085),
    ("My Menu",                1101, 1101),
]

HEAD_FONT, HEAD_SIZE = "Arial-BoldMT", 7.2
ITEM_SIZE = 6.0


def lines(page):
    """The page as reading-order lines of (x, font, size, text)."""
    spans = []
    for b in page.get_text("dict")["blocks"]:
        if b["type"] != 0:
            continue
        for l in b["lines"]:
            for sp in l["spans"]:
                if sp["text"].strip():
                    spans.append((round(sp["bbox"][1], 1),
                                  round(sp["bbox"][0], 1), sp["font"],
                                  round(sp["size"], 1), sp["text"]))
    spans.sort(key=lambda r: (r[0], r[1]))
    out, cur, y0 = [], [], None
    for y, x, f, sz, t in spans:
        if y0 is None or abs(y - y0) <= 2.0:
            cur.append((x, f, sz, t))
            y0 = y if y0 is None else y0
        else:
            out.append(cur)
            cur, y0 = [(x, f, sz, t)], y
    if cur:
        out.append(cur)
    return out


# Item names whose leading word is a Canon glyph, so the text layer loses it.
# Read off the manual's own screenshots on the pages named.
ICON_NAMES = {
    ("Shooting", 1, 1): "JPEG/HEIF quality",
    ("Control customization", 1, 3):
        "direction to set Tv/Av (the three body dials)",
    ("Control customization", 1, 4):
        "direction to set Tv/Av (the control ring)",
    ("Control customization", 1, 5):
        "Switch Main dial / Quick control dial 2 when shooting",
    ("Control customization", 2, 3):
        "multi-controller sensitivity- AF pt select",
    ("Control customization", 3, 2): "Image jump w/ Main dial",
    ("Control customization", 3, 3):
        "Img jump w/ exposure comp. + Quick control dial 1",
    ("Control customization", 3, 4):
        "Switch Main dial / Quick control dial 2 during playback",
}

STOP = {"Caution", "Note", "Tip", "Tips"}


def parse(doc, first, last):
    groups = []
    for p in range(first, last + 1):
        pending = skip = None
        for ln in lines(doc[p - 1]):
            txt = " ".join(t for _, _, _, t in ln).strip()
            txt = re.sub(r"\s+", " ", txt)
            if any(f == HEAD_FONT and sz == HEAD_SIZE for _, f, sz, _ in ln):
                groups.append({"name": txt, "items": []})
                pending = skip = None
                continue
            if not groups:
                continue
            if txt in STOP:
                pending = None
                skip = True     # prose until the next bold heading
                continue
            if skip:
                continue
            if not any(sz == ITEM_SIZE for _, _, sz, _ in ln):
                continue
            m = re.match(r"^\((\d+)\)\s*(.*)$", txt)
            if m:
                pending = {"n": int(m.group(1)), "name": m.group(2).strip(),
                           "sub": []}
                groups[-1]["items"].append(pending)
                continue
            if txt.startswith("•"):
                if pending:
                    s = txt.lstrip("• ").strip()
                    if s:
                        pending["sub"].append(s)
                continue
    for g in groups:
        g["items"] = [i for i in g["items"] if i["name"] or i["sub"]]
    return [g for g in groups if g["items"]]


def number(groups):
    """Give each group its secondary-tab number.

    The still-photo and movie variants of one tab are printed as two blocks
    in the index but are a single numbered tab on the camera, which is why
    Control customization indexes five blocks and the screen says 4/4.
    """
    bare = lambda n: re.sub(r"\s*\((?:still photo shooting|movie recording)\)"
                            r"\s*$", "", n).strip()

    n = 0
    prev = None
    for g in groups:
        b = bare(g["name"])
        variant = b != g["name"]
        if not (prev is not None and b == prev[0] and variant and prev[1]):
            n += 1
        g["name"] = b
        g["page"] = n
        prev = (b, variant)
    for g in groups:
        g["of"] = n
    out, seen = [], set()
    for g in groups:
        if g["page"] in seen:
            continue            # the movie twin of a tab already listed
        seen.add(g["page"])
        out.append(g)
    return out


def build():
    doc = fitz.open(PDF)
    book = []
    for tab, first, last in SECTIONS:
        groups = number(parse(doc, first, last))
        for g in groups:
            g["tab"] = tab
            for it in g["items"]:
                fix = ICON_NAMES.get((tab, g["page"], it["n"]))
                if fix:
                    it["name"] = fix
        book.append({"tab": tab, "pages": groups})
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(book, f, indent=1, ensure_ascii=False)
    with open(OUT_TXT, "w", encoding="utf-8") as f:
        for sec in book:
            f.write("\n### %s\n" % sec["tab"])
            for g in sec["pages"]:
                f.write("  %d/%d  %s\n" % (g["page"], g["of"], g["name"]))
                for it in g["items"]:
                    f.write("      (%d) %s\n" % (it["n"], it["name"]))
                    for s in it["sub"]:
                        f.write("           - %s\n" % s)
    n = sum(len(i["items"]) for s in book for i in s["pages"])
    print("wrote %s and %s" % (OUT_JSON, OUT_TXT))
    print("  %d main tabs, %d secondary tabs, %d items"
          % (len(book), sum(len(s["pages"]) for s in book), n))
    return book


def look(book, needle):
    q = needle.lower()
    for sec in book:
        for g in sec["pages"]:
            for it in g["items"]:
                hay = (it["name"] + " " + " ".join(it["sub"])).lower()
                if q in hay:
                    print("%-24s %d/%d  %-28s -> %s"
                          % (sec["tab"], g["page"], g["of"], g["name"],
                             it["name"]))
                    for s in it["sub"]:
                        if q in s.lower():
                            print(" " * 26 + "   - " + s)


if __name__ == "__main__":
    b = build() if not os.path.exists(OUT_JSON) or len(sys.argv) == 1 else \
        json.load(open(OUT_JSON, encoding="utf-8"))
    for arg in sys.argv[1:]:
        print()
        look(b, arg)
