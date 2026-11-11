#!/usr/bin/env python
"""
Put the book's callouts onto a prepared photograph.

Five rules, each of them a correction of an earlier attempt:

1. **Labels sit outside the subject.** Text laid over a black camera body
   needs a halo to survive, and a haloed label on a photograph is the thing
   that makes a figure look like a bad paste-up. So the canvas is *extended*
   with white gutters and every label lives in a gutter. Nothing but the
   leader crosses the body.
2. **The arrows are drawn, not borrowed.** Matplotlib's arrow styles all have
   a constant-width shaft, which reads as a pipe with a tick on the end. A
   real drawn arrow **tapers**: a hairline at the tail, swelling toward the
   head. So the arrow here is a single filled polygon built along a quadratic
   Bezier, with shaft and head in one outline, so there is no seam where they
   meet.
3. **White fill, thin black outline.** The only treatment that reads on both
   halves of the figure: the white gutter, where the outline carries it, and
   the near-black body, where the fill does.
4. **Leaders never cross.** This is the one that cost a revision. Crossed
   leaders read as amateur work however good the arrow is, so label positions
   are no longer typed in by hand. Each label is placed **beside its own
   target** and then pushed apart from its neighbors **in target order**,
   which is what makes a crossing impossible rather than merely unlikely.
   The script then checks the drawn curves and **says so out loud**: a
   CROSSING line for any pair that intersects, a TEXT line for any leader
   running through another label.
5. **The leader leaves the edge of the text block, never its anchor**, or it
   draws a line straight through the label.

**The names are Canon's own**, from Part Names (pp. 32, 34, 35) and from the
menu-operations diagram on p. 118, which is what settles Quick control dial 1
(the wheel around SET) against dial 2 (the top-plate dial behind the shutter).
Canon's p. 32 also calls the mode control a **button**, not a dial.

Targets are fractions of the *photograph* (of the crop, where a figure
takes one), so re-cropping or re-sizing the source does not break them. A label
carries no position of its own: only which gutter it belongs in.

    python tools/annotate_figures.py

Deterministic. Makes no model calls.
"""

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UI = os.path.join(ROOT, "figures-ui")
OUT = os.path.join(ROOT, "figures-poc")
DPI = 300
COL_IN = 5.75                      # the book's text column
# A figure is RENDERED at the width it is PLACED at, so that a label set
# in 8.8pt prints as 8.8pt. Rendering everything at the full column and
# then placing it smaller is what made the first set print at 5pt.

GAP_IN = 0.055                     # text edge to leader tail
PAD_IN = 0.045                     # breathing room at the figure edge
SHAFT_IN = 0.046                   # arrow weights in inches, so that an
HEAD_W_IN = 0.105                  # arrow is the same arrow on every
HEAD_L_IN = 0.180                  # figure whatever width it is placed at
SHAFT_W = 0.0092                   # widest point of the shaft
HEAD_W = 0.0196
HEAD_L = 0.0345
TAIL_MIN = 0.38                    # narrowest the shaft may get, as a
                                   # fraction of its full width
TAPER = 0.85                       # <1 swells early, so the head grows out
                                   # of the shaft instead of sitting on top
EDGE_LW = 0.65                     # the black outline, in points
FS = 8.8                           # label size, in points
LINE = 1.25                        # line spacing
RAD_PULL = 0.5                     # how far the leader is pulled straight
                                   # out of the label before it sweeps round
CHAR_W = 0.52                      # mean glyph width, in units of font size


# --------------------------------------------------------------- geometry
def bezier(p0, c, p1, n=200):
    t = np.linspace(0.0, 1.0, n)[:, None]
    return (1 - t) ** 2 * p0 + 2 * (1 - t) * t * c + t ** 2 * p1


EXIT = {"left": (1.0, 0.0), "right": (-1.0, 0.0),
        "top": (0.0, 1.0), "bottom": (0.0, -1.0)}


def curve(p0, p1, side):
    """A leader that leaves the label **along the gutter's normal**.

    Pulling the control point straight out of the text, rather than bowing
    about the midpoint, is what keeps the first stretch of the leader inside
    its own row: a leader that angles away immediately clips the label
    stacked above or below it. It also gives the shape of a real drawn
    arrow, a near-straight hairline that sweeps into the target.
    """
    p0, p1 = np.asarray(p0, float), np.asarray(p1, float)
    e = np.asarray(EXIT[side], float)
    return bezier(p0, p0 + e * RAD_PULL * np.hypot(*(p1 - p0)), p1)


