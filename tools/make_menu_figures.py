#!/usr/bin/env python
"""
Draw the camera's menu screens, instead of reproducing Canon's bitmaps.

Why draw them at all. The screenshots available for this body are mostly from
the **original EOS R5**, whose tab layout, page numbering and item lists
differ from the Mark II's: they show *Eco mode*, firmware 3.5.x, and the old
SHOOT1/SET UP1 tags rather than the Mark II's ``n/m``. Cleaning those up would
produce handsome figures that contradict Appendix B on the facing page. So the
screens here are **typeset from the Mark II's own menu structure**
(``working/menu-paths.json``, which was built from the manual's index links),
with the eight tab marks **extracted from a real Mark II capture** by
``tools/extract_ui.py``.

That buys three things at once: they are right for this camera, they are
consistent with each other, and they carry no Canon bitmap.

They are drawn **black on white** rather than white on black. A sixteen-level
e-paper panel renders a large dark field as mud, and the book is printed on
paper; the selected row keeps its emphasis by inverting locally, which is what
the camera does with color.

    python tools/make_menu_figures.py

Deterministic. Makes no model calls.
"""

import io
import json
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UI = os.path.join(ROOT, "figures-ui")
OUT = os.path.join(ROOT, "figures-own")

W = 1020                       # 3.4 in at 300 dpi, deliberately not the
                               # full text column; a menu screen does not
                               # need to be as wide as a photograph
PAD = 26
TAB_H = 92
DASH_H = 30
BAR_H = 66
ROW_H = 74
FS_ITEM = 34
FS_BAR = 34
INK = (0, 0, 0)
DIM = (150, 150, 150)
PAPER = (255, 255, 255)

TAB_ORDER = ["shooting", "af", "playback", "comm", "setup", "control",
             "cfn", "mymenu"]


def font(size, bold=False):
    for name in (("segoeuib.ttf", "arialbd.ttf") if bold
                 else ("segoeui.ttf", "arial.ttf")):
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            continue
    return ImageFont.load_default()


def text_w(d, s, f):
    return d.textbbox((0, 0), s, font=f)[2]


def tab_strip(im, d, active):
    """The eight main tabs, with the active one knocked out of a black box."""
    n = len(TAB_ORDER)
    cell = (W - 2 * PAD) / float(n)
    for i, name in enumerate(TAB_ORDER):
        cx = PAD + cell * (i + 0.5)
        path = os.path.join(UI, "tab_%s.png" % name)
        if not os.path.exists(path):
            continue
        g = Image.open(path).convert("L")
        # The Shooting tab was the *selected* one in the capture these marks
        # were cut from, so its ink is lighter than the rest. Stretch every
        # mark to the same range or that one tab prints gray.
        a = np.asarray(g).astype(np.float32)
        lo, hi = np.percentile(a, 1.0), np.percentile(a, 99.0)
        if hi - lo > 8:
            g = Image.fromarray(
                np.uint8(np.clip((a - lo) / (hi - lo), 0, 1) * 255))
        k = min((cell - 16) / g.width, (TAB_H - 30) / float(g.height))
        g = g.resize((max(int(g.width * k), 1), max(int(g.height * k), 1)),
                     Image.LANCZOS)
        x, y = int(cx - g.width / 2.0), int(PAD + (TAB_H - 30 - g.height) / 2.0)
        if name == active:
            box = [int(cx - cell / 2.0) + 3, PAD - 6,
                   int(cx + cell / 2.0) - 3, PAD + TAB_H - 26]
            d.rounded_rectangle(box, radius=8, fill=INK)
            # knocked out of a black box: threshold first, or the speckle
            # left by the extraction shows up as dirt in the white glyph
            g = Image.eval(g, lambda v: 0 if v > 150 else 255)
            im.paste(Image.new("L", g.size, 255), (x, y), g)
        else:
            im.paste(Image.new("L", g.size, 0), (x, y),
                     Image.eval(g, lambda v: 255 - v))
    d.line([(PAD, PAD + TAB_H - 20), (W - PAD, PAD + TAB_H - 20)],
           fill=INK, width=3)


def dashes(d, page, of, y):
    """The secondary-tab markers, with the open page filled in."""
    wdash, gap = 34, 14
    x = PAD + 4
    for i in range(1, of + 1):
        box = [x, y + 8, x + wdash, y + 16]
        d.rectangle(box, fill=INK if i == page else (205, 205, 205))
        x += wdash + gap


