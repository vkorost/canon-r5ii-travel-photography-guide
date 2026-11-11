#!/usr/bin/env python
"""
Draw the book's own diagrams, from the book's own arithmetic.

Why drawn and not sourced. Wikimedia Commons has aperture and depth-of-field
diagrams, but they illustrate a *concept*, not this camera: the pixel pitch,
the ISO ceiling, the superzoom's aperture curve and the working band are all
particular to the kit this book is about, and a general diagram cannot carry
them. Almost all of the good Commons candidates are also share-alike, which
this project does not take. Drawing them costs an afternoon and gives figures
that agree with the tables they sit beside, in pure black on white, at the
size they will be printed.

Every number here is quoted from a chapter, with the chapter named in the
comment above it, so a figure can never silently drift from its text.

Output goes to figures-epaper/ with an entry merged into that directory's
render report, which is the same path the extracted manual figures take:
tools/binarize_lineart.py then carries them to figures-bw/ as pure black and
white, and tools/build_book_docx.py sizes them from the report.

    python tools/make_diagrams.py            # draw all of them
    python tools/make_diagrams.py d03        # just one

Deterministic. Makes no model calls.
"""

import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "figures-epaper")
REPORT = os.path.join(OUT, "_render_report.json")
DPI = 300

# E-paper has roughly sixteen gray levels and about 1:15 contrast, so every
# line here is pure black and every fill is a hatch rather than a tone.
BLACK = "#000000"
plt.rcParams.update({
    "font.family": "Calibri",
    "font.size": 9,
    "text.color": BLACK,
    "axes.edgecolor": BLACK,
    "axes.labelcolor": BLACK,
    "axes.linewidth": 1.1,
    "xtick.color": BLACK,
    "ytick.color": BLACK,
    "xtick.labelsize": 8.5,
    "ytick.labelsize": 8.5,
    "axes.grid": False,
    "savefig.facecolor": "white",
    "figure.facecolor": "white",
    "hatch.linewidth": 0.8,
    "legend.frameon": False,
    "legend.fontsize": 8.5,
})

FIGS = {}


def figure(fid, width, height):
    """Register a drawing function under a figure id and a placed size."""
    def deco(fn):
        FIGS[fid] = (fn, width, height)
        return fn
    return deco


# A label that has to sit over a line gets the page back under it; on e-paper
# a crossed-out word is simply unreadable.
BOX = dict(boxstyle="square,pad=0.18", fc="white", ec="none")


# --------------------------------------------------------------------------
# Chapter 3, "The Number Is a Ratio, Not a Size":
#   "At f/5.6, a lens set to 28mm has an opening about 5mm across. The same
#    lens at 300mm, at the same f/5.6, has an opening about 54mm across."
# --------------------------------------------------------------------------
@figure("d01_fnumber_ratio", 5.75, 2.35)
def d01(fig):
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4.0)
    ax.axis("off")

    scale = 1.30 / 53.6          # data units per millimetre of real aperture
    cy = 2.35
    for focal, dia, cx in ((28, 5.0, 2.6), (300, 53.6, 6.9)):
        r = dia * scale / 2
        ax.add_patch(Circle((cx, cy), r, fill=False, lw=1.9, ec=BLACK))
        ax.text(cx, cy + r + 0.17, "%dmm at f/5.6" % focal,
                ha="center", va="bottom", fontsize=10, weight="bold")
        ax.text(cx, cy - r - 0.19, "%.1fmm across" % dia,
                ha="center", va="top", fontsize=9.5)
        if r > 0.3:              # an arrow inside the small one is bigger
            ax.annotate("", xy=(cx - r, cy), xytext=(cx + r, cy),
                        arrowprops=dict(arrowstyle="<->", lw=1.0, color=BLACK))

    ax.plot([0.35, 9.65], [0.98, 0.98], lw=0.9, color=BLACK)
    ax.text(5, 0.60, "entrance pupil  =  focal length  \u00f7  f-number",
            ha="center", va="center", fontsize=11, weight="bold")
    ax.text(5, 0.20, "Same number on the screen. Same exposure. "
            "Ten times the diameter.",
            ha="center", va="center", fontsize=9.5)