def arrow_polygon(pts, W):
    """A tapered arrow along ``pts``: hairline tail, head at the far end."""
    seg = np.r_[0.0, np.cumsum(np.hypot(*np.diff(pts, axis=0).T))]
    total = seg[-1]
    head_l = min(HEAD_L_IN, 0.42 * total)       # never a head-only arrow
    head_w, shaft_w = HEAD_W_IN, SHAFT_IN

    k = max(int(np.searchsorted(seg, total - head_l)), 2)
    shaft, s = pts[:k + 1], seg[:k + 1]

    tang = np.gradient(shaft, axis=0)
    tang /= np.maximum(np.hypot(*tang.T)[:, None], 1e-9)
    nrm = np.c_[-tang[:, 1], tang[:, 0]]

    # A taper that runs to a point looks right on screen and fails in
    # print: at the tail the two outline edges merge and the arrow
    # reads as a black stick instead of a white one. So the shaft
    # tapers to a floor, not to nothing.
    t = (s / max(s[-1], 1e-9)) ** TAPER
    half = 0.5 * shaft_w * (TAIL_MIN + (1.0 - TAIL_MIN) * t)
    base, bn = shaft[-1], nrm[-1]
    return np.vstack([shaft + nrm * half[:, None],
                      base + bn * (head_w / 2.0),
                      pts[-1],
                      base - bn * (head_w / 2.0),
                      (shaft - nrm * half[:, None])[::-1]])


def segments_cross(a, b, c, d):
    def side(p, q, r):
        return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
    return (((side(c, d, a) > 0) != (side(c, d, b) > 0)) and
            ((side(a, b, c) > 0) != (side(a, b, d) > 0)))


def polylines_cross(p, q, step=5):
    for i in range(0, len(p) - step, step):
        for j in range(0, len(q) - step, step):
            if segments_cross(p[i], p[i + step], q[j], q[j + step]):
                return True
    return False


# ------------------------------------------------------------ label slots
def place(want, lo, hi, size, gap):
    """Slots in target order, pushed apart only as far as they must be.

    Placing each label beside its *own* target and preserving that order is
    what guarantees the leaders cannot cross; the spacing pass only separates
    labels that would otherwise sit on top of one another.
    """
    order = sorted(range(len(want)), key=lambda i: want[i])
    pos = [want[i] for i in order]
    sz = [size[i] for i in order]
    for k in range(1, len(pos)):
        pos[k] = max(pos[k], pos[k - 1] + (sz[k - 1] + sz[k]) / 2.0 + gap)
    over = pos[-1] + sz[-1] / 2.0 - hi
    if over > 0:
        pos = [p - over for p in pos]
    for k in range(len(pos) - 2, -1, -1):
        pos[k] = min(pos[k], pos[k + 1] - (sz[k + 1] + sz[k]) / 2.0 - gap)
    pos[0] = max(pos[0], lo + sz[0] / 2.0)
    for k in range(1, len(pos)):
        pos[k] = max(pos[k], pos[k - 1] + (sz[k - 1] + sz[k]) / 2.0 + gap)
    out = [0.0] * len(want)
    for slot, i in zip(pos, order):
        out[i] = slot
    return out


