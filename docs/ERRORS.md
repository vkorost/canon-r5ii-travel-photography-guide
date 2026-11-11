# Everything the AI got wrong

This is the section worth reading, because it is the part the enthusiasm around AI writing tends to leave out. **Every one of these reached a draft.** Several reached a built book and were caught by a human looking at a page.

They are grouped by what kind of failure they are, because the kind is what transfers. Your hardware will produce different specifics and the same five kinds.

## 1. Asserting facts about hardware it cannot see

**It stated flatly that the owner's lens adapter had no control ring.** It has one. The owner corrected it in a sentence, and the correction changed a whole section, because the interesting question turned out to be *how do I use a ring I keep nudging by accident*, which produced one of the better answers in the book.

**It labeled a tally lamp as the lens release button.** A small gray tab on the camera's shoulder looks like a button. The manufacturer's own part-names diagram puts the lens release at the mount edge and the tally lamp exactly where the arrow was pointing. The label was removed rather than guessed at a second time.

**It swapped Quick control dial 1 and dial 2** on two figures. The manual's menu-operations diagram settles it: dial 1 is the wheel around SET. The book's own prose had it right; the figures contradicted the text for a whole build.

**What transfers.** An assistant will describe your hardware confidently from general knowledge of similar hardware. Anything it says about a physical object needs an owner to confirm, and the manufacturer's own part-names page is the arbiter, not a photograph and not a plausible reading.

## 2. Research that was confidently wrong

**A research agent reported that a tracking setting had three states.** The manual gives two. Had it not been checked against the page before writing, three separate mode recipes in the book would have been built on a setting that does not exist in that form.

**Menu screenshots gathered from the web were from the previous model**: a setting the current body does not have, firmware two major versions old, a tab layout that contradicted the book's own menu directory. They looked perfect. Had they been cleaned up and used, every one would have argued with the appendix on the facing page.

**What transfers.** Research output arrives in the same confident register whether it is right or wrong. Anything load-bearing gets verified against the primary document before it is written, not after. And material that looks like your hardware very often is not.

## 3. Structural checks that all passed on broken output

**The figure extractor treated inline button glyphs as picture elements.** Screenshots were glued to paragraphs and body text was sliced mid-line. Every structural check passed. A human looked at one page and said *there is something wrong in the way you extracted the image*, an observation that cost 243 false figures and a day of fixing.

**Bold emphasis ran at 17% of body text in one chapter**, with one span running 49 words. Caught by a measurement script, not by reading: the page looked fine until the numbers were printed.

**A build check reports a false positive to this day.** It compares media parts against drawings and fails whenever a figure is reused, so it fails on a book that places 44 figures 62 times. It was verified against an older build before being ignored, and the reason is written down.

**What transfers.** A green check means the thing you tested is fine. Build the review page early, render it, and look at it on the device. Measure the properties a reader would notice; several of this book's worst moments were invisible to every automated check and obvious at a glance.

## 4. Figures that were technically correct and looked amateur

Three successive rounds of this, each one shipped before being called out:

- **Equal-aspect bug.** Axis limits of 0 to 100 on a non-square figure rendered every circle as an ellipse.
- **Drawn glyphs instead of the real ones.** Substituting the word *Shoot* for the camera's pictogram is not a replacement: the mapping between glyph and name is exactly what a new owner lacks.
- **Labels pasted on the body with halos**, arrowheads four times too large, and leaders crossing each other.
- **Arrows printing as black sticks** because the taper ran the shaft to a point and at print size the two outline edges merged.
- **Labels printing at five points** because figures were rendered at the full column and then placed smaller.

**What transfers.** "Technically correct" and "looks like a real book" are different targets, and only the second one matters to a reader. The fix was to stop correcting figures by hand and make the defects structurally impossible, then have the script report any that survive, which is what [FIGURES.md](FIGURES.md) describes.

## 5. Writing in a register nobody asked for

**The book handed down rules.** *You should*, *the right answer*, *the rule is*. It was written for one photographer's habits, and those habits were being presented to every reader as instruction. The same applied to that photographer's preference for not reading a histogram, which had become the book telling readers the histogram was a crutch.

**It used four words for every setting.** *Museum* 39 times, *gallery* 21, *artifact* 34. Nothing wrong with any of them in a travel guide; the problem was that a reader shooting anything else never saw themselves.

**It wrote 946 em dashes**, and repeated the same three bold labels (*What it does*, *What people say*, *When you would want it*) 228 times across one appendix.

**What transfers.** An assistant converges on a register and will not notice. Count things: the same word, the same construction, the same punctuation mark. Decide what the book's relationship to its reader is and check the prose against it, because the default is to sound like instructions.

## What caught each one

Most of the serious ones were caught by the owner looking at a rendered page. The research errors were caught by checking a claim against the primary document, the prose problems by a measurement script that counted something, and the smallest share of all by an automated structural check.

That ranking is the finding. **The cheapest effective check in this whole project was a human looking at one page**, and nothing automated came close to replacing it.
