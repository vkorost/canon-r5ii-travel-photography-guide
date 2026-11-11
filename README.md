[![Canon EOS R5 Mark II Travel Photography Manual: Making the Shot in the Seconds You Have](./book/canon-r5ii-travel-photography-guide-social-1280x640.jpg)](https://github.com/vkorost/canon-r5ii-travel-photography-guide/releases/latest)

# Canon EOS R5 Mark II

### Travel Photography Manual

A 301-page guide to one camera, built around the way a traveler actually uses it, and an account of the method that produced it. Free to download, in PDF, DOCX and EPUB.

**Stills only.** The movie tabs, the movie-side customization table and everything about recording are out of scope, and the book says so where a reader might expect otherwise. A guide that pretends to cover both covers neither.

## Why this book exists

I am not a professional photographer and I do not shoot every day. I shoot when I travel, which is a few times a year, so by the time the next trip comes round I have forgotten most of what I worked out on the last one. I bought the R5 Mark II recently and wanted two things from it: a configuration I could set once, custom modes included, and then stop thinking about, and a refresher I could read before each trip.

Shooting that rarely creates two problems, and much of the book is shaped around them.

**Settings you forget to unset.** You change something for one frame, the moment passes, and the camera goes on obeying you. Nothing on the back screen warns you, and at the magnification you review at, the files look fine. I have found the damage later, at home, in pictures I could not take again. Chapter 13 is about that, with a register of every setting that behaves this way and what each one costs you.

**Customization you cannot remember.** Reassigning buttons and building custom modes is worth doing. Recalling six months later what you changed, and why, while standing in front of something you want to photograph, is a different matter. The book records the reasoning next to each decision, so the configuration can be rebuilt or questioned rather than merely trusted.

## Why it is on GitHub

Not mainly so that people read this particular book about this particular camera. It is here so that anyone who wants a guide like this for their own hardware can see that building one is now possible, and can see exactly what I did, how I did it and why. That account lives in [`docs/`](docs/), and to most visitors it is worth more than the book.

The ingredients are modest: an **AI assistant**, the **manufacturer's manual**, a **few photographs of the hardware**, and **reports of how other owners actually use it**. The two things no assistant supplies are **someone who owns the hardware to say *that is wrong***, and the discipline to label what you do not know.

## Download

The book is attached to the [latest release](../../releases/latest) in three formats: **PDF** for a tablet or e-reader, **EPUB** for a phone or Kindle, and **DOCX** if you want to edit it.

It is typeset for a 6.75 × 9 in page with a 5.75 in text column, and the figures are leveled for a sixteen-gray e-paper panel, because that is what it was built to be read on.

## What is in the book

- **Part I** walks the body control by control: what each one does, what it can be reassigned to, what other photographers put on it, and whether that is sensible.
- **Part II** covers what you set once: the custom menu, the three custom shooting modes, and the register of settings that cost you quietly when you forget to change them back.
- **Part III** leaves the camera: aperture and diffraction, which lens to carry, light you did not choose, holding the camera still, photographing objects behind glass, people who move, framing in two seconds, and what can and cannot be fixed afterwards.
- **Appendix A** is the manufacturer's own customization matrix with its icon-only column headers resolved into names, so it can finally be searched.
- **Appendix B** is the camera's whole menu as an address book: every secondary tab by number and name, all 181 stills items with what each does and when you would want it, and an alphabetical index.
- **Appendix C** is every source, chapter by chapter. **Appendix D** is the whole book on one page: the field card.

Three conventions run through it. **Menu paths** give every setting its full address: the main tab, the numbered secondary tab with its name, and the item as the camera spells it. **Case boxes** hold the specifics of one photographer's kit, marked so you can skip them. **Work-it-out boxes** give the arithmetic rather than the number, so the method survives a change of kit.

## What is in this repository

| | |
|---|---|
| [`docs/METHOD.md`](docs/METHOD.md) | the recipe, step by step, why each step exists, how the book gets built, and what it takes to do this for your own hardware |
| [`docs/ERRORS.md`](docs/ERRORS.md) | every error the AI made, and how each one was caught |
| [`docs/FIGURES.md`](docs/FIGURES.md) | the figure problem: how a book like this gets its illustrations |
| [`docs/RESEARCH.md`](docs/RESEARCH.md) | how claims were sourced, graded and labeled |
| [`tools/`](tools/) | four scripts, kept as exhibits rather than as a toolkit |
| [`NOTICE.md`](NOTICE.md) | third-party material in the book, item by item |

**The chapter sources are not here.** A chapter without its figures is not the chapter, so the text ships as the book and the repository ships the account of how it was made.

**Nor is the whole toolbox.** Thirty-odd scripts were written for this book, and most of them parse one manual, name one camera or draw one interface. Published, they would be thirty files nobody can run. The four that remain are the ones where the code is the point:

| | |
|---|---|
| [`menu_paths.py`](tools/menu_paths.py) | the one discovery that generalizes: the manual's index pages carry PDF link annotations, which are the only machine-readable source for where a setting lives |
| [`annotate_figures.py`](tools/annotate_figures.py) | callouts on a photograph, with gutters sized from measured text and a check that reports any leader crossing another |
| [`make_menu_figures.py`](tools/make_menu_figures.py) | drawing the interface instead of cleaning up screenshots, with its content in `menu_screens.py` beside it |
| [`make_diagrams.py`](tools/make_diagrams.py) | computing a diagram from the book's own arithmetic, every number commented with the chapter it came from |

They are published to be read rather than dropped into another project: paths are project-relative and several constants name this camera. Running them needs Python 3.11+ with `pymupdf`, `pillow`, `numpy` and `matplotlib` installed.

## Start here

If you want **the book**, take the release. The preface says in four pages what it is made of and the rules that kept it honest.

If you want **to do this yourself**, read [`docs/METHOD.md`](docs/METHOD.md), then [`docs/ERRORS.md`](docs/ERRORS.md). The second one is more valuable than the first, because it is the part the enthusiasm around AI writing tends to leave out.

## Coverage cutoff

Written against firmware current in 2026, and against the *EOS R5 Mark II Advanced User Guide* of the same period. Firmware changes menus. Where the book states a page number from the manual, it is from that edition.

## AI assistance, scope of

The prose, the research, the tooling and the figures were produced by Claude Code working under my instruction, and the book says so on its cover rather than burying it here. Editorial decisions were mine, and so was the authority on anything the manual does not settle, because I own the camera and could go and look. Every empirical claim carries a source. Where a claim rests on a single owner's report rather than on documentation, the book says so in the sentence rather than in a footnote.

## Disclaimer

Not affiliated with, endorsed by, or connected to Canon Inc. in any way. *Canon*, *EOS* and *EOS R5 Mark II* are trademarks of their owner, used here only to identify the product the book is about.

Nothing in the book is a rule. It reports what one owner chose in one situation and why. Your camera, your eye and your habits may make a different answer right.

## License

The tooling in [`tools/`](tools/) is MIT, see [`LICENSE`](LICENSE). The book itself is © its author, all rights reserved. It is free to read and to share whole, and not free to repackage. Third-party material is listed in [`NOTICE.md`](NOTICE.md).

---

[![Canon EOS R5 Mark II Travel Photography Manual cover](./book/cover.png)](https://github.com/vkorost/canon-r5ii-travel-photography-guide/releases/latest)