def render_page(spec):
    rows = spec["items"]
    h = PAD + TAB_H + DASH_H + BAR_H + ROW_H * len(rows) + PAD
    im = Image.new("RGB", (W, h), PAPER)
    d = ImageDraw.Draw(im)
    f_item, f_bold = font(FS_ITEM), font(FS_BAR, True)

    tab_strip(im, d, spec["tab"])
    y = PAD + TAB_H
    dashes(d, spec["page"], spec["of"], y)

    y += DASH_H
    d.text((PAD + 4, y + 12), spec["name"], font=f_bold, fill=INK)
    num = "%d/%d" % (spec["page"], spec["of"])
    d.text((W - PAD - 4 - text_w(d, num, f_bold), y + 12), num,
           font=f_bold, fill=INK)
    d.line([(PAD, y + BAR_H - 6), (W - PAD, y + BAR_H - 6)], fill=INK, width=2)

    y += BAR_H
    for i, row in enumerate(rows):
        name, value, state = (row + ("",) * 3)[:3]
        top = y + i * ROW_H
        fg = INK
        if state == "sel":
            d.rectangle([PAD, top + 4, W - PAD, top + ROW_H - 4], fill=INK)
            fg = PAPER
        elif state == "dim":
            fg = DIM
        d.text((PAD + 18, top + 16), name, font=f_item, fill=fg)
        if value:
            d.text((W - PAD - 18 - text_w(d, value, f_item), top + 16),
                   value, font=f_item, fill=fg)
    return im


def render_options(spec):
    """A setting's option list, as the camera draws it over the page."""
    rows = spec["items"]
    title_h = BAR_H
    h = PAD + title_h + ROW_H * len(rows) + PAD
    im = Image.new("RGB", (W, h), PAPER)
    d = ImageDraw.Draw(im)
    f_item, f_bold = font(FS_ITEM), font(FS_BAR, True)

    d.rectangle([PAD, PAD, W - PAD, PAD + title_h - 10], outline=INK, width=3)
    d.text((PAD + 18, PAD + 12), spec["name"], font=f_bold, fill=INK)
    if spec.get("where"):
        wtxt = spec["where"]
        d.text((W - PAD - 18 - text_w(d, wtxt, f_item), PAD + 14), wtxt,
               font=f_item, fill=DIM)

    y = PAD + title_h
    for i, row in enumerate(rows):
        name, value, state = (row + ("",) * 3)[:3]
        top = y + i * ROW_H
        fg = INK
        if state == "sel":
            d.rectangle([PAD, top + 4, W - PAD, top + ROW_H - 4], fill=INK)
            fg = PAPER
        elif state == "dim":
            fg = DIM
        d.text((PAD + (56 if state in ("on", "off") else 36), top + 16),
               name, font=f_item, fill=fg)
        if value:
            d.text((W - PAD - 18 - text_w(d, value, f_item), top + 16),
                   value, font=f_item, fill=fg)
        if state == "cur":
            d.ellipse([PAD + 12, top + 30, PAD + 26, top + 44], fill=INK)
        elif state in ("on", "off"):
            box = [PAD + 10, top + 20, PAD + 44, top + 54]
            d.rectangle(box, outline=fg, width=3)
            if state == "on":                       # a drawn tick, so that
                d.line([(box[0] + 7, top + 38), (box[0] + 14, top + 46),
                        (box[0] + 27, top + 26)], fill=fg, width=4)
    d.rectangle([PAD, PAD, W - PAD, h - PAD], outline=INK, width=3)
    return im


def load_structure():
    p = os.path.join(ROOT, "working", "menu-paths.json")
    with io.open(p, encoding="utf-8") as f:
        return json.load(f)


def main():
    os.makedirs(OUT, exist_ok=True)
    from menu_screens import SCREENS          # the content, kept separate
    made = 0
    for s in SCREENS:
        im = render_options(s) if s.get("kind") == "options" else render_page(s)
        path = os.path.join(OUT, s["id"] + ".png")
        im.save(path, optimize=True)
        made += 1
        print("  %-28s %4d x %-4d  %s" % (s["id"], im.width, im.height,
                                          s["name"]))
    print("\n%d menu screens drawn into %s" % (made, OUT))


if __name__ == "__main__":
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    main()