# --------------------------------------------------------------------------
# Chapter 3, the measured curve for the case kit's superzoom:
#   28-39 f/3.5 | 40-59 f/4 | 60-69 f/4.5 | 70-109 f/5 | 110-300 f/5.6
# --------------------------------------------------------------------------
@figure("d02_zoom_aperture", 5.75, 2.9)
def d02(fig):
    ax = fig.add_subplot(111)
    steps = [(28, 39, 3.5), (40, 59, 4.0), (60, 69, 4.5),
             (70, 109, 5.0), (110, 300, 5.6)]
    for a, b, n in steps:
        ax.plot([a, b], [n, n], lw=2.6, color=BLACK, solid_capstyle="butt")
    for (a1, b1, n1), (a2, b2, n2) in zip(steps, steps[1:]):
        ax.plot([b1, a2], [n1, n2], lw=1.0, color=BLACK, ls=(0, (2, 2)))

    ax.set_xlim(28, 300)
    ax.set_ylim(6.35, 3.15)      # inverted: a wider aperture sits higher
    ax.set_yticks([3.5, 4.0, 4.5, 5.0, 5.6])
    ax.set_yticklabels(["f/3.5", "f/4", "f/4.5", "f/5", "f/5.6"])
    ax.set_xticks([28, 50, 100, 150, 200, 250, 300])
    ax.set_xlabel("focal length, mm", fontsize=9)
    ax.set_ylabel("widest aperture available", fontsize=9)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)

    # A measuring bracket under the stretch that matters, instead of a fill.
    for brk, lo, hi, txt, dy, va in (
            (6.02, 110, 300, "f/5.6 and it cannot open further \u2014 "
             "two-thirds of the range", 0.10, "top"),
            (6.02, 28, 39, "f/3.5 lives only here \u2014 "
             "11mm of a 272mm range", -0.12, "bottom")):
        ax.plot([lo, hi], [brk, brk], lw=1.0, color=BLACK)
        for e in (lo, hi):
            ax.plot([e, e], [brk - 0.07, brk + 0.07], lw=1.0, color=BLACK)
        x = (lo + hi) / 2.0 if va == "top" else hi + 4
        ax.text(x, brk + dy, txt, ha=("center" if va == "top" else "left"),
                va=va, fontsize=8.5, bbox=BOX)

    ax.text(300, 3.22, "set f/5.6 here and the lens is WIDE OPEN;\n"
            "set f/5.6 at 28mm and it is stopped down\n"
            "a stop and a third. Nothing on the screen\nsays which.",
            ha="right", va="top", fontsize=8.5, bbox=BOX)


# --------------------------------------------------------------------------
# Chapter 3, "Where Sharpness Stops Improving":
#   pixel pitch 4.39 microns; disc = 1.34 microns x the f-number;
#   one pixel wide at f/3.3, two at f/6.5. Older tests ran on ~8 micron pixels.
# --------------------------------------------------------------------------
@figure("d03_diffraction", 5.75, 3.1)
def d03(fig):
    ax = fig.add_subplot(111)
    ns = [2.8, 4, 5.6, 8, 11, 16, 22]
    x = list(range(len(ns)))
    here = [1.34 * n / 4.39 for n in ns]
    then = [1.34 * n / 8.00 for n in ns]

    ax.plot(x, here, lw=2.5, color=BLACK, marker="o", ms=5.2,
            mfc="white", mec=BLACK, mew=1.5, zorder=3)
    ax.plot(x, then, lw=1.4, color=BLACK, ls=(0, (5, 3)), marker="s", ms=4.2,
            mfc="white", mec=BLACK, mew=1.1, zorder=3)

    for y, lab in ((1, "1 pixel"), (2, "2 pixels")):
        ax.axhline(y, lw=0.9, color=BLACK, ls=(0, (1, 2.5)), zorder=1)
        ax.text(-0.44, y + 0.07, lab, fontsize=8, va="bottom")

    ax.set_xticks(x)
    ax.set_xticklabels(["f/%g" % n for n in ns])
    ax.set_ylim(0, 7.4)
    ax.set_xlim(-0.5, len(ns) - 0.5)
    ax.set_ylabel("diffraction disc, in pixels", fontsize=9)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)

    ax.text(4.55, 4.35, "this body \u2014 4.39 \u00b5m pixels",
            ha="right", va="center", fontsize=9.5, weight="bold", bbox=BOX)
    ax.text(-0.42, 7.3, "a 2008 body \u2014 8 \u00b5m pixels.\n"
            "The disc hid inside one photosite until\n"
            "about f/12, which is why the old reviews\n"
            "still say f/11 and f/16.",
            ha="left", va="top", fontsize=8.5, bbox=BOX)


# --------------------------------------------------------------------------
# Chapter 3, the relief-panel table:
#   depth available, normal viewing: f/5.6 99mm, f/8 141, f/11 195, f/16 283
#   judged at 100%:                  f/5.6 30mm, f/8  42, f/11  58, f/16  85
#   "Square-on, f/8 covers four centimetres of relief at pixel-level
#    scrutiny." A 60cm panel 30 degrees off square spans 300mm.
# --------------------------------------------------------------------------
@figure("d04_depth_of_field", 5.75, 3.15)
def d04(fig):
    ax = fig.add_subplot(111)
    ns = [5.6, 8, 11, 16]
    x = list(range(len(ns)))
    normal = [99, 141, 195, 283]
    hundred = [30, 42, 58, 85]

    ax.plot(x, normal, lw=1.4, color=BLACK, ls=(0, (5, 3)), marker="s",
            ms=4.2, mfc="white", mec=BLACK, mew=1.1, zorder=3)
    ax.plot(x, hundred, lw=2.5, color=BLACK, marker="o", ms=5.2,
            mfc="white", mec=BLACK, mew=1.5, zorder=3)

    ax.axhline(300, lw=1.7, color=BLACK, zorder=1)
    ax.axhline(40, lw=0.9, color=BLACK, ls=(0, (1, 2.5)), zorder=1)

    ax.set_yscale("log")
    ax.set_ylim(17, 560)
    ax.set_yticks([20, 30, 50, 100, 200, 300, 500])
    ax.set_yticklabels(["20", "30", "50", "100", "200", "300", "500"])
    ax.set_xticks(x)
    ax.set_xticklabels(["f/5.6", "f/8", "f/11", "f/16"])
    ax.set_xlim(-0.4, len(ns) - 0.45)
    ax.set_ylabel("depth of field available, mm", fontsize=9)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)

    ax.text(2.98, 320, "the same panel, 30\u00b0 off square: 300mm",
            ha="right", va="bottom", fontsize=9, weight="bold", bbox=BOX)
    ax.text(3.45, 41, "four centimetres of relief \u2014 more than most "
            "panels carry", ha="right", va="bottom", fontsize=8.5, bbox=BOX)
    ax.text(0.55, 180, "computed for a postcard", ha="left", va="bottom",
            fontsize=9, bbox=BOX)
    ax.text(2.05, 26, "judged at 100%", ha="center", va="top",
            fontsize=9.5, weight="bold", bbox=BOX)


