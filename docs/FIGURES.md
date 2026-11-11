# The figure problem

A guide to a piece of hardware needs pictures of that hardware. The manufacturer has excellent ones and you cannot publish them. This is how that was solved for this book, and it is the part of the method most likely to transfer unchanged to whatever you are documenting.

**Where it ended up: 57 of the 62 figure placements are original.** Four manufacturer screens remain, listed in [`NOTICE.md`](../NOTICE.md), each used to discuss that specific screen, along with one inline glyph.

## Three kinds of figure, three different answers

### Body parts, photographed and annotated and annotate

The manual's line drawings of the body are the publisher's. A **photograph of the body with your own callouts** replaces them, and is better: a line drawing shows an abstraction, a photograph shows the thing.

Preparing them for print is four rules, each of which cost a figure before it was written down:

- **Take the white point from the brightest few per cent.** A white studio background is usually around 240, which prints as a dirty gray box.
- **Open the shadows** (gamma below 1) or a black camera body becomes a silhouette.
- **Trim to content.** Such a photograph is square with the body in a band across the middle; left alone it spends half the text column on empty paper.
- **Do not binarize**, because a camera body is tone rather than line art.

`tools/annotate_figures.py` puts the callouts on. Five rules, each of them a correction of an earlier attempt:

1. **Labels sit outside the subject.** Text over a dark body needs a halo, and a haloed label on a photograph is exactly what makes a figure look like a bad paste-up. The canvas is extended with white gutters and every label lives in one.
2. **The arrows are drawn, not borrowed.** Every built-in matplotlib arrow style has a constant-width shaft, which reads as a pipe with a tick on the end. A real drawn arrow tapers. The arrow here is a single filled polygon along a Bézier, with shaft and head in one outline, so there is no seam.
3. **White fill, thin black outline**, so the same arrow reads on the white gutter and on the near-black body. The shaft tapers **to a floor, not to nothing**: at print size a hairline tail's two outline edges merge and the arrow reads as a black stick.
4. **Leaders never cross**, which the layout below enforces rather than hopes for.
5. **The leader leaves the edge of the text block**, never its anchor, or it draws a line straight through the label.

### Interface screens, drawn

Menu screenshots are the manufacturer's, and the ones available online are usually **from the previous model**. For this camera they showed a setting the current body does not have, firmware two major versions old, and a tab layout that contradicted the book's own menu directory. Cleaning them up would have produced handsome figures that argue with Appendix B on the facing page.

`tools/make_menu_figures.py` typesets them instead, from the menu structure parsed out of the manual's navigation index. 27 of them earned a place in the book. They are drawn **black on white**: a sixteen-level e-paper panel renders a large dark field as mud, and the selected row keeps its emphasis by inverting locally, which is what the camera does with color.

The eight main-tab marks are extracted from a photograph of the camera's own screen rather than drawn, because a hand-drawn approximation of a manufacturer's pictogram is worse at the job: the mapping between the glyph and the tab name is exactly what a new owner lacks.

### Concepts, computed then drawn

`tools/make_diagrams.py` draws from the book's own arithmetic. A generic diagram of depth of field cannot carry your sensor's pixel pitch or your lens's aperture curve, and a figure that disagrees with the table beside it is worse than no figure.

## The no-crossing checker

Crossed leader lines make a figure read as amateur work however good the arrow is. Three rounds of fixing them by hand failed, because moving one label to fix a crossing creates another.

The fix is structural rather than cosmetic, because a layout that merely avoids a crossing on one figure will produce one on the next.

1. **Every label is placed beside its own target**, then pushed apart from its neighbors **in target order**. Preserving that order is what makes a crossing impossible rather than merely unlikely.
2. **The leader is pulled straight out of the text** before it sweeps to the target, so its first stretch stays in its own row instead of clipping the label stacked above.
3. **Gutters are sized from measured text extents**, not from a character count. Estimating width from character count is what clipped three labels and sized three gutters too tight.
4. The script then **checks the drawn curves** and refuses to be trusted silently. It prints one line per defect, in the form shown here.

```
CROSSING  <label> x <label>        two leaders intersect
TEXT      <label> through <label>  a leader runs through a label
CLIPPED   a label runs outside the figure
SQUEEZED  gutters leave the photograph only N% of the width
```

A clean run prints `every leader clear of every other leader and label`.

That check caught six real defects, and a naming error: the manual calls the mode control a **button**, not a dial.

## Render at the width you place at

A figure rendered at the full text column and then **placed** smaller shrinks its type with it. Labels set in 8.8pt were printing at five. Every figure is now rendered at the width it is placed at, so a point is a point.

Label-dense figures earn the full column; a two-label crop does not.

## Verify every target by zoom, before anyone else sees it

At full-figure size, an arrow landing on the icon *beside* a button is indistinguishable from one landing on the button. Four targeting errors in this book were invisible at figure size and obvious at 2×.

`tools/annotate_figures.py` positions are fractions of the photograph, so the check is cheap: overlay crosshairs on the source at the same fractions and look.

Two errors that survived until someone checked against the manufacturer's own part-names diagram:

- **Quick control dial 1 and 2 were swapped.** Dial 1 is the wheel around SET; dial 2 is the top-plate dial behind the shutter.
- A **tally lamp was labeled as the lens release button**. The lens release sits at the mount edge and is not legible in a three-quarter view, so that label was removed rather than guessed at twice.

## Licensing rule for sourced images

Where an image is sourced rather than made: **public domain, CC0 or CC BY only**. Never share-alike, never non-commercial, never no-derivatives, never anything whose license cannot be read programmatically. Share-alike reaches any image derived from it, including a grayscale conversion, which is exactly what this pipeline does to everything.
