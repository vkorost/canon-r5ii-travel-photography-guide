# The method

How a 1,200-page manufacturer's manual becomes a book organized the way a person actually uses the thing. The order below is the order that worked, and each step exists because skipping it cost something.

The four ingredients: an **AI assistant**, the **manual**, a **few photographs of the hardware**, and **reports of how other owners use it**. Plus the two an assistant cannot supply: an owner who says *that is wrong*, and the discipline to label what you do not know.

## 1. Get the manual as a PDF

The firmware-current one, not the first search result. Page numbers quoted in a book are worthless if they are from a different edition, and manufacturers revise these silently.

## 2. Extract its text and figures programmatically

**Expect the first pass to be structurally wrong in a way you only see by looking at rendered pages.** On this book the extractor treated the manual's inline button glyphs as picture elements, so screenshots were glued to paragraphs and body text was sliced mid-line. Every structural check passed. A human looked at one page and said *there is something wrong in the way you extracted the image*. That single observation cost 243 false figures and a day of fixing.

Build a review page early, one chapter with its figures in place, and look at it on the device.

## 3. Photograph the hardware, or get photographs of it

The manual's line drawings belong to the manufacturer and a guide built from them cannot be shared. **A handful of photographs of the body, annotated with your own callouts, replaces nearly all of them** and reads better than the originals, because a photograph shows the thing and a line drawing shows an abstraction of it.

Level them for print first (white point from the brightest few per cent, open the shadows, trim to content, never binarize), then put the callouts on with [`tools/annotate_figures.py`](../tools/annotate_figures.py). See [FIGURES.md](FIGURES.md) for why the annotator refuses to ship a figure whose leaders cross.

## 4. Draw the interface screens rather than reproducing them

[`tools/make_menu_figures.py`](../tools/make_menu_figures.py), with the content in `menu_screens.py` beside it. Menu screenshots belong to the manufacturer too, and the ones you find online are usually **from the previous model**. On this camera, the screenshots available showed a setting the current body does not have, a firmware two major versions old, and a tab layout that contradicted the book's own menu directory.

Typesetting them from the manual's menu structure gives figures that are right for your firmware, consistent with each other, smaller on the page, and yours.

## 5. Collect what other owners report

Forums, reviews, the manufacturer's own support threads, video transcripts. **Label every claim with where it came from and how firmly it is held.** The gap between what the manual states and what owners find is most of the value in a guide like this; it is also where every error of this kind originates, which is the subject of [RESEARCH.md](RESEARCH.md).

## 6. Build a machine-readable index of the reference tables

Which controls accept which functions, which settings live where. Then **cross-check it with a second pass that is paid to disagree with the first**. The parsing is a day's work against one specific table. The cross-check is a second reading of the same pages, not a second run of the same script.

## 7. Parse the manual's navigation index into an address book

[`tools/menu_paths.py`](../tools/menu_paths.py). Manufacturers print one: a section that reproduces every menu page in order. **It is the only machine-readable source for where a setting actually lives**, and on this manual the index pages carry PDF link annotations whose destinations give each item's documentation page. That one discovery mapped 171 of the 181 menu items without a human reading a single page.

Without it, a screenshot shows the destination and nothing about the road.

## 8. Draw the conceptual figures rather than sourcing them

[`tools/make_diagrams.py`](../tools/make_diagrams.py). Freely-licensed diagrams of general physics exist; diagrams of *your* hardware's numbers do not, and **a figure that disagrees with the table beside it is worse than no figure**. Every number in the drawing code names the chapter it came from.

## 9. Choose a spine that is not the manual's

For a camera, the hands: index finger, thumb, top plate, front, dials, switches, screen, viewfinder. For another instrument, whatever order a person actually meets it in. The manual is indexed by **where a setting lives**; a guide should be indexed by **when you need it**.

## 10. For each chapter, write down what the manual does not answer

Then research exactly that. Most of the genuinely useful findings in this book came from a list of the manual's silences, written before any research began. A manual never says what it does not say, and that invisibility is the single biggest reason a manual is not a guide.

## 11. Compute every number you can

And show the formula, so a reader with different hardware can redo it. The book's "work it out" boxes exist because a number is worth less than the method that produced it.

## 12. Make it specific to one real setup

**A guide written for everyone is the manual again.** Write it for one real person, one real bag and one real way of working, then **box the specifics** so another reader can skip them.

Nothing in such a book should read as a rule. Report what that owner chose and why, give the reversal where it is cheap, and let the reader decide.

## 13. Look at the rendered page on the device it will be read on

Not a structural check. The actual rendered page, at the actual size, on the actual panel. Three separate classes of defect in this book were invisible to every automated check and obvious at a glance.

## 14. Keep a log of your own errors

It is the most valuable artifact of the whole exercise. See [ERRORS.md](ERRORS.md), which is the part of this repository most worth your time.

## 15. Make it a book, and let the design live in a file

The manuscript is markdown; the book is a DOCX converted to PDF. Everything about how it looks comes from **a formatted DOCX you already like**, passed to pandoc as the reference document and to a post-processor that copies its cover, title page and header treatment, so nothing about the design has to live in code.

Four things cost a build each, and all four generalize:

- **Place a figure at the width it was rendered at.** Render at the full column and then place it smaller and the type shrinks with it. That is how a book ends up with five-point labels that looked fine on screen.
- **Level the figures for the panel they will be read on.** On a sixteen-gray e-paper screen a large dark field renders as mud, so the figures are black on white wherever there is a choice.
- **A custom character style has to exist in the reference document.** If it does not, pandoc emits an empty definition of its own, the run comes through unformatted, and the build reports success.
- **The front matter is not the build's to own.** A cover and a title page collect hand edits, and a post-processor that rebuilds them from the template throws those away silently. Splice the approved pages back in at the end of the build, or stop editing them by hand.

And one check that matters more than it looks: the build should state **how many figures it placed and whether any image was missing**. A missing figure is silent in every other way.

## Doing this for your own hardware

The camera is incidental. The method works for anything with a reference manual and a community that has worked out what the manual leaves out.

**What transfers unchanged:** the spine (organize by when a person needs a thing, not by where it sits in a menu tree), the silences list, the three evidence grades visible in the sentence, the figure strategy, the error log, and writing it for one real person with the specifics boxed.

**What has to be rewritten:** anything that parses your manual or names your hardware. The figure extractor is shaped by one publisher's PDF conventions; the table parsers parse one table; the screen renderer draws one interface's visual language. In this project that was most of the code, which is why so little of it is published here. What survives the move is the approach, since every constant in those scripts names this manual or this camera.

**What you need before you start:** the manual as a PDF, firmware-current. Photographs of the hardware showing every face of it. A way to find what owners report. An assistant, and the willingness to tell it that it is wrong.

**The part people underestimate:** looking at the rendered page, at size, on the device. Most of the serious defects in this book were invisible to every automated check and obvious at a glance.

**The part people overestimate:** how much of this is the writing. The prose was the fastest part. The time went into the figures, the verification, and finding out which confident claims were wrong.