# --------------------------------------------------------------------------
# Chapter 3: "at 0.3x magnification, a marked f/11 behaves like about f/14."
# Chapter 21: "at 0.3x magnification a set f/12 already is an effective f/16."
#   Effective f-number = set f-number x (1 + magnification).
# --------------------------------------------------------------------------
@figure("d05_effective_aperture", 5.75, 2.8)
def d05(fig):
    ax = fig.add_subplot(111)
    ms = [i / 100.0 for i in range(0, 51)]
    for setn, style, lw, bold in ((8, (0, (5, 3)), 1.4, False),
                                  (11, "-", 2.5, True)):
        ax.plot(ms, [setn * (1 + m) for m in ms], color=BLACK, ls=style, lw=lw)
        ax.text(0.507, setn * 1.5, "set f/%d" % setn, fontsize=9.5,
                va="center", weight=("bold" if bold else "normal"))

    ax.axhline(16, lw=0.9, color=BLACK, ls=(0, (1, 2.5)), zorder=1)
    ax.text(0.008, 16.28, "effective f/16 \u2014 no pixel-scale detail left",
            fontsize=8.5, va="bottom", ha="left", bbox=BOX)
    ax.plot([0.3, 0.3], [8.0, 14.3], lw=0.9, color=BLACK, ls=(0, (1, 2.5)))
    ax.plot([0.3], [14.3], marker="o", ms=6, mfc="white", mec=BLACK, mew=1.7,
            zorder=3)
    ax.text(0.315, 13.85, "at 0.3\u00d7 a set f/11\nis really f/14.3",
            ha="left", va="top", fontsize=8.5, bbox=BOX)
    ax.text(0.012, 10.45, "a small artefact at the long end,\n"
            "focused close, sits at about 0.3\u00d7",
            ha="left", va="center", fontsize=8.5, bbox=BOX)

    ax.set_xlim(0, 0.5)
    ax.set_ylim(7.5, 17.6)
    ax.set_xticks([0, 0.1, 0.2, 0.3, 0.4, 0.5])
    ax.set_xticklabels(["0", "0.1\u00d7", "0.2\u00d7", "0.3\u00d7",
                        "0.4\u00d7", "0.5\u00d7"])
    ax.set_yticks([8, 10, 12, 14, 16])
    ax.set_yticklabels(["f/8", "f/10", "f/12", "f/14", "f/16"])
    ax.set_xlabel("magnification", fontsize=9)
    ax.set_ylabel("aperture the light actually sees", fontsize=9)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    fig.subplots_adjust(right=0.855)


def merge(entries):
    """Add these figures to the render report without disturbing the rest."""
    with open(REPORT, encoding="utf-8") as f:
        data = json.load(f)
    by_id = {r["id"]: r for r in data["figures"]}
    for e in entries:
        by_id[e["id"]] = e
    data["figures"] = sorted(by_id.values(), key=lambda r: r["id"])
    with open(REPORT, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1)


def main():
    want = sys.argv[1:]
    entries = []
    for fid, (fn, w, h) in sorted(FIGS.items()):
        if want and not any(fid.startswith(a) for a in want):
            continue
        fig = plt.figure(figsize=(w, h), dpi=DPI)
        fn(fig)
        path = os.path.join(OUT, fid + ".png")
        fig.savefig(path, dpi=DPI, facecolor="white",
                    bbox_inches="tight", pad_inches=0.04)
        plt.close(fig)
        px = (int(w * DPI), int(h * DPI))
        entries.append({"id": fid, "page": None, "vector": True, "dpi": DPI,
                        "px": list(px), "bytes": os.path.getsize(path),
                        "drawn": True, "place_width_in": w})
        print("  %-24s %4dx%-4d px  %6.1f KB  placed %.2f in"
              % (fid, px[0], px[1], os.path.getsize(path) / 1024.0, w))
    if entries:
        merge(entries)
        print("report updated: %d diagram(s)" % len(entries))


if __name__ == "__main__":
    main()
