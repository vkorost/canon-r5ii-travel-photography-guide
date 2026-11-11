# Third-party material

What is in the book that did not originate here. This exists so that anyone with a question about a particular figure can get an answer without having to ask.

Nothing in this list is redistributed as a loose file in this repository. All of it is embedded in the book.

## Quotations from the manufacturer's manual

The book quotes the *Canon EOS R5 Mark II Advanced User Guide* throughout, always in quotation marks and always with a page number, in Appendix C. The quotations are short and are used to discuss what the manual does and does not say. Several chapters exist specifically because of what the manual leaves out.

## Figures from the manufacturer's manual, all four of them

Everything else was replaced. These four could not be reproduced honestly from the camera's own menu structure, so they remain as the manufacturer's figures, each used to discuss that specific screen:

| Figure | What it shows | Why it could not be redrawn |
|---|---|---|
| p. 1052 | Customize buttons | a grid of control pictograms, not a text list |
| p. 1065 | Customize dials | the assignments vary with the exposure mode, so a text list loses the point |
| p. 295 | the Quick Control screen | the screen itself is the subject |
| p. 166 | Img type/size | the two card rows are the point of the caption |

They are converted to ink-on-paper rather than reproduced as-is, so that they sit with the drawn screens and print correctly on an e-paper panel.

One further item is the manufacturer's: the electronic-shutter **ES** glyph in Chapter 2, cut out of the manual's running text and set inline in a sentence at the size the camera draws it, because the whole point of that passage is what the mark on the screen looks like.

## Photographs of the camera body

The six body figures are photographs of this camera on a white background, converted to grayscale, re-leveled, trimmed to content, cropped and overlaid with original callouts drawn by `tools/annotate_figures.py`. The callout text uses the manufacturer's own part names, read off the Part Names pages of the manual, which are pages 32, 34 and 35 in the edition this book cites.

Nothing in the annotation is traced or copied: the gutters, the labels and the arrows are drawn by the script.

## Menu screens

**Drawn, not reproduced.** The 27 menu screens in the book were typeset from the camera's own menu structure, which was parsed out of the manual's navigation index. The eight main-tab marks were extracted from a photograph of the camera's own screen and cleaned up. See [`docs/FIGURES.md`](docs/FIGURES.md) for why this was worth doing, beyond the licensing: the screenshots available online for this body are mostly from the **previous model**, and would have contradicted the book's own menu directory.

## Diagrams

The five conceptual diagrams in Chapter 3 are drawn from the book's own arithmetic by `tools/make_diagrams.py`. Every number in the drawing code names the chapter it came from.

## Sourced images, policy

Where an image is sourced rather than made, the license tier is **public domain, CC0 or CC BY only**. Never share-alike, never non-commercial, never no-derivatives, and never anything whose license cannot be read programmatically. Share-alike in particular reaches any image derived from it, including a grayscale conversion.

## Trademarks

*Canon*, *EOS* and *EOS R5 Mark II* are trademarks of Canon Inc. This project is not affiliated with, endorsed by, or connected to Canon in any way, and uses the names only to identify the product the book is about.