# ----------------------------------------------------------------- figures
# Each label is (text, target, gutter). Where it lands in that gutter is
# computed, not typed, which is the whole point of rule 4.
FIGS = {
    "top_plate": dict(
        place=5.2, src="body_top.png", out="f01_top_plate.png",
        pad=(0.05, 0.28, 0.07, 0.22), emph="M-Fn",
        labels=[
            ("Shutter button", (0.829, 0.084), "right"),
            ("M-Fn",           (0.762, 0.172), "right"),
            ("Main dial",      (0.845, 0.227), "right"),
            ("Power switch",   (0.840, 0.458), "right"),
            ("MODE button",    (0.809, 0.579), "right"),
            ("Stills / movie", (0.148, 0.596), "bottom"),
            ("Hot shoe",       (0.377, 0.588), "bottom"),
            ("Top LCD panel",  (0.580, 0.600), "bottom"),
        ]),

    "back": dict(
        place=5.75, src="body_back.png", out="f02_back.png",
        emph="Viewfinder eyepiece",
        labels=[
            ("Viewfinder eyepiece",       (0.330, 0.215), "top"),
            ("Dioptric\nadjustment knob", (0.123, 0.205), "left"),
            ("Rating /\nvoice memo",      (0.085, 0.347), "left"),
            ("MENU",                      (0.150, 0.343), "left"),
            ("Screen",                    (0.300, 0.700), "left"),
            ("Playback",                  (0.744, 0.912), "bottom"),
            ("Erase",                     (0.812, 0.912), "bottom"),
        ]),

    "thumb": dict(
        place=5.75, src="body_back.png", out="f03_thumb_cluster.png",
        crop=(0.58, 0.12, 1.00, 0.86),
        pad=(0.44, 0.44, 0.19, 0.05), emph="AF start (AF-ON)",
        labels=[
            ("AF start (AF-ON)",      (0.405, 0.255), "top"),
            ("Quick control dial 2",  (0.600, 0.105), "top"),
            ("Multi-controller",      (0.195, 0.260), "left"),
            ("Magnify / reduce",      (0.315, 0.425), "left"),
            ("INFO",                  (0.315, 0.560), "left"),
            ("Quick control\ndial 1", (0.295, 0.790), "left"),
            ("AE lock",               (0.725, 0.270), "right"),
            ("AF point selection",    (0.855, 0.275), "right"),
            ("Q (Quick Control)",     (0.505, 0.565), "right"),
            ("SET",                   (0.470, 0.825), "right"),
        ]),

    "front": dict(
        place=5.75, src="body_front.png", out="f04_front.png",
        pad=(0.34, 0.34, 0.21, 0.19),
        labels=[
            # the two top-plate controls come down from above, so the
            # self-timer leader no longer skims the shutter button
            ("Shutter button",                    (0.120, 0.300), "top"),
            ("Self-timer lamp /\nAF-assist beam", (0.339, 0.280), "top"),
            ("Grip (battery\ncompartment)",       (0.140, 0.700), "left"),
            ("Depth-of-field\npreview",           (0.347, 0.814), "left"),
            # Canon p.32 puts the lens release button (21) at the mount edge;
            # the gray tab on the shoulder is (19), the tally lamp. The
            # button is not legible in this three-quarter view, so it is
            # not labeled rather than labeled wrongly.
            ("RF lens mount\nindex",              (0.565, 0.335), "right"),
            ("Shutter curtain /\nimage sensor",   (0.555, 0.585), "right"),
            ("Lens mount",                        (0.395, 0.520), "bottom"),
            ("Contacts",                          (0.580, 0.720), "bottom"),
        ]),

    "ports": dict(
        place=5.0, src="body_side.png", out="f05_ports.png",
        crop=(0.10, 0.08, 0.82, 0.96),
        pad=(0.46, 0.46, 0.05, 0.05),
        labels=[
            ("Terminal cover",            (0.270, 0.285), "left"),
            ("External\nmicrophone IN",   (0.375, 0.405), "left"),
            ("Headphone",                 (0.360, 0.700), "left"),
            ("Sync terminal",             (0.360, 0.865), "left"),
            ("Digital terminal\n(USB-C)", (0.610, 0.470), "right"),
            ("HDMI OUT",                  (0.640, 0.775), "right"),
        ]),

    "cards": dict(
        place=4.6, src="body_cards.png", out="f06_card_slots.png",
        crop=(0.44, 0.22, 1.00, 0.95),
        pad=(0.42, 0.40, 0.15, 0.07),
        labels=[
            ("Card 1\n(CFexpress)", (0.235, 0.520), "left"),
            ("Card eject button",   (0.247, 0.733), "left"),
            ("Card 2 (SD)",         (0.390, 0.520), "top"),
            ("Card slot cover",     (0.800, 0.300), "right"),
        ]),

    # ---- close crops, each replacing one of Canon's line drawings
    "shutter": dict(
        src="body_top.png", out="f07_shutter_button.png",
        crop=(0.66, 0.00, 1.00, 0.30),
        pad=(0.10, 0.46, 0.10, 0.10), emph="Shutter button",
        labels=[
            ("Shutter button", (0.497, 0.280), "right"),
            ("M-Fn",           (0.300, 0.573), "right"),
        ]),

    "main_dial": dict(
        src="body_top.png", out="f08_main_dial.png",
        crop=(0.64, 0.06, 1.00, 0.36),
        pad=(0.10, 0.46, 0.10, 0.10), emph="Main dial",
        labels=[
            ("M-Fn",      (0.339, 0.373), "right"),
            ("Main dial", (0.569, 0.557), "right"),
        ]),

    "mode_button": dict(
        src="body_top.png", out="f09_mode_button.png",
        crop=(0.62, 0.10, 1.00, 0.70),
        pad=(0.12, 0.50, 0.08, 0.08), emph="MODE button",
        labels=[
            ("Main dial",   (0.592, 0.212), "right"),
            ("MODE button", (0.497, 0.798), "right"),
        ]),

    "power_switch": dict(
        place=4.2, src="body_top.png", out="f10_power_switch.png",
        crop=(0.72, 0.33, 1.00, 0.70),
        pad=(0.14, 0.62, 0.08, 0.08), emph="Power switch",
        labels=[
            ("Power switch\nOFF / LOCK / ON", (0.429, 0.346), "right"),
            ("MODE button",                   (0.318, 0.673), "right"),
        ]),

    "multi_controller": dict(
        src="body_back.png", out="f11_multi_controller.png",
        crop=(0.55, 0.15, 0.88, 0.45),
        pad=(0.34, 0.34, 0.12, 0.12), emph="Multi-controller",
        labels=[
            ("Multi-controller", (0.333, 0.533), "left"),
            ("AF start (AF-ON)", (0.621, 0.550), "right"),
        ]),

    "viewfinder": dict(
        place=4.6, src="body_back.png", out="f12_viewfinder.png",
        crop=(0.03, 0.03, 0.56, 0.42),
        emph="Viewfinder eyepiece",
        labels=[
            ("Dioptric\nadjustment knob", (0.175, 0.449), "left"),
            ("Viewfinder eyepiece",       (0.566, 0.474), "top"),
        ]),
}


