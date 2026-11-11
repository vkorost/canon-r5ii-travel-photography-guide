# Grounded, and then checked against the camera

The objection to a book like this is reasonable: an AI assistant will state a wrong menu path in the same confident tone as a right one, so why trust 301 pages of them.

The answer is in two halves. The assistant never worked from memory, and nothing it wrote went into the book until the person who owns the camera had been through it with the camera in hand.

## What the book was grounded in

**Canon's own manual, quoted with page numbers.** Every mechanism claim comes from the *EOS R5 Mark II Advanced User Guide*. Appendix C gives the page for each one, so any claim can be checked against the source in under a minute.

**Menu addresses parsed out of the manual, not typed.** The manual prints an index that reproduces every menu page in order, and those index pages carry PDF link annotations whose destinations give each item's documentation page. Reading those links produced the address book behind every menu path in the book, which is why a setting is always given as its main tab, its numbered secondary tab with that tab's name, and the item as the camera spells it. 171 of the 181 stills items were mapped that way without a human retyping anything.

**Reports from other owners, labeled as reports.** Where the manual is silent, the book says what owners have published and attributes it. Where a claim rests on one report rather than on documentation, the sentence says so rather than a footnote. Where owners contradict the documentation, both sides are recorded instead of one being picked.

**Arithmetic computed rather than quoted.** Shutter floors, diffraction limits, depth of field, motion blur and ISO requirements are derived in the open with the formula shown, so a reader with different gear can redo them.

## What the owner did with the camera

This is the part a chatbot answer never has.

- **Every setting in the book was set on the actual body**, walking every menu tab in turn rather than reading about them.
- **C1, C2 and C3 were built from the book's own recipes**, in the order the book gives, including the teardown that puts the camera back to its base state afterwards.
- **The configuration was then used.** Tips that worked stayed in. Tips that did not were fixed in the book rather than left standing.
- **The built book was read end to end** as a stranger would read it, which caught a different class of problem: passages that were technically right and read as patronizing, figures that were correct and looked amateur, and advice that had drifted into handing down rules.

## What that caught

| Found with the camera in hand | What it changed |
|---|---|
| **Detect priority AE while AF** cannot be enabled unless **Metering mode** is **Evaluative metering** (p. 335). The camera grays the item out and names *"metering mode"* without naming the value it wants. | Chapter 12 now states the prerequisite and orders the C2 steps by dependency rather than by menu tab. |
| **Highlight tone priority** silently raises the ISO floor to 200, so a recipe that fixes ISO at 100 does not get ISO 100. | Recorded as a gate in the custom-mode procedure. |
| **Long exposure noise reduction** fires on exposure duration, one second or slower at any ISO, and is a different item from **High ISO speed NR** one row below it. | Chapter 12's C1 table says why ISO 100 does not exempt the mode. |
| **12 frames per second** from High-speed continuous **+** depends on the shutter mode, not on the drive mode alone (p. 581). | Stated where the drive mode is set. |
| The lens adapter does have a control ring. The assistant had stated flatly that it did not. | A whole section was rewritten, and the useful question turned out to be how to live with a ring you keep nudging. |
| A tally lamp on the camera's shoulder had been labeled as the lens release button on a body figure. | The label was removed rather than guessed at twice, and the figures were checked against Canon's part-names pages. |
| **Eye detection** appearing stuck on one eye, with no way to change it. | **AF → 5/7 Customized controls → L/R eye detection** prunes the Eye detection list (p. 569), so an option removed there disappears rather than graying out. |

The loop is still running. The last of those came up after the book was finished, and it will be in the next revision.

## What is still open

Four things about custom-mode behavior are recorded in the book as reported rather than confirmed: whether a change made inside a mode reverts on a power cycle, whether button and dial assignments are stored per mode, whether exposure compensation is stored per mode, and whether loading a settings file from a card disturbs the registered modes. The book says which they are, and says they are unconfirmed.

Firmware moves. The book was written against the firmware and the manual edition current in 2026, and it says so.

## And it is not error-free

No book is. Manufacturers ship manuals with errata pages, and books by human experts get corrected in the second printing. The difference here is that the errors are published instead of quietly fixed: [`ERRORS.md`](ERRORS.md) lists every one that was caught while the book was being built, grouped by kind, with what caught each one. The ranking at the end of that page is the honest finding of the whole project. A human with the hardware caught most of the serious ones, and nothing automated came close.