def measure(text, size, bold):
    """The true width and height of a label, in inches.

    Estimating text width from a character count is what clipped three
    labels and sized three gutters too tight. Matplotlib can be asked, so
    ask it: everything downstream (the gutter widths, the slot spacing
    and the collision boxes) is built on the measurement, not on a guess.
    """
    fig = plt.figure(figsize=(1, 1), dpi=DPI)
    t = fig.text(0, 0, text, fontsize=size, linespacing=LINE,
                 fontweight="bold" if bold else "normal")
    bb = t.get_window_extent(fig.canvas.get_renderer())
    plt.close(fig)
    return bb.width / DPI, bb.height / DPI


def draw(spec):
    img = Image.open(os.path.join(UI, spec["src"]))
    if spec.get("crop"):
        cw, ch = img.size
        x0, y0, x1, y1 = spec["crop"]
        img = img.crop((int(x0 * cw), int(y0 * ch), int(x1 * cw), int(y1 * ch)))
    pw, ph = img.size
    place_in = spec.get("place", COL_IN)
    emph = spec.get("emph")

    # ---- measure every label, then size the gutters to fit the widest
    size = {}
    for text, _t, side in spec["labels"]:
        big = text == emph
        size[text] = measure(text, FS * (1.1 if big else 1.0), big)

    side_of = {}
    for text, _t, side in spec["labels"]:
        side_of.setdefault(side, []).append(text)

    def gutter(side, axis):
        if side not in side_of:
            return 0.0
        return max(size[t][axis] for t in side_of[side]) + GAP_IN + PAD_IN

    gl, gr = gutter("left", 0), gutter("right", 0)
    gt, gb = gutter("top", 1), gutter("bottom", 1)

    img_w = place_in - gl - gr
    img_h = img_w * ph / float(pw)
    fig_h = img_h + gt + gb

    squeezed = img_w < 0.50 * place_in

    fig = plt.figure(figsize=(place_in, fig_h), dpi=DPI)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, place_in); ax.set_ylim(fig_h, 0)   # inches, y downward
    ax.set_axis_off()
    ax.imshow(img, cmap="gray", vmin=0, vmax=255, interpolation="lanczos",
              extent=(gl, gl + img_w, gt + img_h, gt), zorder=1)

    # ---- one slot per label, in target order, pushed apart only as needed
    anchors = {}
    for side, texts in side_of.items():
        vert = side in ("left", "right")
        idx = [i for i, (t, _g, s_) in enumerate(spec["labels"]) if s_ == side]
        want, sz = [], []
        for i in idx:
            text, (tx, ty), _ = spec["labels"][i]
            want.append(gt + ty * img_h if vert else gl + tx * img_w)
            sz.append(size[text][1] if vert else size[text][0])
        lo, hi = (0.0, fig_h) if vert else (0.0, place_in)
        slots = place(want, lo, hi, sz, 0.16 if vert else 0.16)
        for i, v in zip(idx, slots):
            anchors[i] = {"left": (gl - GAP_IN, v),
                          "right": (place_in - gr + GAP_IN, v),
                          "top": (v, gt - GAP_IN)}.get(side, (v, gt + img_h + GAP_IN))

    leaders, boxes, report = [], [], []
    for i, (text, (tx, ty), side) in enumerate(spec["labels"]):
        X, Y = gl + tx * img_w, gt + ty * img_h
        LX, LY = anchors[i]
        big = text == emph
        ha = {"left": "right", "right": "left"}.get(side, "center")
        va = {"top": "bottom", "bottom": "top"}.get(side, "center")
        ax.text(LX, LY, text, ha=ha, va=va, linespacing=LINE,
                fontsize=FS * (1.1 if big else 1.0),
                fontweight="bold" if big else "normal", color="black", zorder=4)

        tw, th = size[text]
        x0 = {"right": LX, "center": LX - tw / 2.0}.get(ha, LX - tw)
        y0 = {"bottom": LY - th, "center": LY - th / 2.0}.get(va, LY)
        boxes.append((x0, y0, x0 + tw, y0 + th))

        tail_pt = {"left": (LX + GAP_IN, LY), "right": (LX - GAP_IN, LY),
                   "top": (LX, LY + GAP_IN)}.get(side, (LX, LY - GAP_IN))
        leaders.append(curve(tail_pt, (X, Y), side))

    name = lambda i: spec["labels"][i][0].replace(chr(10), " ")
    for i in range(len(leaders)):
        for j in range(i + 1, len(leaders)):
            if polylines_cross(leaders[i], leaders[j]):
                report.append("CROSSING  %-24s x %s" % (name(i), name(j)))
    for i, pts in enumerate(leaders):
        for j, (bx0, by0, bx1, by1) in enumerate(boxes):
            if i != j and ((pts[:, 0] > bx0) & (pts[:, 0] < bx1) &
                           (pts[:, 1] > by0) & (pts[:, 1] < by1)).any():
                report.append("TEXT      %-24s through %s" % (name(i), name(j)))
    if squeezed:
        report.append("SQUEEZED  gutters leave the photograph only %.0f%% "
                      "of the width" % (100.0 * img_w / place_in))
    for x0, y0, x1, y1 in boxes:
        if x0 < -1e-6 or x1 > place_in + 1e-6 or y0 < -1e-6 or y1 > fig_h + 1e-6:
            report.append("CLIPPED   a label runs outside the figure")

    for i, pts in enumerate(leaders):
        ax.add_patch(Polygon(arrow_polygon(pts, place_in), closed=True,
                             fc="white", ec="black",
                             lw=EDGE_LW * (1.15 if name(i) == emph else 1.0),
                             joinstyle="round", zorder=3))

    path = os.path.join(OUT, spec["out"])
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)
    return path, report


def main():
    os.makedirs(OUT, exist_ok=True)
    bad = 0
    for key, spec in FIGS.items():
        if not os.path.exists(os.path.join(UI, spec["src"])):
            print("  MISSING source %s" % spec["src"])
            continue
        p, report = draw(spec)
        print("  %-17s -> %-26s %2d labels  %s"
              % (key, os.path.basename(p), len(spec["labels"]),
                 "clean" if not report else "%d PROBLEM(S)" % len(report)))
        for line in report:
            print("        " + line)
        bad += len(report)
    print("\n%s" % ("every leader clear of every other leader and label"
                    if not bad else "%d problem(s) to fix" % bad))


if __name__ == "__main__":
    main()
